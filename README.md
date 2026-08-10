# SMS Story Video Generator (9:16)


## Use

python3 render.py --scenario scenario.json --output video_finale.mp4 
       
## Purpose

Automate the generation of vertical videos (Reels / TikTok / Shorts) simulating an animated SMS conversation in iOS iMessage style, from a simple JSON configuration file. The final video is ready to publish as MP4, with synchronized sound effects and no text-to-speech (TTS).

---

## Architecture & Technologies

| Layer | Technology | Role |
|---|---|---|
| Input format | JSON | Structured data file defining the conversation sequence |
| UI | HTML5 / CSS3 / Vanilla JS | Visual template at 9:16 ratio (1080×1920 px), bubble animations and audio triggering |
| Recording engine | Python + Playwright | Drives a headless Chromium browser at native 1080×1920 resolution and captures the video/audio stream |
| Video post-processing | FFmpeg | Encodes the temporary container (`.webm`) into a universal final file (`.mp4` H.264 / AAC) |

---

## Features

### JSON Scenario Parsing
- Sender side support (`sent` / `received`)
- Fine-grained pause control between messages (`delay` in ms)
- Contact name and avatar customization
- Audio assets chosen directly in the JSON (send sound, receive sound, notification sound), with default fallbacks
- Conversation title configurable via JSON
- Triggerable notifications configurable via JSON

### Visual Rendering — Authentic iOS Style
- Interface faithful to an Apple phone screen (dark mode, system typography, rounded bubbles with tails)
- Sender on the right in **green**, receiver on the left in **gray** (Apple convention)
- Smooth bubble appearance animation (CSS `transform` + `opacity` transition)
- Automatic scroll to bottom as new messages appear
- Full emoji support in messages
- **"... is typing"** animation before each received message, faithful to iOS — duration configurable in JSON

### Audio (Sound Effects Only)
- Local audio file triggered in sync with each bubble appearance
- Distinct configurable sounds: send, receive, notification
- No text-to-speech (TTS) whatsoever

### Video Export
- Strict resolution: **1080 × 1920 pixels** (9:16 ratio)
- Frame rate: **30 fps minimum**
- Output format: `.mp4` with **H.264 (yuv420p)** video encoding and **AAC** audio

---

## Execution Workflow

```
[ scenario.json ]
       │
       ▼
[ index.html ] ───── Reads scenario, runs CSS animations, triggers audio
       │
       ▼
[ render.py ] ──────  Playwright records Chromium at 1080×1920
       │
       ▼
[ output.webm ] ──── Raw temporary container
       │
       ▼
[ video_finale.mp4 ] ← FFmpeg re-encodes video (H.264) + audio (AAC)
```

---

## `scenario.json` Specification

```json
{
  "config": {
    "contactName": "Alex",
    "avatarEmoji": "👤",
    "conversationTitle": "Alex",
    "sounds": {
      "send": "send.mp3",
      "receive": "pop.mp3",
      "notification": "notification.mp3"
    }
  },
  "messages": [
    { "sender": "received", "text": "Where are you?", "delay": 1000, "typingDuration": 1500 },
    { "sender": "sent", "text": "Be there in 5 min!", "delay": 1800 },
    { "sender": "received", "text": "You're still at home, admit it.", "delay": 2000, "typingDuration": 2000 },
    { "sender": "sent", "text": "No way 😅", "delay": 1500 }
  ],
  "notifications": [
    { "at": 0, "title": "Alex", "body": "Where are you?" }
  ]
}
```

### Key Parameters

| Parameter | Type | Description |
|---|---|---|
| `config.contactName` | string | Name displayed at the top of the conversation |
| `config.avatarEmoji` | string | Emoji used as the contact's avatar |
| `config.conversationTitle` | string | Title displayed in the navigation bar |
| `config.sounds.send` | string | Audio file played when a message is sent |
| `config.sounds.receive` | string | Audio file played when a message is received |
| `config.sounds.notification` | string | Audio file played when a notification appears |
| `messages[].sender` | `"sent"` \| `"received"` | Which side the bubble appears on |
| `messages[].text` | string | Message content (emojis supported) |
| `messages[].delay` | number (ms) | Pause before the message appears |
| `messages[].typingDuration` | number (ms) | Duration of the "... is typing" animation (received messages only) |
| `notifications[].at` | number | Index of the message after which the notification appears |
| `notifications[].title` | string | Notification title |
| `notifications[].body` | string | Notification body text |

---

## Usage (CLI)

The project runs entirely from the command line and is designed to run on **non-standard ports** (compatible with multi-project environments). Simply pass a `scenario.json` file as argument:

```bash
python render.py --scenario scenario.json --output video_finale.mp4
```

A sample `scenario.json` file is included to test the project immediately.

---

## Roadmap — Version 2

- [x] Configurable notifications via JSON
- [x] Configurable conversation title via JSON
- [ ] Multi-contact support in a single conversation
- [ ] Optional light mode theme
- [ ] GIF export alongside MP4
