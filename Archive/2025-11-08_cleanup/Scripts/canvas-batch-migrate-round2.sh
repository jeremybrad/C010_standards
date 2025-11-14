#!/bin/bash
# Canvas Migration Script - Round 2 - 2025-07-11

SOURCE="/Users/jeremybradford/Downloads/Private & Shared 2/Canvas 1d99826889d480148b55cc78bde4058b"
VAULT="/Users/jeremybradford/Obsidian-Vault"

# Process the named files first
echo "Processing named Canvas files..."

# The important named ones
cp "$SOURCE/Research & Design Hub"*.md "$VAULT/00-Inbox/Canvas-Migration/Personal/Research & Design Hub.md" 2>/dev/null
cp "$SOURCE/Tags Db Structure"*.md "$VAULT/00-Inbox/Canvas-Migration/Personal/Tags Db Structure.md" 2>/dev/null
cp "$SOURCE/Canva Db System Reference"*.md "$VAULT/00-Inbox/Canvas-Migration/Personal/Canvas Db System Reference.md" 2>/dev/null
cp "$SOURCE/Isp Trends Presentation"*.md "$VAULT/00-Inbox/Canvas-Migration/Work-Related/Isp Trends Presentation.md" 2>/dev/null
cp "$SOURCE/Meeting Summary Analytics Insights"*.md "$VAULT/00-Inbox/Canvas-Migration/Work-Related/Meeting Summary Analytics Insights v2.md" 2>/dev/null

# Handle duplicates with version numbers
cp "$SOURCE/Lead Data Doc"*.md "$VAULT/00-Inbox/Canvas-Migration/Work-Related/Lead Data Doc v2.md" 2>/dev/null
cp "$SOURCE/Project – First Open Ai Api Chatbot"*.md "$VAULT/00-Inbox/Canvas-Migration/Mixed-Review/Project – First Open Ai Api Chatbot v2.md" 2>/dev/null

# Process untitled files with sequential numbering
echo "Processing untitled Canvas files..."
counter=1
for file in "$SOURCE"/Untitled*.md; do
    if [ -f "$file" ]; then
        cp "$file" "$VAULT/00-Inbox/Canvas-Migration/Mixed-Review/Untitled-Canvas-$(printf "%02d" $counter).md" 2>/dev/null
        echo "Copied Untitled file $counter"
        ((counter++))
    fi
done

echo "Migration Round 2 complete!"
echo "Named files: 7"
echo "Untitled files: 9"
echo "Total new files: 16"
