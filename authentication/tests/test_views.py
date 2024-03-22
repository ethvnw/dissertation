import shutil
from unittest import mock

from django.core.files import File
from django.test import TestCase, override_settings
from django.urls import reverse

from authentication.models import Student, User

TEST_DIR = 'test_files'

class StudentSignUpViewTest(TestCase):
    def test_student_sign_up_view_url_exists_at_desired_location(self):
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)

    def test_student_sign_up_form_exists(self):
        response = self.client.get(reverse('signup'))
        self.assertContains(response, 'Sign Up.')

    def test_student_sign_up_form_creates_user(self):
        self.client.post(reverse('signup'), {
            'first_name': 'Test',
            'last_name': 'Test',
            'email': 'test@test.com',
            'department': 'COM',
            'password1': 'testpassword',
            'password2': 'testpassword',
            'study_level': 1,
            'course': 'Computer Science',
        })

        user = User.objects.get(first_name='Test')
        self.assertTrue(user)

    @override_settings(MEDIA_ROOT=(TEST_DIR + '/media'))
    def test_support_plan_file_name_is_renamed(self):
        file = mock.MagicMock(spec=File)
        file.name = 'test.pdf'

        self.client.post(reverse('signup'), {
                'first_name': 'Test',
                'last_name': 'Test',
                'email': 'test@test.com',
                'department': 'COM',
                'password1': 'testpassword',
                'password2': 'testpassword',
                'study_level': 1,
                'course': 'Computer Science',
                'support_plan': file,
            })
        
        student = Student.objects.get(user__first_name='Test')
        self.assertNotEqual(student.support_plan.name, file.name)
       

class SignoutViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(
            email="foo@bar.com", 
            password="testpassword"
        )

    def test_signut_view_redirects_to_signin(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('signout'))
        self.assertRedirects(response, '/accounts/signin/')



def tearDownModule():
    shutil.rmtree(TEST_DIR, ignore_errors=True)