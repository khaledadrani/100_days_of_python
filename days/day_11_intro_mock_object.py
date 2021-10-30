import datetime
from unittest.mock import Mock

# Save a couple of test days
tuesday = datetime.datetime(year=2019, month=1, day=1)
saturday = datetime.datetime(year=2019, month=1, day=5)

# Mock datetime to control today's date
datetime = Mock()

def is_weekday():
    today = datetime.datetime.today()
    # Python's datetime library treats Monday as 0 and Sunday as 6
    return (0 <= today.weekday() < 5)

def mock_is_weekday():
    # Mock .today() to return Tuesday
    datetime.datetime.today.return_value = tuesday
    # Test Tuesday is a weekday
    assert is_weekday()
    # Mock .today() to return Saturday
    datetime.datetime.today.return_value = saturday
    # Test Saturday is not a weekday
    assert not is_weekday()

import requests
from requests.exceptions import Timeout
import unittest

def get_holidays():
    r = requests.get('http://localhost/api/holidays')
    if r.status_code == 200:
        return r.json()
    return None

requests = Mock()

# class TestCalendar(unittest.TestCase):
#     def test_get_holidays_timeout(self):
#         # Test a connection timeout
#         requests.get.side_effect = Timeout
#         with self.assertRaises(Timeout):
#             get_holidays()

# class TestCalendar(unittest.TestCase):
#     def log_request(self, url):
#         # Log a fake request for test output purposes
#         print(f'Making a request to {url}.')
#         print('Request received!')

#         # Create a new Mock to imitate a Response
#         response_mock = Mock()
#         response_mock.status_code = 200
#         response_mock.json.return_value = {
#             '12/25': 'Christmas',
#             '7/4': 'Independence Day',
#         }
#         return response_mock

#     def test_get_holidays_logging(self):
#         # Test a successful, logged request
#         requests.get.side_effect = self.log_request
#         assert get_holidays()['12/25'] == 'Christmas'

class TestCalendar(unittest.TestCase):
    def test_get_holidays_retry(self):
        # Create a new Mock to imitate a Response
        response_mock = Mock()
        response_mock.status_code = 200
        response_mock.json.return_value = {
            '12/25': 'Christmas',
            '7/4': 'Independence Day',
        }
        # Set the side effect of .get()
        requests.get.side_effect = [Timeout, response_mock]
        # Test that the first request raises a Timeout
        with self.assertRaises(Timeout):
            get_holidays()
        # Now retry, expecting a successful response
        assert get_holidays()['12/25'] == 'Christmas'
        # Finally, assert .get() was called twice
        assert requests.get.call_count == 2

if __name__ == "__main__":
    unittest.main()

