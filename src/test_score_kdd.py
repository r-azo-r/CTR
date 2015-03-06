import unittest
import scoreKDD

class TestScoreKDD(unittest.TestCase):
    def test_scoreNWMAE(self):
        clicks = [0.0,1.0]
        impressions = [1.0,1.0]
        predicted_ctr = [0.1,0.9]
        score = scoreKDD.scoreNWMAE(clicks, impressions, predicted_ctr)
        self.assertAlmostEqual(0.1,score)

        predicted_ctr = [0.0,0.0]
        impressions = [1.0,2.0]
        score = scoreKDD.scoreNWMAE(clicks, impressions, predicted_ctr)
        self.assertAlmostEqual(1.0/3.0, score)

    def test_scoreWRMSE(self):
    	import math

        clicks = [0.0,1.0]
        impressions = [1.0,1.0]
        predicted_ctr = [0.1,0.9]
        score = scoreKDD.scoreWRMSE(clicks, impressions, predicted_ctr)
        self.assertAlmostEqual(0.1,score)

        predicted_ctr = [0.0,0.0]
        impressions = [1.0,2.0]
        score = scoreKDD.scoreWRMSE(clicks, impressions, predicted_ctr)
        self.assertAlmostEqual(1.0/math.sqrt(6.0), score)

    def test_scoreClickAUC(self):
    	clicks = [2, 1, 2, 2, 10, 1, 2, 0, 1, 0]
    	impressions = [800, 220, 45, 300, 420, 50, 8, 420, 50, 8]
    	predicted_ctr = [.02, .005, .12517, .123, .12517, .12512, .02, .2519, .12512, .0232]
    	score = scoreKDD.scoreClickAUC(clicks, impressions, predicted_ctr)
    	self.assertAlmostEqual(0.57042443, score)

    	predicted_ctr = [0.0 for x in clicks]
    	score = scoreKDD.scoreClickAUC(clicks, impressions, predicted_ctr)
    	self.assertAlmostEqual(0.5, score)


if __name__=="__main__":
    unittest.main()