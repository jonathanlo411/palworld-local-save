import os
import argparse
from json import load
from shutil import copytree
from subprocess import run
from datetime import datetime


SAVE_PATH = lambda drive, user, sID: \
    fr'{drive}:\Users\{user}\AppData\Local\Pal\Saved\SaveGames\{sID}'


SELECT_MSG = lambda saves: f"""
{COLORS.okcyan}--- Please select a save using -n or use the -a flag to backup all saves ---{COLORS.endc}
Saves: {saves}
"""


def main():
    # Load user setup
    user_setup = load(open('config.json', 'r'))

    # Parse Args
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--name', help='Name of the save file.')
    parser.add_argument('-a', '--all', help='Backs up all saves.', action='store_true')
    args = parser.parse_args()

    # Setup for saving
    local_save_path = SAVE_PATH (
        user_setup['localDrive'],
        user_setup['localUser'],
        user_setup['steamID']
    )
    if 'saves' not in os.listdir('.'): os.mkdir('saves')

    # Copying files to local dir
    if (args.name):
        local_save = os.path.join(local_save_path, args.name)
        copytree(local_save, f'./saves/{args.name}-{datetime.now().timestamp()}')
    elif (args.all):
        local_saves = os.listdir(local_save_path)
        local_saves.pop()
        for save in local_saves:
            local_save = os.path.join(local_save_path, save)
            copytree(local_save, f'./saves/{save}-{datetime.now().timestamp()}')
    else:
        local_saves = os.listdir(local_save_path)
        local_saves.pop()
        print(SELECT_MSG(local_saves))
        return
    
    # Pushing files to remote
    try:
        run("git add world_data/", shell=True)
        run(f'git commit -m "World save: {datetime.now()}"', shell=True)
        run("git push", shell=True)
        print(f"{COLORS.okgreen}Local World data saved to GitHub{COLORS.endc}")
    except Exception as e:
        print(f"{COLORS.fail}Error occured when pushing:{COLORS.endc}\n{e}")
    

# --- UTILITY ---


class COLORS:
    okgreen = "\033[92m"
    okcyan = '\033[96m'
    warning = "\033[93m"
    fail = "\033[91m"
    endc = "\033[0m"


# Hoisting
if __name__ == '__main__':
    main()