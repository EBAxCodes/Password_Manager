# ...existing code...
import json
from pathlib import Path
from getpass import getpass
from hashlib import pbkdf2_hmac
from cryptography.fernet import Fernet
from colorama import init, Fore, Style
import pyperclip
import secrets
import string
import os
from datetime import datetime

init(autoreset=True)
# --------------------- FILES & STORAGE -----------------#
DATA_FILE = Path("passwords.json")
MASTER_FILE = Path("master.hash")
KEY_FILE = Path("key.key")

# ------------------- SECURITY UTILITIES -----------------#
def generate_salt():
    return secrets.token_bytes(16)

def hash_master(password, salt):
    return pbkdf2_hmac("sha256", password.encode(), salt, 100_000).hex()

def generate_key():
    key = Fernet.generate_key()
    KEY_FILE.write_bytes(key)
    return key

def load_key():
    # call read_bytes() not the method object
    return KEY_FILE.read_bytes() if KEY_FILE.exists() else generate_key()

def encrypt_data(data):
    f = Fernet(load_key())
    raw = json.dumps(data).encode()
    return f.encrypt(raw)

def decrypt_data(token):
    f = Fernet(load_key())
    try:
        return json.loads(f.decrypt(token).decode())
    except Exception:
        return []

# -------------------- PASSWORD UTILITIES ----------------------#
def strong_password(length=16):
    # use punctuation rather than printable (printable contains whitespace/newlines)
    chars = string.ascii_letters + string.digits + string.punctuation
    return "".join(secrets.choice(chars) for _ in range(length))

# ------------------ MASTER PASSWORD ----------------------#
def set_master_password():
    salt = generate_salt()
    while True:
        pwd = getpass(Fore.CYAN + "Set master password: ")
        confirm = getpass(Fore.CYAN + "Confirm master password: ")
        if pwd == confirm and pwd.strip():
            hashed = hash_master(pwd, salt)
            MASTER_FILE.write_bytes(salt + hashed.encode())
            print(Fore.GREEN + "✅ Master password set successfully!\n")
            return
        print(Fore.RED + "Passwords do not match or empty. Try again.\n")

def check_master_password():
    if not MASTER_FILE.exists():
        set_master_password()
    # load stored salt+hash after ensuring file exists
    stored = MASTER_FILE.read_bytes()
    salt = stored[:16]
    hashed_stored = stored[16:].decode()
    for _ in range(3):
        pwd = getpass(Fore.CYAN + "Enter master password: ")
        if hash_master(pwd, salt) == hashed_stored:
            return
        print(Fore.RED + "Incorrect password!")
    print(Fore.RED + "Too many failed attempts. Exiting...")
    exit(1)

