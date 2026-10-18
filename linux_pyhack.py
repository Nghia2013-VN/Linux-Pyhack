#!/usr/bin/env python3
# ============================================================
# Linux-Pyhack
# Python Kali-inspired terminal environment
# ============================================================

import os
import cmd
import shlex
import socket
import ssl
import hashlib
import platform
import subprocess
import urllib.request
import urllib.error
import time
from pathlib import Path
from datetime import datetime

try:
    import psutil
except ImportError:
    psutil = None

BANNER = r"""
██╗     ██╗███╗   ██╗██╗   ██╗██╗  ██╗      ██████╗ ██╗   ██╗██╗  ██╗ █████╗  ██████╗██╗  ██╗
██║     ██║████╗  ██║██║   ██║╚██╗██╔╝      ██╔══██╗╚██╗ ██╔╝██║  ██║██╔══██╗██╔════╝██║ ██╔╝
██║     ██║██╔██╗ ██║██║   ██║ ╚███╔╝ █████╗██████╔╝ ╚████╔╝ ███████║███████║██║     █████╔╝
██║     ██║██║╚██╗██║██║   ██║ ██╔██╗ ╚════╝██╔═══╝   ╚██╔╝  ██╔══██║██╔══██║██║     ██╔═██╗
███████╗██║██║ ╚████║╚██████╔╝██╔╝ ██╗      ██║        ██║   ██║  ██║██║  ██║╚██████╗██║  ██╗
╚══════╝╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚═╝  ╚═╝      ╚═╝        ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝

        Kali-inspired Python Security Terminal
"""

HELP_TEXT = """
================ Linux-Pyhack =================

Basic Bash
-----------
help
clear
pwd
ls
cd <path>
cat <file>
mkdir <dir>
touch <file>
rm <file>
whoami
uname
date
history
sysinfo
exit

Security Tools (6)
------------------
1. monitor              Live CPU/RAM monitor
2. ping <host>          Network test
3. dns <host>           DNS lookup
4. scan <host> [ports]  TCP port scanner
5. headers <url>        HTTP header inspector
6. tls <host>           TLS certificate viewer

Example
-------
scan 127.0.0.1 22,80,443
"""

