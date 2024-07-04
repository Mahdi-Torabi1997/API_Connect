import unittest
from unittest.mock import patch, MagicMock
from src.main import RecordParser

class TestRecordParser(unittest.TestCase):

    @patch('requests.post')
    def setUp(self, mock_post):
        mock_post.return_value.json.return_value = {"access_token": "fake_token"}
        self.parser = RecordParser()

    @patch('src.main.RecordParser.fetch_recording')
    def test_fetch_all(self, mock_fetch_recording):
        self.parser.recordid_pairs = [["cam1", "rec1"], ["cam2", "rec2"]]
        self.parser.fetch_all()
        self.assertEqual(mock_fetch_recording.call_count, 2)

    @patch('requests.get')
    def test_fetch_recording(self, mock_get):
        mock_get.return_value.content = b'binary_data'
        mock_get.return_value.status_code = 200
        self.parser.fetch_recording('rec1', 'cam1')
        self.assertEqual(len(self.parser.binary_datas), 1)
        self.assertEqual(self.parser.binary_datas[0], b'binary_data')

    @patch('requests.api.get')
    def test_get_records(self, mock_get):
        mock_get.return_value.json.return_value = {
            "data": {
                "records": [
                    {"camera_id": "cam1", "record_ids": ["rec1", "rec2"]},
                    {"camera_id": "cam2", "record_ids": ["rec3"]}
                ]
            }
        }
        start_date = 1698054064
        end_date = 1700154064
        self.parser.get_records(start_date, end_date)
        expected_records = [["cam1", "rec1"], ["cam1", "rec2"], ["cam2", "rec3"]]
        self.assertEqual(self.parser.recordid_pairs, expected_records)

if __name__ == "__main__":
    unittest.main()
