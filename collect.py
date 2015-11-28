import sys
import json
import time
import socket
socket.setdefaulttimeout(60)

from crawler import __all__ as all_crawlers
from crawler import *
from crawler.utils import tbd
call = globals()
from utils import matchfile
from utils import domain

cooldown = {crawler:0 for crawler in all_crawlers}
cd = 360

while True:
    pool = []
    timestamp = time.time()
    for crawler in [x for x in all_crawlers if cooldown[x] < timestamp]:
        try:
            for match in call[crawler].crawl_full():
                with matchfile(match) as fw:
                    print(match.webpage)
                    fw.write(str(match) + '\n')
                if 0 < match.tostart < 3600 and not tbd in match.teams:
                    pool.append(match)
        except KeyboardInterrupt:
            sys.exit(0)
        except Exception:
            cooldown[crawler] = time.time() + cd
            print('{0} cooldowned for {1} seconds for exception')
    with open('httpalias', 'a') as fw:
        for s1 in pool:
            for s2 in pool:
                if not domain(s1) == domain(s2):
                    if s1.__eq__(s2):
                        fw.write('{0} {1}'.format(s1.webpage, s2.webpage))
    print('done one-round crawling')
    time.sleep(5)
