#!/usr/bin/env python3
"""Unittests for utils module."""
import unittest
from parameterized import parameterized
from unittest.mock import patch, Mock
import utils


class TestAccessNestedMap(unittest.TestCase):
    """Tests for access_nested_map."""

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """access_nested_map returns the expected value for given path."""
        self.assertEqual(utils.access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",)),
        ({"a": 1}, ("a", "b")),
    ])
    def test_access_nested_map_exception(self, nested_map, path):
        """access_nested_map raises KeyError for invalid path."""
        with self.assertRaises(KeyError) as ctx:
            utils.access_nested_map(nested_map, path)
        self.assertEqual(str(ctx.exception), repr(path[-1]))   


class TestGetJson(unittest.TestCase):
    """Tests for get_json."""

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    def test_get_json(self, test_url, test_payload):
        """get_json calls requests.get and returns the json payload."""
        mock_resp = Mock()
        mock_resp.json.return_value = test_payload
        with patch("utils.requests.get", return_value=mock_resp) as mocked_get:
            result = utils.get_json(test_url)
            mocked_get.assert_called_once_with(test_url)
            self.assertEqual(result, test_payload)