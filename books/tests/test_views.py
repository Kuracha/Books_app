from django.test import TestCase
from django.urls import reverse


class AddBookViewTest(TestCase):

    def test_url_response(self):
        response = self.client.get(reverse('add_book'))
        self.assertEqual(response.status_code, 200)

    def test_add_new_book(self):
        data = {
            'title': 'Django',
            'authors': 'Antonio Mele',
            'published_date': 2017,
            'pages': 356,
            'language': 'pl',
            'image': 'https://miro.medium.com/max/2400/1*PXHkfdYyliqb1qCrznu5TQ.jpeg',
            'industry_identifiers':''
        }
        response = self.client.post(reverse('add_book'), data)
        self.assertEqual(response.status_code, 200)
