# API_Connect

## Overview

This repository contains a script that interacts with a remote API to fetch and process data from camera recordings. The script retrieves binary data, parses it, and converts it into CSV format. It also includes automated tests to ensure the functionality of the code.

## Main Script

- **Functionality**: The main script,  connects to the AltumView API using client credentials, fetches recording data, parses the binary data, and converts it to a CSV file.
- **API Interaction**: The script uses HTTP protocols to communicate with the AltumView API. It sends HTTP GET requests to the API to retrieve recordings based on specified time intervals and camera IDs. The authentication is handled using client credentials to obtain an access token, which is then used in the Authorization header of subsequent API requests.
- **Data Processing**: The script parses the binary data received from the API. It extracts essential information such as timestamps, camera IDs, and skeleton coordinates. This involves converting the binary data into readable formats (e.g., integers, floats) and organizing it into structured data models.
- **CSV Conversion**: The processed data is then saved into a CSV file for further analysis or storage. 

## Testing

The repository includes unit tests to validate various components of the script:
- **Utility Functions**: Tests for data parsing functions.
- **Data Models**: Tests for the `SkeletonModel` and `Frame` classes.
- **Record Parser**: Tests for the `RecordParser` class, including token fetching, data retrieval, and parsing methods.

## Continuous Integration

The repository is set up with a CI pipeline using GitHub Actions. The pipeline runs the tests automatically on each push to ensure code reliability and functionality.


