import subprocess
import os
from datetime import datetime
import time
import random

# TODO LIST
    # Make it work with double digit commit max/min
    # Add time of check when check ins are made
    # Can convert program to make all files via Python instead of having to mess with try-except block for command line /: wish I thought of this earlier, but it's fine, I'm fine.
    


# FILE PATHS
settings_file_path = "./git-real-green-folder/settings_file.txt"
save_file_path = "./git-real-green-folder/save_file.txt"
git_repo_link_file_path = "./git-real-green-folder/git_repo_link_file.txt"
excluded_days_file_path = "./git-real-green-folder/excluded_days_file.txt"
commit_js_file_path = "./git-real-green-folder/git-repo-for-commits/main.js"


now = datetime.now() # Current date and time
today_weekday = str(datetime.today().weekday()) # Current day of the week
interval = 43200 # Sleep interval / cooldown between checks (seconds)
commit_cooldown = 10 # Sleep interval for cooldown between GitHub commits (seconds)



def startup_mode_selector():
    is_settings_file_exist = os.path.isfile(settings_file_path)
    if is_settings_file_exist == False:
        first_time_startup()
    else:
        startup()


def first_time_startup():
    is_save_file_exist = os.path.isfile(save_file_path)
    if is_save_file_exist == False:
        subprocess.run("mkdir git-real-green-folder", shell=True, check=True)
        save_file_creator = open(save_file_path, "a+")
        save_file_creator.close()

    settings_file = open(settings_file_path, "a+")

    print('\n\nFirst time setup: ')



    max_commits_per_day = int(input("\n\n\tEnter max number of commits you would like per day (int 1-9):\n"))

    if max_commits_per_day > 9:
        max_commits_per_day = 9

    elif max_commits_per_day < 1:
        max_commits_per_day = 1

    settings_file.write(f"max_commits_per_day = {max_commits_per_day}\n")



    min_commits_per_day = int(input("\n\n\tEnter the minimum number of commits you would like per day (on days you roll a commit)(int 1-9):\n"))

    if min_commits_per_day > 9:
        min_commits_per_day = 9

    elif min_commits_per_day < 1:
        min_commits_per_day = 1

    settings_file.write(f"min_commits_per_day = {min_commits_per_day}\n")



    commit_chance = input(f"\n\n\tEnter your preferred commit chance(int 10-99)(Example: 75 - you will commit between {min_commits_per_day} and {max_commits_per_day} times on 75 percent of days and commit nothing on 25 percent of days):\n")

    if int(commit_chance) > 99:
        commit_chance = 99

    elif int(commit_chance) < 10:
        commit_chance = 10

    settings_file.write(f"commit_chance = {commit_chance}\n")

    settings_file.close()

    

    excluded_days_file = open(excluded_days_file_path, "a+")

    print('\n\n\t\tMonday - 0\n\t\tTuesday - 1\n\t\tWednesday - 2\n\t\tThursday - 3\n\t\tFriday - 4\n\t\tSaturday - 5\n\t\tSunday - 6')

    excluded_days = input("\n\n\tEnter corresponding numbers for any days you would like to never make commits on(Example - '4 5 6' - would exclude Friday through Sunday):\n")

    excluded_days_file.write(f"{excluded_days}")

    excluded_days_file.close()
    


    repo_link_file = open(git_repo_link_file_path, "a+")

    repo_link = input("\n\n\tCreate the private github repository and paste the repo link here (Should look like: 'https://github.com/<username>/<repo-name>.git'):\n")

    repo_link_file.write(f"{repo_link}")

    repo_link_file.close()


    

    # CODE FOR MAKING PROJECT DIRECTORY AND FILES

    print("\n...\n...\n...\n")

    print("Making folder for Git repo...")
    subprocess.run("cd git-real-green-folder && mkdir git-repo-for-commits", shell=True, check=True)
    
    print("Trying Linux/MacOS command to make file in repo folder...")

    try:
        subprocess.run("cd git-real-green-folder && touch git-repo-for-commits/main.js", shell=True, check=True)
    except:
        print("Linux command didn't work, trying windows command...")
        subprocess.run("cd git-real-green-folder && cd git-repo-for-commits && type nul > main.js", shell=True, check=True)


    subprocess.run("cd git-real-green-folder && cd git-repo-for-commits && git init", shell=True, check=True)
    subprocess.run(f"cd git-real-green-folder && cd git-repo-for-commits && git remote add origin {repo_link}", shell=True, check=True)
    subprocess.run("cd git-real-green-folder && cd git-repo-for-commits && git branch -M main", shell=True, check=True)


    startup()


