# Houston Interface Blueprint

## Goals
Provide a mission-control style console that stays visible across tabs, supports text and voice interactions, and exposes quick actions for common Houston tasks. The interface should feel like a dedication station console anchored to the bottom of the Mission Control app.

## Modalities
- **Text Input Bar**: Primary entry point, docked bottom-center. Supports markdown, code fencing, and drag/drop snippets.
- **Voice Input**: Wake phrase (`Houston…`) plus push-to-talk hotkey. Visual feedback on listen state (mic icon + VU meter).
- **Clipboard/Context**: "Send to Houston" context menu, optional auto-attach of current file path/function scope.
- **File Attachments**: Drag files onto the bar or press `📎` to attach documents for analysis.

## Output & Feedback
- **Conversation Stream**: Scrollable history with actor badges (`Jeremy`, `Houston`). Markdown rendering, collapsible code blocks, and ability to pin responses.
- **Audio Playback**: TTS with radio/static effects configurable via `houston-features.json` (`audio.voice` block). Playback is interruptible; include play/pause button.
- **Status Indicators**: LED trio (listening, thinking, acting). Progress bar for long-running pipelines with estimated time.
- **Suggested Actions**: Buttons appearing under the latest Houston reply (e.g., `System Status`, `Check Services`, `Open Logs`).

## Layout Sketch
```
┌─────────────────────────────────────────────────────────────┐
│  HOUSTON — Mission Console                                 │
├─────────────────────────────────────────────────────────────┤
│  Conversation History (markdown, audio playback controls)   │
│  …                                                         │
├─────────────────────────────────────────────────────────────┤
│ [🎙️ Mic] [📎 Attach] [📋 Clipboard]  Houston, help me with… │
│ [System Status] [Check Services] [Recent Changes] [Deploy]  │
└─────────────────────────────────────────────────────────────┘
```

## Configuration & Hotkeys
- Extend `30_config/houston-features.json` with `ide_integration.hotkeys` overrides per workstation.
- Reserve `Cmd+Shift+H` for “Ask Houston”, `Cmd+Shift+V` for voice toggle, and allow overrides.
- Store interface prefs (e.g., transcript font size, always-on-top) in a new `30_config/houston-ui.json` (future work).

## Mission Control Integration
- Component lives in a shared shell so it persists across app tabs (e.g., React portal into root layout footer).
- Provide an API for other panels to inject context (active project, selected service, etc.).
- Ensure Houston’s presence indicator mirrors system health (telemetry feed).

## Future Enhancements
- Smart clipper to auto-summarize highlighted text into the prompt.
- Trust dashboard showing Houston’s "trust score" metrics before elevating phases.
- VPS route indicator icon (local vs. remote tool execution).

Track implementation under Phase 2 once validators and telemetry are stabilized.
