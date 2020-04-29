from colorama import Fore, init

import numpy as np

import sys
import random
import string

LETTERS = string.ascii_letters + string.digits + string.punctuation
RMAP = [(1000, 'M'), (900, 'CM'), (500, 'D'), (400, 'CD'), (100, 'C'), (90, 'XC'), (50, 'L'), (40, 'XL'), (10, 'X'),
        (9, 'IX'), (5, 'V'), (4, 'IV'), (1, 'I')]
rot = {}
next = ''


def main():
    rot = make()

    # main loop
    while True:
        w = input(">>>")
        k = w.split(" ", 1)
        if k[0] == "-e":
            print(Fore.BLUE + cipher(rot, k[1], "e"))

        elif k[0] == "-d":
            print(Fore.BLUE + cipher(rot, k[1], "d"))

        elif k[0] == "-s":
            save_config(rot, k[1])

        elif k[0] == "-l":
            rot = load_config(k[1])

        elif k[0] == "-h":
            print_help()

        elif k[0] == "-q":
            sys.exit(0)

        else:
            print(Fore.RED + "Unknow parameter")
            print_help()


def n2r(n):
    r = []
    for v, s in RMAP:
        while n >= v:
            r.append(s)
            n -= v
    return ''.join(r)


def generate_permutation(length=len(LETTERS)):
    let = LETTERS
    return ''.join(random.choice(let) for i in range(length))


def save_config(dic, name):
    np.save(name + '.npy', dic)
    print(Fore.LIGHTYELLOW_EX + "Configuration Saved")


def load_config(name):
    try:
        dic = np.load(name + '.npy', allow_pickle=True).item()
        print(Fore.LIGHTYELLOW_EX + "Configuration Loaded")
        return dic

    except:
        print(Fore.RED + "No Config Named " + name)
        dic = make()
        return dic


def print_help():
    print(Fore.RED +
          "-e [string]: encrypt\n"
          "-d [encrypted string]: decrypt\n"
          "-s [config name]: save the current config\n"
          "-l [config name] : load a config\n"
          "-h : show help\n"
          "-q : exit")


def cipher(dic, msg, mode):
    if mode == "e":
        encode = ''
        for char in msg:
            q = char
            for rot in dic:
                q = dic[rot].permute(char=q)
            encode += q
            for rot in dic:
                dic[rot].position = 0
        return encode

    elif mode == "d":
        decode = ''
        for char in msg:
            q = char
            for rot in dic:
                q = dic[rot].reverse(q)
            decode += q
            for rot in dic:
                dic[rot].position = 0
        return decode




def make():
    global rot

    i = input("Type \"-l [config name]\" to load a config else press enter to create a new config: ")

    if i.startswith("-l"):
        o = i.split()
        rot = load_config(o[1])

    else:
        inp = input('How many rotors do you need:')
        for x in range(1, int(inp) + 1):
            rot[x] = Rotors(n2r(x), generate_permutation())
            print(Fore.GREEN + rot[x].name + ':' + rot[x].permutation)
    return rot


class Rotors(object):

    def __init__(self, name, permutation, position=0):
        super(Rotors, self).__init__()
        self.name = name
        self.permutation = permutation
        self.position = position

    def turn(self):
        self.position += 1

    def permute(self, char=None):
        if not char is None:
            pos = self.position
            perm = list(self.permutation)
            letter = perm[pos]
            new = ord(char) + ord(letter)
            new_letter = chr(new)
            self.turn()
            if self.position == len(LETTERS):
                self.position = 0
            return new_letter

    def reverse(self, char=None):

        if not char is None:
            pos = self.position
            perm = list(self.permutation)
            letter = perm[pos]
            old = ord(char) - ord(letter)
            old_letter = chr(old)
            self.turn()
            if self.position == len(LETTERS):
                self.position = 0
            return old_letter


if __name__ == '__main__':
    init(autoreset=True)
    main()
