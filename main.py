import time
import curses
from curses import wrapper
import random


def start(screen):
    screen.clear()  # Clear screen
    screen.addstr("Welcome to Typing Speed Test!")  # Print a message
    screen.addstr("\nPress any key to begin")  # Print a message
    screen.refresh()  # refresh screen
    screen.getkey()  # Wait for any key to be pressed


def display_text(screen, target, current, wpm=0):
    screen.addstr(target)
    screen.addstr(1, 0, f"WPM: {wpm}")

    for i, j in enumerate(current):
        color = curses.color_pair(1) if j == target[i] else curses.color_pair(2)
        screen.addstr(0, i, j, color)


def load_text():
    with open("sentence.txt", "r") as f:
        lines = f.readlines()
        return random.choice(lines).strip()


def wpm_test(screen):
    target_text = load_text()
    current_text = []
    wpm = 0
    start_time = time.time()
    screen.nodelay(True)

    while True:
        time_elapsed = max(time.time() - start_time, 1)
        wpm = round((len(current_text) / (time_elapsed / 60)) / 5)
        screen.clear()
        display_text(screen, target_text, current_text, wpm)
        screen.refresh()

        if "".join(current_text) == target_text:
            screen.nodelay(False)
            break

        try:
            key = screen.getkey()
        except:
            continue

        if ord(key) == 27:
            break
        if key in ("KEY_BACKSPACE", "\b", "\x7f"):
            if len(current_text) > 0:
                current_text.pop()
        elif len(current_text) < len(target_text):
            current_text.append(key)


def main(screen):
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    start(screen)
    while True:
        wpm_test(screen)
        screen.addstr(2, 0, "You completed the test")
        screen.addstr("\nPress any key to test again")
        screen.addstr("\nPress ESC to exit")
        screen.refresh()
        key = screen.getkey()
        if ord(key) == 27:
            break


wrapper(main)
