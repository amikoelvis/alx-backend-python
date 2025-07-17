#!/usr/bin/env python3
"""Unit tests for client.GithubOrgClient"""

import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Test cases for GithubOrgClient"""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        """
        Test that GithubOrgClient.org returns expected payload for given org.
        Ensures get_json is called once with the correct URL.
        """
        expected_payload = {"login": org_name}
        mock_get_json.return_value = expected_payload

        client = GithubOrgClient(org_name)
        result = client.org

        expected_url = f"https://api.github.com/orgs/{org_name}"
        mock_get_json.assert_called_once_with(expected_url)
        self.assertEqual(result, expected_payload)

    def test_public_repos_url(self):
        """
        Test that _public_repos_url returns the correct URL from the mocked org.
        """
        test_payload = {"repos_url": "https://api.github.com/orgs/test-org/repos"}

        # Patch GithubOrgClient.org as a PropertyMock
        with patch(
            "client.GithubOrgClient.org",
            new_callable=PropertyMock,
            return_value=test_payload
        ) as mock_org:
            client = GithubOrgClient("test-org")
            result = client._public_repos_url

            # Should return the repos_url from the mocked org payload
            self.assertEqual(result, test_payload["repos_url"])

            # Ensure the org property was accessed exactly once
            mock_org.assert_called_once()


if __name__ == "__main__":
    unittest.main()
