# Static ⚡
A static web site generator inspired by React and written in Python 🐍

Static gives complete flexibility for building the site as it just focus on sew the pieces together. All you require is basic web programing skills and a bit of Python!

### Instalation
Clone this repository and uncompress the program. Copy the 'skel' folder where you want to work and give 'static' execution permissions.

#### Debian
If you have a Debian-like distro installed, you can install the _DEB_ package, available [here](https://github.com/GearFox98/static/releases/tag/1.0.1).
```bash
$ dpkg -i static_1.0-1_all.deb
```

### Usage
```bash
$ static [command]
```

> ## **Commands available:**
> **check**: checks the directory structure looking for missing directories. If there are some folders missing, this command will create them. The program stops if 'html' or 'pages' folders are not in the directory.<br /><br />
> **build**: implies 'check', if there's no errors found, the program will generate the pages' content in a temporary folder and tailor the pieces in one file for each page in the 'dist' folder.