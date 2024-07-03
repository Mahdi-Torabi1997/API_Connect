import unittest
from unittest.mock import patch, MagicMock
from src.main import RecordParser

class TestRecordParser(unittest.TestCase):

    @patch('requests.api.post')
    def test_get_token(self, mock_post):
        mock_post.return_value.json.return_value = {"access_token": "fake_token"}
        parser = RecordParser()
        self.assertEqual(parser.token, "fake_token")

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
        parser = RecordParser()
        parser.get_records(1234567890, 1234567891)
        self.assertEqual(parser.recordid_pairs, [["cam1", "rec1"], ["cam1", "rec2"], ["cam2", "rec3"]])

    @patch('requests.get')
    def test_fetch_recording(self, mock_get):
        mock_get.return_value.content = b'binary_data'
        mock_get.return_value.status_code = 200
        parser = RecordParser()
        parser.fetch_recording("rec1", "cam1")
        self.assertIn(b'binary_data', parser.binary_datas)

    @patch('main.RecordParser.fetch_recording')
    def test_fetch_all(self, mock_fetch_recording):
        parser = RecordParser()
        parser.recordid_pairs = [["cam1", "rec1"], ["cam2", "rec2"]]
        parser.fetch_all()
        self.assertEqual(len(parser.binary_datas), 2)

    # Assuming parse_binary and to_csv methods are already tested with integration tests

if __name__ == '__main__':
    unittest.main()
