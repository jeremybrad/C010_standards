---
id: b0e954c5-5628-4ef5-b931-0d201557c84f
title: Notion Canvas API Extraction Guide
created: '2025-07-11T00:20:49.382238'
modified: '2025-07-11T00:20:49.382238'
tags:
- untagged
status: active
category: general
---
# Notion Canvas API Extraction Guide

Created: 2025-07-11
Purpose: Step-by-step guide for extracting Canvas data using MCP tools

## Overview

Since Notion Canvases are a special type of page with visual layout components, we need to:
1. Find Canvas pages using search
2. Extract their content including embedded blocks
3. Convert visual layouts to structured markdown
4. Classify and route content appropriately

## Step 1: Finding Canvas Pages

### Using Zapier MCP Search
```javascript
// Search for pages with "Canvas" in title
Zapier:notion_find_page_by_title
- title: "Canvas"
- exact_match: "no"
```

### Using Direct API Search
```javascript
Zapier:notion_api_request_beta
- method: POST
- url: https://api.notion.com/v1/search
- body: {
    "query": "Canvas",
    "filter": {
      "property": "object",
      "value": "page"
    },
    "sort": {
      "direction": "descending",
      "timestamp": "last_edited_time"
    }
  }
```

## Step 2: Getting Canvas Content

For each Canvas page found, we need to:

### A. Get Page Properties
```javascript
Zapier:notion_retrieve_a_page
- pageId: "[canvas-page-id]"
```

### B. Get Canvas Blocks
```javascript
Zapier:notion_retrieve_block_children
- blockId: "[canvas-page-id]"
```

## Step 3: Understanding Canvas Structure

Notion Canvases contain special block types:
- `synced_block` - References to other pages/databases
- `embed` - External content
- `link_to_page` - Internal Notion links
- `child_page` - Nested pages
- Groups and visual arrangements (stored as properties)

## Step 4: Content Classification

Use these indicators for classification:

### Work-Exclusive Indicators:
- Meeting notes with company names
- Analytics/KPI discussions
- Executive communication
- Proprietary project names

### Personal/Mixed Indicators:
- Codify references
- Betty AI mentions
- Philosophy/creative content
- Personal project names

## Step 5: Conversion Strategy

### For Visual Layouts:
1. Convert spatial arrangement to hierarchical structure
2. Group related blocks under headers
3. Preserve relationships through links

### For Embedded Content:
1. Extract embed URLs
2. Fetch content if possible
3. Create reference links

### For Synced Blocks:
1. Note the source
2. Decide whether to copy or link
3. Flag for manual review

## Example MCP Tool Chain

Here's the sequence to extract one Canvas:

```bash
# 1. Find Canvas by title
Zapier:notion_find_page_by_title
  title: "Research & Design Hub"

# 2. Get page ID from results
# Let's say it returns: "abc123..."

# 3. Retrieve full page
Zapier:notion_retrieve_a_page
  pageId: "abc123..."

# 4. Get all blocks
Zapier:notion_retrieve_block_children
  blockId: "abc123..."

# 5. For each child block that's interesting:
Zapier:notion_retrieve_block_children
  blockId: "[child-block-id]"
```

## Automation Opportunities

### Using Notion's API Pagination
When retrieving blocks, handle pagination:
```json
{
  "has_more": true,
  "next_cursor": "..."
}
```

### Batch Processing
Create a batch script that:
1. Gets all Canvas pages
2. Filters empty ones
3. Processes in order of last_edited
4. Generates migration report

## Manual Review Checklist

For each migrated Canvas:
- [ ] Check work content sensitivity
- [ ] Verify embed conversions
- [ ] Update internal links
- [ ] Add project connections
- [ ] Route to final location

## Next Actions

1. **Get Notion API Token**
   - Settings & Members → Integrations → New Integration
   - Grant content capabilities
   - Copy token for script

2. **Test with One Canvas**
   - Use "Research & Design Hub" as pilot
   - Document any issues
   - Refine classification rules

3. **Run Full Migration**
   - Process all 28 canvases
   - Review empty ones for deletion
   - Generate final report

## Troubleshooting

### Common Issues:
1. **Empty results**: Canvas might be in a private workspace
2. **Missing blocks**: Check permissions for integration
3. **Synced content**: May need separate API calls
4. **Large canvases**: Use pagination for blocks

### MCP Tool Errors:
- "validation_error": Usually means invalid page/block ID
- "unauthorized": Check integration permissions
- "rate_limited": Add delays between calls

## References
- [[00-Governance/Scripts/canvas-migration-script.py|Migration Script]]
- [[00-Inbox/Canvas-Migration/Canvas-Migration-Dashboard|Migration Dashboard]]
- [Notion API Docs](https://developers.notion.com/reference/retrieve-a-page)

---

Ready to start the extraction? Let's begin with getting your Notion API token!