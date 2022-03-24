import sys,os
import curses

from fractions import Fraction

import thread_globals
import time
import pretty_midi

TIME_RESOLUTION = Fraction(1, 8)
SHOW_NOTE_OFFS = False

def sleep_until(until_time_beats: Fraction):
    timeInTheFuture = (until_time_beats*60.0)/thread_globals.bpm
    time.sleep(max(timeInTheFuture - (time.time()-thread_globals.canonical_start_time), 0))

def isNoteOn(message):
    return message[2] > 0

def draw_menu(stdscr):
    stdscr.nodelay(True)
    ui_current_time = Fraction(0) # TODO probably set this to global time
    time.sleep(0.1)

    def drawChannel(track_id, height, width):
        channelMessages = [(time, message) for (time, (channel, message)) in thread_globals.play_queue.queue if channel==track_id]
        y_coordMessages = [((time-ui_current_time)//TIME_RESOLUTION, message) for (time, message) in channelMessages]
        #draw background
        for j in range(0, height):
            channelWidth = width//8 # take off one for the line
            # turning on attributes for title


            channelString = "-"*(channelWidth - 1)

            # rendering title
            stdscr.addstr(j, track_id*(channelWidth), channelString)

            trackSeperatorLocation = (track_id + 1)*(channelWidth) - 1
            if(trackSeperatorLocation < width - 1):
                stdscr.addstr(j, trackSeperatorLocation, "|")

        #TODO current assumption is no chords only single notes
        for (yCoord, message) in y_coordMessages:
            lineContent = ""

            if(yCoord < height):
                lineContent = pretty_midi.note_number_to_name(message[1])[:channelWidth - 1]
                if(isNoteOn(message)):
                    stdscr.attron(curses.color_pair(2))
                    stdscr.attron(curses.A_BOLD)
                    # rendering title
                    stdscr.addstr(yCoord, track_id*(channelWidth), lineContent)

                    stdscr.attroff(curses.color_pair(2))
                    stdscr.attroff(curses.A_BOLD)
                elif SHOW_NOTE_OFFS: #TODO properly
                    stdscr.addstr(yCoord, track_id*(channelWidth), lineContent)




    k = 0
    cursor_x = 0
    cursor_y = 0

    # Clear and refresh the screen for a blank canvas
    #stdscr.clear()
    #stdscr.refresh()


    # Start colors in curses
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)

    # Loop where k is the last character pressed
    while (k != ord('q')):

        # Initialization
        #stdscr.clear()
        height, width = stdscr.getmaxyx()

        #if k == ord('j'):
        #    cursor_y = cursor_y + 1
        #elif k == ord('k'):
        #    cursor_y = cursor_y - 1
        #elif k == ord('l'):
        #    cursor_x = cursor_x + 1
        #elif k == ord('h'):
        #    cursor_x = cursor_x - 1

        cursor_x = max(0, cursor_x)
        cursor_x = min(width-1, cursor_x)

        cursor_y = max(0, cursor_y)
        cursor_y = min(height-1, cursor_y)

        statusbarstr = "Press 'q' to exit | STATUS BAR | Pos: {}, {}".format(cursor_x, cursor_y)
        if k == 0:
            keystr = "No key press detected..."[:width-1]

        ## draw channels
        for i in range(0,8):
            drawChannel(i, height - 2, width)

        # draw 16 bar progress
        progressWidth = width // 3
        progress16 = progressWidth * ((ui_current_time / 4) % 16) // 16
        progressStr = "#"*progress16 + (progressWidth-progress16 - 1)*" " + "|"
        stdscr.addstr(height-2, 0, progressStr)

        # Render status bar
        stdscr.attron(curses.color_pair(3))
        stdscr.addstr(height-1, 0, statusbarstr)
        stdscr.addstr(height-1, len(statusbarstr), " " * (width - len(statusbarstr) - 1))
        stdscr.attroff(curses.color_pair(3))

        stdscr.move(cursor_y, cursor_x)

        # Refresh the screen
        stdscr.refresh()

        # Wait for next input
        k = stdscr.getch()
        ui_current_time = ui_current_time + TIME_RESOLUTION
        sleep_until(ui_current_time)

def run_gui():
    curses.wrapper(draw_menu)
    curses.wrapper(draw_menu)

if __name__ == "__main__":
    run_gui()
