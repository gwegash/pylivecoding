def loop(channel=0):
    pattern = ringMax(
            euclid(8,3),
            lambda x: 2*euclid(12,2)(x),
            #lambda x: 3*euclid(8,2)(x - 2)
            )

    for i in range(0,8):
        hit = pattern(tick())
        if(hit):
            play(hit - 1)
        sleep(0.5)


