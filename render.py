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
import time
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
    events = list of (timestamp_ms, sound_key, trim_ms|None) from JS console events.
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
            # Couper le son typing exactement à la fin de la période d'écriture
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


async def capture_frames(scenario_path: Path, duration: float, port: int) -> tuple[Path, int, list]:
    """
    Launch Playwright, capture PNG frames.
    Returns (frames_dir, frame_count, audio_events).

    Audio events are collected via console messages emitted by JS at the exact
    moment each sound fires. We record the wall-clock time of each event and
    each frame, then map events → frame indices → video timestamps.
    This eliminates any drift between JS time and actual capture speed.
    """
    project_dir       = scenario_path.resolve().parent
    scenario_filename = scenario_path.name

    server = start_http_server(project_dir, port)
    print(f"[INFO] HTTP server on port {port}")

    # Collected in real-time by the console listener
    # Tuples: (wall_clock, key, trim_ms|None)
    audio_events_wall: list[tuple] = []

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
        context = await browser.new_context(
            viewport={"width": WIDTH, "height": HEIGHT},
            device_scale_factor=1,
        )
        page = await context.new_page()

        # Intercept console.log() from JS to capture audio events in real-time
        def on_console(msg):
            t = time.time()
            try:
                data = json.loads(msg.text)
                if isinstance(data, dict) and "__audio" in data:
                    trim_ms = data.get("ms")  # only set for 'typing'
                    audio_events_wall.append((t, data["__audio"], trim_ms))
            except Exception:
                pass

        page.on("console", on_console)

        url = f"http://127.0.0.1:{port}/index.html?scenario={scenario_filename}"
        print(f"[INFO] Loading {url}")
        await page.goto(url, wait_until="domcontentloaded")

        print("[INFO] Capturing frames...")
        frames_dir     = Path(tempfile.mkdtemp())
        frame_times: list[float] = []   # wall-clock time of each captured frame
        frame_index    = 0
        frame_interval = 1.0 / FPS
        deadline       = time.time() + duration + 5

        while time.time() < deadline:
            t0 = time.time()
            frame_path = frames_dir / f"frame_{frame_index:06d}.png"
            await page.screenshot(path=str(frame_path), full_page=False)
            frame_times.append(time.time())   # record AFTER screenshot is complete
            frame_index += 1

            done = await page.evaluate("() => window.__RENDER_DONE__ === true")
            if done:
                for _ in range(FPS * 2):   # 2s tail
                    await asyncio.sleep(frame_interval)
                    frame_path = frames_dir / f"frame_{frame_index:06d}.png"
                    await page.screenshot(path=str(frame_path), full_page=False)
                    frame_times.append(time.time())
                    frame_index += 1
                break

            await asyncio.sleep(max(0, frame_interval - (time.time() - t0)))

        await browser.close()

    server.shutdown()

    # Map each audio event to the closest captured frame, then convert to video ms
    audio_events: list[tuple] = []
    for event_wall, key, trim_ms in audio_events_wall:
        idx = min(range(len(frame_times)), key=lambda i: abs(frame_times[i] - event_wall))
        video_ms = round(idx / FPS * 1000)
        audio_events.append((video_ms, key, trim_ms))

    # For typing events: replace trim_ms by the delta to the next send/receive event.
    # This guarantees the typing sound stops exactly when the message appears,
    # regardless of any drift between setTimeout and actual capture timing.
    audio_events_synced: list[tuple] = []
    for i, (video_ms, key, trim_ms) in enumerate(audio_events):
        if key == 'typing':
            next_msg_ms = next(
                (audio_events[j][0] for j in range(i + 1, len(audio_events))
                 if audio_events[j][1] in ('send', 'receive')),
                None
            )
            trim_ms = (next_msg_ms - video_ms) if next_msg_ms is not None else trim_ms
        audio_events_synced.append((video_ms, key, trim_ms))

    print(f"[INFO] Captured {frame_index} frames | {len(audio_events_synced)} audio events (wall-clock synced)")
    return frames_dir, frame_index, audio_events_synced


def encode_video(frames_dir: Path, frame_count: int, audio_path: Path | None, output_path: Path):
    """Assemble frames + optional audio into final MP4."""
    duration_s = frame_count / FPS
    tmp_video  = Path(tempfile.mktemp(suffix=".mp4"))

    # Step 1 — frames → silent MP4
    cmd = [
        "ffmpeg", "-y",
        "-framerate", str(FPS),
        "-i", str(frames_dir / "frame_%06d.png"),
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-crf", "18",
        "-preset", "medium",
        "-movflags", "+faststart",
        str(tmp_video),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print("[ERROR] Video encoding failed:")
        print(result.stderr)
        sys.exit(1)

    # Step 2 — mux audio if available
    if audio_path and audio_path.exists():
        print("[INFO] Muxing audio into video...")
        cmd = [
            "ffmpeg", "-y",
            "-i", str(tmp_video),
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
            tmp_video.rename(output_path)
        else:
            tmp_video.unlink(missing_ok=True)
            audio_path.unlink(missing_ok=True)
    else:
        tmp_video.rename(output_path)

    # Cleanup frames
    for f in frames_dir.iterdir():
        f.unlink()
    frames_dir.rmdir()


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

    # Capture frames + collect JS audio events (perfectly timed)
    frames_dir, frame_count, audio_events = asyncio.run(
        capture_frames(scenario_path, duration, args.port)
    )

    actual_duration = frame_count / FPS

    # Build audio track from JS-reported timestamps
    audio_path = build_audio_track(audio_events, actual_duration, project_dir, sounds)

    # Encode final MP4
    print("[INFO] Encoding final MP4...")
    encode_video(frames_dir, frame_count, audio_path, output_path)

    print(f"[DONE] {output_path.resolve()}")
    print(f"       {frame_count} frames | {actual_duration:.1f}s | {FPS}fps | audio: {'yes' if audio_path else 'no'}")


if __name__ == "__main__":
    main()
