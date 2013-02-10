import unittest
from StoneBuilder import aiMaxmin
from Renju import black

def putStones():
    stonesPattern =         '''  1234567890
                                |               
                                |               
                                |               
                                |       X       
                                |    X X        
                                |     OX        
                                |     XOO       
                                |       O       
                                |      OOO?     
                                |       X X   
                                '''

    (rank, move), expects = aiMaxmin(stonesPattern, black, black, 3)
        
class TestAIPlayerPerformance(unittest.TestCase):
    def testPerformance(self):
        import cProfile
        profiler = cProfile.Profile()
        profiler.runcall(putStones)
        profiler.print_stats(1)
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()