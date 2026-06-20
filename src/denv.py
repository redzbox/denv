#!/usr/bin/env python3

import argparse
import shutil
import subprocess
from datetime import date
from pathlib import Path

VERSION = "1.2.0"

BASE_DIR = Path(__file__).resolve().parent
TEMPLATES_DIR = BASE_DIR / "templates"


def get_templates():
    templates = {}

    if not TEMPLATES_DIR.exists():
        return templates

    for language_dir in TEMPLATES_DIR.iterdir():
        if not language_dir.is_dir():
            continue

        variants = {}

        for variant_dir in language_dir.iterdir():
            if variant_dir.is_dir():
                variants[variant_dir.name] = f"{language_dir.name}/{variant_dir.name}"

        templates[language_dir.name] = variants

    return templates


def generate_from_template(template_name):
    template_dir = TEMPLATES_DIR / template_name

    if not template_dir.exists():
        print(f"Template '{template_name}' not found.")
        return False

    for item in template_dir.iterdir():
        destination = Path.cwd() / item.name

        if item.is_dir():
            shutil.copytree(item, destination, dirs_exist_ok=True)
        else:
            shutil.copy2(item, destination)

    return True


def replace_placeholders(variables):
    for file in Path.cwd().rglob("*"):
        if not file.is_file():
            continue

        try:
            content = file.read_text(encoding="utf-8")

            for key, value in variables.items():
                content = content.replace(f"{{{key}}}", str(value))

            file.write_text(content, encoding="utf-8")

        except Exception:
            pass


def create_project(language, variant, project_name, author, git):
    templates = get_templates()

    if language not in templates:
        print(f"Unknown language: {language}")
        return

    if variant not in templates[language]:
        print(f"Unknown variant '{variant}' for '{language}'")
        return

    project_dir = Path(project_name)

    if project_dir.exists():
        print(f"Project '{project_name}' already exists.")
        return

    project_dir.mkdir()

    old_cwd = Path.cwd()

    try:
        import os

        os.chdir(project_dir)

        template = templates[language][variant]

        variables = {
            "PROJECT_NAME": project_name,
            "AUTHOR": author,
            "YEAR": date.today().year,
            "DATE": date.today().isoformat(),
            "LANGUAGE": language,
            "DENV_VERSION": VERSION,
        }

        if generate_from_template(template):
            replace_placeholders(variables)
            if git:
                initialize_git()

    finally:
        import os

        os.chdir(old_cwd)

    message = f"Created {language} project '{project_name}' ({variant})"

    if git:
        message += " with Git initialized"

    print(message)


def initialize_git():
    subprocess.run(
        ["git", "init"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )

    subprocess.run(
        ["git", "add", "."], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )

    subprocess.run(
        ["git", "commit", "-m", "Initial commit"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def command_create(args):
    create_project(
        args.language, args.variant, args.project_name, args.author, args.git
    )


def command_list(args):
    templates = get_templates()

    print("Available templates:\n")

    for language, variants in templates.items():
        print(f"{language}")

        for variant in variants:
            print(f"  └─ {variant}")

        print()


def command_info(args):
    templates = get_templates()

    language = args.language

    if language not in templates:
        print(f"Unknown language: {language}")
        return

    print(f"Language: {language}")
    print("\nVariants:")

    for variant, path in templates[language].items():
        print(f"  - {variant}")
        print(f"    path: {path}")


def command_version(args):
    print(f"DEnv version {VERSION}\nCopyright (C) 2026 Alex Pesta")


def main():
    parser = argparse.ArgumentParser(
        prog="denv", description="Developer Environment Generator"
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    create_parser = subparsers.add_parser("create", help="Create a new project")

    create_parser.add_argument("language", help="Programming language")

    create_parser.add_argument("project_name", help="Project name")

    create_parser.add_argument("--variant", default="default", help="Template variant")

    create_parser.set_defaults(func=command_create)

    create_parser.add_argument("--author", default="Unknown")

    create_parser.add_argument(
        "--git", action="store_true", help="Initialize a Git repository"
    )

    list_parser = subparsers.add_parser("list", help="List available templates")

    list_parser.set_defaults(func=command_list)

    info_parser = subparsers.add_parser(
        "info", help="Show information about a template"
    )

    info_parser.add_argument("language", help="Programming language")

    info_parser.set_defaults(func=command_info)

    version_parser = subparsers.add_parser("version", help="Show version")

    version_parser.set_defaults(func=command_version)

    args = parser.parse_args()

    args.func(args)


if __name__ == "__main__":
    main()
