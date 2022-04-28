def loop(channel=0):
    pattern = euclid(8,3)
    for i in range(0,8):
        if(pattern(i)):
            play(0)
            sleep(1.0)