def startup():
    settings_file = open(settings_file_path, "r")

    print("\n...\n...\n...\n")

    settings_file.seek(22, 0)
    max_commits_per_day = settings_file.readline().strip()
    print(f"Max commits per day setting: {max_commits_per_day}")

    settings_file.seek(46, 0)
    min_commits_per_day = settings_file.readline().strip()
    print(f"Min commits per day setting: {min_commits_per_day}")

    settings_file.seek(64, 0)
    commit_chance = settings_file.readline().strip()
    settings_file.seek(66, 0)
    commit_chance_windows = settings_file.readline().strip()
    print(f"Commit chance setting: {commit_chance}%")
    print(f"Commit chance for windows setting: {commit_chance_windows}%")

    settings_file.close()


    excluded_days_file = open(excluded_days_file_path, "r")

    excluded_days_file.seek(0, 0)
    excluded_days = excluded_days_file.readline().strip()
    print(f"Excluded days setting: {excluded_days}")

    excluded_days_file.close()

    
    git_repo_link_file = open(git_repo_link_file_path, "r")

    git_repo_link_file.seek(0, 0)
    repo_link = git_repo_link_file.readline().strip()
    print(f"Repository link setting: {repo_link}")

    git_repo_link_file.close()



    check_in_result = check_in()


    if check_in_result == False:
        print(f"Checking in again in {(interval / 60) / 60} hours...")
        time.sleep(interval)
        startup_mode_selector()
        
    elif check_in_result == True:
        

        print("\n...\n...\n...\n")
        print("Checking excluded days...")

        check_exclude_days(excluded_days)

        print("Trying roll with Linux commit chance...")
        try:
            commit_click_or_nah_roll = commit_click_or_nah(int(commit_chance))
        except:
            print("Linux commit chance failed, trying windows commit chance...")
            commit_click_or_nah_roll = commit_click_or_nah(int(commit_chance_windows))

        if commit_click_or_nah_roll == True:
            print("Rolling for number of commits today...")
            commits_for_today = roll_commits(int(min_commits_per_day), int(max_commits_per_day))
            print("\n**** IMAGINE DICE ROLL SOUNDS HERE ****")
            print(f"Rolled {commits_for_today} commits today...\n")

            

            print("Committing...")

            commit_for_me(repo_link, commits_for_today)


        
        else:
            print(f"Checking in again in {(interval / 60) / 60} hours...")
            time.sleep(interval)
            startup_mode_selector()


        

    
# check_in() returns False if commits are NOT needed today (They've already been done) and True if commits ARE needed today
def check_in():
    save_file = open(save_file_path, "r")
    save_file.seek(0, 0)
    last_check_in_date = save_file.readline()
    save_file.close()
    current_date = now.strftime("%m/%d/%Y")

    print(f"Last check in date: {last_check_in_date}")
    print(f"Current date: {current_date}")

    if last_check_in_date == now.strftime("%m/%d/%Y"):
        print("Already checked today...")
        return False
    else:
        print("Have not yet committed today...")
        print("Updating save file to current date...")
        current_date = now.strftime("%m/%d/%Y")
        save_file = open(save_file_path, "w+")
        save_file.seek(0, 0)
        save_file.write(current_date)
        return True

def check_exclude_days(excluded_days):
    excluded_days_list = list(excluded_days.split(" "))
    print(f"Excluded Days (list form): {excluded_days_list}")
    print(f"Today is {today_weekday}...")

    print("Comparing today weekday to excluded days list...")

    if today_weekday in excluded_days_list:
        print(f"Today is an excluded day, checking in again in {(interval / 60) / 60} hours...")
        time.sleep(interval)
        startup_mode_selector()
    else:
        print("Today is not an excluded day...")

def roll_commits(min, max):
    return random.randint(min, max)

def commit_click_or_nah(commit_chance_percentage):
    print("Rolling for commit chance...")
    chance_roll = random.randint(0, 100)
    if chance_roll > commit_chance_percentage:
        print("Unlucky...")
        return False
    else:
        print("Lucky...")
        return True

def commit_for_me(repo_link, commits_for_today):
    for commit in range(commits_for_today):
        # EDIT COMMIT FILE
        commit_js_file = open(commit_js_file_path, "a")
        commit_js_file.write(f"x\n")
        commit_js_file.close()

        subprocess.run("cd git-real-green-folder && cd git-repo-for-commits && git status", shell=True, check=True)
        subprocess.run("cd git-real-green-folder && cd git-repo-for-commits && git add -A", shell=True, check=True)
        subprocess.run("cd git-real-green-folder && cd git-repo-for-commits && git status", shell=True, check=True)
        subprocess.run(f'cd git-real-green-folder && cd git-repo-for-commits && git commit -m "Commit {commit + 1} for today"', shell=True, check=True)
        subprocess.run("cd git-real-green-folder && cd git-repo-for-commits && git status", shell=True, check=True)
        subprocess.run("cd git-real-green-folder && cd git-repo-for-commits && git push -u origin main", shell=True, check=True)

        print(f"Commit {commit + 1} pushed, waiting {commit_cooldown} seconds...")
        time.sleep(commit_cooldown)

    startup_mode_selector()


    
startup_mode_selector()