#!/usr/bin/env python3
"""Unit tests for utils module."""

import unittest
from unittest.mock import patch, Mock
from parameterized import parameterized
from utils import access_nested_map, get_json, memoize


class TestAccessNestedMap(unittest.TestCase):
    """Test cases for access_nested_map function."""

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """Test access_nested_map returns correct value for given path."""
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",), "a"),
        ({"a": 1}, ("a", "b"), "b"),
    ])
    def test_access_nested_map_exception(self, nested_map, path, expected_key):
        """
        Test that KeyError is raised for missing keys,
        and the exception message matches the missing key.
        """
        with self.assertRaises(KeyError) as cm:
            access_nested_map(nested_map, path)
        self.assertEqual(str(cm.exception), f"'{expected_key}'")


class TestGetJson(unittest.TestCase):
    """Test cases for get_json function."""

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    @patch("utils.requests.get")
    def test_get_json(self, test_url, test_payload, mock_get):
        """
        Test get_json returns expected payload and calls requests.get once.
        """
        # Mock response with .json() returning test_payload
        mock_response = Mock()
        mock_response.json.return_value = test_payload
        mock_get.return_value = mock_response

        # Call the function
        result = get_json(test_url)

        # Assertions
        mock_get.assert_called_once_with(test_url)
        self.assertEqual(result, test_payload)


class TestMemoize(unittest.TestCase):
    """Test cases for the memoize decorator."""

    def test_memoize(self):
        """Test that memoize caches the result after first call."""

        class TestClass:
            """Inner class to test memoization."""

            def a_method(self):
                """Return a fixed value."""
                return 42

            @memoize
            def a_property(self):
                """Return the value of a_method, memoized."""
                return self.a_method()

        obj = TestClass()

        with patch.object(obj, "a_method", return_value=42) as mock_method:
            # First call should call a_method
            result1 = obj.a_property

            # Second call should return cached value
            # It should NOT call a_method again
            result2 = obj.a_property

            # Both results should be correct
            self.assertEqual(result1, 42)
            self.assertEqual(result2, 42)

            # a_method should only be called once in total
            mock_method.assert_called_once()


if __name__ == "__main__":
    unittest.main()
