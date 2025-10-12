---
id: 7c5447c4-a295-4a7a-9997-522bb47856e4
title: Stream Deck Configuration Preview
created: '2025-07-17T21:09:40.770956'
modified: '2025-07-17T21:09:40.770956'
tags:
- untagged
status: active
category: general
---
# Stream Deck Configuration Preview

**Profile:** Obsidian Projects
**Grid:** 5x5 (25 buttons)

## Button Layout

| Col 1 | Col 2 | Col 3 | Col 4 | Col 5 |
| --- | --- | --- | --- | --- |
| 📅<br>**Daily Note** | 🏠<br>**Command Center** | 📥<br>**Inbox** | 🔥<br>**Active Projects** | 🎯<br>**Battle Journal** |
| 📍<br>**Betty Tracker** | 🤖<br>**Claude Code** | 💻<br>**Codify** | 💬<br>**Conv Archive** | 🌐<br>**Digital Unify** |
| 🧠<br>**Knowledge Tool** | 🔧<br>**MCP Impl** | 📊<br>**WOW Lead Attr** | 🎛️<br>**Ableton MCP** | 🎹<br>**Band in Box AI** |
| 🤖<br>**Betty AI** | 🔌<br>**Betty MCP** | ⌨️<br>**Macromancer** | 💾<br>**Memory System** | 🎼<br>**Midi Gesture** |
| 🔄<br>**N8n MCP** | 💻<br>**PC Setup** | 🔊<br>**Resonance** | 🎙️<br>**Voice Pipeline** | *[Empty]* |

## Button Details

### Utility Buttons (Row 1, Positions 1-3)

#### 1. 📅 Daily Note
- **Action:** `obsidian://daily-note`
- **Colors:** Background `#4F5D75`, Text `#FFFFFF`
- Opens today's daily note

#### 2. 🏠 Command Center
- **Path:** `🏠 Command Center.md`
- **URL:** `obsidian://open?vault=Obsidian-Vault&file=%F0%9F%8F%A0%20Command%20Center.md`
- **Colors:** Background `#EF8354` (Orange), Text `#FFFFFF`

#### 3. 📥 Inbox
- **Path:** `00-Inbox`
- **URL:** `obsidian://open?vault=Obsidian-Vault&file=00-Inbox`
- **Colors:** Background `#4F5D75`, Text `#FFFFFF`

### Project Buttons (Remaining positions)

All project buttons use:
- **Background Color:** `#2D3142` (Dark blue-gray)
- **Text Color:** `#FFFFFF` (White)

#### Key Projects:

**🎯 Battle Journal Attribution Win** - Your current high-priority project for Monday delivery

**📊 WOW Lead Attribution Infrastructure** - The comprehensive Lead ID tracking project

**🧠 Knowledge Synthesis Tool** - Your PKM integration system

**💬 Conversation Archive System** - Betty & Claude conversation management

**🔧 MCP Implementation** - Various MCP tool integrations

## Usage Instructions

1. **Import to Stream Deck:**
   - Copy the JSON from `00-Governance/stream-deck-config.json`
   - In Stream Deck software, create a new profile
   - Import or manually configure buttons using the JSON data

2. **Button Actions:**
   - Each button opens the corresponding Obsidian location
   - URLs are pre-encoded for special characters
   - Utility buttons (Daily Note, Command Center, Inbox) are highlighted with different colors

3. **Customization:**
   - Adjust colors to your preference
   - Rearrange buttons based on frequency of use
   - Add keyboard shortcuts for quick access

## Color Scheme
- **Utility Buttons:** Mixed colors for visual distinction
  - Daily Note & Inbox: `#4F5D75` (Medium blue-gray)
  - Command Center: `#EF8354` (Vibrant orange)
- **Project Buttons:** `#2D3142` (Consistent dark theme)

---

**Files Generated:**
- JSON Config: `00-Governance/stream-deck-config.json`
- Preview: `00-Governance/stream-deck-preview.md` (this file)
- Generator Script: `Code Library/Python/Automation/stream-deck-config-generator.py`
