Linux-Pyhack 🐧

A Python-powered, Kali-inspired terminal and security toolkit.

Linux-Pyhack provides a Linux-style command shell, system monitoring, network diagnostics, and six built-in security tools. It runs as a Python application on Linux, Windows, and macOS.

Note: Linux-Pyhack is a terminal application, not a standalone bootable Linux distribution.

Features

Bash-style terminal

ls — List directory contents

cd — Change directories

pwd — Print working directory

cat — Read text files

mkdir — Create directories

touch — Create files

rm — Remove files

whoami — Display the current user

uname — Display system information

history — Show command history

clear — Clear the terminal

Six security tools

Tool

Command

Purpose

System Monitor

monitor

Live CPU, RAM, and process statistics

Network Ping

ping

Test network connectivity

DNS Lookup

dns

Resolve hostnames to IP addresses

TCP Scanner

scan

Check TCP port connectivity

HTTP Inspector

headers

Inspect HTTP response headers

TLS Inspector

tls

Inspect TLS certificates

Requirements

Python 3.10 or newer

Internet access for external network diagnostics

psutil for detailed system monitoring

The native ping utility for ping commands

Installation

1. Clone the repository

git clone https://github.com/YOUR_USERNAME/Linux-Pyhack.git
cd Linux-Pyhack

Replace YOUR_USERNAME with your GitHub username.

2. Create a virtual environment (recommended)

Linux:

python3 -m venv .venv
source .venv/bin/activate

Windows:

py -m venv .venv
.venv\Scripts\Activate.ps1

3. Install dependencies

python -m pip install -r requirements.txt

4. Start Linux-Pyhack

Linux:

python3 linux_pyhack.py

Windows:

py linux_pyhack.py

Usage

Once the terminal starts, enter:

help
sysinfo
pwd
ls
monitor
dns example.com
ping example.com
scan 127.0.0.1 22,80,443
headers https://example.com
tls example.com
exit

Use Ctrl+C to stop the live monitor.

Project Structure

Linux-Pyhack/
├── linux_pyhack.py
├── requirements.txt
├── README.md
└── .gitignore

Security Notice

Linux-Pyhack is intended for education, personal labs, and authorized security testing.

Only scan systems you own or have explicit permission to test.

Network results depend on firewalls, routing, and host availability.

TLS inspection uses certificate verification by default.

Commands passed through to the host run with the permissions of the current Python process.

This application does not provide a Linux kernel, bootloader, or a complete replacement for Kali Linux.

License

This project is available under the MIT License. Add a LICENSE file containing the MIT license text before distributing the project under that license.

Linux-Pyhack — Learn Linux. Explore networking. Practice security.