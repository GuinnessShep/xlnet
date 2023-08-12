import subprocess
import sys

def install_required_modules():
    required_modules = [
        "rich", "colorama", "PyInquirer", "halo", "pyfiglet", "termcolor", "tqdm", "requests"
    ]

    installed_modules = subprocess.check_output([sys.executable, '-m', 'pip', 'freeze'])
    installed_modules = installed_modules.decode('utf-8').split('\n')

    for module in required_modules:
        if module not in installed_modules:
            subprocess.call([sys.executable, "-m", "pip", "install", module])

install_required_modules()

import os
import subprocess
import webbrowser
import requests
import platform
import time
import zipfile
from rich.console import Console
from rich.panel import Panel
from rich.progress import track
from colorama import Fore, Back, init
from PyInquirer import prompt, Separator
from halo import Halo
from pyfiglet import figlet_format
from termcolor import colored
from tqdm import tqdm

init(autoreset=True)

console = Console()

def display_title():
    os.system('cls' if os.name == 'nt' else 'clear')
    title = figlet_format("OTP Bot Setup", font="slant")
    console.print(colored(title, "yellow"))

def download_ngrok():
    system = platform.system()
    ngrok_url = {
        "Windows": "https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-windows-amd64.zip",
        "Linux": "https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-amd64.zip",
        "Darwin": "https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-darwin-amd64.zip"
    }.get(system)

    if not ngrok_url:
        return False

    r = requests.get(ngrok_url)
    with open('ngrok.zip', 'wb') as file:
        file.write(r.content)

    with zipfile.ZipFile('ngrok.zip', 'r') as zip_ref:
        zip_ref.extractall('.')

    return True

def install_dependencies():
    packages = ["discord", "Flask", "discord-py-slash-command", "twilio"]
    for package in packages:
        subprocess.call(f"pip3 install {package}", shell=True)

def modify_bot_file(bot_token, server_id, account_sid, auth_token, twilio_phone_number, ngrok_url):
    with open("bot.py", "r") as file:
        bot_content = file.readlines()

    updates = {
        "bot_token_placeholder": bot_token,
        "server_id_placeholder": server_id,
        "account_sid_placeholder": account_sid,
        "auth_token_placeholder": auth_token,
        "twilio_phone_number_placeholder": twilio_phone_number,
        "ngrok_url_placeholder": ngrok_url
    }

    for index, line in enumerate(bot_content):
        for placeholder, value in updates.items():
            if placeholder in line:
                bot_content[index] = line.replace(placeholder, value)

    with open("bot.py", "w") as file:
        file.writelines(bot_content)

def main_menu():
    questions = [
        {
            "type": "list",
            "name": "action",
            "message": "What would you like to do?",
            "choices": [
                "Setup",
                "Exit"
            ]
        }
    ]
    answer = prompt(questions)
    return answer["action"]

def setup():
    spinner = Halo(text="Starting Setup", spinner="dots")
    spinner.start()

    # Step 1: Download ngrok
    spinner.text = "Downloading ngrok..."
    if not download_ngrok():
        spinner.fail("Failed to download ngrok!")
        return

    # Step 2: Install Dependencies
    spinner.text = "Installing Python packages..."
    install_dependencies()

    # Step 3: Discord Bot Setup
    webbrowser.open("https://discord.com/developers/applications/")
    bot_token = console.input(f"[cyan]Enter your bot token from Discord Developer Portal: [/cyan]")

    # Step 4: Obtain Server ID
    server_id = console.input(f"[cyan]Paste your server ID from Discord: [/cyan]")

    # Step 5: Twilio Setup
    account_sid = console.input(f"[cyan]Enter your Twilio 'Account SID': [/cyan]")
    auth_token = console.input(f"[cyan]Enter your Twilio 'Auth Token': [/cyan]")
    twilio_phone_number = console.input(f"[cyan]Enter your Twilio Phone Number: [/cyan]")

    # Step 6: Start ngrok and fetch the URL
    console.print("Starting ngrok...", style="bold blue")
    subprocess.Popen("./ngrok http 5000", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    time.sleep(5)
    ngrok_url = console.input(f"[cyan]Paste your ngrok https link/url here: [/cyan]")

    # Update bot.py
    spinner.text = "Updating bot.py with your details..."
    modify_bot_file(bot_token, server_id, account_sid, auth_token, twilio_phone_number, ngrok_url)
    spinner.succeed("Setup completed successfully!")

if __name__ == "__main__":
    while True:
        display_title()
        action = main_menu()
        if action == "Setup":
            setup()
        elif action == "Exit":
            console.print("Exiting. Goodbye!", style="bold red")
            break
