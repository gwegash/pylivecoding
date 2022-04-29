import time
import rtmidi

from rtmidi.midiconstants import CONTROL_CHANGE

from threading import Thread
import sys

from fractions import Fraction
from nvim import run_nvim_listener

import pretty_midi
import thread_globals
from pychord import Chord
import ipdb

from math import sin, pi

from euclid import euclid as euclidArr

import logging

from pycurses import run_gui


midiouts = []

#available_ports = midiout.get_ports()

code_map = {}

def normalizeMap(x):
    return min(max(int(x*127), 0), 127)

def clampMidi(x):
    return min(max(x, 0), 127)

def infiniteChord(chordArray):
    return lambda i: chordArray[i % len(chordArray)] + 12*(i//len(chordArray))

def sleep_until(until_time_beats: Fraction):
    timeInTheFuture = (until_time_beats*60.0)/thread_globals.bpm
    #print(f'TimeWeWant: {timeInTheFuture}')
    time.sleep(max(timeInTheFuture - (time.time()-thread_globals.canonical_start_time), 0))

def beats_at_current_time():
    return Fraction((time.time()-thread_globals.canonical_start_time)*thread_globals.bpm/60)

def get_bar_modulo(modulo, time):
    return (int(time/4) % modulo) + 1

def ring(*args):
    return lambda x: args[x % len(args)]

def main():
    thread_globals.initialise()
    midiout = rtmidi.MidiOut()

    for index in enumerate(midiout.get_ports()):
        print(f'{index}: port')

    portIdx = int(input("Select port\n"))
    midiout.open_port(portIdx) # hack, find a better way. on startup wait for input on a list of midi options

    def note_on(note, time, channel, velocity=127):
        message = [0x90 | channel, note, velocity]
        thread_globals.play_queue.put((time, (channel, message)))

    def note_off(note, time, channel):
        message = [0x90 | channel, note, 0]
        thread_globals.play_queue.put((time, (channel, message)))

    def midi_cc(cc, value, time, channel):
        message = [CONTROL_CHANGE | channel, cc, value]
        thread_globals.play_queue.put((time, (channel, message)))

    def program_change(program_int, time, channel):
        midi_cc(16, program_int, time, channel) #we'll use the General purpose cc
    def mute_channel(time, channel):
        midi_cc(120, 0, time, channel)

    def euclid(beats, hits):
        return ring(*euclidArr(beats, hits))

    def nsin(x):
        return 0.5*sin(x*(2*pi)) + 0.5

    def nsaw(x):
        return (x % 1)

    # produces notes for a particular channel
    def producer_fn(channel_id, current_time):
        local_time = current_time
        drones = {}
        current_instrument = None

        ticker = 0

        def instrument(instrument_int):
            nonlocal current_instrument
            if (current_instrument != instrument_int):
                program_change(instrument_int, local_time, channel_id)

            current_instrument = instrument_int

            return ticker

        def look():
            return ticker

        def tick():
            nonlocal ticker
            ticker += 1
            return ticker - 1

        def bar(of): # which bar (of a on 'of' length section are we?)
            return (int(local_time/4) % of) + 1

        def play(note, duration=0.5, velocity=1, channel=channel_id):

            note_on(note, local_time, channel, normalizeMap(velocity))
            note_off(note, local_time + Fraction(duration), channel)

        def sleep(t):
            ##TODO zero check
            nonlocal local_time
            local_time += Fraction(t)

        def cc(cc, v, channel=channel_id):
            midi_cc(cc, normalizeMap(v), local_time, channel)

        def time():
            return local_time

        def ringMax(*args):
            return lambda x: max(*[(arg(x) for arg in args)])

        def drone(note, channel=channel_id):
            if (note, channel) in drones:
                drones[(note, channel)] += 1
            else:
                drones[(note, channel)] = 1
                note_on(note, local_time, channel)

        def diatonic(scale="Cmaj", note=1, quality=""):
            chordObject = Chord.from_note_index(note=note, scale=scale, quality=quality, diatonic=True)
            chordArray = [pretty_midi.note_name_to_number(note_name) for note_name in chordObject.components_with_pitch(root_pitch=4)]
            return infiniteChord(chordArray)

        def chord(chord_name, root_pitch=4):
            chordObject = Chord(chord_name)
            chordArray = [pretty_midi.note_name_to_number(note_name) for note_name in chordObject.components_with_pitch(root_pitch=root_pitch)]
            return infiniteChord(chordArray)

        def cleanup_drones(time_at_start):
            for ((note, channel), val) in list(drones.items()):
                if val <= 0:
                    note_off(note, time_at_start, channel)
                    del drones[(note, channel)]
                else:
                    drones[(note, channel)] = val - 1

        # main live_loop
        while True:
            time_at_beginning = local_time

            # runnable code here:
            if (channel_id, 'now') in code_map:
                the_code = code_map[(channel_id, 'now')]
                try:
                    exec(the_code + "\nloop()", {'nsaw' : nsaw, 'nsin' : nsin, 'ringMax' : ringMax, 'euclid' : euclid, 'ring': ring, 'cc': cc, 'diatonic': diatonic, 'sleep': sleep, 'time': time, 'chord': chord, 'play': play, 'tick': tick, 'look': look, 'bar': bar, 'drone': drone, 'instrument' : instrument})
                    #print(local_time)
                except Exception as e:
                    logging.exception(f'Error evaluating channel {channel_id}\n{str(e)}')
                    code_map.pop((channel_id, 'now'))
                    sleep(4 - (local_time % 4))
            else:
                for i in range(0, 4):
                    #print('nothing!')
                    thread_globals.play_queue.put((local_time, (-1, -1)))
                    sleep(1)


            code_snippet_length_beats = local_time - time_at_beginning

            if(code_snippet_length_beats/4 >= 16 or get_bar_modulo(16, local_time) < get_bar_modulo(16, time_at_beginning)): # we must have moved over a 16 bar boundary. Therefore check if the code needs changing & reset threads local time to the next (respective to the time_at_beginning).
                #ipdb.set_trace()
                if ((channel_id, '16') in code_map):
                    code_map[(channel_id, 'now')] = code_map[(channel_id, '16')]
                    code_map.pop((channel_id, '16'))
                    local_time = 4*(int(time_at_beginning/4) + 16 - (int(time_at_beginning/4) % 16)) # go back to the last 16 bar line
                    code_snippet_length_beats = local_time - time_at_beginning # recalculate

            cleanup_drones(time_at_beginning)

            sleep_until(local_time - code_snippet_length_beats)  # we want to run these things ideally a bar (snippet length) ahead of time


    producers = []
    for i in range(0, 8 + 1): #we'd like an additional one for cc sends
        producer = Thread(target=producer_fn, args=(i, Fraction(0),))
        producer.setDaemon(True)
        producer.start()


    def consumer_fn():
        #thread_globals.playhead_time = Fraction(0) # TODO might need this probably not

        time.sleep(0.1) # eww - work out a better way of doing this
        while True:
            #if play_queue.empty():
            #    next_time = playhead_time + Fraction(4)
            #    playhead_time = next_time
            #    print('sleeping 4 bars!')
            #    sleep_until(playhead_time)
            #else:
            (current_time, (channel, message)) = thread_globals.play_queue.get_nowait()
            if not channel == -1:
                midiout.send_message(message)
            thread_globals.playhead_time = current_time

                #if not play_queue.empty():
            (next_time, (channel, next_message)) = thread_globals.play_queue.get_nowait()
            thread_globals.play_queue.put_nowait((next_time, (channel, next_message)))
            sleep_until(next_time)


    consumer = Thread(target=consumer_fn)
    consumer.setDaemon(True)

    consumer.start()
    run_nvim_listener(code_map)

    guiThread = Thread(target=run_gui)
    guiThread.setDaemon(True)
    guiThread.start()

    guiThread.join()
    producer.join()
    consumer.join()
    midiout.close_port()

if __name__ == "__main__":
    sys.exit(main() or 0)