# ------------------------- PASSWORD MANAGER --------------------------#
class PasswordManager:
    def __init__(self):
        self.passwords = self.load_passwords()

    def load_passwords(self):
        if DATA_FILE.exists():
            try:
                with open(DATA_FILE, "rb") as f:
                    return decrypt_data(f.read()) or []
            except Exception:
                return []
        return []

    def save_passwords(self):
        with open(DATA_FILE, "wb") as f:
            f.write(encrypt_data(self.passwords))

    def add_password(self):
        site = input(Fore.CYAN + "Website/App: ").strip()
        username = input(Fore.CYAN + "Username: ").strip()
        choice = input(Fore.CYAN + "Generate strong password? (y/n): ").lower()
        if choice in ("y", "yes"):
            pwd = strong_password()
            print(Fore.GREEN + f"Generated password: {pwd}")
        else:
            pwd = getpass(Fore.CYAN + "Password: ")
        note = input(Fore.CYAN + "Note (optional): ").strip()
        now = datetime.now().strftime("%Y-%m-%d %H:%M")
        self.passwords.append({
            "site": site,
            "username": username,
            "password": pwd,
            "note": note,
            "created": now,
            "updated": now
        })
        self.save_passwords()
        print(Fore.GREEN + "✅ Password added successfully!")

    def view_passwords(self):
        if not self.passwords:
            print(Fore.YELLOW + "No passwords stored.\n")
            return
        print(Fore.MAGENTA + f"\n======= Stored Passwords ({len(self.passwords)}) =======")
        for idx, p in enumerate(self.passwords, 1):
            print(Fore.CYAN + f"{idx}. {p['site']} | {p['username']} | Note: {p.get('note','')}")
        print(Fore.MAGENTA + "====================================\n")
        choice = input(Fore.CYAN + "Copy password to clipboard? Enter number (or press Enter to skip): ").strip()
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(self.passwords):
                pyperclip.copy(self.passwords[idx]["password"])
                print(Fore.CYAN + "✅ Password copied to clipboard!")

    def delete_password(self):
        self.view_passwords()
        if not self.passwords:
            return
        choice = input(Fore.CYAN + "Enter number to delete: ").strip()
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(self.passwords):
                confirm = input(Fore.RED + f"Confirm delete {self.passwords[idx]['site']}? (y/n): ").lower()
                if confirm in ("y", "yes"):
                    removed = self.passwords.pop(idx)
                    self.save_passwords()
                    print(Fore.RED + f"🚮 Deleted password for {removed['site']}.")

    def edit_password(self):
        self.view_passwords()
        if not self.passwords:
            return
        choice = input(Fore.CYAN + "Enter number to edit: ").strip()
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(self.passwords):
                p = self.passwords[idx]
                p["site"] = input(Fore.CYAN + f"Website/App ({p['site']}): ") or p["site"]
                p["username"] = input(Fore.CYAN + f"Username ({p['username']}): ") or p["username"]
                new_pwd = getpass(Fore.CYAN + "New Password (leave blank to keep current): ")
                if new_pwd.strip():
                    p["password"] = new_pwd
                p["note"] = input(Fore.CYAN + f"Note ({p.get('note','')}): ") or p.get("note","")
                p["updated"] = datetime.now().strftime("%Y-%m-%d %H:%M")
                self.save_passwords()
                print(Fore.GREEN + "✅ Password updated.")

    def search_passwords(self):
        keyword = input(Fore.CYAN + "Enter site/app keyword to search: ").lower()
        results = [p for p in self.passwords if keyword in p["site"].lower()]
        if not results:
            print(Fore.YELLOW + "No matches found.\n")
            return
        print(Fore.MAGENTA + f"\n======= Search Results ({len(results)}) =======")
        for idx, p in enumerate(results, 1):
            print(Fore.CYAN + f"{idx}. {p['site']} | {p['username']} | Note: {p.get('note','')}")
        print(Fore.MAGENTA + "=========================================\n")

# ------------------------------------ MAIN MENU ---------------------------------- #
def main():
    print(Fore.GREEN + "\n🔐 ELITE PASSWORD MANAGER\n")
    check_master_password()
    manager = PasswordManager()
    while True:
        print(Fore.MAGENTA + "\n=====================MENU ============2")
        print(Fore.CYAN + "1. Add Password")
        print(Fore.CYAN + "2. View Password")
        print(Fore.CYAN + "3. Edit Password")
        print(Fore.CYAN + "4. Delete Password")
        print(Fore.CYAN + "5. Search Passwords")
        print(Fore.CYAN + "6. Generate Strong Password")
        print(Fore.CYAN + "7. Exit")
        print(Fore.MAGENTA + "===========================================")
        choice = input(Fore.YELLOW + " Enter choice: ").strip()

        if choice == "1":
            manager.add_password()
        elif choice == "2":
            manager.view_passwords()
        elif choice == "3":
            manager.edit_password()
        elif choice == "4":
            manager.delete_password()
        elif choice == "5":
            manager.search_passwords()
        elif choice == "6":
            length = input(Fore.CYAN + "Password length (default 16): ").strip()
            length = int(length) if length.isdigit() else 16
            print(Fore.GREEN + f"Generated password: {strong_password(length)}")
        elif choice == "7":
            print(Fore.CYAN + "Goodbye 👋")
            break
        else:
            print(Fore.RED + "Invalid choice. Try again.")

if __name__ == "__main__":
    main()
# ...existing code...