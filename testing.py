
def loop(channel=0):
    import random
    import string

    def loose_patterns():
        # return random.choice(["1--1--39", "1--1--59"])
        return ''.join([random.choice(string.digits) for i in range(0, 8)])

    pattern = random.choice([
        "1--1-1-1",
        "0--1--1-",
        "1--11-2-",
        "1-91--00",
        ]) if not bar(8) == 8 else loose_patterns()
    for char in pattern:
        if not char == '-':
            play(36 + int(char), 0.5, 0)
        sleep(0.5)

def loop(channel=4):
    play(65, 1)
    sleep(32)

def loop(channel=3):
    currentChord = chord("Em")
    #play(currentChord[tick() % len(currentChord) ], 0.07)
    sleep(0.25)

def loop(channel=1):
    for char in "10318591":
        if not char == '-':
            play(36 + int(char), 1, 1)
        sleep(1.5)

:luado vim.rpcnotify(48, 'code_change', 'now', table.concat(require('utils').get_current_function_name(), "\n"))
