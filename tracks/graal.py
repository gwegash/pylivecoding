def loop(channel=0):
    instrument(2)
    pattern = ringMax(
            euclid(8,3),
            lambda x: 3*euclid(8,5)(x),
            lambda x: 2*euclid(8,5)(x)
            )
    for i in range(0,8):
        hit = pattern(i)
        if(hit):
            play(hit - 1)
        sleep(0.5)
