from pynvim import attach
from threading import Thread
import re

def do_code_change(code_map, when, code):
    channel = parse_channel(code)
    code_map[(channel, when)] = code
    print(code_map)
    return False

def parse_channel(buffer):
    match = re.search("channel\s?=\s?[0-9]*", buffer).group(0)
    return int(match.split("=")[1])


def run_nvim_listener(code_map):
    nvim = attach('socket',  path='/tmp/nvim')

    nvim.command(f'let g:livecode_channel = {nvim.channel_id}')

    nvim.subscribe('code_change')

    def nvim_loop():
        while True:
            [_, method, args] = nvim.next_message()

            if method == 'code_change':
                do_code_change(code_map, *args)

    listener = Thread(target=nvim_loop)

    listener.start()
