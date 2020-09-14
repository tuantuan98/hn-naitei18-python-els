from django.test import TestCase
from django.urls import reverse

from gogoedu.models import Catagory

class CatagoryListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create 13 authors for pagination tests
        number_of_catagories = 10

        for catagory_id in range(number_of_catagories):
            Catagory.objects.create(
                name=f' Le Minh Quang {catagory_id}',
            )
           
    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/gogoedu/catagory/')
        self.assertEqual(response.status_code, 200)
           
    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('catagory'))
        self.assertEqual(response.status_code, 200)
        
    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('catagory'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'gogoedu/catagory_list.html')
        
    def test_pagination_is_two(self):
        response = self.client.get(reverse('catagory'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertTrue(len(response.context['catagory_list']) == 2)

    def test_lists_all_catagories(self):
        # Get second page and confirm it has (exactly) remaining 3 items
        response = self.client.get(reverse('catagory')+'?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertTrue(len(response.context['catagory_list']) == 2)
