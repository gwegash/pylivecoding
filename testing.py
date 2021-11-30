
def loop(channel=1):
    for char in "1--1--1-":
        if not char == '-':
            play(35 + int(char), 0.3)
        sleep(0.5) 

def loop(channel=2):
    for char in "1--0-1-9":
        if not char == '-':
            play(36 + int(char))
        sleep(0.5) 



:luado vim.rpcnotify(48, 'code_change', 0, 'now', table.concat(require('utils').get_current_function_name(), "\n"))
