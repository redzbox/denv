#!/usr/bin/env python3

import json
import os
import shutil
from pathlib import Path

import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")

from gi.repository import Adw, Gtk

MANIFEST_FILE = Path.home() / ".config" / "denv" / "install.json"

DEFAULT_INSTALL_DIR = Path.home() / ".local" / "share" / "denv"

DEFAULT_BIN_DIR = Path.home() / ".local" / "bin"


def detect_shell():
    return os.path.basename(os.environ.get("SHELL", ""))


def get_shell_config(shell):
    configs = {
        "bash": Path.home() / ".bashrc",
        "zsh": Path.home() / ".zshrc",
        "fish": (Path.home() / ".config" / "fish" / "config.fish"),
    }

    return configs.get(shell)


def remove_path_entry():
    shell = detect_shell()

    config = get_shell_config(shell)

    if config is None:
        return

    if not config.exists():
        return

    lines = config.read_text().splitlines()

    filtered = []

    for line in lines:
        if "DEnv" in line:
            continue

        if ".local/bin" in line:
            continue

        if "fish_add_path" in line:
            continue

        filtered.append(line)

    config.write_text("\n".join(filtered) + "\n")


def load_manifest():
    if not MANIFEST_FILE.exists():
        return None

    try:
        return json.loads(MANIFEST_FILE.read_text())
    except Exception:
        return None


def uninstall(install_dir):
    install_dir = Path(install_dir)

    launcher = DEFAULT_BIN_DIR / "denv"

    if launcher.exists():
        launcher.unlink()

    if install_dir.exists():
        shutil.rmtree(install_dir)

    remove_path_entry()

    if MANIFEST_FILE.exists():
        MANIFEST_FILE.unlink()


class UninstallerWindow(Adw.ApplicationWindow):
    def __init__(self, app):
        super().__init__(application=app)

        self.set_title("DEnv Uninstaller")

        self.set_default_size(800, 600)

        self.manifest = load_manifest()

        self.stack = Gtk.Stack()

        self.set_content(self.stack)

        self.build_pages()

    def build_pages(self):
        self.build_welcome()
        self.build_location()
        self.build_summary()
        self.build_finished()

    def build_welcome(self):
        box = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=24,
            margin_top=48,
            margin_start=48,
            margin_end=48,
        )

        title = Gtk.Label()

        title.set_markup("<span size='xx-large' weight='bold'>DEnv Uninstaller</span>")

        box.append(title)

        if self.manifest:
            version = self.manifest.get("version", "Unknown")

            text = f"Detected DEnv {version}\n\nPress Next to continue."
        else:
            text = (
                "No install manifest found.\n\n"
                "You can still manually select a directory."
            )

        box.append(Gtk.Label(label=text))

        next_btn = Gtk.Button(label="Next")

        next_btn.connect(
            "clicked", lambda *_: self.stack.set_visible_child_name("location")
        )

        box.append(next_btn)

        self.stack.add_named(box, "welcome")

    def build_location(self):
        box = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=24,
            margin_top=48,
            margin_start=48,
            margin_end=48,
        )

        box.append(Gtk.Label(label="Installation Directory"))

        path_box = Gtk.Box(
            orientation=Gtk.Orientation.HORIZONTAL,
            spacing=8,
        )

        self.location_entry = Gtk.Entry()

        self.location_entry.set_hexpand(True)

        if self.manifest:
            default_path = self.manifest.get("install_dir", str(DEFAULT_INSTALL_DIR))
        else:
            default_path = str(DEFAULT_INSTALL_DIR)

        self.location_entry.set_text(default_path)

        browse_btn = Gtk.Button(label="Browse")

        browse_btn.connect("clicked", self.on_browse_clicked)

        path_box.append(self.location_entry)

        path_box.append(browse_btn)

        box.append(path_box)

        next_btn = Gtk.Button(label="Next")

        next_btn.connect("clicked", self.location_next)

        box.append(next_btn)

        self.stack.add_named(box, "location")

    def on_browse_clicked(
        self,
        button,
    ):
        dialog = Gtk.FileDialog()

        dialog.select_folder(
            self,
            None,
            self.on_folder_selected,
        )

    def on_folder_selected(
        self,
        dialog,
        result,
    ):
        try:
            folder = dialog.select_folder_finish(result)

            if folder:
                self.location_entry.set_text(folder.get_path())

        except Exception as e:
            print(e)

    def location_next(
        self,
        *_,
    ):
        self.install_dir = self.location_entry.get_text()

        self.summary_label.set_text(
            (
                "The following will be removed:\n\n"
                f"{self.install_dir}\n\n"
                "Launcher\n"
                "PATH entries\n"
                "Manifest"
            )
        )

        self.stack.set_visible_child_name("summary")

    def build_summary(self):
        box = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=24,
            margin_top=48,
            margin_start=48,
            margin_end=48,
        )

        self.summary_label = Gtk.Label()

        box.append(self.summary_label)

        remove_btn = Gtk.Button(label="Remove DEnv")

        remove_btn.add_css_class("destructive-action")

        remove_btn.connect("clicked", self.run_uninstall)

        box.append(remove_btn)

        self.stack.add_named(box, "summary")

    def run_uninstall(
        self,
        *_,
    ):
        try:
            uninstall(self.install_dir)

            self.stack.set_visible_child_name("finished")

        except Exception as e:
            print(e)

    def build_finished(self):
        box = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=24,
            margin_top=48,
            margin_start=48,
            margin_end=48,
        )

        box.append(Gtk.Label(label=("DEnv was removed successfully.")))

        finish_btn = Gtk.Button(label="Finish")

        finish_btn.connect("clicked", lambda *_: self.close())

        box.append(finish_btn)

        self.stack.add_named(box, "finished")


class UninstallerApplication(Adw.Application):
    def __init__(self):
        super().__init__(application_id=("io.github.apesta0.denv.uninstaller"))

    def do_activate(self):
        window = UninstallerWindow(self)

        window.present()


if __name__ == "__main__":
    app = UninstallerApplication()

    app.run()
