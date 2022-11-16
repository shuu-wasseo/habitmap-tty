import curses
import random
import time

s = ["ysy", "jhr", "ljw", "kcy", "kyy", "ksm", "knk", "gyb", "ked"]

stdscr = curses.initscr()
def main(stdscr):
    stdscr.clear()

    stdscr.addstr("tripleS", curses.A_REVERSE)
    stdscr.chgat(-1, curses.A_REVERSE) 

    stdscr.addstr(curses.LINES-1, 0, "s to req new s, q to quit")
    stdscr.chgat(curses.LINES-1, 0, curses.A_BOLD | curses.color_pair(2))
    stdscr.chgat(curses.LINES-1, 16, curses.A_BOLD | curses.color_pair(3))

    quotewin = curses.newwin(curses.LINES-2, curses.COLS, 1, 0)
    quotetextwin = quotewin.subwin(curses.LINES-6, curses.COLS-4, 3, 2)

    quotetextwin.addstr("press s to initiate s")

    stdscr.noutrefresh()
    quotewin.noutrefresh()
    curses.doupdate()

    while True:
        c = quotewin.getch()
        match chr(c).lower():
            case "s":
                for x in range(len(s)):
                    quotetextwin.move(quotetextwin.getyx()[0], 0)
                    quotetextwin.clrtoeol()
                    quotetextwin.addstr("retrieving s")
                    quotetextwin.refresh()
                    for y in range(3):
                        time.sleep(0.1)
                        quotetextwin.addstr(".")
                        quotetextwin.refresh()
                   
                    time.sleep(0.1)
                    quotetextwin.addstr(quotetextwin.getyx()[0], 0, f"S{x+1} {s[x]}\n")
                    quotetextwin.refresh()
            case "q":
                break

if curses.has_colors():
    curses.start_color()
        
curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_BLACK)

curses.init_color(1, 255, 0, 0)
curses.init_color(2, 0, 255, 0)
curses.init_color(3, 0, 0, 255)

curses.wrapper(main)
