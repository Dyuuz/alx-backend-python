#!/usr/bin/env python3
"""Unittests and integration tests for client.GithubOrgClient."""
import unittest
from parameterized import parameterized, parameterized_class
from unittest.mock import patch, Mock
import client
from client import GithubOrgClient
import fixtures
import utils


class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for GithubOrgClient."""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        """org returns the result of get_json called with the org url."""
        mock_get_json.return_value = {"some": "payload"}
        gh = GithubOrgClient(org_name)
        self.assertEqual(gh.org(), mock_get_json.return_value)
        mock_get_json.assert_called_once()

    def test_public_repos_url(self):
        """_public_repos_url returns repos_url from org payload."""
        payload = {"repos_url": "https://api.github.com/orgs/test/repos"}
        with patch.object(GithubOrgClient, "org", return_value=payload):
            gh = GithubOrgClient("test")
            self.assertEqual(gh._public_repos_url, payload["repos_url"])

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """public_repos returns list of repo names from get_json results."""
        repos_payload = [
            {"name": "repo1"},
            {"name": "repo2"},
        ]
        mock_get_json.return_value = repos_payload
        with patch.object(GithubOrgClient, "_public_repos_url",
                          return_value="https://api.github.com/orgs/test/repos"):
            gh = GithubOrgClient("test")
            self.assertEqual(gh.public_repos(), ["repo1", "repo2"])
            mock_get_json.assert_called_once()

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """has_license returns True when repo license matches license_key."""
        gh = GithubOrgClient("test")
        self.assertEqual(gh.has_license(repo, license_key), expected)

@parameterized_class(("org_payload", "repos_payload", "expected_repos",
                      "apache2_repos"), [
    (fixtures.org_payload, fixtures.repos_payload,
     fixtures.expected_repos, fixtures.apache2_repos),
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for GithubOrgClient.public_repos using fixtures."""
    @classmethod
    def setUpClass(cls):
        """Start patcher for requests.get to return fixtures."""
        cls.get_patcher = patch("utils.requests.get")
        mocked_get = cls.get_patcher.start()

        # Create two mocked responses: one for the org payload and one for repos
        mock_resp_org = Mock()
        mock_resp_org.json.return_value = cls.org_payload

        mock_resp_repos = Mock()
        mock_resp_repos.json.return_value = cls.repos_payload

        # requests.get will be called multiple times; return responses in order
        mocked_get.side_effect = [mock_resp_org, mock_resp_repos]

    @classmethod
    def tearDownClass(cls):
        """Stop the requests.get patcher."""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """public_repos returns expected repos from fixtures."""
        gh = GithubOrgClient(self.org_payload.get("login"))
        self.assertEqual(gh.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """public_repos can filter repos by license (apache-2.0 example)."""
        gh = GithubOrgClient(self.org_payload.get("login"))
        self.assertEqual(gh.public_repos(license="apache-2.0"), self.apache2_repos)