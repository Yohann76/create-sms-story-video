#!/usr/bin/env python3
"""
SMS Story Video Generator
Usage: python3 render.py [--scenario scenario.json] [--output video_finale.mp4] [--port 9753]
"""

import argparse
import asyncio
import http.server
import json
import os
import subprocess
import sys
import tempfile
import threading
from pathlib import Path

try:
    from playwright.async_api import async_playwright
except ImportError:
    print("[ERROR] Playwright not installed. Run: pip3 install playwright --break-system-packages")
    print("        Then: python3 -m playwright install chromium")
    sys.exit(1)


WIDTH  = 1080
HEIGHT = 1920
FPS    = 30

DEFAULT_SOUNDS = {
    "send":         "assets/send.mp3",
    "receive":      "assets/receive.mp3",
    "typing":       "assets/typing.mp3",
    "notification": "assets/notification.mp3",
}


def resolve_sounds(config: dict) -> dict:
    sounds = dict(DEFAULT_SOUNDS)
    sounds.update(config.get("sounds", {}))
    return sounds


def compute_total_duration(scenario: dict) -> float:
    """Mirror of the JS timeline, returns seconds."""
    if "script" in scenario:
        total_ms = 2000
        for action in scenario.get("script", []):
            total_ms += action.get("delay", 0)
            kind = action.get("action")
            if kind == "message":
                if action.get("sender") == "received":
                    total_ms += action.get("typingDuration", 0)
                elif action.get("sender") == "sent":
                    total_ms += len(action.get("text", "")) * 60
                total_ms += 400
            elif kind == "switch":
                total_ms += 700
        total_ms += 3000
        return total_ms / 1000

    # Legacy format
    messages = scenario.get("messages", [])
    notifs   = scenario.get("notifications", [])

    total_ms = 2000
    if any(n.get("at") == -1 for n in notifs):
        total_ms += 800 + 3000

    for msg in messages:
        total_ms += msg.get("delay", 1000)
        if msg.get("sender") == "received":
            total_ms += msg.get("typingDuration", 0)
        total_ms += 400

    total_ms += 3000
    return total_ms / 1000


