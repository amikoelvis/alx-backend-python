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
        """Test GithubOrgClient.org returns expected payload."""
        expected_payload = {"login": org_name}
        mock_get_json.return_value = expected_payload

        client = GithubOrgClient(org_name)
        result = client.org

        expected_url = f"https://api.github.com/orgs/{org_name}"
        mock_get_json.assert_called_once_with(expected_url)
        self.assertEqual(result, expected_payload)

    def test_public_repos_url(self):
        """Test that _public_repos_url returns correct URL from mocked org."""
        test_payload = {"repos_url": "https://api.github.com/orgs/test-org/repos"}

        with patch(
            "client.GithubOrgClient.org",
            new_callable=PropertyMock,
            return_value=test_payload
        ) as mock_org:
            client = GithubOrgClient("test-org")
            result = client._public_repos_url

            self.assertEqual(result, test_payload["repos_url"])
            mock_org.assert_called_once()

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """
        Test that public_repos returns the expected repo list.
        Mocks both _public_repos_url and get_json.
        """
        # Mock repo payload returned by get_json
        mock_repos_payload = [
            {"name": "repo1"},
            {"name": "repo2"},
            {"name": "repo3"}
        ]
        mock_get_json.return_value = mock_repos_payload

        # Fake URL for _public_repos_url
        fake_repos_url = "https://api.github.com/orgs/test-org/repos"

        with patch(
            "client.GithubOrgClient._public_repos_url",
            new_callable=PropertyMock,
            return_value=fake_repos_url
        ) as mock_url:
            client = GithubOrgClient("test-org")
            result = client.public_repos()

            # Should return only repo names
            expected_repos = ["repo1", "repo2", "repo3"]
            self.assertEqual(result, expected_repos)

            # Ensure _public_repos_url was accessed once
            mock_url.assert_called_once()

            # Ensure get_json was called once with the fake URL
            mock_get_json.assert_called_once_with(fake_repos_url)


if __name__ == "__main__":
    unittest.main()
