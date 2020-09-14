from django.test import TestCase

from gogoedu.models import Test,Lesson

class TestModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        Test.objects.create(name='Love Shiba', time=20,question_num=20)

    def test_name_label(self):
        test = Test.objects.get(id=1)
        field_label = test._meta.get_field('name').verbose_name
        self.assertEquals(field_label, 'name')

    def test_lesson_label(self):
        test=Test.objects.get(id=1)
        field_label = test._meta.get_field('lesson').verbose_name
        self.assertEquals(field_label, 'lesson')
    
    def test_time_label(self):
        test=Test.objects.get(id=1)
        field_label = test._meta.get_field('time').verbose_name
        self.assertEquals(field_label, 'time')
    
    def test_question_num_label(self):
        test=Test.objects.get(id=1)
        field_label = test._meta.get_field('question_num').verbose_name
        self.assertEquals(field_label, 'question num')

    def test_name_max_length(self):
        test = Test.objects.get(id=1)
        max_length = test._meta.get_field('name').max_length
        self.assertEquals(max_length, 50)

    def test_object_name_is_name(self):
        test = Test.objects.get(id=1)
        expected_object_name = f'{test.name}'
        self.assertEquals(expected_object_name, str(test))

    def test_get_absolute_url(self):
        test = Test.objects.get(id=1)
        # This will also fail if the urlconf is not defined.
        self.assertEquals(test.get_absolute_url(), '/gogoedu/test/1')

    def test_get_test_url(self):
        test = Test.objects.get(id=1)
        # This will also fail if the urlconf is not defined.
        self.assertEquals(test.get_absolute_url(), '/gogoedu/test/1')
