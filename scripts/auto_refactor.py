#!/usr/bin/env python3
"""
Automated code quality improvements for FarBox Bucket.
Run this to systematically refactor all Python files.
"""
import subprocess
import sys
from pathlib import Path


def run_black():
    """Format all code with Black."""
    print("📝 Running Black formatter...")
    result = subprocess.run(
        ["black", "farbox_bucket/", "--line-length", "100"],
        capture_output=True,
        text=True
    )
    print(result.stdout)
    return result.returncode == 0


def run_ruff_fix():
    """Auto-fix issues with ruff."""
    print("🔧 Running ruff --fix...")
    result = subprocess.run(
        ["ruff", "check", "farbox_bucket/", "--fix"],
        capture_output=True,
        text=True
    )
    print(result.stdout)
    return result.returncode == 0


def run_isort():
    """Sort imports with isort."""
    print("📦 Sorting imports with isort...")
    result = subprocess.run(
        ["isort", "farbox_bucket/", "--profile", "black"],
        capture_output=True,
        text=True
    )
    print(result.stdout)
    return result.returncode == 0


def check_mypy():
    """Run type checking (won't fail, just report)."""
    print("🔍 Running mypy type checker...")
    result = subprocess.run(
        ["mypy", "farbox_bucket/", "--ignore-missing-imports", "--no-error-summary"],
        capture_output=True,
        text=True
    )
    print(result.stdout)
    print(f"Type checking complete (found {result.stdout.count('error')} issues)")


def main():
    """Run all automated refactorings."""
    print("🚀 Starting automated refactoring...\n")

    # Change to project root
    project_root = Path(__file__).parent.parent
    import os
    os.chdir(project_root)

    steps = [
        ("Black formatting", run_black),
        ("Import sorting", run_isort),
        ("Ruff auto-fix", run_ruff_fix),
    ]

    failed = []
    for name, func in steps:
        try:
            if not func():
                failed.append(name)
        except FileNotFoundError:
            print(f"⚠️  {name} tool not found. Install with:")
            print(f"   pip install black ruff isort mypy")
            failed.append(name)
        except Exception as e:
            print(f"❌ {name} failed: {e}")
            failed.append(name)

    # Always run mypy (doesn't fail the process)
    try:
        check_mypy()
    except FileNotFoundError:
        print("⚠️  mypy not found. Install with: pip install mypy")

    print("\n" + "="*50)
    if failed:
        print(f"❌ Some steps failed: {', '.join(failed)}")
        print("Please install missing tools and rerun.")
        return 1
    else:
        print("✅ All automated refactoring complete!")
        print("\nNext steps:")
        print("1. Review changes with: git diff")
        print("2. Run tests: pytest tests/")
        print("3. Commit if all looks good")
        return 0


if __name__ == "__main__":
    sys.exit(main())
