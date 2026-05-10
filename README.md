# linux-tosu-ingame-overlay
[中文](README_CN.md)|English

A gtk4 implement of a general(tosu/gosumemory/etc.) in-game overlay for Linux.

## Notice
This overlay is compatible only with KDE Plasma and has been tested exclusively on osu-winello (osu!stable) and Arch Linux. Compatibility with osu!lazer and other Linux distributions is uncertain.

## Known Issues
- Sometimes the KWin Script will stop working after system reboot. Just disable the script and re-enable it to fix it.

## How to Use

### 1. Install Dependencies

#### Arch Linux:
```bash
sudo pacman -Syu --needed gtk4 webkit2gtk python-gobject python-cairo gtk-layer-shell
```

#### Debian/Ubuntu (not tested, but expected to work):
```bash
sudo apt install -y python3-gi python3-gi-cairo gir1.2-gtk-4.0 gir1.2-webkit2-6.0 libwebkit2gtk-6.0-0 libgtk-4-1 libgtk-layer-shell-1.0-0
```

### 2. Download and Extract
Download the `.zip` file from the Release page and extract it to anywhere you like.

### 3. Install KWin Script
Download kwinscript.zip from the Release page and install the script via System Settings.

### 4. Customize the Overlay
Edit the `src/index.html` file to customize your overlay. Imagine a 1920x1080 canvas and place fixed elements on it using something like `</iframe>`. The default file includes the [osumania_map_analyser](https://github.com/LeoBlackMT/osumania_map_analyser/tree/main) created by [Leo_Black](https://github.com/LeoBlackMT) (which is an excellent tool for us mania players)

### 5. Run the Application
Open osu! and run the application using the following command:
```bash
./osuoverlay
```
