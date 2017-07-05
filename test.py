#!/usr/bin/env python3
from agent import *
from piece import *
from core import *
import random
from envy_free_allocation import *
from copy import copy
from time import time

if __name__ == '__main__':
    set_debug(True)

    ## Breaks ranking plus agent ordering
    ## But it doesn't break in test.py. Why?
    seed =  1499115613878

    random.seed(seed)
    agents = [Agent(division_count=random.randint(10,20)) for i in range(12)]
    core_number = get_envy_free_allocation(agents, Piece.get_whole_piece(), get_call_number=True)
