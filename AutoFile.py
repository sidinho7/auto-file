import os
import sys
import shutil

print("Welcome to AutoFile, a smart file organizer built entirely using Python!")
print("Starting organization...")
quiet = input("Would you like to enable quiet mode? This ensures your console does not print the file names, extensions, etc. (Y/N): ").lower()

home_folder = os.path.expanduser("~")

folder_name = input("Enter the name of the target folder: ")
target_folder = os.path.join(home_folder, folder_name)

if os.path.exists(target_folder):
    print("Successfully found target folder.")
    print("Targeting organization at", target_folder)
else:
    print("Sorry, we couldn't find that folder!")

files = os.listdir(target_folder)

for item in files:
    if quiet == "n":
        full_path = os.path.join(target_folder, item) 
        if os.path.isfile(full_path):
            name, extension = os.path.splitext(item)
            print("File:", item,"Extension:", extension)
        elif os.path.isdir(full_path):
            print("Folder:", item)
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
    "Executables": [".exe", ".msi", ".bat"],
}

for item in files:
    full_path = os.path.join(target_folder, item)
    if os.path.isfile(full_path):
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
                break
        
        if not found and quiet == "n":
            print(f"{item} → Unknown type")
print("Organization complete.")
input("Press enter / return to exit.")