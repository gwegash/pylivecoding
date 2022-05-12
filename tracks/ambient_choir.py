def loop(channel=3):
    lol
    instrument(6)
    c = chord(ring("Fmaj9")(bar(64)//2))
    for i in range(0, ring(5,6,7)(tick())):
        play(c(i*ring(2)(look()) - 12 + ring(0,1,2,3)(look())), 32)
    sleep(8)

def loop(channel=4):
    c = chord("Fmaj7")
    for i in range(0,9):
        play(c(ring(*range(0,7))(-i)) + 12, 0.1)
        sleep(0.5)

