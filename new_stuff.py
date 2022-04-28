def loop(channel=0):
    pattern = ringMax(
            #lambda x: 3 * euclid(9,2)(x),
            euclid(8,3),
            lambda x: 2 * euclid(12,2)(x),
            lambda x: 4 * euclid(31,1)(x-2),
            lambda x: 5 * euclid(63,1)(x-5),
            )

    for i in range(0,8):
        hit = pattern(tick())
        if hit:
            play(hit - 1)
        sleep(0.5)

def loop(channel=2):
    pattern = ringMax(
            euclid(8,3),
            #lambda x: 2 * euclid(12,2)(x),
            lambda x: 1 * euclid(31,1)(x-2),
            lambda x: 2 * euclid(63,1)(x-5),
            )
    for i in range(0,8):
        hit = pattern(tick())
        if hit:
            play(chord("C5", 3)(hit-1), 2)
        sleep(0.5)
    sleep(4)


def loop(channel=5):
    play(ring(0,1,2,3)(tick()))
    sleep(16)

def loop(channel=3):
    chords = ring(("Dmaj9", 4), ("Gmaj9", 3), ("Cmaj9", 4), ("Fmaj9", 3))
    current = chord(*chords(bar(8)//2))
    for i in range(0,5):
        play(current(i*2) - 12, 8)
    sleep(8)
