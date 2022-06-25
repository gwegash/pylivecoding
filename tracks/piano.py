def loop(channel=1):
    ch = "Cmaj7" if bar(64) > 32 else "Fmaj7"
    c = chord(ch)
    for i in range(0,5):
        play(c(i*2) - 12, 8, 0.8)
        sleep(2)

def loop(channel=2):
    ch = "Cmaj9" if bar(64) > 32 else "Fmaj9"
    c = chord(ch)
    for i in range(0,5):
        play(c(i*2), 8, 1, channel=1)
        sleep(1)

def loop(channel=3):
    ch = "Cmaj9" if bar(64) > 32 else "Fmaj9"
    c = chord(ch)
    play(c(randrange(0,8)) + 12, 8, 0.8, channel=1)
    sleep(3)
