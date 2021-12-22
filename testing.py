
def loop(channel=1):
    import random
    import string

    def loose_patterns():
        # return random.choice(["1--1--39", "1--1--59"])
        return ''.join([random.choice(string.digits) for i in range(0, 8)])

    pattern = random.choice(["1--1--1-", "2--1--1-"]) if not bar(8, 8) else loose_patterns()
    for char in pattern:
        if not char == '-':
            play(35 + int(char), 0.3, 1)
        sleep(0.5) 

def loop(channel=4):
    for char in "10318591":
        if not char == '-':
            play(36 + int(char), 1, 0)
        sleep(0.5) 

def loop(channel=4):
    for char in "10318591":
        if not char == '-':
            play(36 + int(char), 1, 0)
        sleep(0.5) 

:luado vim.rpcnotify(48, 'code_change', 'now', table.concat(require('utils').get_current_function_name(), "\n"))
