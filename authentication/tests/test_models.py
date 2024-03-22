from django.test import TestCase

from authentication.models import Student, User


class UserModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(
            email="foo@bar.com", 
            first_name="Foo",
            last_name="Bar",
            department="COM",
        )

    def test_email_label(self):
        field_label = self.user._meta.get_field('email').verbose_name
        self.assertEqual(field_label, 'email')
        
    def test_first_name_label(self):
        field_label = self.user._meta.get_field('first_name').verbose_name
        self.assertEqual(field_label, 'first name')

    def test_last_name_label(self):
        field_label = self.user._meta.get_field('last_name').verbose_name
        self.assertEqual(field_label, 'last name')

    def test_deparment_label(self):
        field_label = self.user._meta.get_field('department').verbose_name
        self.assertEqual(field_label, 'department')

    def test_user_str_is_first_name_space_last_name(self):
        self.assertEqual(str(self.user), 'Foo Bar')
        
    def test_user_absolute_url(self):
        self.assertEqual(self.user.get_absolute_url(), '/profile/')

    def test_user_manager_create_user(self):
        user = User.objects.create_user(
            email="test@test.com",
            password="testpassword",
        )
        self.assertTrue(user)

    def test_user_manager_raises_error_with_no_email(self):
        with self.assertRaises(ValueError):
            User.objects.create_user(
                email="",
                password="testpassword",
            )

    def test_user_manager_creates_superuser(self):
        user = User.objects.create_superuser(
            email="test@test.com"
        )
        self.assertTrue(user.is_staff)

    def test_user_manager_raises_error_with_is_staff_false(self):
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email="test@test.com",
                is_staff=False,
            )

    def test_user_manager_raises_error_with_is_superuser_false(self):
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email="test@test.com",
                is_superuser=False,
            )



class StudentModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.student = User.objects.create(
            email="bar@fo.com", 
            first_name="Bar",
            last_name="Foo",
            department="COM",
        )

        cls.student_obj = Student.objects.create(
            user=User.objects.get(id=1),
            study_level=1,
            course="Computer Science",
            support_plan="support_plans/elliscd.ico"
        )

    def test_study_level_label(self):
        field_label = self.student_obj._meta.get_field('study_level').verbose_name
        self.assertEqual(field_label, 'study level')
