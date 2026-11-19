from pathlib import Path
import shutil
from datetime import datetime
import psutil
import time

def get_save_folder_path():
    original_folder_path = Path.home() / "AppData" / "LocalLow" / "TheFarmerWasReplaced" / "TheFarmerWasReplaced" / "Saves"
    if original_folder_path.is_dir():
        print(f"Folder exists: {original_folder_path}")
        for path in original_folder_path.iterdir():
            print(f"Found file: {path.name}")
    else:
        print(f"Folder does not exist: {original_folder_path}")
        return None
    return original_folder_path


def backup_save_files(original_folder_path: Path):
    now = datetime.now()
    now_foldername = now.strftime("%Y-%m-%d_%H-%M-%S")
    backup_folder_path = Path(__file__).resolve().parent / "backup_saves" / now_foldername

    if backup_folder_path.exists():
        print(f"Backup folder already exists: {backup_folder_path}")
        return False

    try:
        shutil.copytree(original_folder_path, backup_folder_path)
        print(f"Backup completed from {original_folder_path} to {backup_folder_path}")
        return True

    except Exception as e:
        shutil.rmtree(backup_folder_path, ignore_errors=True)
        print(f"Error occurred while backing up: {e}")
        return False


def is_game_running():
    process_name = "TheFarmerWasReplaced.exe"
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] == process_name:
            return True
    return False

previous_state = None
current_state = is_game_running()

print("Monitoring the game process...")

while True:
    current_state = is_game_running()
    if previous_state is False and current_state is True:
        print("The game has started")

    elif previous_state is True and current_state is False:
        print("The game has stopped")
        original_folder_path = get_save_folder_path()
        if original_folder_path:
            if backup_save_files(original_folder_path):
                print("Backup process completed!")
            else:
                print("Backup process failed")

    previous_state = current_state
    time.sleep(3)  #3秒ごとに監視