import time
import rtmidi
from threading import Thread
import sys

from queue import PriorityQueue
from fractions import Fraction

midiout = rtmidi.MidiOut()
available_ports = midiout.get_ports()

play_queue = PriorityQueue()

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





    def producer_fn(current_time):
        notes = [(40, 2), (41, 2.5), (43, 2)]

        local_time = current_time
        for _ in range (0, 100):
            note = 36
            duration = 1
            note_on(note, local_time)
            note_off(note, local_time + Fraction(duration))

            local_time = local_time + Fraction(duration)

        local_time = current_time + 0.5
        for _ in range (0, 100):
            note = 38
            duration = 1
            note_on(note, local_time)
            note_off(note, local_time + Fraction(duration))

            local_time = local_time + Fraction(duration)

        local_time = current_time 
        for _ in range (0, 400):
            note = 42
            duration = 0.125/2.0 
            note_on(note, local_time)
            note_off(note, local_time + Fraction(duration))

            local_time = local_time + Fraction(duration)

        for (note, duration) in notes:

            note_on(note, current_time)
            note_off(note, current_time + Fraction(duration))

            current_time = current_time + Fraction(duration)


    producer = Thread(target=producer_fn, args=(Fraction(0),))


    def consumer_fn():
        playhead_time = Fraction(0)
        bpm = 100.0

        time.sleep(1)

        thread_start_time_ms = time.time()
        while not play_queue.empty():
            (current_time, message) = play_queue.get_nowait()
            midiout.send_message(message)
            playhead_time = current_time

            (next_time, next_message) = play_queue.get_nowait()
            play_queue.put_nowait((next_time, next_message))
            timeSinceStart = time.time()-thread_start_time_ms
            timeInTheFuture = (next_time*60.0)/bpm
            print(f'TimeSinceStart: {timeSinceStart}')
            print(f'TimeWeWant: {timeInTheFuture}')
            time.sleep(max(timeInTheFuture - (time.time()-thread_start_time_ms), 0))


    consumer = Thread(target=consumer_fn)

    producer.start()
    consumer.start()


    producer.join()
    consumer.join()
    midiout.close_port()

if __name__ == "__main__":
    sys.exit(main() or 0)
