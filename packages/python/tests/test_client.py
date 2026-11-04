import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from parse_everything import ParseEverything, ParseEverythingError

class TestParseEverythingClient(unittest.TestCase):
    def test_client_init(self):
        client = ParseEverything("pe_live_test_key_123")
        self.assertEqual(client.api_key, "pe_live_test_key_123")
        self.assertEqual(client.base_url, "https://parse-everything.com")

    def test_client_init_empty_key(self):
        with self.assertRaises(ValueError):
            ParseEverything("")

if __name__ == "__main__":
    unittest.main()
