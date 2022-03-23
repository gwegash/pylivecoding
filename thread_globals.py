from fractions import Fraction
from queue import PriorityQueue
import time
import logging

def initialise():

    logging.basicConfig(filename='debug.log', level=logging.DEBUG, force=True)
    global playhead_time
    playhead_time = Fraction(0) # Should only be updated by the consumer thread.
    global play_queue
    play_queue = PriorityQueue() # should only (really) be added to by the producer threads consumed by consumer :)
    global bpm
    bpm = 170
    global canonical_start_time
    canonical_start_time = time.time()

