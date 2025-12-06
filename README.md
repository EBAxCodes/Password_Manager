🔐 Elite Password Manager (Python)
A secure, offline-first, AES-256 encrypted password manager built for speed, privacy and absolute control.
Designed by EBAxCodes, engineered with Python, and powered by modern cyptography.

✨ Overview
Elite Password Manager is a terminal-based, military upgrade encrypted credential vault that stores, retrieves, and exports passwords without ever exposing raw data to disk.
All passwords are protected using the Fernet implementation of AES-256, ensuring that even if someone gets access to your device, your login credentials remain unreadable.
This project is ideal for:
 ● Cybersecurity learners
 ● Python beginners looking for real projects
 ● Anyone who wants a private, offline alternative to commercial  password managers
 Everything is stored locally - you own your data.
 
 💎 Core Features
 
 🔐 AES-256 Encryption
 All passwords are enctypted using the Cryptography library's Fernet symmetric encryption.
 Your master password is transformed into a secure encryption key.
 
  📝 Add, View & Search Passwords
  ● Add new credentials
  ● Retrieve saved ones
  ● Search by account name(eg., gmail, facebook)

🔁 Automatic Encryption/Decryption
The program safely decrypts only when needed and immediately re-encrypts after use.

🛡 Export Encrypted Backup
Create a .vault file backup - still encypted - and restore it on any device.

📂 Local Secure Storage
All saved entries are stored inside passwords.json, encrypted end-to-end

🎨 Colored UI (Colorama)
Clean output formatting to clipboard without printing them on the screen.

🧠 Upcoming Pro Features (Roadmap)
  Feature                                                  Status
  ● Auto-lock after inactivity                              🟡 Planned
  ● Wrong-Password lockout + fake vault                     🟡 Planned
  ● UI App (Tkinter/ PyQt)                                  🔵 In Progress
  ● Background stealth mode                                 🟡 Planned
  ● Keyword tagging system                                  🟡 Planned
  ● Password expiry notifications                           🔵 In Progress

 🛠 Installation
  ● Make sure Python is installed:
  > python --version 
  ● Install required dependencies
  > pip install colorama cryptography pyperclip
    if pip is not recognized, run:
    > py -m pip install colorama cryptography pyperclip

 📂 Project Structure
 ElitePasswordManager/
 | ------ main.py                           # The main program
 | ------ passwords.json                    # Encrypted password storage(auto-generated)
 |------ vault.key                          # Encryption key file (auto-generated)
 |------ README.md                          # Documentation (license included)
 |------ gitignore                          # Git ignore config

 ▶ How to Use
 Start tha app
 > python main.py
 
 1. Set your master password
 The first time you run the program, it will ask you to create a master password

 2. Add entries
 Example:
 Enter account/service: Gmail
 Enter username/email: example@gmail.com
 Enter password: (auto or manual)

 3. View stored passwords
 Only decrypted in memory during your session

 4. Copy to Clipboard
 You can copy passwords without printing anything to the terminal for extra privacy.

 🔐 Security Notes
  ●  Your master password cannot be recovered. Lose it → lose the vault.
  ●  Never share or upload vault.key or passwords.json
  ●  Keep backup in a safe location
  ●  All encryption is offline - no cloud sync
  
   
 


