#!/usr/bin/env python3
"""Constitution guardrail validator.

Enforces documentation drift guardrails for C010_standards:
- No C000_info-center identity outside 70_evidence/
- No exit code 99 references in docs
- Consistent 0/1/2 exit code contract in docs
- Correct validator run location (from repo root, not cd validators)
- Consistent Python minimum version across docs
- Correct KNOWN_PROJECTS.md path references
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

CURRENT_DIR = Path(__file__).resolve().parent
REPO_ROOT = CURRENT_DIR.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from validators.common import report_validation_results, safe_print  # noqa: E402


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Check constitution guardrails")
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Enable verbose output"
    )
    return parser.parse_args(argv)


def get_doc_files(repo_root: Path) -> list[Path]:
    """Get all markdown and YAML files outside 70_evidence/ and 20_receipts/."""
    excluded_dirs = {"70_evidence", "20_receipts", ".git", "venv", ".venv", "node_modules"}
    doc_files = []

    for pattern in ["**/*.md", "**/*.yaml", "**/*.yml"]:
        for path in repo_root.glob(pattern):
            # Skip excluded directories
            if any(excluded in path.parts for excluded in excluded_dirs):
                continue
            doc_files.append(path)

    return doc_files


def check_c000_identity(doc_files: list[Path], verbose: bool) -> list[str]:
    """Check for C000_info-center identity references (not allowed)."""
    errors = []
    pattern = re.compile(r"C000[_-]info[_-]center", re.IGNORECASE)

    for path in doc_files:
        try:
            content = path.read_text(encoding="utf-8", errors="replace")
            matches = pattern.findall(content)
            if matches:
                rel_path = path.relative_to(REPO_ROOT)
                errors.append(
                    f"{rel_path}: Contains C000_info-center identity reference "
                    f"(found {len(matches)} occurrence(s))"
                )
        except Exception as e:
            if verbose:
                safe_print(f"  Warning: Could not read {path}: {e}")

    if verbose and not errors:
        safe_print("  ✓ No C000_info-center identity references found")

    return errors


def check_exit_code_99(doc_files: list[Path], verbose: bool) -> list[str]:
    """Check for exit code 99 references (deprecated)."""
    errors = []
    # Match "exit code 99" or "exit.*99" but not in historical context
    patterns = [
        re.compile(r"exit\s+code\s+99", re.IGNORECASE),
        re.compile(r"exit[s]?\s+with\s+(?:status\s+)?99", re.IGNORECASE),
        re.compile(r"returns?\s+99", re.IGNORECASE),
    ]

    for path in doc_files:
        try:
            content = path.read_text(encoding="utf-8", errors="replace")
            for pattern in patterns:
                matches = pattern.findall(content)
                if matches:
                    rel_path = path.relative_to(REPO_ROOT)
                    # Check if it's in a context explaining removal (allowed)
                    if "removed" in content.lower() or "no longer" in content.lower():
                        if verbose:
                            safe_print(f"  ✓ {rel_path}: Exit code 99 in historical context (allowed)")
                        continue
                    errors.append(
                        f"{rel_path}: Contains exit code 99 reference (deprecated)"
                    )
                    break  # Only report once per file
        except Exception as e:
            if verbose:
                safe_print(f"  Warning: Could not read {path}: {e}")

    if verbose and not errors:
        safe_print("  ✓ No active exit code 99 references found")

    return errors


def check_exit_code_contract(doc_files: list[Path], verbose: bool) -> list[str]:
    """Check that docs consistently present 0/1/2 exit code contract."""
    errors = []
    # Look for exit code documentation that's missing code 2
    exit_code_section_pattern = re.compile(
        r"(?:exit\s+code|validator\s+exit)[s]?\s*:?\s*\n"
        r"(?:[-*]\s*`?0`?[:\s]+.*\n)"
        r"(?:[-*]\s*`?1`?[:\s]+.*\n)"
        r"(?![-*]\s*`?2`?)",  # Negative lookahead - missing code 2
        re.IGNORECASE | re.MULTILINE
    )

    for path in doc_files:
        try:
            content = path.read_text(encoding="utf-8", errors="replace")
            # Look for exit code sections
            if re.search(r"exit\s+code", content, re.IGNORECASE):
                # Check if it has 0 and 1 but not 2
                has_0 = re.search(r"`?0`?\s*[:=]?\s*(?:all\s+checks\s+pass|pass)", content, re.IGNORECASE)
                has_1 = re.search(r"`?1`?\s*[:=]?\s*(?:validation\s+fail|fail)", content, re.IGNORECASE)
                has_2 = re.search(r"`?2`?\s*[:=]?\s*(?:config|parse|error)", content, re.IGNORECASE)

                if has_0 and has_1 and not has_2:
                    rel_path = path.relative_to(REPO_ROOT)
                    errors.append(
                        f"{rel_path}: Exit code documentation missing code 2 (config/parse error)"
                    )
        except Exception as e:
            if verbose:
                safe_print(f"  Warning: Could not read {path}: {e}")

    if verbose and not errors:
        safe_print("  ✓ Exit code contract (0/1/2) documented consistently")

    return errors


def check_run_location(doc_files: list[Path], verbose: bool) -> list[str]:
    """Check for incorrect validator run location instructions."""
    errors = []
    # Match "cd validators" followed by running a validator (bad pattern)
    bad_patterns = [
        re.compile(r"cd\s+validators\s*&&\s*python", re.IGNORECASE),
        re.compile(r"cd\s+validators\s*\n\s*python\s+(?:check_|run_)", re.IGNORECASE),
    ]

    # Allow "cd validators" in "wrong" example contexts
    wrong_context_pattern = re.compile(r"(?:wrong|don't|incorrect|bad)", re.IGNORECASE)

    for path in doc_files:
        try:
            content = path.read_text(encoding="utf-8", errors="replace")
            lines = content.split("\n")

            for i, line in enumerate(lines):
                for pattern in bad_patterns:
                    if pattern.search(line):
                        # Check surrounding context for "wrong" indicator
                        context_start = max(0, i - 3)
                        context = "\n".join(lines[context_start:i+1])

                        if wrong_context_pattern.search(context):
                            if verbose:
                                rel_path = path.relative_to(REPO_ROOT)
                                safe_print(f"  ✓ {rel_path}:{i+1}: 'cd validators' in 'wrong' example (allowed)")
                            continue

                        rel_path = path.relative_to(REPO_ROOT)
                        errors.append(
                            f"{rel_path}:{i+1}: Recommends 'cd validators' before running "
                            f"(should run from repo root: python validators/run_all.py)"
                        )
                        break
        except Exception as e:
            if verbose:
                safe_print(f"  Warning: Could not read {path}: {e}")

    if verbose and not errors:
        safe_print("  ✓ All validator run instructions use repo root pattern")

    return errors


def check_python_version(doc_files: list[Path], verbose: bool) -> list[str]:
    """Check for inconsistent Python version requirements."""
    errors = []
    version_pattern = re.compile(r"Python\s+3\.(\d+)\+?", re.IGNORECASE)
    canonical_version = "3.11"  # From pyproject.toml

    versions_found: dict[str, list[str]] = {}

    for path in doc_files:
        try:
            content = path.read_text(encoding="utf-8", errors="replace")
            matches = version_pattern.findall(content)
            for minor_ver in matches:
                version = f"3.{minor_ver}"
                if version not in versions_found:
                    versions_found[version] = []
                rel_path = str(path.relative_to(REPO_ROOT))
                if rel_path not in versions_found[version]:
                    versions_found[version].append(rel_path)
        except Exception as e:
            if verbose:
                safe_print(f"  Warning: Could not read {path}: {e}")

    # Check for versions lower than canonical (wrong minimum)
    for version, files in versions_found.items():
        minor = int(version.split(".")[1])
        canonical_minor = int(canonical_version.split(".")[1])
        if minor < canonical_minor:
            for f in files:
                errors.append(
                    f"{f}: States Python {version}+ but canonical minimum is {canonical_version}+"
                )

    if verbose:
        if versions_found:
            safe_print(f"  Python versions found: {', '.join(sorted(versions_found.keys()))}")
        if not errors:
            safe_print(f"  ✓ Python version requirements consistent with {canonical_version}+")

    return errors


def check_known_projects_path(doc_files: list[Path], verbose: bool) -> list[str]:
    """Check for incorrect KNOWN_PROJECTS.md path references."""
    errors = []
    # Correct path is 70_evidence/workspace/KNOWN_PROJECTS.md
    correct_path = "70_evidence/workspace/KNOWN_PROJECTS.md"

    for path in doc_files:
        try:
            content = path.read_text(encoding="utf-8", errors="replace")

            # Check if file references KNOWN_PROJECTS.md
            if "KNOWN_PROJECTS" not in content:
                continue

            # Find all KNOWN_PROJECTS.md references
            # Correct patterns (should not trigger errors):
            # - 70_evidence/workspace/KNOWN_PROJECTS.md
            # - `70_evidence/workspace/KNOWN_PROJECTS.md`
            # - (70_evidence/workspace/KNOWN_PROJECTS.md)
            # - [70_evidence/workspace/KNOWN_PROJECTS.md]
            #
            # Incorrect patterns (should trigger errors):
            # - workspace/KNOWN_PROJECTS.md (without 70_evidence prefix)
            # - `workspace/KNOWN_PROJECTS.md`

            incorrect_refs = []

            # Find all occurrences of workspace/KNOWN_PROJECTS.md
            for match in re.finditer(r"workspace/KNOWN_PROJECTS\.md", content):
                start = match.start()
                # Check if preceded by "70_evidence/"
                prefix_start = max(0, start - 12)  # len("70_evidence/") = 12
                prefix = content[prefix_start:start]
                if "70_evidence/" not in prefix:
                    # Get context for error message
                    line_start = content.rfind("\n", 0, start) + 1
                    line_end = content.find("\n", start)
                    if line_end == -1:
                        line_end = len(content)
                    context = content[line_start:line_end].strip()[:60]
                    incorrect_refs.append(context)

            if incorrect_refs:
                rel_path = path.relative_to(REPO_ROOT)
                errors.append(
                    f"{rel_path}: References workspace/KNOWN_PROJECTS.md without 70_evidence/ prefix "
                    f"({len(incorrect_refs)} occurrence(s))"
                )
        except Exception as e:
            if verbose:
                safe_print(f"  Warning: Could not read {path}: {e}")

    if verbose and not errors:
        safe_print(f"  ✓ KNOWN_PROJECTS.md path references use correct {correct_path}")

    return errors


def cli(argv: list[str] | None = None) -> int:
    args = parse_args(argv if argv is not None else [])

    if args.verbose:
        safe_print("Constitution guardrail validator")
        safe_print(f"Repository root: {REPO_ROOT}")
        safe_print("")

    # Get doc files to check
    doc_files = get_doc_files(REPO_ROOT)

    if args.verbose:
        safe_print(f"Checking {len(doc_files)} documentation files...")
        safe_print("")

    all_errors: list[str] = []

    # Run all constitution checks
    if args.verbose:
        safe_print("1. Checking for C000_info-center identity references...")
    all_errors.extend(check_c000_identity(doc_files, args.verbose))

    if args.verbose:
        safe_print("\n2. Checking for exit code 99 references...")
    all_errors.extend(check_exit_code_99(doc_files, args.verbose))

    if args.verbose:
        safe_print("\n3. Checking exit code contract consistency (0/1/2)...")
    all_errors.extend(check_exit_code_contract(doc_files, args.verbose))

    if args.verbose:
        safe_print("\n4. Checking validator run location instructions...")
    all_errors.extend(check_run_location(doc_files, args.verbose))

    if args.verbose:
        safe_print("\n5. Checking Python version consistency...")
    all_errors.extend(check_python_version(doc_files, args.verbose))

    if args.verbose:
        safe_print("\n6. Checking KNOWN_PROJECTS.md path references...")
    all_errors.extend(check_known_projects_path(doc_files, args.verbose))

    # Build remediation suggestions
    suggestions = {}
    if any("C000" in e for e in all_errors):
        suggestions["identity"] = [
            "Replace C000_info-center with C010_standards as repo identity",
            "Keep 'info center' only as descriptive language, not an ID",
        ]
    if any("exit code 99" in e.lower() for e in all_errors):
        suggestions["exit_codes"] = [
            "Remove exit code 99 references (deprecated)",
            "Document only 0/1/2 exit code contract",
        ]
    if any("cd validators" in e for e in all_errors):
        suggestions["run_location"] = [
            "Change to: python validators/run_all.py (from repo root)",
            "Remove 'cd validators' instructions",
        ]
    if any("Python" in e for e in all_errors):
        suggestions["python_version"] = [
            "Update Python version to 3.11+ (per pyproject.toml)",
        ]
    if any("KNOWN_PROJECTS" in e for e in all_errors):
        suggestions["paths"] = [
            "Use 70_evidence/workspace/KNOWN_PROJECTS.md (correct path)",
            "registry/repos.yaml is source of truth; KNOWN_PROJECTS.md is derived",
        ]

    return report_validation_results(
        "Constitution guardrail",
        all_errors,
        suggestions if suggestions else None,
        args.verbose,
    )


if __name__ == "__main__":
    raise SystemExit(cli())
