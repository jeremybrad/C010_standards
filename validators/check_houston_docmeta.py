#!/usr/bin/env python3
"""Validator for Houston DocMeta tag conventions.

Ensures Houston-targeted documents follow tagging conventions for precise retrieval.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, cast

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from validators.common import safe_print

try:
    import yaml

    HAS_YAML = True
except ImportError:
    HAS_YAML = False

DEFAULT_TARGETS = (
    "schemas",
    "notes",
)
TAXONOMY_PATH = Path("taxonomies/topic_taxonomy.yaml")


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Check Houston DocMeta tagging")
    parser.add_argument(
        "paths",
        nargs="*",
        default=DEFAULT_TARGETS,
        help="Directories or files to inspect for Houston-tagged DocMeta entries",
    )
    parser.add_argument(
        "--taxonomy",
        default=TAXONOMY_PATH,
        type=Path,
        help="Path to topic taxonomy YAML",
    )
    parser.add_argument(
        "--fix", action="store_true", help="Suggest fixes for missing tags"
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Show detailed output"
    )
    parser.add_argument(
        "--json-output",
        type=Path,
        help="Write results to JSON file (e.g., 70_evidence/validator_docmeta.json)",
    )
    return parser.parse_args(argv)


def load_yaml_front_matter(file_path: Path) -> dict[str, Any] | None:
    """Extract YAML front matter from markdown file."""
    if not HAS_YAML:
        return None

    try:
        content = file_path.read_text()
        if not content.startswith("---"):
            return None

        # Extract YAML between --- delimiters
        parts = content.split("---", 2)
        if len(parts) < 3:
            return None

        data = yaml.safe_load(parts[1])
        return cast(dict[str, Any], data) if data else None
    except Exception:
        return None


def load_yaml_file(file_path: Path) -> dict[str, Any] | None:
    """Load standalone YAML file."""
    if not HAS_YAML:
        return None

    try:
        data = yaml.safe_load(file_path.read_text())
        return cast(dict[str, Any], data) if data else None
    except Exception:
        return None


def load_topic_taxonomy(taxonomy_path: Path) -> set[str]:
    """Load allowed topics from taxonomy file."""
    if not HAS_YAML or not taxonomy_path.exists():
        return set()

    try:
        data = yaml.safe_load(taxonomy_path.read_text())
        if isinstance(data, dict) and "topics" in data:
            return set(data["topics"])
        return set()
    except Exception:
        return set()


def is_houston_document(metadata: dict) -> bool:
    """Check if document is tagged for Houston agent."""
    routing_tags = metadata.get("routing", {}).get("tags", [])
    if isinstance(routing_tags, str):
        routing_tags = [routing_tags]

    return any(
        tag in ["agent:houston", "source:mission-control"] for tag in routing_tags
    )


def validate_document(
    file_path: Path, metadata: dict, allowed_topics: set[str], verbose: bool = False
) -> list[str]:
    """Validate a single Houston-tagged document. Returns list of errors."""
    errors: list[str] = []

    if not is_houston_document(metadata):
        if verbose:
            print(f"  ⊘ {file_path.name}: Not a Houston document, skipping")
        return errors

    # Check 1: doc.projects includes "Mission Control" and "C010"
    projects = metadata.get("doc", {}).get("projects", [])
    required_projects = {"Mission Control", "C010", "P210"}  # Accept old P210 too
    if not any(p in projects for p in required_projects):
        errors.append(
            f"{file_path}: Missing required project in doc.projects. "
            f"Expected one of {required_projects}, got {projects}"
        )

    # Check 2: routing.tags contains "agent:houston" and "sensitivity:internal"
    routing_tags = metadata.get("routing", {}).get("tags", [])
    if isinstance(routing_tags, str):
        routing_tags = [routing_tags]

    required_tags = {"agent:houston", "sensitivity:internal"}
    missing_tags = required_tags - set(routing_tags)
    if missing_tags:
        errors.append(
            f"{file_path}: Missing required tags in routing.tags: {missing_tags}"
        )

    # Check 3: doc.topics values exist in taxonomy
    topics = metadata.get("doc", {}).get("topics", [])
    if topics and allowed_topics:
        invalid_topics = set(topics) - allowed_topics
        if invalid_topics:
            errors.append(
                f"{file_path}: Invalid topics not in taxonomy: {invalid_topics}. "
                f"See taxonomies/topic_taxonomy.yaml"
            )

    # Check 4: connections.related_docs required for playbook:success docs
    if "playbook:success" in routing_tags:
        related_docs = metadata.get("connections", {}).get("related_docs", [])
        if not related_docs:
            errors.append(
                f"{file_path}: routing.tags contains 'playbook:success' but "
                "connections.related_docs is empty. Add related documentation."
            )

    if verbose and not errors:
        safe_print(f"  ✓ {file_path.name}: All checks passed")

    return errors


def find_yaml_files(paths: list[str | Path]) -> list[Path]:
    """Find all YAML and markdown files in given paths."""
    files = []
    for path_str in paths:
        path = Path(path_str)
        if path.is_file():
            if path.suffix in {".yaml", ".yml", ".md"}:
                files.append(path)
        elif path.is_dir():
            files.extend(path.rglob("*.yaml"))
            files.extend(path.rglob("*.yml"))
            files.extend(path.rglob("*.md"))
    return files


def cli(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)

    if not HAS_YAML:
        print("ERROR: PyYAML library not installed. Install with: pip install pyyaml")
        return 2

    # Load topic taxonomy
    allowed_topics = load_topic_taxonomy(args.taxonomy)
    if not allowed_topics and args.verbose:
        print(f"WARNING: Could not load topic taxonomy from {args.taxonomy}")

    # Find all relevant files
    files = find_yaml_files(args.paths)
    if args.verbose:
        print(f"Scanning {len(files)} files for Houston DocMeta tags...\n")

    # Validate each file
    results = {}
    all_errors = []

    for file_path in files:
        # Try loading as front matter first (for .md), then as YAML
        metadata = load_yaml_front_matter(file_path)
        if metadata is None and file_path.suffix in {".yaml", ".yml"}:
            metadata = load_yaml_file(file_path)

        if metadata is None:
            continue

        # Only validate Houston documents
        if not is_houston_document(metadata):
            continue

        errors = validate_document(file_path, metadata, allowed_topics, args.verbose)
        if errors:
            all_errors.extend(errors)
            results[str(file_path)] = {"status": "fail", "errors": errors}
        else:
            results[str(file_path)] = {"status": "pass", "errors": []}

    # Write JSON output if requested
    if args.json_output:
        args.json_output.parent.mkdir(parents=True, exist_ok=True)
        output_data = {
            "total_files": len(files),
            "validated_files": len(results),
            "passed": sum(1 for r in results.values() if r["status"] == "pass"),
            "failed": sum(1 for r in results.values() if r["status"] == "fail"),
            "results": results,
        }
        args.json_output.write_text(json.dumps(output_data, indent=2))
        if args.verbose:
            print(f"\nResults written to {args.json_output}")

    # Report summary
    if all_errors:
        safe_print(f"\n❌ DocMeta validation FAILED ({len(all_errors)} issues):\n")
        for i, error in enumerate(all_errors, 1):
            safe_print(f"  {i}. {error}")

        if args.fix:
            safe_print("\n💡 Fix suggestions:")
            safe_print('  - Add required projects: ["Mission Control", "C010"]')
            safe_print('  - Add required tags: ["agent:houston", ...]')
            safe_print("  - Validate topics against taxonomies/topic_taxonomy.yaml")
            safe_print("  - Add connections.related_docs for playbook:success")

        return 1
    else:
        validated_count = len(results)
        if args.verbose:
            safe_print(f"\n✅ DocMeta checks passed ({validated_count} documents)")
        else:
            safe_print(f"✅ DocMeta validation passed ({validated_count} docs)")
        return 0


if __name__ == "__main__":
    raise SystemExit(cli())
