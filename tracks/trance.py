def loop(channel=0):
    instrument(2)
    pattern = ringMax(
            euclid(8,3),
            lambda x: 6*euclid(63,2)(x-3),
            lambda x: 4*euclid(63,2)(x-6),
            lambda x: 1*euclid(15,2)(x-1),
            )
    for i in range(0,8):
        hit = pattern(tick())
        if(hit):
            play(-1 + hit)
        sleep(0.5)

def loop(channel=1):
    pattern = ringMax(
            euclid(8,3),
            lambda x: 3*euclid(8,2)(x),
            lambda x: 4*euclid(16,3)(x),
            lambda x: 8*euclid(16,3)(x - 4),
            )

    for i in range(0,8):
        hit = pattern(tick())
        if(hit):
            play(35 + hit)
        sleep(0.25)

def loop(channel=2):
    mod = (time()//16) % 2
    play(30 - mod, 8)
    sleep(16)
