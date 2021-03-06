# -*- coding: utf-8 -*-

import os
import time
import json

from slugify import slugify
from Levenshtein import distance

headers = {
'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.93 Safari/537.36',
}
tbd = 'TBD'
stops = {'dota2', 'dota-2', 'united', 'gaming', 'team', '-', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0'}

def pc(x):
    return float(x[:-1]) / 100

def close(s1, s2, k=1.25):
    if not isinstance(s1, str) and len(s1) == len(s2) == 2:
        return (close(s1[0], s2[1]) and close(s1[1], s2[0])) or (close(s1[0], s2[0]) and close(s1[1], s2[1]))
    return distance(s1, s2) <= k * abs(len(s1) - len(s2))

def seriesclose(s1, s2, k1=1.25, k2=0.5):
    return distance(s1, s2) <= k1 * abs(len(s1) - len(s2)) or distance(s1, s2) <= k2 * min(len(s1), len(s2))

def stem(x):
    if not isinstance(x, str) and len(x) == 2:
        return [stem(x[0]), stem(x[1])] 
    for stop in stops:
        x = x.replace(stop, '')
    return x

class Match(object):
    def __init__(self, active='', matchtime='1990-01-01 00:00', webpage='', series='', teams=(tbd, tbd), odds=(-1, -1), returns=(-1, -1), notes=None, result=(-1, -1), poolsize=-1, bestof=-1, tostart=-1):
        self.active = active
        self.matchtime = matchtime
        self.series = slugify(series)
        teams = [slugify(team) for team in teams]
        for i in range(len(teams)):
            if 'tbd' in teams[i] or 'TBD' in teams[i]:
                teams[i] = tbd
        odds = [float(odd) for odd in odds]
        returns = [float("{0:.2f}".format(float(_return))) for _return in returns]
        result = [int(score) for score in result]
        if teams[0] <= teams[1]:
            self.teams = teams
            self.odds = odds
            self.returns = returns
            self.result = result
        else:
            self.teams = teams[::-1]
            self.odds = odds[::-1]
            self.returns = returns[::-1]
            self.result = result[::-1]
        self.notes = notes
        self.webpage = webpage
        self.poolsize = int(poolsize)
        self.bestof = int(bestof)
        self.timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        self.tostart = int(tostart)

    def __eq__(self, s):
        assert(isinstance(s, Match))
        assert(not tbd in self.teams and not tbd in s.teams)
        if seriesclose(stem(self.series), stem(s.series)) and close(stem(self.teams), stem(s.teams)):
            return True
        else:
            return False

    def __str__(self):
        return json.dumps(self.__dict__)

    @staticmethod
    def loads(s):
        obj = Match(active='', matchtime='', webpage='')
        obj.__dict__ = json.loads(s)
        return obj
