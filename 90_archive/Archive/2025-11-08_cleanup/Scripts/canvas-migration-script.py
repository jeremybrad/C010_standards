#!/usr/bin/env python3
"""
Notion Canvas to Obsidian Migration Script
Created: 2025-07-11
Purpose: Extract Canvas content from Notion and convert to Obsidian-compatible format

This script handles the migration of Notion Canvas content to Obsidian, dealing with:
1. Visual layouts that need text representation
2. Embedded blocks and databases
3. Work/personal content classification
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Any
import requests
from pathlib import Path

class NotionCanvasMigrator:
    def __init__(self, notion_token: str, obsidian_vault: str):
        self.notion_token = notion_token
        self.obsidian_vault = Path(obsidian_vault)
        self.headers = {
            "Authorization": f"Bearer {notion_token}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28"
        }
        self.migration_log = []

    def search_canvases(self) -> List[Dict]:
        """Search for all Canvas pages in Notion"""
        url = "https://api.notion.com/v1/search"
        payload = {
            "query": "Canvas",
            "filter": {
                "property": "object",
                "value": "page"
            },
            "page_size": 100
        }

        response = requests.post(url, headers=self.headers, json=payload)
        if response.status_code == 200:
            return response.json().get('results', [])
        else:
            print(f"Error searching: {response.status_code}")
            return []

    def get_canvas_content(self, page_id: str) -> Dict:
        """Retrieve full content of a Canvas page"""
        # Get page properties
        page_url = f"https://api.notion.com/v1/pages/{page_id}"
        page_response = requests.get(page_url, headers=self.headers)

        # Get page blocks (content)
        blocks_url = f"https://api.notion.com/v1/blocks/{page_id}/children"
        blocks_response = requests.get(blocks_url, headers=self.headers)

        return {
            'properties': page_response.json() if page_response.status_code == 200 else {},
            'blocks': blocks_response.json().get('results', []) if blocks_response.status_code == 200 else []
        }

    def classify_content(self, content: Dict) -> str:
        """Classify content as work-exclusive, personal, or mixed"""
        # Simple keyword-based classification
        work_keywords = ['analytics', 'kpi', 'conversion', 'executive', 'meeting', 'report']
        personal_keywords = ['codify', 'macromancer', 'betty', 'philosophy', 'ideas']

        text_content = json.dumps(content).lower()

        work_score = sum(1 for keyword in work_keywords if keyword in text_content)
        personal_score = sum(1 for keyword in personal_keywords if keyword in text_content)

        if work_score > 0 and personal_score == 0:
            return "work-exclusive"
        elif personal_score > 0 and work_score == 0:
            return "personal"
        elif work_score > 0 and personal_score > 0:
            return "mixed"
        else:
            return "unclassified"

    def convert_to_obsidian(self, canvas_data: Dict, classification: str) -> str:
        """Convert Notion Canvas to Obsidian-compatible format"""
        # Extract metadata
        properties = canvas_data.get('properties', {})
        title = self._extract_title(properties)
        created_time = properties.get('created_time', '')
        last_edited = properties.get('last_edited_time', '')

        # Build markdown content
        markdown = f"""# {title}

---
created: {created_time}
last_edited: {last_edited}
source: notion_canvas
classification: {classification}
migration_date: {datetime.now().isoformat()}
tags: [canvas-migration, {classification}]
---

## Original Canvas Structure

"""

        # Process blocks
        blocks = canvas_data.get('blocks', [])
        for block in blocks:
            markdown += self._process_block(block)

        # Add migration notes
        markdown += f"""

---

## Migration Notes

- **Classification**: {classification}
- **Original Notion ID**: {properties.get('id', 'unknown')}
- **Migration Date**: {datetime.now().strftime('%Y-%m-%d')}

### Action Items Extracted
- [ ] Review for work sensitivity
- [ ] Link to relevant projects
- [ ] Extract reusable components

### Related Projects
<!-- Add links to related Obsidian projects here -->