class LinuxPyhack(cmd.Cmd):

    intro = BANNER
    prompt = "root@linux-pyhack:~$ "

    def __init__(self):
        super().__init__()
        self.cwd = Path.cwd()
        self.history_log = []
        self.update_prompt()

    def update_prompt(self):
        self.prompt = f"root@linux-pyhack:{self.cwd}$ "

    def precmd(self, line):
        if line.strip():
            self.history_log.append(line)
        return line

    def postcmd(self, stop, line):
        self.update_prompt()
        return stop

    def emptyline(self):
        pass

    def resolve(self, p="."):
        p = Path(p).expanduser()
        if not p.is_absolute():
            p = self.cwd / p
        return p.resolve()

    # =========================================================
    # Bash Commands
    # =========================================================

    def do_help(self, arg):
        print(HELP_TEXT)

    def do_clear(self, arg):
        os.system("cls" if os.name == "nt" else "clear")

    def do_pwd(self, arg):
        print(self.cwd)

    def do_ls(self, arg):
        target = self.resolve(arg or ".")
        try:
            for item in sorted(target.iterdir()):
                mark = "/" if item.is_dir() else ""
                print(item.name + mark)
        except Exception as e:
            print(e)

    def do_cd(self, arg):
        target = self.resolve(arg or str(Path.home()))
        if target.is_dir():
            self.cwd = target
        else:
            print("Directory not found.")

    def do_cat(self, arg):
        if not arg:
            return
        try:
            print(self.resolve(arg).read_text(errors="replace"))
        except Exception as e:
            print(e)

    def do_touch(self, arg):
        if not arg:
            return
        self.resolve(arg).touch(exist_ok=True)

    def do_mkdir(self, arg):
        if not arg:
            return
        self.resolve(arg).mkdir(exist_ok=True)

    def do_rm(self, arg):
        if not arg:
            return
        try:
            self.resolve(arg).unlink()
        except Exception as e:
            print(e)

    def do_history(self, arg):
        for i, cmdline in enumerate(self.history_log, 1):
            print(f"{i:3} {cmdline}")

    def do_whoami(self, arg):
        print(os.getenv("USERNAME") or os.getenv("USER"))

    def do_uname(self, arg):
        print(platform.platform())

    def do_date(self, arg):
        print(datetime.now())

    def do_sysinfo(self, arg):
        print("OS      :", platform.platform())
        print("Python  :", platform.python_version())
        print("Machine :", platform.machine())
        print("Host    :", socket.gethostname())
        if psutil:
            print("CPU     :", psutil.cpu_count())
            print("RAM     :", round(psutil.virtual_memory().total/1024**3,2),"GB")

    # =========================================================
    # TOOL 1 : Live Monitor
    # =========================================================

    def do_monitor(self, arg):
        if not psutil:
            print("Install psutil first.")
            return

        try:
            while True:
                os.system("cls" if os.name=="nt" else "clear")
                print("Linux-Pyhack Monitor\n")
                print("Time:",datetime.now())
                print("CPU :",psutil.cpu_percent(),"%")
                mem=psutil.virtual_memory()
                print("RAM :",mem.percent,"%")
                print("Processes:",len(psutil.pids()))
                print("\nTop Processes")
                print("-"*40)

                plist=sorted(
                    psutil.process_iter(["pid","name","memory_percent"]),
                    key=lambda p:p.info["memory_percent"],
                    reverse=True
                )[:10]

                for p in plist:
                    i=p.info
                    print(f"{i['pid']:6} {i['memory_percent']:5.1f}% {i['name']}")

                print("\nCtrl+C to exit")
                time.sleep(1)

        except KeyboardInterrupt:
            print()

    # =========================================================
    # TOOL 2 : Ping
    # =========================================================

    def do_ping(self,arg):
        if not arg:
            return
        cmdline=["ping","-n","4",arg] if os.name=="nt" else ["ping","-c","4",arg]
        subprocess.run(cmdline)

    # =========================================================
    # TOOL 3 : DNS Lookup
    # =========================================================

    def do_dns(self,arg):
        if not arg:
            return
        try:
            res=socket.getaddrinfo(arg,None)
            ips=sorted({x[4][0] for x in res})
            for ip in ips:
                print(ip)
        except Exception as e:
            print(e)

    # =========================================================
    # TOOL 4 : TCP Port Scanner
    # =========================================================

    def do_scan(self,arg):
        if not arg:
            print("scan HOST [22,80,443]")
            return

        parts=arg.split()
        host=parts[0]

        if len(parts)>1:
            ports=[int(x) for x in parts[1].split(",")]
        else:
            ports=[21,22,23,53,80,110,143,443,445,3306,8080]

        print(f"Scanning {host}\n")

        for port in ports:
            s=socket.socket()
            s.settimeout(0.5)
            try:
                s.connect((host,port))
                print(f"{port}/tcp OPEN")
            except:
                print(f"{port}/tcp closed")
            s.close()

    # =========================================================
    # TOOL 5 : HTTP Headers
    # =========================================================

    def do_headers(self,arg):
        if not arg:
            return
        try:
            req=urllib.request.Request(arg,method="HEAD")
            with urllib.request.urlopen(req,timeout=5) as r:
                print("Status:",r.status)
                for k,v in r.headers.items():
                    print(f"{k}: {v}")
        except urllib.error.HTTPError as e:
            print("Status:",e.code)
            for k,v in e.headers.items():
                print(f"{k}: {v}")
        except Exception as e:
            print(e)

    # =========================================================
    # TOOL 6 : TLS Certificate
    # =========================================================

    def do_tls(self,arg):
        if not arg:
            return

        try:
            ctx=ssl.create_default_context()

            with socket.create_connection((arg,443),timeout=5) as sock:
                with ctx.wrap_socket(sock,server_hostname=arg) as s:

                    cert=s.getpeercert()

                    print("TLS Version :",s.version())
                    print("Cipher      :",s.cipher()[0])

                    print("\nSubject")
                    for x in cert["subject"]:
                        print(x)

                    print("\nIssuer")
                    for x in cert["issuer"]:
                        print(x)

                    print("\nValid From :",cert["notBefore"])
                    print("Valid Until:",cert["notAfter"])

        except Exception as e:
            print(e)

    # =========================================================
    # Extra Utility
    # =========================================================

    def do_sha256(self,arg):
        if not arg:
            return
        try:
            data=self.resolve(arg).read_bytes()
            print(hashlib.sha256(data).hexdigest())
        except Exception as e:
            print(e)

    # =========================================================

    def do_exit(self,arg):
        print("Shutting down Linux-Pyhack...")
        return True

    do_quit=do_exit

    def default(self,line):
        try:
            subprocess.run(
                shlex.split(line),
                cwd=self.cwd,
                shell=False
            )
        except FileNotFoundError:
            print("Command not found.")
        except Exception as e:
            print(e)

if __name__=="__main__":
    LinuxPyhack().cmdloop()