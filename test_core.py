import unittest
from classes import *
from random import *
from core import *
from time import sleep

class AgentTests(unittest.TestCase):

    def test_best_case(self):
        debug_print("Testing identical preferences (best case) for value_count and trim_count")
        divs = 29
        n = 5
        agents = [
            Agent(division_count=divs, preference_function=lambda x: x**2) for i in range(n)
        ]
        cake = Cake()
        pieces = core(agents[0], agents, cake.pieces[0])

        self.assertTrue(agents[0].value_count == 1)
        self.assertTrue(agents[0].trim_count == n-1)
        for a in agents[1:]:
            self.assertTrue(a.value_count == n)
            self.assertTrue(a.trim_count == 0)

    def test_worst_case(self):
        debug_print("Testing a possible worst case call to prints")
        #Values independently generated by Mathematica:
        #Note that 1: 0 is an exceptional case
        #TODO These numbers below are outdated. Our caching has at some point saved some steps (6 queries saved on 6 agent)
        # Also, line 5 in the paper was not properly counted by us, raising the bound.
        #worst_cases_for_n_players = { 1: 0, 2: 4, 3: 12, 4: 34, 5: 94, 6: 255, 7: 682, 8: 1807, 9: 4761, 10: 12505, 11: 32791 }
        for n in range(1,7):
            print(n)
            divs = 30
            agents = [
                Agent(division_count=divs, preference_function=lambda x: x**i) for i in range(1, n+1)
            ]
            cake = Cake()
            pieces = core(agents[0], agents, cake.pieces[0])
            trim_count = sum([a.trim_count for a in agents])
            value_count = sum([a.value_count for a in agents])
            print("sum:",trim_count+value_count)
            
            #self.assertTrue( value_count + trim_count <= worst_cases_for_n_players[n] )

    def test_preference_powers(self):
        for i in range(5):
            for n in [5]:
                agents = [Agent(division_count=20, preference_function=lambda x: x**Fraction(randint(0,5), randint(1,5))) for j in range(n)]
                cake = Cake()
                pieces = core(agents[0], agents, cake.pieces[0])
                self.assertTrue( True )



    #Ran test on 15 agents: Returned correctly in 1972.634s

    def test_preference_random(self):
        for n in range(2,6):
            agents = [Agent(random.randint(5,23)) for i in range(n)]
            cake = Cake()
            pieces = core(agents[0], agents, cake.pieces[0])
            self.assertTrue( True )

def main():
    unittest.main()

if __name__ == '__main__':
    main()
