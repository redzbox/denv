#!/usr/bin/env python3

import json
import os
import shutil
import stat
from pathlib import Path

import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")

from gi.repository import Adw, Gtk

VERSION = "1.2.0"

ROOT_DIR = Path(__file__).resolve().parents[2]

DEFAULT_INSTALL_DIR = Path.home() / ".local" / "share" / "denv"
DEFAULT_BIN_DIR = Path.home() / ".local" / "bin"

MANIFEST_DIR = Path.home() / ".config" / "denv"
MANIFEST_FILE = MANIFEST_DIR / "install.json"


def detect_shell():
    return os.path.basename(os.environ.get("SHELL", ""))


def get_shell_config(shell):
    configs = {
        "bash": Path.home() / ".bashrc",
        "zsh": Path.home() / ".zshrc",
        "fish": Path.home() / ".config" / "fish" / "config.fish",
    }

    return configs.get(shell)


def add_path_entry(bin_dir):
    shell = detect_shell()
    config = get_shell_config(shell)

    if config is None:
        return

    config.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    if shell == "fish":
        entry = f"fish_add_path {bin_dir}"
    else:
        entry = f'export PATH="{bin_dir}:$PATH"'

    if config.exists():
        content = config.read_text()

        if entry in content:
            return

    with open(config, "a") as f:
        f.write("\n# DEnv\n")
        f.write(entry + "\n")


def create_launcher(
    install_dir,
    bin_dir,
):
    bin_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    launcher = bin_dir / "denv"

    launcher.write_text(
        f'''#!/bin/bash
python3 "{install_dir / "src" / "denv.py"}" "$@"
'''
    )

    launcher.chmod(launcher.stat().st_mode | stat.S_IEXEC)


def write_manifest(
    install_dir,
    bin_dir,
):
    MANIFEST_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    data = {
        "version": VERSION,
        "install_dir": str(install_dir),
        "bin_dir": str(bin_dir),
        "shell": detect_shell(),
    }

    MANIFEST_FILE.write_text(
        json.dumps(
            data,
            indent=4,
        )
    )


def install(
    install_dir,
):
    install_dir = Path(install_dir)

    bin_dir = DEFAULT_BIN_DIR

    if install_dir.exists():
        shutil.rmtree(install_dir)

    install_dir.mkdir(parents=True)

    for item in ROOT_DIR.iterdir():
        if item.name == ".git":
            continue

        destination = install_dir / item.name

        if item.is_dir():
            shutil.copytree(
                item,
                destination,
            )
        else:
            shutil.copy2(
                item,
                destination,
            )

    create_launcher(
        install_dir,
        bin_dir,
    )

    add_path_entry(bin_dir)

    write_manifest(
        install_dir,
        bin_dir,
    )


class InstallerWindow(Adw.ApplicationWindow):
    def __init__(
        self,
        app,
    ):
        super().__init__(application=app)

        self.set_title("DEnv Installer")

        self.set_default_size(
            800,
            600,
        )

        self.install_dir = str(DEFAULT_INSTALL_DIR)

        self.stack = Gtk.Stack()

        self.set_content(self.stack)

        self.build_pages()

    def build_pages(
        self,
    ):
        self.build_welcome()
        self.build_location()
        self.build_options()
        self.build_summary()
        self.build_finished()

    def build_welcome(
        self,
    ):
        box = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=24,
            margin_top=48,
            margin_start=48,
            margin_end=48,
        )

        title = Gtk.Label()

        title.set_markup("<span size='xx-large' weight='bold'>DEnv Installer</span>")

        box.append(title)

        box.append(
            Gtk.Label(label=(f"Welcome to the DEnv Setup Wizard.\nVersion {VERSION}"))
        )

        next_btn = Gtk.Button(label="Next")

        next_btn.connect(
            "clicked",
            lambda *_: self.stack.set_visible_child_name("location"),
        )

        box.append(next_btn)

        self.stack.add_named(
            box,
            "welcome",
        )

    def build_location(
        self,
    ):
        box = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=24,
            margin_top=48,
            margin_start=48,
            margin_end=48,
        )

        box.append(Gtk.Label(label="Installation Directory"))

        self.location_entry = Gtk.Entry()

        self.location_entry.set_text(str(DEFAULT_INSTALL_DIR))

        box.append(self.location_entry)

        next_btn = Gtk.Button(label="Next")

        next_btn.connect(
            "clicked",
            self.location_next,
        )

        box.append(next_btn)

        self.stack.add_named(
            box,
            "location",
        )

    def location_next(
        self,
        *_,
    ):
        self.install_dir = self.location_entry.get_text()

        self.summary_label.set_text(
            (
                f"Version: {VERSION}\n\n"
                f"Location:\n"
                f"{self.install_dir}\n\n"
                f"Shell:\n"
                f"{detect_shell()}"
            )
        )

        self.stack.set_visible_child_name("options")

    def build_options(
        self,
    ):
        box = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=24,
            margin_top=48,
            margin_start=48,
            margin_end=48,
        )

        self.path_check = Gtk.CheckButton(label="Add launcher to PATH")

        self.path_check.set_active(True)

        box.append(self.path_check)

        next_btn = Gtk.Button(label="Next")

        next_btn.connect(
            "clicked",
            lambda *_: self.stack.set_visible_child_name("summary"),
        )

        box.append(next_btn)

        self.stack.add_named(
            box,
            "options",
        )

    def build_summary(
        self,
    ):
        box = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=24,
            margin_top=48,
            margin_start=48,
            margin_end=48,
        )

        self.summary_label = Gtk.Label()

        box.append(self.summary_label)

        install_btn = Gtk.Button(label="Install")

        install_btn.add_css_class("suggested-action")

        install_btn.connect(
            "clicked",
            self.run_install,
        )

        box.append(install_btn)

        self.stack.add_named(
            box,
            "summary",
        )

    def run_install(
        self,
        *_,
    ):
        try:
            install(self.install_dir)

            self.stack.set_visible_child_name("finished")

        except Exception as e:
            dialog = Gtk.AlertDialog()

            dialog.set_message("Installation Failed")

            dialog.set_detail(str(e))

            dialog.show(self)

    def build_finished(
        self,
    ):
        box = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=24,
            margin_top=48,
            margin_start=48,
            margin_end=48,
        )

        box.append(
            Gtk.Label(
                label=(
                    "DEnv installed successfully.\n\n"
                    "Restart your shell to use PATH changes."
                )
            )
        )

        finish_btn = Gtk.Button(label="Finish")

        finish_btn.connect(
            "clicked",
            lambda *_: self.close(),
        )

        box.append(finish_btn)

        self.stack.add_named(
            box,
            "finished",
        )


class InstallerApplication(Adw.Application):
    def __init__(
        self,
    ):
        super().__init__(application_id=("io.github.apesta0.denv.installer"))

    def do_activate(
        self,
    ):
        window = InstallerWindow(self)

        window.present()


if __name__ == "__main__":
    app = InstallerApplication()

    app.run()
