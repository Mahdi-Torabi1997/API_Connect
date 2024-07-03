import unittest
from ..src.main import SkeletonModel

class TestSkeletonModel(unittest.TestCase):

    def test_skeleton_model_initialization(self):
        tracker_id = 1
        person_id = 1
        XCoords = [0.1] * 18
        YCoords = [0.2] * 18

        skeleton = SkeletonModel(tracker_id, person_id, XCoords, YCoords)

        self.assertEqual(skeleton.TrackerId, tracker_id)
        self.assertEqual(skeleton.PersonId, person_id)
        self.assertEqual(skeleton.XCoords, XCoords)
        self.assertEqual(skeleton.YCoords, YCoords)

if __name__ == '__main__':
    unittest.main()
