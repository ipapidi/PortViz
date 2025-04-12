<p align="center">
  <img src="portviz-icon.png" width="100" alt="PortViz icon">
</p>

<h1 align="center">PortViz</h1>

<p align="center">
  A sonar-style visual port scanner with real-time radar animation, pulse effects, and live scan logs.
</p>

---

## Disclaimer

This tool is intended for educational and authorized network diagnostics only.  
**Unauthorized scanning of systems you do not own or have explicit permission to test is illegal and punishable by law. Use PortViz responsibly.**  

*Note: The radar animation is for visual effect only! The position of the dots on the radar does not reflect the actual port numbers or physical locations of services.*

---

## Features

<table>
  <tr>
    <th>Feature</th>
    <th>Description</th>
  </tr>
  <tr>
    <td>Radar Visualization</td>
    <td>Displays open ports as glowing dots on a sweeping radar interface</td>
  </tr>
  <tr>
    <td>Live Log Panel</td>
    <td>Real-time log output with colored entries for open (green) and closed (red) ports</td>
  </tr>
  <tr>
    <td>Pulse Animation</td>
    <td>Pulse effect when the radar needle passes detected open ports</td>
  </tr>
  <tr>
    <td>Dark Mode</td>
    <td>Fully styled dark theme for an eye-friendly experience</td>
  </tr>
  <tr>
    <td>Flexible Input</td>
    <td>Supports IP address validation and custom port range input, or use "any" to scan common ports</td>
  </tr>
  <tr>
    <td>Launcher Integration</td>
    <td>Includes .desktop file and icon for menu integration on Linux Mint and other DEs</td>
  </tr>
</table>

---

## Installation

### Option 1: Clone with Git

```bash
git clone https://github.com/ipapidi/PortViz.git
cd PortViz
chmod +x install.sh
./install.sh
```

### Option 2: Download Manually

1. [Download the ZIP](https://github.com/ipapidi/PortViz/archive/refs/heads/main.zip)
2. Extract the contents
3. Open a terminal in the extracted folder and run:

```bash
chmod +x install.sh
./install.sh
```

---

## Launch PortViz

After installation, you can either:

- Search “PortViz” in your system’s application menu, or
- Run it manually:

```bash
./launch.sh
```

---

## Add to Applications Menu (Manual)

If needed, you can manually add PortViz to your applications menu:

```bash
chmod +x launch.sh
chmod +x portviz.desktop
cp portviz.desktop ~/.local/share/applications/
update-desktop-database ~/.local/share/applications/
```

You can also mark the launcher as trusted:

```bash
gio set ~/.local/share/applications/portviz.desktop "metadata::trusted" yes
```

---

## Folder Overview

<table>
  <tr>
    <th>File</th>
    <th>Description</th>
  </tr>
  <tr>
    <td><code>portviz.py</code></td>
    <td>Main Python application (PyQt5 GUI)</td>
  </tr>
  <tr>
    <td><code>launch.sh</code></td>
    <td>Launches the app using a relative path setup</td>
  </tr>
  <tr>
    <td><code>install.sh</code></td>
    <td>Installer script that symlinks the .desktop launcher and sets permissions</td>
  </tr>
  <tr>
    <td><code>portviz.desktop</code></td>
    <td>Application launcher for desktop menu integration</td>
  </tr>
  <tr>
    <td><code>themes/dark.qss</code></td>
    <td>Dark mode styling (Qt stylesheet)</td>
  </tr>
  <tr>
    <td><code>ui/radar_widget.py</code></td>
    <td>Custom widget for radar animation and port rendering</td>
  </tr>
  <tr>
    <td><code>portviz-icon.png</code></td>
    <td>Transparent PNG icon used in the launcher</td>
  </tr>
</table>

---

## License

This project is licensed under the MIT License.  
See the [LICENSE](LICENSE) file for more information.

---

## Author

**Ioli Papidi**  
GitHub: [@ipapidi](https://github.com/ipapidi)
