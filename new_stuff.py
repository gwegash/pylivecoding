def loop(channel=0):
    pattern = ringMax(
            euclid(8,3),
            lambda x: 3 * euclid(9,2)(x),
            lambda x: 4 * euclid(31,1)(x-2),
            lambda x: 5 * euclid(63,1)(x-5),
            )

    for i in range(0,8):
        hit = pattern(tick())
        if hit:
            play(35 + hit)
        sleep(0.5)

def loop(channel=3):
    for i in range(0,8):
        cc(8, nsaw(time()/6), 2)
        sleep(0.125)
        cc(8, 0, 2)
        sleep(0.125)

