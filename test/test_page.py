import unittest

from unittest.mock import Mock, patch
from scripts import scrape


class TestPageParse(unittest.TestCase):

    def test_blog_author(self):
        result = scrape.get_author(None)
        self.assertEqual(result, None)

    @patch('scripts.scrape.get_author', return_value='Lisa McNamara')
    def test_author_name(self, mock_check):
        result = scrape.get_author('')
        self.assertEqual(result, 'Lisa McNamara')

    def test_title_author(self):
        result = scrape.get_title(None)
        self.assertEqual(result, None)

    def test_title_name(self):
        result_title_mock = Mock()
        mock_bs4 = Mock()

        result_title_mock.contents = ['Hello Title']
        mock_bs4.find(class_='read-time').return_value = result_title_mock

        result = scrape.get_title(mock_bs4)
        self.assertEqual(result, 'Hello Title')

    def test_post_date_author(self):
        result = scrape.get_post_date(None)
        self.assertEqual(result, None)

    def test_read_time_author(self):
        result = scrape.get_read_time(None)
        self.assertEqual(result, None)

    def test_parse_url(self):
        result = scrape.parse_url('')
        self.assertEqual(result, None)
