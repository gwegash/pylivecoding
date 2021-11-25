import time
import rtmidi
from threading import Thread
import sys

from queue import PriorityQueue
from fractions import Fraction
from nvim import run_nvim_listener

midiout = rtmidi.MidiOut()
available_ports = midiout.get_ports()

play_queue = PriorityQueue()

code_map = {}
bpm = 120
canonical_start_time = time.time()

def sleep_until(until_time_beats: Fraction):
    timeInTheFuture = (until_time_beats*60.0)/bpm
    print(f'TimeWeWant: {timeInTheFuture}')
    time.sleep(max(timeInTheFuture - (time.time()-canonical_start_time), 0))

def beats_at_current_time():
    return Fraction((time.time()-canonical_start_time)*bpm/60)



def main():
    print(available_ports)

    if available_ports:
        midiout.open_port(0)
    else:
        midiout.open_virtual_port(available_ports[0])


    def note_on(note, time, velocity=127):
        message = [0x90, note, velocity]  # channel 1, middle C, velocity 112
        play_queue.put((time, message))


    def note_off(note, time):
        message = [0x90, note, 0]  # channel 1, middle C, velocity 112
        play_queue.put((time, message))





    # produces notes for a particular channel
    def producer_fn(current_time):
        local_time = current_time

        ticker = 0

        def look():
            return ticker

        def tick():
            nonlocal ticker
            ticker += 1
            return ticker - 1

        def play(note, duration=0.5):
            note_on(note, local_time)
            note_off(note, local_time + Fraction(duration))

        def sleep(t):
            nonlocal local_time
            local_time += Fraction(t)

        # main live_loop
        while True:
            time_at_beginning = local_time
            # runnable code here:
            if (0, 'now') in code_map:
                exec(code_map[(0, 'now')] + "\nloop()", {'sleep': sleep, 'play': play, 'tick': tick, 'look': look})
                print(local_time)
            else:
                for i in range(0, 4):
                    print('nothing!')
                    play_queue.put((local_time, 0))
                    sleep(1)

            code_snippet_length_beats = local_time - time_at_beginning

            sleep_until(local_time - code_snippet_length_beats)  # we want to run these things ideally a bar (snippet length) ahead of time


    producer = Thread(target=producer_fn, args=(Fraction(0),))


    def consumer_fn():
        playhead_time = Fraction(0)

        time.sleep(1.0) # eww - work out a better way of doing this
        while True:
            #if play_queue.empty():
            #    next_time = playhead_time + Fraction(4)
            #    playhead_time = next_time
            #    print('sleeping 4 bars!')
            #    sleep_until(playhead_time)
            #else:
            (current_time, message) = play_queue.get_nowait()
            if not message == 0:
                midiout.send_message(message)
            playhead_time = current_time

                #if not play_queue.empty():
            (next_time, next_message) = play_queue.get_nowait()
            play_queue.put_nowait((next_time, next_message))
            sleep_until(next_time)


    consumer = Thread(target=consumer_fn)

    producer.start()
    consumer.start()
    run_nvim_listener(code_map)


    producer.join()
    consumer.join()
    midiout.close_port()

if __name__ == "__main__":
    sys.exit(main() or 0)