"""

        return markdown

    def _extract_title(self, properties: Dict) -> str:
        """Extract title from Notion properties"""
        title_prop = properties.get('properties', {}).get('title', {})
        if title_prop.get('type') == 'title':
            title_array = title_prop.get('title', [])
            if title_array:
                return title_array[0].get('plain_text', 'Untitled Canvas')
        return 'Untitled Canvas'

    def _process_block(self, block: Dict, indent: int = 0) -> str:
        """Process individual Notion blocks"""
        block_type = block.get('type', '')
        indent_str = "  " * indent

        # Handle different block types
        if block_type == 'paragraph':
            text = self._extract_text(block.get(block_type, {}))
            return f"{indent_str}{text}\n\n"

        elif block_type == 'heading_1':
            text = self._extract_text(block.get(block_type, {}))
            return f"{indent_str}## {text}\n\n"

        elif block_type == 'heading_2':
            text = self._extract_text(block.get(block_type, {}))
            return f"{indent_str}### {text}\n\n"

        elif block_type == 'bulleted_list_item':
            text = self._extract_text(block.get(block_type, {}))
            return f"{indent_str}- {text}\n"

        elif block_type == 'numbered_list_item':
            text = self._extract_text(block.get(block_type, {}))
            return f"{indent_str}1. {text}\n"

        elif block_type == 'code':
            code_block = block.get(block_type, {})
            language = code_block.get('language', '')
            text = self._extract_text(code_block)
            return f"{indent_str}```{language}\n{text}\n```\n\n"

        # Canvas-specific blocks
        elif block_type == 'embed':
            url = block.get(block_type, {}).get('url', '')
            return f"{indent_str}> [Embedded Content]({url})\n\n"

        elif block_type == 'synced_block':
            return f"{indent_str}> [Synced Block - Manual Review Needed]\n\n"

        else:
            return f"{indent_str}> [{block_type} - Needs Manual Conversion]\n\n"

    def _extract_text(self, text_object: Dict) -> str:
        """Extract plain text from Notion text object"""
        if isinstance(text_object, dict):
            rich_text = text_object.get('rich_text', [])
            if isinstance(rich_text, list):
                return ''.join([item.get('plain_text', '') for item in rich_text])
        return ''

    def migrate_canvas(self, canvas_id: str, dry_run: bool = False) -> Dict:
        """Migrate a single canvas"""
        print(f"Migrating canvas {canvas_id}...")

        # Get content
        content = self.get_canvas_content(canvas_id)

        # Classify
        classification = self.classify_content(content)

        # Convert
        markdown = self.convert_to_obsidian(content, classification)

        # Determine path
        title = self._extract_title(content.get('properties', {}))
        safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).rstrip()

        if classification == "work-exclusive":
            folder = self.obsidian_vault / "00-Inbox" / "Canvas-Migration" / "Work-Related"
        elif classification == "mixed":
            folder = self.obsidian_vault / "00-Inbox" / "Canvas-Migration" / "Mixed-Content"
        else:
            folder = self.obsidian_vault / "00-Inbox" / "Canvas-Migration" / "Personal"

        filepath = folder / f"{safe_title}.md"

        if not dry_run:
            folder.mkdir(parents=True, exist_ok=True)
            filepath.write_text(markdown)

        result = {
            'canvas_id': canvas_id,
            'title': title,
            'classification': classification,
            'filepath': str(filepath),
            'dry_run': dry_run
        }

        self.migration_log.append(result)
        return result

    def generate_migration_report(self) -> str:
        """Generate a migration report"""
        report = f"""# Canvas Migration Report

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}

## Summary
- Total Canvases Processed: {len(self.migration_log)}
- Work-Exclusive: {sum(1 for log in self.migration_log if log['classification'] == 'work-exclusive')}
- Personal: {sum(1 for log in self.migration_log if log['classification'] == 'personal')}
- Mixed: {sum(1 for log in self.migration_log if log['classification'] == 'mixed')}
- Unclassified: {sum(1 for log in self.migration_log if log['classification'] == 'unclassified')}

## Migration Details

| Canvas Title | Classification | File Path | Status |
|-------------|----------------|-----------|--------|
"""

        for log in self.migration_log:
            status = "Dry Run" if log['dry_run'] else "Migrated"
            report += f"| {log['title']} | {log['classification']} | {log['filepath']} | {status} |\n"

        return report


# Example usage
if __name__ == "__main__":
    # Configuration
    NOTION_TOKEN = os.environ.get('NOTION_TOKEN', 'your-token-here')
    OBSIDIAN_VAULT = "/Users/jeremybradford/Obsidian-Vault"

    # Initialize migrator
    migrator = NotionCanvasMigrator(NOTION_TOKEN, OBSIDIAN_VAULT)

    # Search for canvases
    canvases = migrator.search_canvases()
    print(f"Found {len(canvases)} canvases")

    # Migrate each canvas (dry run first)
    for canvas in canvases[:3]:  # Start with first 3
        result = migrator.migrate_canvas(canvas['id'], dry_run=True)
        print(f"Would migrate: {result['title']} -> {result['classification']}")

    # Generate report
    report = migrator.generate_migration_report()
    report_path = Path(OBSIDIAN_VAULT) / "00-Inbox" / "Canvas-Migration" / "migration-report.md"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(report)
    print(f"Report saved to: {report_path}")
