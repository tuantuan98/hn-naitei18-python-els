from django.shortcuts import redirect
from django.test import TestCase
from django.urls import reverse
from gogoedu.models import Catagory, myUser

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

class ProfileUpdateViewTest(TestCase):
    def setUp(self):
        # Create a user
        test_user1 = myUser.objects.create_user(username='testuser1', password='2HJ1vRV0Z&3iD', is_active=True)
        test_user2 = myUser.objects.create_user(username='testuser2', password='2HJ1vRV0Z&3iD', is_active=True)

        test_user1.save()
        test_user2.save()

        self.test_user1 = test_user1
        self.test_user2 = test_user2

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('profile-update', kwargs={'pk': self.test_user2.pk}))
        # Manually check redirect (Can't use assertRedirect, because the redirect URL is unpredictable)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/accounts/login/'))

    def test_logged_in(self):
        login = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
        response = self.client.get(reverse('profile-update', kwargs={'pk': self.test_user2.pk}))
        self.assertEqual(response.status_code, 200)

    def test_uses_correct_template(self):
        login = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
        response = self.client.get(reverse('profile-update', kwargs={'pk': self.test_user2.pk}))
        self.assertEqual(response.status_code, 200)

        # Check we used correct template
        self.assertTemplateUsed(response, 'gogoedu/myuser_update.html')

    def test_redirects_to_profile_update_on_success(self):
        login = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
        first_name, last_name, email = 'Nguyen', 'Quang Anh', 'test11@gmail.com'
        response = self.client.post(reverse('profile-update', kwargs={'pk': self.test_user2.pk}),
                                    {'first_name': first_name,
                                     'last_name': last_name,
                                     'email': email})
        self.assertEqual(response.status_code, 200)

    def test_invalid_user_redirect(self):
        login = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
        response = self.client.get(reverse('profile-update', kwargs={'pk': self.test_user1.pk}))
        self.assertTrue(response.url.startswith('/gogoedu/'))
