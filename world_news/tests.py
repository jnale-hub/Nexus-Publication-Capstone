from django.test import TestCase
from django.urls import reverse
from datetime import datetime
import requests
from unittest.mock import patch

class IndexTestCase(TestCase):

    @patch('requests.get')
    def test_index(self, mock_get):
        # Mock the requests.get method and provide a sample response
        mock_response = {
            "status": "ok",
            "articles": [
                {
                    "title": "News Title 1",
                    "description": "News Description 1",
                    "url": "https://example.com/news1",
                    "urlToImage": "https://example.com/image1.jpg",
                    "publishedAt": "2023-06-27T12:34:56Z"
                },
                {
                    "title": "News Title 2",
                    "description": "News Description 2",
                    "url": "https://example.com/news2",
                    "urlToImage": None,
                    "publishedAt": "2023-06-26T09:12:34Z"
                }
            ]
        }
        mock_get.return_value.json.return_value = mock_response

        # Make a GET request to the index view
        response = self.client.get(reverse('index'))

        # Check the response status code
        self.assertEqual(response.status_code, 200)

        # Check the rendered template
        self.assertTemplateUsed(response, 'world_news/index.html')

        # Check the context variables
        context = response.context
        self.assertTrue(context['success'])
        self.assertEqual(len(context['data']), 2)
        self.assertEqual(len(context['more_data']), 0)
        self.assertEqual(context['search'], None)
        self.assertEqual(context['categories'], ['Top News', 'Business', 'Technology', 'Entertainment', 'Sports', 'Science', 'Health'])

        # Check the data in the context
        news1 = context['data'][0]
        self.assertEqual(news1['title'], "News Title 1")
        self.assertEqual(news1['description'], "News Description 1")
        self.assertEqual(news1['url'], "https://example.com/news1")
        self.assertEqual(news1['image'], "https://example.com/image1.jpg")
        self.assertEqual(news1['publishedat'], datetime(2023, 6, 27, 12, 34, 56).strftime("%B %d, %Y"))

        news2 = context['data'][1]
        self.assertEqual(news2['title'], "News Title 2")
        self.assertEqual(news2['description'], "News Description 2")
        self.assertEqual(news2['url'], "https://example.com/news2")
        self.assertEqual(news2['image'], "https://www.spectraresearch.com/wp-content/uploads/2022/09/default-image.jpg")
        self.assertEqual(news2['publishedat'], datetime(2023, 6, 26, 9, 12, 34).strftime("%B %d, %Y"))
