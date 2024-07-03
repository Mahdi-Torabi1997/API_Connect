import unittest
from main import Frame, SkeletonModel

class TestFrame(unittest.TestCase):

    def test_frame_initialization(self):
        camera_id = 1
        timestamp = 1234567890
        people = [SkeletonModel(1, 1, [0.1] * 18, [0.2] * 18)]

        frame = Frame(camera_id, people, timestamp)

        self.assertEqual(frame.cameraId, camera_id)
        self.assertEqual(frame.timestamp, timestamp)
        self.assertEqual(frame.skeletons, people)

if __name__ == '__main__':
    unittest.main()
