
def loop(channel=0):
    import random
    import string

    def loose_patterns():
        # return random.choice(["1--1--39", "1--1--59"])
        return ''.join([random.choice(string.digits) for i in range(0, 8)])

    pattern = random.choice([
        "0----0--",
        "1--1--1-",
        #"0-0---1-",
        #"0----1--",
        #"000--1--",
        #"0-0---1-",
        #"0--0--0-",
        #"1--1--1-",
        #"1-1-1-51",
        #"0-0---1-",
        #"9----5-5",
        #"1--0--1-",
        #"0----199",
        ]) if not bar(8) == 8 else loose_patterns()
    for char in pattern:
        if not char == '-':
            play(36 + int(char), 0.5, 0)
        sleep(0.5)

def loop(channel=2):
    import random
    if (bar(4) == 4):
        pattern = random.choice([
            "0------2",
            "0------3",
            "0-----4-",
            "0----111",
            ])
    else:
        pattern = "0-------"

    for char in pattern:
        if not char == '-':
            play(36 + int(char), 1)
        sleep(0.5)


def loop(channel=3):
    play(65 - 13, 1)
    sleep(16)


def loop(channel=3):
    currentChord = chord("Em")
    play(currentChord[tick() % len(currentChord) ], 0.07)
    sleep(0.25)

def loop(channel=1):
    for char in "10318591":
        if not char == '-':
            play(36 + int(char), 1, 1)
        sleep(1.5)

:luado vim.rpcnotify(48, 'code_change', 'now', table.concat(require('utils').get_current_function_name(), "\n"))
