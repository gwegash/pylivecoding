def loop(channel=0):
    pattern = ringMax(
            euclid(8,3),
            lambda x: 2 * euclid(16,3)(x),
            lambda x: 4 * euclid(31,1)(x-2),
            lambda x: 6 * euclid(63,1)(x-5),
            #lambda x: 3 * euclid(8,2)(x),
            )

    for i in range(0,8):
        hit = pattern(tick())
        if hit:
            play(hit - 1)
        sleep(0.5)

def loop(channel=2):
    pattern = ringMax(
            euclid(12,4),
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
    play(ring(0)(tick()), 16)
    sleep(16)

def loop(channel=8):
    pattern = euclid(8, 3)
    for i in range(0, 16):
        sleep(0.125)
        hit = pattern(tick())
        if(not hit):
            cc(6, (0.7 + nsin(time()/128)), 5)
        else:
            cc(6, 0, 5)

def loop(channel=3):
    chords = ring(
            ("Dmaj9", 4),
            ("Gmaj9", 3),
            ("Cmaj9", 4),
            ("Fmaj9", 3)
            )
    current = chord(*chords(bar(8)//2))
    for i in range(0,5):
        play(current(i*2) - 12, 8)
    sleep(8)
