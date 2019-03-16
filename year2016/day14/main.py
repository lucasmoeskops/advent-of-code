from collections import deque
from hashlib import md5
from operator import itemgetter
from sys import argv
from typing import List, Tuple, Deque, Dict, Optional


class KeyGenerator:
    def __init__(self, salt: str, stretch: int = 0):
        self.index = 0
        self.salt: str = salt
        self.stretch: int = stretch
        self.used_indices: List[int] = []

    def generate(self) -> Tuple[str]:
        look_ahead = 1000
        hashes_needed = 64
        usable_hashes: Dict[int, str] = {}
        salt = self.salt.encode('utf-8')
        index = 0
        check_list: Deque[Optional[Tuple[int, str, str]]] = deque()
        while hashes_needed > 0 or len(check_list):
            while check_list and index + 1 > check_list[0][0]:
                check_list.popleft()
            h = md5(salt + str(index).encode('utf-8')).hexdigest()
            for i in range(self.stretch):
                h = md5(h.encode('utf-8')).hexdigest()
            for n, (index_limit, check, g) in enumerate(check_list):
                if check in h:
                    usable_hashes[index_limit - look_ahead] = g
                    hashes_needed -= 1
                    check_list[n] = None
            while None in check_list:
                check_list.remove(None)
            if hashes_needed > 0:
                for i in range(30):
                    if h[i] == h[i + 1] == h[i + 2]:
                        check_list.append((index + look_ahead, h[i] * 5, h))
                        break
            index += 1
        self.used_indices = sorted(usable_hashes.keys())[:64]
        return tuple(
            map(itemgetter(1),
                sorted(usable_hashes.items(), key=itemgetter(0))))[:64]


def solve(salt='ngcjuoqr'):
    key_generator = KeyGenerator(salt)
    key_generator.generate()
    key_generator2 = KeyGenerator(salt, 2016)
    key_generator2.generate()

    part1 = key_generator.used_indices[-1]
    part2 = key_generator2.used_indices[-1]

    return part1, part2


if __name__ == '__main__':
    kwargs = {}

    stdout = '-s' in argv and (argv.remove('-s') or True)

    if len(argv) > 1:
        kwargs['salt'] = argv[1]

    solution = solve(**kwargs)

    if stdout:
        print(solution)
    else:
        open('output.txt', 'w').write(str(solution))


