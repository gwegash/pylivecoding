
def loop(channel=0):
    import random
    import string
    import math
    instrument(2)

    def loose_patterns():
        # return random.choice(["1--1--39", "1--1--59"])
        return ''.join([random.choice(string.digits) for i in range(0, 8)])

    patterns = ring(
        "1-1--1-1",
        "1--1--1-",
        "000-10--",
        "1--1--1-",
        "0----0--",
        "1--1--1-",
        "0-0---1-",
        "0----1--",
        "000--1--",
        "0-0---1-",
        "0--0--0-",
        "1--1--1-",
        "1-1-1-51",
        "0--1--1-",
        "9----5-5",
        "0--1--1-",
        "0----199",
        )
    pattern = patterns("--------") if not bar(16) == 16 else "-----5--",
    #pattern = "--------"
    for char in pattern:
        if not char == '-':
            play(36 + int(char), 1.0)
        sleep(0.5)

def loop(channel=2):
    pattern = "0--0----"

    for char in pattern:
        if not char == '-':
            play(30 + 8 + int(char), 1)
        sleep(0.5)

def loop(channel=2):
    drone(10)
    sleep(0.5)

def loop(channel=4):
    c = chord("Ebsus4")
    play(c(tick), 0.2)
    sleep(0.5)

def loop(channel=2):
    import math
    instrument(1)
    play(39 + ring(0, -4, -2, -7, -9, 0)(tick()), 16, velocity=(0.5 + 0.4*math.sin(time())))
    sleep(16)

def loop(channel=4):
    c = chord("Ebsus4")
    play(c(tick()), 0.2)
    sleep(0.5)

def loop(channel=4):
    play(24, 16)
    sleep(16)


def loop(channel=4):
    import math
    for i in range(0, 16):
        sleep(0.25)
        cc(6, (tick() % 2 ), 3)
        cc(7, 0.5 + 0.2*math.sin(time()/16), 3)




def loop(channel=3):
    instrument(5)
    tick()
    play(ring(40, 42, 38, 40)(look()) + 3, 8)
    sleep(8)


def loop(channel=3):
    play(36 + 16 + 13, 1)
    sleep(16)


def loop(channel=3):
    currentChord = chord("Em")
    play(currentChord[tick() % len(currentChord) ], 0.07)
    sleep(0.5)

def loop(channel=1):
    instrument(3)
    for char in "10318591":
        if not char == '-':
            play(36 + int(char), 1, 1)
        sleep(1.5)

:luado vim.rpcnotify(48, 'code_change', 'now', table.concat(require('utils').get_current_function_name(), "\n"))
