import os
import sys
import shutil
import configparser

config = configparser.ConfigParser()
config.read("config.ini")
log_file = "autofile.log"

enable_logs = config.getboolean("settings", "enable_logs", fallback=True)

def log(message):
    if not enable_logs:
        return
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(message + "\n")


def run_organizer():
    print("Welcome to AutoFile, a smart file organizer built entirely using Python!\n")
    print("Starting organization...\n")
    log("[INFO] AutoFile launched.")

    quiet = "n"
    if config.has_section("settings"):
        quiet_mode = config.getboolean("settings", "quiet_mode", fallback=False)
        quiet = "y" if quiet_mode else "n"

    if quiet not in ["y", "n"]:
        while quiet != "y" and quiet != "n":
            quiet = input("Would you like to enable quiet mode? (Y/N): ").lower()

    home_folder = os.path.expanduser("~")

    default_folder = config.get("settings", "default_folder", fallback="")

    if default_folder:
        folder_name = default_folder
    else:
        folder_name = input("Enter the name of the target folder: ")

    target_folder = os.path.join(home_folder, folder_name)

    while not os.path.exists(target_folder):
        print("\nSorry, we couldn't find that folder!\n")
        folder_name = input("\nPlease re-enter the name of the target folder: ")
        target_folder = os.path.join(home_folder, folder_name)

    print("\nSuccessfully found target folder.\n")
    print("Targeting organization at", target_folder, "\n")
    log(f"[INFO] Target folder: {target_folder}")

    files = [
        f for f in os.listdir(target_folder)
        if os.path.isfile(os.path.join(target_folder, f))
    ]

    total_files = len(files)
    processed_files = 0
    log(f"[INFO] Total files detected: {total_files}")

    for item in files:
        if quiet == "n":
            full_path = os.path.join(target_folder, item)
            name, extension = os.path.splitext(item)
            print("File:", item, "Extension:", extension)

    categories = {
        "Text": [".txt", ".pdf", ".rtf", ".csv", ".json", ".xml", ".html"],
        "Images": [".jpg", ".png", ".gif", ".bmp", ".tiff", ".jpeg"],
        "Office Suite": [".docx", ".pptx", ".xlsx", ".xls"],
        "Music": [".mp3", ".wav", ".aac", ".flac"],
        "Video": [".mp4", ".mkv", ".avi", ".mov", ".flv"],
        "Code": [".py", ".ipynb", ".c", ".cpp", ".java", ".js", ".sh", ".bat"],
        "Archives": [".zip", ".tar", ".gz", ".7z", ".rar"],
        "Data": [".pickle", ".pkl", ".npy", ".h5"],
        "Python_Specific": [".pyc", ".pyd", ".pyw", ".pyi", ".pyx"],
        "Executables": [".exe", ".msi", ".app"],
    }

    for item in files:
        full_path = os.path.join(target_folder, item)
        if not os.path.isfile(full_path):
            continue

        name, extension = os.path.splitext(item)
        extension = extension.lower()

        found = False
        for category_name, extensions_list in categories.items():
            if extension in extensions_list:
                if quiet == "n":
                    print(f"{item} → {category_name}")
                found = True
                category_folder = os.path.join(target_folder, category_name)
                os.makedirs(category_folder, exist_ok=True)
                shutil.move(full_path, os.path.join(category_folder, item))
                log(f"[INFO] Moved: {item} → {category_name}")
                break

        if not found:
            category_folder = os.path.join(target_folder, "Others")
            os.makedirs(category_folder, exist_ok=True)
            shutil.move(full_path, os.path.join(category_folder, item))
            log(f"[WARN] Moved to Others: {item}")

        processed_files += 1
        log(f"[INFO] Progress: {processed_files}/{total_files}")
        print(f"\rProcessed {processed_files}/{total_files} files...", end="", flush=True)

    log("[INFO] Organization complete")
    print("\nOrganization complete.\n")
    input("Press enter / return to exit.\n")


def settings_menu():
    if not config.has_section("settings"):
        config.add_section("settings")

    while True:
        print("\n=== Settings ===")
        print("1. Toggle quiet mode")
        print("2. Toggle logging")
        print("3. Set default folder")
        print("4. Back")

        choice = input("Choose: ").strip()

        if choice == "1":
            current = config.getboolean("settings", "quiet_mode", fallback=False)
            config.set("settings", "quiet_mode", str(not current))
            print(f"Quiet mode set to {not current}")

        elif choice == "2":
            current = config.getboolean("settings", "enable_logs", fallback=True)
            config.set("settings", "enable_logs", str(not current))
            print(f"Logging set to {not current}")

        elif choice == "3":
            folder = input("Enter default folder name (inside home): ").strip()
            config.set("settings", "default_folder", folder)
            print("Default folder updated")

        elif choice == "4":
            with open("config.ini", "w") as f:
                config.write(f)
            break

        else:
            print("Invalid option.")


def main_menu():
    while True:
        print("\n=== AutoFile Main Menu ===")
        print("1. Organize files")
        print("2. Settings")
        print("3. Exit")

        choice = input("Select an option (1-3): ").strip()

        if choice == "1":
            run_organizer()
        elif choice == "2":
            settings_menu()
        elif choice == "3":
            print("Goodbye.")
            break
        else:
            print("Invalid choice. Try again.")


main_menu()
