# Developer Environment (DEnv)

DEnv is a project scaffolding tool that generates ready-to-use development environments from templates.

Create projects for multiple programming languages in seconds, with support for template variants, placeholder variables, Git initialization, and more.

---

## Features

- Multiple language templates
  - Python
  - C
  - C++
  - C#
  - Java
  - A#
    **and more**

- Template variants

- Automatic placeholder replacement

- Git repository initialization

- Project information and template discovery

- Graphical installer and uninstaller

- Extensible template-based architecture

---

## Installation

Download the latest release from:

:contentReference[oaicite:0]{index=0}

### Installer (Recommended)

Run:

```bash
src/installer/install.py
```

The installer will:

- Install DEnv
- Create the launcher
- Configure PATH automatically
- Verify the installation

### Uninstall

Run:

```bash
src/installer/uninstall.py
```

---

## Usage

### Create a Project

```bash
denv create python MyProject
```

### Create a Project with a Variant

```bash
denv create python MyProject --variant nopycache
```

### Create a Project with Git Initialized

```bash
denv create python MyProject --git
```

### Specify an Author

```bash
denv create python MyProject --author "Alex Pesta"
```

### List Available Templates

```bash
denv list
```

### View Template Information

```bash
denv info python
```

### Show Version

```bash
denv version
```

---

## Contributing

Contributions, bug reports, feature requests, and pull requests are welcome.

### Getting Started

1. Fork the repository.
2. Create a feature branch.
3. Make your changes.
4. Commit your work.
5. Open a pull request.

Issues can be reported here:

:contentReference[oaicite:1]{index=1}

---

## License

Licensed under the GNU Affero General Public License v3.0.

See the LICENSE file for details.
