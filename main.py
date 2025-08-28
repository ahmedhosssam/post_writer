import urllib.request
import subprocess
import platform
import json
import time
import os
import re
import sys

import pyautogui

def main():
    pyautogui.FAILSAFE = True
    pyautogui.PAUSE = 0.1

    url = "https://jsonplaceholder.typicode.com/posts"
    posts_count = 10
    base_dir = os.path.expanduser("~/tjm-project")
    post_dirs = []

    os.makedirs(base_dir, exist_ok=True)

    for i in range(posts_count):
        post_path = os.path.join(base_dir, f"post_{i+1}.txt")
        with open(post_path, "w") as f:
            f.write("")

        post_dirs.append(post_path)

    try:
        subprocess.Popen(['gedit'])
        print("Opening gedit...")
    except FileNotFoundError:
        print("Gedit is not found")
        sys.exit(1)

    if 'gnome-shell' in subprocess.check_output(["ps", "-e"], text=True):
        time.sleep(5)
    else:
        # I had to do 30 seconds sleep because Gnome stuff is very slow on my system,
        # because I don't run on Gnome so there are some bugs on my system.
        # But on regular Gnome it should open in a second.
        time.sleep(30)

    for i in range(posts_count):
        try:
            if platform.system() == 'Linux':
                cur_window = subprocess.check_output(["xdotool", "getactivewindow", "getwindowname"]).decode("utf-8").strip()

                if not re.search("gedit", cur_window.lower()):
                    raise RuntimeError("Expected Gedit to be the active window, but found: " + cur_window)
            else:
                raise RuntimeError("This script only works on Linux right now.")

            url_post = url+'/'+str(i+1)
            post = {}
            subprocess.Popen(['gedit', post_dirs[i]])

            with urllib.request.urlopen(url_post) as response:
                data = response.read().decode("utf-8")
                parsed = json.loads(data)
                post = parsed

            title = post["title"]
            body = post["body"]

            expected_content = "Title: " + title + "\nBody: \n" + body + "\n"

            pyautogui.write("Title: ", interval=0.02)
            pyautogui.write(title, interval=0.02)
            pyautogui.press('enter')

            pyautogui.write("Body: ", interval=0.02)
            pyautogui.press('enter')
            pyautogui.write(body, interval=0.02)

            pyautogui.hotkey('ctrl', 's')
            time.sleep(0.5)

            with open(post_dirs[i], "r") as f:
                final_content = f.read()
            
            if final_content != expected_content:
                raise RuntimeError(f"Something went wrong with post number {i+1}, please try again")

            pyautogui.hotkey('ctrl', 'w')
        except pyautogui.FailSafeException:
            print("FailSafe triggered! Mouse moved outside the window of Gedit.")

    pyautogui.hotkey('ctrl', 'w') # Close Gedit

    print(f"Finished writing {posts_count} posts successfully.")

if __name__ == "__main__":
    main()