def build_audio_track(events: list, duration_s: float, project_dir: Path, sounds: dict) -> Path | None:
    """Mix all sound events into a single AAC audio file using FFmpeg.
    events = list of (timestamp_ms, sound_key, trim_ms|None).
    trim_ms is only set for 'typing' — the sound is cut at that exact duration.
    """
    resolved = []
    for item in events:
        ts_ms, key = item[0], item[1]
        trim_ms     = item[2] if len(item) > 2 else None
        if key not in sounds:
            continue
        sf = project_dir / sounds[key]
        if sf.exists():
            resolved.append((ts_ms, sf, trim_ms))

    if not resolved:
        print("[WARN] No valid sound files found — video will be silent.")
        return None

    print(f"[INFO] Mixing {len(resolved)} audio events...")

    input_args   = []
    filter_parts = []
    out_labels   = []

    for idx, (ts_ms, sf, trim_ms) in enumerate(resolved):
        input_args += ["-i", str(sf)]
        label = f"s{idx}"
        if trim_ms is not None:
            cut_at = ts_ms / 1000 + trim_ms / 1000
            filter_parts.append(
                f"[{idx}]adelay={ts_ms}|{ts_ms},"
                f"atrim=end={cut_at:.3f},"
                f"apad=whole_dur={duration_s:.3f}[{label}]"
            )
        else:
            filter_parts.append(f"[{idx}]adelay={ts_ms}|{ts_ms},apad=whole_dur={duration_s:.3f}[{label}]")
        out_labels.append(f"[{label}]")

    n = len(out_labels)
    mix_filter = f"{''.join(out_labels)}amix=inputs={n}:normalize=0:dropout_transition=0,atrim=end={duration_s:.3f},asetpts=PTS-STARTPTS[out]"
    filter_complex = ";".join(filter_parts) + ";" + mix_filter

    tmp_audio = Path(tempfile.mktemp(suffix=".aac"))
    cmd = [
        "ffmpeg", "-y",
        *input_args,
        "-filter_complex", filter_complex,
        "-map", "[out]",
        "-c:a", "aac", "-b:a", "192k",
        str(tmp_audio),
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print("[WARN] Audio mixing failed:")
        print(result.stderr[-800:])
        return None

    return tmp_audio


def start_http_server(directory: Path, port: int) -> http.server.HTTPServer:
    handler = http.server.SimpleHTTPRequestHandler
    handler.log_message = lambda *args: None

    original_dir = os.getcwd()
    os.chdir(directory)
    server = http.server.HTTPServer(("127.0.0.1", port), handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    os.chdir(original_dir)
    return server


async def capture_via_playwright_video(scenario_path: Path, duration: float, port: int) -> tuple[Path, list]:
    """
    Record the animation in real-time using Playwright's built-in video capture.
    Audio events are collected from JS console with performance.now() timestamps,
    which map directly to the video timeline since both run in real-time.
    Returns (webm_path, audio_events).
    """
    project_dir       = scenario_path.resolve().parent
    scenario_filename = scenario_path.name

    server = start_http_server(project_dir, port)
    print(f"[INFO] HTTP server on port {port}")

    audio_events_js: list[tuple] = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=[
                "--no-sandbox",
                "--disable-setuid-sandbox",
                "--disable-dev-shm-usage",
                f"--window-size={WIDTH},{HEIGHT}",
                "--autoplay-policy=no-user-gesture-required",
            ],
        )

        video_dir = Path(tempfile.mkdtemp())
        context = await browser.new_context(
            viewport={"width": WIDTH, "height": HEIGHT},
            device_scale_factor=1,
            record_video_dir=str(video_dir),
            record_video_size={"width": WIDTH, "height": HEIGHT},
        )
        page = await context.new_page()

        def on_console(msg):
            try:
                data = json.loads(msg.text)
                if isinstance(data, dict) and "__audio" in data:
                    audio_events_js.append((
                        int(data.get("t", 0)),
                        data["__audio"],
                        data.get("ms"),
                    ))
            except Exception:
                pass

        page.on("console", on_console)

        url = f"http://127.0.0.1:{port}/index.html?scenario={scenario_filename}"
        print(f"[INFO] Loading {url}")
        await page.goto(url, wait_until="domcontentloaded")

        print(f"[INFO] Recording animation in real-time (~{duration:.0f}s)...")
        timeout_ms = int((duration + 60) * 1000)
        await page.wait_for_function(
            "() => window.__RENDER_DONE__ === true",
            timeout=timeout_ms,
        )
        await asyncio.sleep(2.5)  # 2.5s tail

        webm_path = Path(await page.video.path())
        await page.close()
        await context.close()
        await browser.close()

    server.shutdown()

    # Sync typing trim: stop at the moment the next send/receive fires
    events_synced: list[tuple] = []
    for i, (t_ms, key, trim_ms) in enumerate(audio_events_js):
        if key == "typing":
            next_ms = next(
                (audio_events_js[j][0] for j in range(i + 1, len(audio_events_js))
                 if audio_events_js[j][1] in ("send", "receive")),
                None,
            )
            trim_ms = (next_ms - t_ms) if next_ms is not None else trim_ms
        events_synced.append((t_ms, key, trim_ms))

    print(f"[INFO] Recorded | {len(events_synced)} audio events (JS-timestamp synced)")
    return webm_path, events_synced


def encode_video(webm_path: Path, audio_path: Path | None, output_path: Path):
    """Convert Playwright WebM → H.264 MP4, then mux audio if available."""
    tmp_mp4 = Path(tempfile.mktemp(suffix=".mp4"))

    # Step 1 — WebM → silent MP4 at 30fps
    cmd = [
        "ffmpeg", "-y",
        "-i", str(webm_path),
        "-r", str(FPS),
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-crf", "18",
        "-preset", "medium",
        "-movflags", "+faststart",
        str(tmp_mp4),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print("[ERROR] Video encoding failed:")
        print(result.stderr)
        sys.exit(1)

    webm_path.unlink(missing_ok=True)

    # Step 2 — mux audio if available
    if audio_path and audio_path.exists():
        print("[INFO] Muxing audio into video...")
        cmd = [
            "ffmpeg", "-y",
            "-i", str(tmp_mp4),
            "-i", str(audio_path),
            "-c:v", "copy",
            "-c:a", "aac",
            "-shortest",
            "-movflags", "+faststart",
            str(output_path),
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print("[WARN] Audio mux failed, saving video without audio:")
            print(result.stderr[-400:])
            tmp_mp4.rename(output_path)
        else:
            tmp_mp4.unlink(missing_ok=True)
            audio_path.unlink(missing_ok=True)
    else:
        tmp_mp4.rename(output_path)


def probe_duration(path: Path) -> float:
    result = subprocess.run(
        ["ffprobe", "-v", "quiet", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", str(path)],
        capture_output=True, text=True,
    )
    try:
        return float(result.stdout.strip())
    except ValueError:
        return 0.0


def main():
    parser = argparse.ArgumentParser(description="SMS Story Video Generator")
    parser.add_argument("--scenario", default="scenario.json")
    parser.add_argument("--output",   default="video_finale.mp4")
    parser.add_argument("--port",     type=int, default=9753)
    args = parser.parse_args()

    scenario_path = Path(args.scenario)
    output_path   = Path(args.output)

    if not scenario_path.exists():
        print(f"[ERROR] Scenario not found: {scenario_path}")
        sys.exit(1)

    print(f"[INFO] Scenario : {scenario_path}")
    print(f"[INFO] Output   : {output_path}")

    with open(scenario_path) as f:
        scenario = json.load(f)

    duration    = compute_total_duration(scenario)
    project_dir = scenario_path.resolve().parent
    sounds      = resolve_sounds(scenario.get("config", {}))

    print(f"[INFO] Estimated duration : {duration:.1f}s")

    # Capture animation in real-time + collect JS audio events
    webm_path, audio_events = asyncio.run(
        capture_via_playwright_video(scenario_path, duration, args.port)
    )

    actual_duration = probe_duration(webm_path)
    if actual_duration <= 0:
        actual_duration = duration + 2.5
    print(f"[INFO] Recorded duration  : {actual_duration:.1f}s")

    # Build audio track from JS-reported timestamps
    audio_path = build_audio_track(audio_events, actual_duration, project_dir, sounds)

    # Encode final MP4
    print("[INFO] Encoding final MP4...")
    encode_video(webm_path, audio_path, output_path)

    final_duration = probe_duration(output_path)
    print(f"[DONE] {output_path.resolve()}")
    print(f"       {final_duration:.1f}s | {FPS}fps | audio: {'yes' if audio_path else 'no'}")


if __name__ == "__main__":
    main()
