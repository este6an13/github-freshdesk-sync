import unittest
from unittest.mock import patch
import os

from main import (
    get_github_user,
    search_freshdesk_contacts,
    create_freshdesk_contact,
    update_freshdesk_contact,
)

class GitHubFreshdeskSyncTest(unittest.TestCase):
    def setUp(self):
        os.environ["GITHUB_TOKEN"] = "your_github_token"
        os.environ["FRESHDESK_TOKEN"] = "your_freshdesk_token"

    def tearDown(self):
        del os.environ["GITHUB_TOKEN"]
        del os.environ["FRESHDESK_TOKEN"]

    @patch("requests.get")
    def test_get_github_user_success(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "login": "john_doe",
            "id": 123456,
            "name": "John Doe",
            "company": "ABC Company",
            "location": "New York",
            "email": "john.doe@example.com",
            "twitter_username": "johndoe",
        }

        result = get_github_user("john_doe")

        self.assertEqual(result["login"], "john_doe")
        self.assertEqual(result["id"], 123456)
        self.assertEqual(result["name"], "John Doe")
        self.assertEqual(result["company"], "ABC Company")
        self.assertEqual(result["location"], "New York")
        self.assertEqual(result["email"], "john.doe@example.com")
        self.assertEqual(result["twitter_username"], "johndoe")

    @patch("requests.get")
    def test_get_github_user_failure(self, mock_get):
        mock_get.return_value.status_code = 404
        mock_get.return_value.text = "User not found"

        result = get_github_user("john_doe")

        self.assertIsNone(result)

    @patch("requests.get")
    def test_search_freshdesk_contacts_success(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "total": 1,
            "results": [{"id": 123}],
        }

        result = search_freshdesk_contacts("john.doe@example.com")

        self.assertEqual(result["total"], 1)
        self.assertEqual(result["results"][0]["id"], 123)

    @patch("requests.get")
    def test_search_freshdesk_contacts_failure(self, mock_get):
        mock_get.return_value.status_code = 500
        mock_get.return_value.text = "Internal server error"

        result = search_freshdesk_contacts("john.doe@example.com")

        self.assertIsNone(result)

    @patch("requests.post")
    def test_create_freshdesk_contact_success(self, mock_post):
        mock_post.return_value.status_code = 201
        mock_post.return_value.json.return_value = {
            "name": "John Doe",
            "email": "john.doe@example.com",
            "id": 123,
        }

        data = {
            "name": "John Doe",
            "email": "john.doe@example.com",
            "phone": "",
            "mobile": "",
            "twitter_id": "johndoe",
            "unique_external_id": "123456",
            "custom_fields": {
                "github_login": "john_doe",
                "github_company": "ABC Company",
                "github_location": "New York",
            },
        }

        result = create_freshdesk_contact(data)

        self.assertIsNone(result)

    @patch("requests.put")
    def test_update_freshdesk_contact_success(self, mock_put):
        mock_put.return_value.status_code = 200
        mock_put.return_value.json.return_value = {
            "name": "John Doe",
            "email": "john.doe@example.com",
            "id": 123,
        }

        data = {
            "name": "John Doe",
            "email": "john.doe@example.com",
            "phone": "",
            "mobile": "",
            "twitter_id": "johndoe",
            "unique_external_id": "123456",
            "custom_fields": {
                "github_login": "john_doe",
                "github_company": "ABC Company",
                "github_location": "New York",
            },
        }

        result = update_freshdesk_contact(123, data)

        self.assertEqual(result["name"], "John Doe")
        self.assertEqual(result["email"], "john.doe@example.com")
        self.assertEqual(result["id"], 123)

    @patch("requests.put")
    def test_update_freshdesk_contact_failure(self, mock_put):
        mock_put.return_value.status_code = 404
        mock_put.return_value.text = "Contact not found"

        data = {
            "name": "John Doe",
            "email": "john.doe@example.com",
            "phone": "",
            "mobile": "",
            "twitter_id": "johndoe",
            "unique_external_id": "123456",
            "custom_fields": {
                "github_login": "john_doe",
                "github_company": "ABC Company",
                "github_location": "New York",
            },
        }

        result = update_freshdesk_contact(123, data)

        self.assertIsNone(result)

if __name__ == "__main__":
    unittest.main()
