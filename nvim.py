from pynvim import attach
from example import do_code_change

nvim = attach('socket',  path='/tmp/nvim')

nvim.command(f'echo "hello world" {nvim.channel_id}')

nvim.subscribe('code_change')


def do_param_change():
    return False


while True:
    [_, method, args] = nvim.next_message()

    if method == 'code_change':
        do_code_change(*args)
    elif method == 'param_change':
        do_param_change(*args)

