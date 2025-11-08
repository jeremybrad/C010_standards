#!/usr/bin/env python3
"""
Canvas Migration Sorter
Created: 2025-07-11
Purpose: Sort and migrate exported Canvas files from Notion to appropriate Obsidian folders
"""

import os
import shutil
from pathlib import Path
from datetime import datetime

# Define paths
SOURCE_DIR = Path("/Users/jeremybradford/Downloads/Private & Shared/Canvas (working copy) 1dc9826889d48090aa5fdd543f43e045")
OBSIDIAN_VAULT = Path("/Users/jeremybradford/SyncedProjects/SharedData/Obsidian-Vault")

# Define categorization
CATEGORIZATION = {
    "betty_ai": {
        "files": [
            "Betty Ai Companion Setup",
            "Betty Memory Blueprint",
            "Betty Memory Technical Reference",
            "Betty Project Glossary",
            "Claude Research Summary – Betty Memory System",
            "Gemini Research Summary – Persistent Memory Layer",
            "Multithreaded Ai Conversation Model",
            "AI Preferences Metadata Layer"
        ],
        "destination": OBSIDIAN_VAULT / "Betty Prompt Library" / "Canvas-Imports"
    },
    "work_exclusive": {
        "files": [
            "Cro Analytics Backlog",
            "Executive Summary 3 31",
            "Sem Brand Analysis",
            "Sem Brand Test Report",
            "Weekly Performance Report May20-Jun02 2025",
            "Wow X Chrometrics",
            "Lead Data Doc",
            "Lead Data Project Summary",
            "Lead Discrepancy Email",
            "Lead Tracking Investigation",
            "Leadid Tracking Walkthrough",
            "Leadid Union Generator",
            "Wci 001 Data Mapping",
            "Canvas Reporting",
            "Data Dictionary",
            "Digital Innovation Template",
            "Fiber Attribution Analysis",
            "Quarterly Report Guide",
            "Q1 Review Session Journal",
            "Notion Query Tracker",
            "Task Tracker",
            "Team Style Guide Project"
        ],
        "destination": OBSIDIAN_VAULT / "00-Inbox" / "Canvas-Migration" / "Work-Related"
    },
    "personal_projects": {
        "files": [
            "Macromancer Arcanum",
            "Macromancer Glossary",
            "Macromancer Project Hub",
            "Codify + Notion Knowledgebase",
            "Codify Biofeedback Review",
            "Codify Glossary",
            "Master Tag Glossary",
            "Jamdeck Project Doc",
            "Project – Interactive Ai Duet Instrument",
            "Ambient Lighting Ai Project",
            "Socrates Project Blueprint"
        ],
        "destination": OBSIDIAN_VAULT / "00-Inbox" / "Canvas-Migration" / "Personal"
    },
    "personal_creative": {
        "files": [
            "Abandoned Cart Journal",
            "Mesa Reflections Journal",
            "Loop Of Absurd Ascension",
            "Reflections With Jeremy",
            "Skinner Suit Conversation Recap",
            "Owner Manual Natalie Edition",
            "Woodwinds Master Catalog",
            "Conversation Summarization Process",
            "Fact Detection"
        ],
        "destination": OBSIDIAN_VAULT / "00-Inbox" / "Canvas-Migration" / "Personal"
    },
    "system_meta": {
        "files": [
            "Chatgpt Response Prefs",
            "Gpt Pro Archive",
            "Gpt Profile Full Context",
            "Codex Of Al Master Archive",
            "Jpr To Notion Automation",
            "Project – First Open Ai Api Chatbot",
            "Experiment Oracle",
            "Ableton Mcp Ai Plan"
        ],
        "destination": OBSIDIAN_VAULT / "00-Inbox" / "Canvas-Migration" / "Mixed-Review"
    }
}

def clean_filename(filename):
    """Remove the hash suffix from Notion export filenames"""
    # Remove the hash (space + 32 chars + .md)
    if len(filename) > 36 and filename[-36:-3].count(' ') == 1:
        return filename[:-36] + ".md"
    return filename

def categorize_file(filename):
    """Determine which category a file belongs to"""
    # Remove .md extension for matching
    name_without_ext = filename.replace('.md', '').replace('.pdf', '')

    for category, info in CATEGORIZATION.items():
        for pattern in info['files']:
            if pattern.lower() in name_without_ext.lower():
                return category, info['destination']

    # Default to mixed review if not categorized
    return "uncategorized", OBSIDIAN_VAULT / "00-Inbox" / "Canvas-Migration" / "Mixed-Review"

def migrate_files(dry_run=True):
    """Migrate files to their appropriate locations"""
    migration_log = []

    # Get all files
    files = list(SOURCE_DIR.glob("*.md")) + list(SOURCE_DIR.glob("*.pdf"))

    print(f"Found {len(files)} files to process")

    for file_path in files:
        filename = file_path.name
        category, destination = categorize_file(filename)

        # Clean the filename
        clean_name = clean_filename(filename)

        # Determine destination path
        dest_path = destination / clean_name

        # Log the action
        action = {
            'original': filename,
            'cleaned': clean_name,
            'category': category,
            'source': str(file_path),
            'destination': str(dest_path),
            'exists': dest_path.exists()
        }

        if not dry_run:
            # Create destination directory if needed
            destination.mkdir(parents=True, exist_ok=True)

            # Copy file (don't move, in case we need to re-run)
            if not dest_path.exists():
                shutil.copy2(file_path, dest_path)
                action['status'] = 'copied'
            else:
                action['status'] = 'skipped - exists'
        else:
            action['status'] = 'dry run'

        migration_log.append(action)
        print(f"{category:20} | {clean_name}")

    return migration_log

def generate_report(migration_log):
    """Generate a migration report"""
    report = f"""# Canvas Migration Report
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}

## Summary
Total Files: {len(migration_log)}

## By Category:
"""

    # Count by category
    categories = {}
    for entry in migration_log:
        cat = entry['category']
        categories[cat] = categories.get(cat, 0) + 1

    for cat, count in sorted(categories.items()):
        report += f"- {cat}: {count}\n"

    report += "\n## Detailed Migration Log\n\n"
    report += "| Original File | Category | Destination | Status |\n"
    report += "|--------------|----------|-------------|--------|\n"

    for entry in migration_log:
        report += f"| {entry['cleaned']} | {entry['category']} | {entry['destination'].split('Canvas-Migration/')[-1] if 'Canvas-Migration' in entry['destination'] else 'Betty Library'} | {entry['status']} |\n"

    return report

if __name__ == "__main__":
    print("Canvas Migration Script")
    print("======================")

    # First, do a dry run
    print("\nDRY RUN - Showing what would happen:")
    print("-" * 50)
    log = migrate_files(dry_run=True)

    # Generate report
    report = generate_report(log)

    # Save report
    report_path = OBSIDIAN_VAULT / "00-Inbox" / "Canvas-Migration" / "migration-report-2025-07-11.md"
    report_path.write_text(report)
    print(f"\nReport saved to: {report_path}")

    # Ask for confirmation
    response = input("\nProceed with actual migration? (yes/no): ")
    if response.lower() == 'yes':
        print("\nMigrating files...")
        log = migrate_files(dry_run=False)

        # Update report with actual results
        report = generate_report(log)
        report_path.write_text(report)
        print("Migration complete!")
    else:
        print("Migration cancelled.")
