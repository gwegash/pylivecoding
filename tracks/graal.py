
def loop(channel=0):
    instrument(2)
    pattern = ringMax(
            lambda x: 1*euclid(8,2)(x),
            lambda x: 2*euclid(8,3)(x-1),
            #lambda x: 3*euclid(8,5)(x),
            #lambda x: 2*euclid(8,5)(x)
            )
    for i in range(0,8):
        hit = pattern(i)
        if(hit):
            play(hit - 1 + 36)
        sleep(0.5)


def loop(channel=3):
    c = chord("Cmaj7")
    for i in range(0,5):
        play(c(i*1), 8)
    sleep(8)


