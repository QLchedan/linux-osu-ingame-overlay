# linux-tosu-ingame-overlay

中文|[English](README.md)

这是使用gtk4实现的一个适用于Linux平台的通用osu游戏内overlay

## 注意事项
该软件仅支持KDE Plasma并且只在Arch Linux和osu-winello(osu!stable)上测试过。我不知道在lazer和其它发行版上能不能用。

## 已知问题
- KWin Script在重启之后可能会出现问题，禁用再启用一次就可以了。

## 如何使用

### 1. 安装依赖

#### Arch Linux:
```bash
sudo pacman -Syu --needed gtk4 webkit2gtk python-gobject python-cairo gtk-layer-shell qt5-tools
```

#### Debian/Ubuntu (没测试过，应该能用):
```bash
sudo apt install -y python3-gi python3-gi-cairo gir1.2-gtk-4.0 gir1.2-webkit2-6.0 libwebkit2gtk-6.0-0 libgtk-4-1 libgtk-layer-shell-1.0-0
```

### 2. 下载软件
从Release界面下载`.zip`文件并且解压到你喜欢的地方。

### 3. 安装KWin脚本
在Release界面下载kwinscript.zip并在系统设置中安装。

### 4. 自定义overlay
编辑`src/index.html`来自定义overlay。想象这是一个1920x1080的画布然后用`</iframe>`之类的东西添加你想要的固定元素。默认的`index.html`包含[Leo_Black](https://github.com/LeoBlackMT)大佬的[osumania_map_analyser](https://github.com/LeoBlackMT/osumania_map_analyser/tree/main)。

### 5. 运行程序
打开osu!并确保tosu/gosumemory正常运行，然后运行:
```bash
./osuoverlay
```
