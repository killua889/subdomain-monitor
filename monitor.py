#!/usr/bin/env python3
import subprocess
import time
import argparse
import tempfile
import sys
import os
from datetime import datetime


def run_cmd(cmd, stdin=None):
    """Run a command safely and return stdout"""
    result = subprocess.run(
        cmd,
        stdin=stdin,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=True
    )
    return result.stdout


def send_notify(message, notifyid):
    """Send Telegram notification (signal only)"""
    try:
        subprocess.run(
            ["notify", "-p", "telegram", "-id", notifyid],
            input=message,
            text=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=True
        )
    except subprocess.CalledProcessError:
        print("[!] Failed to send Telegram notification")


def new_sub_alert(domainfile, notifyid, folderpath):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    now_readable = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print(f"[+] Starting subdomain check at {now_readable}")
    print(f"[+] Domain list: {domainfile}")
    print(f"[+] Program folder: {folderpath}")

    # Ensure main folder exists
    os.makedirs(folderpath, exist_ok=True)

    # Create subfolder for new subdomain files
    subs_folder = os.path.join(folderpath, "new-subs")
    os.makedirs(subs_folder, exist_ok=True)

    new_log_file = os.path.join(subs_folder, f"new-subs-{timestamp}.txt")

    with tempfile.NamedTemporaryFile(mode="w+", delete=True) as tmp:
        try:
            # Run subfinder
            run_cmd([
                "subfinder",
                "-dL", domainfile,
                "-all",
                "-silent",
                "-o", tmp.name
            ])

            # Detect only new subdomains (compared to domainfile)
            with open(tmp.name, "r") as temp_output:
                new_subs = run_cmd(
                    ["anew", domainfile],
                    stdin=temp_output
                ).strip()

            if new_subs:
                subs_list = new_subs.splitlines()
                count = len(subs_list)

                # Save ONLY this run's new subdomains
                with open(new_log_file, "w") as f:
                    f.write(new_subs + "\n")

                # Send notification (signal only)
                send_notify(
                    f"🚨 New subdomains detected\n"
                    f"📁 Program: {os.path.basename(folderpath)}\n"
                    f"🧾 Count: {count}\n"
                    f"⏰ Time: {now_readable}",
                    notifyid
                )

                print(f"[+] {count} new subdomains saved to {new_log_file}")
            else:
                print("[-] No new subdomains found")

        except subprocess.CalledProcessError as e:
            print(f"[!] Error: {e.stderr}")

    print("-" * 60)


def main():
    parser = argparse.ArgumentParser(
        description="Automated subdomain monitoring with Telegram alerts"
    )
    parser.add_argument(
        "-l", "--domainlist",
        required=True,
        help="File containing root domains"
    )
    parser.add_argument(
        "-f", "--folderpath",
        required=True,
        help="Program folder path (used for storing results)"
    )
    parser.add_argument(
        "-n", "--notifyid",
        required=True,
        help="Notify provider ID"
    )
    parser.add_argument(
        "-s", "--sleep",
        type=int,
        default=28800,
        help="Sleep time between runs in seconds (default: 28800 = 8h)"
    )

    args = parser.parse_args()

    if args.sleep <= 0:
        print("[!] Sleep time must be greater than 0")
        sys.exit(1)

    try:
        while True:
            new_sub_alert(
                args.domainlist,
                args.notifyid,
                args.folderpath
            )
            print(f"[i] Sleeping for {args.sleep} seconds...\n")
            time.sleep(args.sleep)
    except KeyboardInterrupt:
        print("\n[!] Script stopped by user")
        sys.exit(0)


if __name__ == "__main__":
    main()