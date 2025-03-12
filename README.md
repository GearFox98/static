# Static ⚡
A static web site generator inspired by React and written in Python 🐍

Static gives complete flexibility for building the site as it just focus on sew the pieces together. All you require is basic web programing skills and a bit of Python!

### Instalation
Clone this repository and uncompress the program. Copy the 'skel' folder where you want to work and give 'static' execution permissions.

#### Debian
If you have a Debian-like distro installed, you can install the _DEB_ package, available [here](https://github.com/GearFox98/static/releases).
```bash
sudo dpkg -i static_1.0-x_all.deb
```

#### Arch (AUR)
If you have Arch installed, you can install the `static` from _AUR_
```bash
git clone https://aur.archlinux.org/static-git.git
cd static-git
pkgbuild -i
```

### Usage
#### Starting a new project
```bash
static-init <path> [options]
```

> #### **Options available:**
> **-b, --bootstrap**: gets a Bootstrap dist and installs it in the `data` folder in the project. Useful to code in places with unstable network

_Note_: If no `path` provided Static⚡ will assume `current directory` to initialize the project.

#### Running the project
```bash
static [command]
```

> #### **Commands available:**
> **check**: checks the directory structure looking for missing directories. If there are some folders missing, this command will create them. The program stops if `html` or `pages` folders are not in the directory.<br /><br />
> **build**: implies `check`, if there's no errors found, the program will generate the pages' content in a temporary folder and tailor the pieces in one file for each page in the `dist` folder.
> **run** - Serves `dist` folder of the project, if the site is not built it calls `build` command.
