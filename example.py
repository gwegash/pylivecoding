import time
import rtmidi
from threading import Thread
import sys

from queue import PriorityQueue
from fractions import Fraction
from nvim import run_nvim_listener

midiouts = []

#available_ports = midiout.get_ports()

play_queue = PriorityQueue()

code_map = {}
bpm = 170
canonical_start_time = time.time()

def sleep_until(until_time_beats: Fraction):
    timeInTheFuture = (until_time_beats*60.0)/bpm
    print(f'TimeWeWant: {timeInTheFuture}')
    time.sleep(max(timeInTheFuture - (time.time()-canonical_start_time), 0))

def beats_at_current_time():
    return Fraction((time.time()-canonical_start_time)*bpm/60)



def main():

    for i in range(0, 6):
        midiouts.append(rtmidi.MidiOut())
        midiouts[i].open_port(i)


    def note_on(note, time, channel, velocity=127):
        message = [0x90, note, velocity]  # channel 1, middle C, velocity 112
        play_queue.put((time, (channel, message)))


    def note_off(note, time, channel):
        message = [0x90, note, 0]  # channel 1, middle C, velocity 112
        play_queue.put((time, (channel, message)))





    # produces notes for a particular channel
    def producer_fn(channel_id, current_time):
        local_time = current_time

        ticker = 0

        def look():
            return ticker

        def tick():
            nonlocal ticker
            ticker += 1
            return ticker - 1

        def bar(desired_bar, of):
            return (int(local_time/4) % of) == desired_bar

        def play(note, duration=0.5, channel=channel_id):
            note_on(note, local_time, channel)
            note_off(note, local_time + Fraction(duration), channel)

        def sleep(t):
            nonlocal local_time
            local_time += Fraction(t)

        # main live_loop
        while True:
            time_at_beginning = local_time
            # runnable code here:
            if (channel_id, 'now') in code_map:
                the_code = code_map[(channel_id, 'now')]
                exec(the_code + "\nloop()", {'sleep': sleep, 'play': play, 'tick': tick, 'look': look})
                print(local_time)
            else:
                for i in range(0, 4):
                    print('nothing!')
                    play_queue.put((local_time, (-1, 0)))
                    sleep(1)

            code_snippet_length_beats = local_time - time_at_beginning

            sleep_until(local_time - code_snippet_length_beats)  # we want to run these things ideally a bar (snippet length) ahead of time


    producers = []
    for i in range(0, 6):
        producer = Thread(target=producer_fn, args=(i, Fraction(0),))
        producer.start()


    def consumer_fn():
        playhead_time = Fraction(0)

        time.sleep(0.1) # eww - work out a better way of doing this
        while True:
            #if play_queue.empty():
            #    next_time = playhead_time + Fraction(4)
            #    playhead_time = next_time
            #    print('sleeping 4 bars!')
            #    sleep_until(playhead_time)
            #else:
            (current_time, (channel, message)) = play_queue.get_nowait()
            if not channel == -1:
                midiouts[channel].send_message(message)
            playhead_time = current_time

                #if not play_queue.empty():
            (next_time, (channel, next_message)) = play_queue.get_nowait()
            play_queue.put_nowait((next_time, (channel, next_message)))
            sleep_until(next_time)


    consumer = Thread(target=consumer_fn)

    consumer.start()
    run_nvim_listener(code_map)


    producer.join()
    consumer.join()
    midiout.close_port()

if __name__ == "__main__":
    sys.exit(main() or 0)
