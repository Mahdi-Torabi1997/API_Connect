import struct
import requests
import pandas as pd

# Constants for API authentication
CLIENT_ID = "NnPOAzszR8TKZVnT"
CLIENT_SECRET = "lvvdFj8p58YRTjWQACMzDo4PIopuKfNgxkhXr1nehblkQpRDQSNRgoDzk2C2BBCx"

################# Utility Functions ###################
def parseStringInt32(stringData, startIndex):
    """
    Parses a 32-bit integer from a binary string starting at the given index.
    
    Args:
        stringData (bytes): Binary string data.
        startIndex (int): Starting index to parse the integer.
        
    Returns:
        int: Parsed 32-bit integer.
    """
    b = stringData[startIndex: startIndex + 4]
    return int.from_bytes(b, byteorder="little")

def parseStringInt16(stringData, startIndex):
    """
    Parses a 16-bit integer from a binary string starting at the given index.
    
    Args:
        stringData (bytes): Binary string data.
        startIndex (int): Starting index to parse the integer.
        
    Returns:
        int: Parsed 16-bit integer.
    """
    b = stringData[startIndex: startIndex + 2]
    return int.from_bytes(b, byteorder="little")

def parseStringFloat(stringData, startIndex):
    """
    Parses a float from a binary string starting at the given index.
    
    Args:
        stringData (bytes): Binary string data.
        startIndex (int): Starting index to parse the float.
        
    Returns:
        float: Parsed float.
    """
    b = stringData[startIndex: startIndex + 4]
    return struct.unpack("f", b)[0]
########################################################

class SkeletonModel(object):
    """
    Class representing a skeleton model with tracker ID, person ID, and coordinates.
    """
    def __init__(self, tracker_id, person_id, XCoords, YCoords):
        """
        Initializes the SkeletonModel.
        
        Args:
            tracker_id (int): Tracker ID.
            person_id (int): Person ID.
            XCoords (list): X coordinates of keypoints.
            YCoords (list): Y coordinates of keypoints.
        """
        self.TrackerId = tracker_id
        self.PersonId = person_id
        self.XCoords = XCoords
        self.YCoords = YCoords

class Frame(object):
    """
    Class representing a frame with camera ID, skeletons, and timestamp.
    """
    def __init__(self, camera_id, people, timestamp):
        """
        Initializes the Frame.
        
        Args:
            camera_id (int): Camera ID.
            people (list): List of SkeletonModel objects.
            timestamp (int): Timestamp of the frame.
        """
        self.cameraId = camera_id
        self.skeletons = people
        self.timestamp = timestamp

