import os
import platform
import subprocess
import sys
from pathlib import Path
import os
import getpass
import shutil
from win32com.client import Dispatch


def create_windows_startup_shortcut(executable_path):

    startup_folder_path = os.path.join(
        os.getenv("APPDATA"),
        "Microsoft",
        "Windows",
        "Start Menu",
        "Programs",
        "Startup",
    )
    # Define the path to the shortcut file
    shortcut_path = os.path.join(startup_folder_path, "DateReminder.lnk")

    # Create a WScript Shell object
    shell = Dispatch("WScript.Shell")

    # Create a shortcut object
    shortcut = shell.CreateShortCut(shortcut_path)

    # Set the properties of the shortcut
    shortcut.TargetPath = executable_path
    shortcut.WorkingDirectory = os.path.dirname(
        executable_path
    )  # Set the working directory to the directory of the executable

    # Save the shortcut
    shortcut.Save()


def create_macos_startup_plist(executable_path):
    plist_contents = f"""<?xml version="1.0" encoding="UTF-8"?>
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>DateReminder</string>
    <key>ProgramArguments</key>
    <array>
        <string>{executable_path}</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
</dict>
</plist>
"""
    plist_path = os.path.expanduser("~/Library/LaunchAgents/com.date_reminder.plist")
    with open(plist_path, "w") as plist_file:
        plist_file.write(plist_contents)


def create_linux_startup_service(executable_path):
    service_contents = f"""[Unit]
Description=Date Reminder Service
After=network.target

[Service]
ExecStart={executable_path}

[Install]
WantedBy=default.target
"""
    service_path = "/etc/systemd/system/date-reminder.service"
    with open(service_path, "w") as service_file:
        service_file.write(service_contents)
    subprocess.run(["systemctl", "daemon-reload"])
    subprocess.run(["systemctl", "enable", "date-reminder.service"])


def main():
    executable_path = os.path.join(
        os.path.expanduser("~"), "Downloads", "date_reminder", "main_widget.exe"
    )

    if not os.path.exists(executable_path):
        print(executable_path)
        print("Error: main_widget.exe not found.")
        sys.exit(1)

    os.makedirs(
        os.path.join(os.path.expanduser("~"), "Downloads", "date_reminder"),
        exist_ok=True,
    )

    system = platform.system()

    if system == "Windows":
        create_windows_startup_shortcut(executable_path)
    elif system == "Darwin":  # macOS
        create_macos_startup_plist(executable_path)
    elif system == "Linux":
        create_linux_startup_service(executable_path)
    else:
        print(f"Error: Unsupported operating system - {system}")
        sys.exit(1)

    print("Startup shortcut created successfully.")


if __name__ == "__main__":
    main()
