# AirCrack-Py 🔓📡

*A Python-powered WiFi security testing toolkit for ethical pentesters*  
![GitHub](https://img.shields.io/github/license/k5522/aircrack-py?color=red)
![Python](https://img.shields.io/badge/Python-3.8%2B-yellowgreen)

<img src="https://i.imgur.com/3bXQf3P.png" width="400" align="right" alt="WPA Handshake">

## 🌟 Features
- Monitor mode activation automation
- Network scanning with signal analysis
- Deauthentication attack module
- Handshake capture system
- Dictionary-based password cracking
- Clean terminal interface

## ⚡ Quick Start

### Requirements
- Kali Linux/WSL2 or similar security distro
- `aircrack-ng` suite
- Wireless adapter with monitor mode support
- Root privileges

```bash
# Installation
sudo apt update && sudo apt install aircrack-ng
git clone https://github.com/yourusername/aircrack-py.git
cd aircrack-py
chmod +x wifi_cracker.py

# Execution
sudo ./wifi_cracker.py


## 🛠️ Usage Guide
Interface Preparation
Automatically handles monitor mode setup

### Network Discovery
Scans and displays available WPA/WPA2 networks

### Target Selection
Interactive menu for choosing targets

### Handshake Harvesting
Automated deauth + capture sequence

### Password Cracking
Integrated rockyou.txt dictionary attack

```ascii
[+] Workflow Diagram
+-------------------+     +----------------+     +-------------------+
| Monitor Mode      | --> | Network Scan   | --> | Target Selection  |
+-------------------+     +----------------+     +-------------------+
                          | Handshake Capture | <-->| Deauth Attack    |
                          +-------------------+     +-------------------+
                                                    | Password Crack    |
                                                    +-------------------+
