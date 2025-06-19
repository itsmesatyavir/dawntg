import json
import os
import subprocess

ACCOUNTS_FILE = "accounts.json"


def menu():
    print("\n--- Dawn Validator Manager ---")
    print("\n--- http://t.me/forestarmy ---")
    print("1. Run Script")
    print("2. Account Setup")
    choice = input("Enter choice (1/2): ").strip()
    if choice == "1":
        run_script()
    elif choice == "2":
        setup_accounts()
    else:
        print("Invalid option. Please choose 1 or 2.")
        menu()


def setup_accounts():
    accounts = []

    try:
        count = int(input("How many accounts do you want to save? ").strip())
    except ValueError:
        print("Please enter a valid number.")
        return setup_accounts()

    for i in range(count):
        print(f"\nEnter details for Account {i + 1}:")
        email = input("Email: ").strip()
        token = input("Token: ").strip()
        accounts.append({
            "name": f"Account {i + 1}",
            "email": email,
            "token": token
        })

    # Save to accounts.json
    with open(ACCOUNTS_FILE, "w") as f:
        json.dump(accounts, f, indent=2)
    
    print(f"\n✅ {count} account(s) saved to '{ACCOUNTS_FILE}'")


def run_script():
    print("\n🔄 Running bot.py...")
    try:
        subprocess.run(["python", "bot.py"])
    except FileNotFoundError:
        print("❌ 'bot.py' not found. Please make sure it exists in the same folder.")
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    menu()