class RecordParser(object):
    """
    Class to handle fetching and parsing of recordings.
    """
    def __init__(self, client_id=CLIENT_ID, client_secret=CLIENT_SECRET):
        """
        Initializes the RecordParser with API credentials and retrieves the access token.
        
        Args:
            client_id (str): Client ID for API access.
            client_secret (str): Client secret for API access.
        """
        self.client_id = client_id
        self.client_secret = client_secret
        self.get_token()
        self.binary_datas = []
        self.recordid_pairs = []
        self.records = []

    def get_token(self):
        """
        Requests and sets the access token for API authentication.
        """
        url = "https://canada-1.oauth.altumview.com/v1.0/token"
        token_data = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "grant_type": "client_credentials",
            "scope": "camera:write camera:read",
        }
        self.token = requests.api.post(url, data=token_data).json()["access_token"]

    def get_records(self, start_date, end_date, camera_id=None):
        """
        Retrieves record IDs for the given date range and optional camera ID, and stores them in recordid_pairs.
        
        Args:
            start_date (int): Start date in epoch time.
            end_date (int): End date in epoch time.
            camera_id (str, optional): Specific camera ID to filter records.
        """
        records = []
        url = "https://api.altumview.ca/v1.0/recordings"
        headers = {"Authorization": f"Bearer {self.token}"}
        body = {
            "start_date": start_date,
            "end_date": end_date,
        }
        if camera_id is not None:
            body["camera_ids"] = camera_id
        resp = requests.api.get(url, headers=headers, params=body)
        requested_records = resp.json()["data"]["records"]
        for pair in requested_records:
            camera_id = pair["camera_id"]
            record_ids = pair["record_ids"]
            for record_id in record_ids:
                records.append([camera_id, record_id])
        self.recordid_pairs = self.recordid_pairs + records

    def fetch_recording(self, record_id, camera_id):
        """
        Fetches a single recording by record ID and camera ID and stores the binary data.
        
        Args:
            record_id (str): Record ID.
            camera_id (str): Camera ID.
        """
        headers = {"Authorization": f"Bearer {self.token}"}
        url = f"https://api.altumview.ca/v1.0/recordings/{camera_id}/{record_id}"
        response = requests.get(url, headers=headers)
        assert response.status_code == 200, \
            f"Failed to fetch recording {record_id} for camera {camera_id}, status code: {response.status_code}, Reason: {response.reason}"
        binary_data = response.content
        self.binary_datas.append(binary_data)

    def fetch_all(self):
        """
        Fetches all recordings in recordid_pairs and stores the binary data.
        """
        for record in self.recordid_pairs:
            camera_id, record_id = record
            self.fetch_recording(record_id, camera_id)
            self.recordid_pairs.remove(record)

    def parse_binary(self):
        """
        Parses all binary data in binary_datas and stores the parsed frames in records.
        """
        for byteList in self.binary_datas:
            cameraId = parseStringInt32(byteList, 8)
            timestamp = parseStringInt32(byteList, 12) * 1000
            frameNum = parseStringInt32(byteList, 16)
            frames = []
            pos = 20  # frame data begins
            for _ in range(frameNum):
                delta_time = parseStringInt16(byteList, pos)
                numPeople = parseStringInt16(byteList, pos + 2)
                pos = pos + 4  # people data begins
                people = []
                for _ in range(numPeople):
                    personId = parseStringInt32(byteList, pos + 0)
                    trackerId = byteList[pos + 4]
                    numPoints = byteList[pos + 5]
                    pos = pos + 16  # key point data begins
                    xs = [0 for _ in range(18)]
                    ys = [0 for _ in range(18)]
                    for _ in range(numPoints):
                        pt_index = (byteList[pos + 0]) & int(0b00001111)
                        xs[pt_index] = parseStringInt16(byteList, pos + 2) / 65536
                        ys[pt_index] = parseStringInt16(byteList, pos + 4) / 65536
                        pos = pos + 6
                    skeleton = SkeletonModel(trackerId, personId, xs, ys)
                    people.append(skeleton)
                timestamp = delta_time + timestamp  # update current timestamp (in milliseconds)
                frames.append(Frame(cameraId, people, timestamp))
            self.records.append(frames)
            self.binary_datas.remove(byteList)

    def to_csv(self, filename):
        """
        Converts all parsed data in records to a CSV file.
        
        Args:
            filename (str): Name of the output CSV file.
        """
        keypoint_names = [f"keypoint{i}" for i in range(18)]
        df = pd.DataFrame(columns=(["time", "camera_id", "person_id"] + keypoint_names))
        for frames in self.records:
            for frame in frames:
                timestamp = frame.timestamp
                camera_id = frame.cameraId
                people = frame.skeletons
                for person in people:
                    person_id = person.PersonId
                    xs = person.XCoords
                    ys = person.YCoords
                    new_df_row = {"time": timestamp, "camera_id": camera_id, "person_id": person_id}
                    for k in range(18):
                        new_df_row[f"keypoint{k}"] = (xs[k], ys[k])
                    df = df.append(new_df_row, ignore_index=True)
        df.to_csv(filename, index=False)
        self.records = []

if __name__ == '__main__':
    # Instantiate and use the RecordParser
    parser = RecordParser()
    end_date = 1700154064
    start_date = 1698054064
    # Retrieve record IDs for the given date range
    parser.get_records(start_date, end_date)
    # Fetch all recordings based on the retrieved record IDs
    parser.fetch_all()
    # Parse the fetched binary data
    parser.parse_binary()
    # Convert the parsed data to a CSV file
    parser.to_csv("tmp.csv")
