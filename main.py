import subprocess
import curses
import json


with open("data.json", "r") as file:
    data = json.load(file)["packages"]

def update():
    with open("data.json", "w") as file:
        json.dump({"packages": data}, file, indent=4)



def initalizeCommand():
    for package in data:
        wingetCommand = package.get("winget")

        if package["selected"]:
            subprocess.run(wingetCommand,shell=True)



def main(stdscr):
    curses.curs_set(0)
    finished = False
    selected = 0

    while not finished:
        stdscr.clear()

        try:
            max_y, max_x = stdscr.getmaxyx()

            for i, winget in enumerate(data):
                if i == selected:
                    stdscr.addstr(f"-> ")
                else:
                    stdscr.addstr(f"   ")

                if winget["selected"]:
                    stdscr.addstr("[x] ")
                else:
                    stdscr.addstr("[ ] ")

                label = winget['label'][:max_x - 10]
                stdscr.addstr(f"{label}\n")

        except curses.error as e:
            stdscr.addstr(f"Error: {e}")

        stdscr.refresh()

        key = stdscr.getch()

        if key == curses.KEY_UP:
            selected = max(0, selected - 1)
        elif key == curses.KEY_DOWN:
            selected = min(len(data) - 1, selected + 1)
        elif key == 10: 
            finished = True
            update()

            stdscr.clear()
            stdscr.refresh()


        elif key == 32:  # Boşluk tuşu
            data[selected]["selected"] = not data[selected]["selected"]

    curses.endwin()
    initalizeCommand()

if __name__ == "__main__":
    curses.wrapper(main)
    
