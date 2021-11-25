
def loop():
    for _ in range(0, 8):
        bd = 36
        sn = 38
        hh = 42
        tick()
        if look() % 32 == 16: play(sn)
        if look() % 32 == 0: play(bd)
        play(hh)
        sleep(0.125/2.0) 




:luado vim.rpcnotify(48, 'code_change', 0, 'now', table.concat(require('utils').get_current_function_name(), "\n"))
