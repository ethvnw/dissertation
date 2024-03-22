import shutil
from unittest import mock

from django.core.files import File
from django.test import TestCase, override_settings
from django.urls import reverse

from authentication.models import Student, User
from dashboard.models import Notification
from ecf_applications.models import ECFApplication
from meetings.models import Meeting
from django.utils import timezone

TEST_DIR = 'test_files'

class IndexViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.student = User.objects.create(
            email="test@test.com",
            password="testpassword"
        )

    def test_index_view_redirects_to_dashboard_if_logged_in(self):
        self.client.force_login(self.student)
        response = self.client.get(reverse('index'))
        self.assertRedirects(response, reverse('dashboard'))

    def test_index_view_redirects_to_login_if_not_logged_in(self):
        response = self.client.get(reverse('index'))
        self.assertRedirects(response, '/accounts/signin/?next=/')


class DashboardViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.student = User.objects.create(
            email="test@test.com",
            password="testpassword",
            department="COM"
        )

        cls.secretary = User.objects.create(
            email="test@secretary.com",
            password="testpassword",
            role=User.SECRETARY,
            department="COM"
        )

        cls.scrutiny = User.objects.create(
            email="test@scrutiny.com",
            password="testpassword",
            role=User.SCRUTINY,
            department="COM"
        )

        Notification.objects.create(
            application=ECFApplication.objects.create(
                applicant=cls.student,
                status=1,
                start_date='2021-01-01',
                circumstance=1,
                description='Test description'
            ),
            user=cls.student,
            message='Test message'
        )

    def test_dashboard_view_template_for_student(self):
        self.client.force_login(self.student)
        response = self.client.get(reverse('dashboard'))
        self.assertTemplateUsed(response, 'dashboard/dashboard.html')

    def test_dashboard_view_template_for_secretary(self):
        self.client.force_login(self.secretary)
        ECFApplication.objects.all().delete()
        response = self.client.get(reverse('dashboard'))
        self.assertTemplateUsed(response, 'dashboard/secretary_dashboard.html')

    def test_dashboard_view_template_for_scrutiny(self):
        self.client.force_login(self.scrutiny)
        response = self.client.get(reverse('dashboard'))
        self.assertTemplateUsed(response, 'dashboard/scrutiny_dashboard.html')

    def test_dashboard_view_student_template_contains_recent_apps(self):
        self.client.force_login(self.student)
        application = ECFApplication.objects.create(
            applicant=self.student,
            status=1,
            start_date='2021-01-01',
            circumstance=1 
        )
        response = self.client.get(reverse('dashboard'))
        self.assertContains(response, application.get_circumstance_display())

    def test_dashboard_view_secretary_template_contains_attention_apps(self):
        self.client.force_login(self.secretary)
        application = ECFApplication.objects.create(
            applicant=self.student,
            status=1,
            start_date='2021-01-01',
            circumstance=1 
        )
        response = self.client.get(reverse('dashboard'))
        self.assertContains(response, application.get_circumstance_display())

    def test_dashboard_view_secretary_template_contains_other_apps(self):
        self.client.force_login(self.secretary)
        application = ECFApplication.objects.create(
            applicant=self.student,
            status=2,
            start_date='2021-01-01',
            circumstance=1 
        )
        response = self.client.get(reverse('dashboard'))
        self.assertContains(response, application.get_circumstance_display())

    def test_dashboard_view_secretary_template_contains_upcoming_meetings(self):
        self.client.force_login(self.secretary)
        meeting = Meeting.objects.create(
            creator=self.secretary,
            category=Meeting.SCRUTINY_PANEL,
            date_time=timezone.now() + timezone.timedelta(days=1)
        )
        response = self.client.get(reverse('dashboard'))
        self.assertContains(response, meeting.get_category_display())
            
    def test_dashboard_view_secretary_template_contains_ongoing_meetings(self):
        self.client.force_login(self.secretary)
        meeting = Meeting.objects.create(
            creator=self.secretary,
            category=Meeting.SCRUTINY_PANEL,
            date_time=timezone.now() - timezone.timedelta(minutes=20)
        )
        response = self.client.get(reverse('dashboard'))
        self.assertContains(response, meeting.get_category_display())

    def test_dashboard_view_scrutiny_template_contains_upcoming_meetings(self):
        self.client.force_login(self.scrutiny)
        meeting = Meeting.objects.create(
            creator=self.secretary,
            category=Meeting.SCRUTINY_PANEL,
            date_time=timezone.now() + timezone.timedelta(days=1)
        )
        response = self.client.get(reverse('dashboard'))
        self.assertContains(response, meeting.get_category_display())
            
    def test_dashboard_view_scrutiny_template_contains_ongoing_meetings(self):
        self.client.force_login(self.scrutiny)
        meeting = Meeting.objects.create(
            creator=self.secretary,
            category=Meeting.SCRUTINY_PANEL,
            date_time=timezone.now() - timezone.timedelta(minutes=20)
        )
        response = self.client.get(reverse('dashboard'))
        self.assertContains(response, meeting.get_category_display())
                                       

class ProfileViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.student = User.objects.create(
            email="test@test.com",
            password="testpassword"
        )

        cls.student_obj = Student.objects.create(
            user=cls.student,
            course="Test",
            study_level=1
        )

        cls.secretary = User.objects.create(
            email="test@secretary.com",
            password="testpassword",
            role=User.SECRETARY
        )

    def setUp(self):
        self.client.force_login(self.student)


    def test_student_form_on_page_for_student(self):
        response = self.client.get(reverse('profile'))
        self.assertContains(response, 'Course:')
       
    def test_student_form_not_present_for_staff(self):
        self.client.force_login(self.secretary)
        response = self.client.get(reverse('profile'))
        self.assertNotContains(response, 'Course:')

    def test_profile_form_updates_student_details(self):
        self.client.post(reverse('profile'), {
            'first_name': 'test',
            'last_name': 'test',
            'email': 'test2@test2.com',
            'department': 'COM',
            'course': 'Test',
            'study_level': 1,
            'support_plan': ''
        })

        user = User.objects.get(email="test2@test2.com")
        self.assertTrue(user)

    def test_invalid_profile_form_returns_error_for_student(self):
        response = self.client.post(reverse('profile'), {
            'first_name': 'test',
            'last_name': 'test',
            'email': 'error'
        })

        self.assertContains(response, 'Enter a valid email address.')

    def test_profile_form_updates_staff_details(self):
        self.client.force_login(self.secretary)
        self.client.post(reverse('profile'), {
            'first_name': 'test',
            'last_name': 'test',
            'email': 'test@secretary2.com',
            'department': 'COM',
        })

        user = User.objects.get(email="test@secretary2.com")
        self.assertTrue(user)
    
    def test_invalid_profile_form_returns_error_for_staff(self):
        self.client.force_login(self.secretary)
        response = self.client.post(reverse('profile'), {
            'first_name': 'test',
            'last_name': 'test',
            'email': 'test',
            'department': 'COM',
        })

        self.assertContains(response, 'Enter a valid email address.')

    def test_profile_template_shows_support_plan(self):
        self.student_obj.support_plan = 'test.pdf'
        self.student_obj.save()
        
        response = self.client.get(reverse('profile'))
        self.assertContains(response, 'Support Plan')


class NotificationMarkReadViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.student = User.objects.create(
            email="test@test.com",
            password="testpassword"
        )

    def setUp(self):
        self.client.force_login(self.student)

    def test_notification_mark_read(self):
        notification = mock.Mock(spec=Notification)
        self.client.post(reverse('mark_read'))
        self.assertTrue(notification.viewed)


class DownloadViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.student = User.objects.create(
            email="test@test.com",
            password="testpassword"
        )

        cls.diff_student = User.objects.create(
            email="test@diff.com",
            password="testpassword"
        )

        support_plan = mock.MagicMock(spec=File)
        support_plan.name = 'support_plan.pdf'

        cls.student_obj = Student.objects.create(
            user=cls.student,
            course="Test",
            study_level=1,
            support_plan=support_plan
        )

        evidence = mock.MagicMock(spec=File)
        evidence.name = 'evidence.pdf'

        cls.app = ECFApplication.objects.create(
            applicant=cls.student,
            status=1,
            start_date='2021-01-01',
            circumstance=1,
            description='Test description',
            evidence=evidence
        )

    @override_settings(MEDIA_ROOT=(TEST_DIR + '/media'))
    def test_can_download_support_plan(self):
        self.client.force_login(self.student)
        response = self.client.post(reverse('download'), {
            'file': self.student_obj.support_plan.name
        })
        self.assertEqual(response.status_code, 200)

    @override_settings(MEDIA_ROOT=(TEST_DIR + '/media'))
    def test_can_download_application_evidence(self):
        self.client.force_login(self.student)
        response = self.client.post(reverse('download'), {
            'file': self.app.evidence.name
        })
        self.assertEqual(response.status_code, 200)

    def test_cannot_download_other_students_support_plan(self):
        self.client.force_login(self.diff_student)
        response = self.client.post(reverse('download'), {
            'file': self.student_obj.support_plan.name
        })
        self.assertEqual(response.status_code, 403)

    def test_cannot_download_other_students_application_evidence(self):
        self.client.force_login(self.diff_student)
        response = self.client.post(reverse('download'), {
            'file': self.app.evidence.name
        })
        self.assertEqual(response.status_code, 403)
    
    def test_invalid_file_type_returns_error(self):
        self.client.force_login(self.student)
        response = self.client.post(reverse('download'), {
            'file': 'invalid.pdf'
        })
        self.assertEqual(response.status_code, 403)


class PasswordChangeViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.student = User.objects.create_user(
            email="test@test.com",
            password="testpassword"
        )

    def setUp(self):
        self.client.force_login(self.student)

    def test_password_change_form_on_page(self):
        response = self.client.get(reverse('change_password'))
        self.assertContains(response, 'Old password')

    def test_password_change_form_updates_password(self):
        response = self.client.post(reverse('change_password'), {
            'old_password': 'testpassword',
            'new_password1': 'TestPassword!',
            'new_password2': 'TestPassword!'
        })
        user = User.objects.get(email="test@test.com")
        self.assertTrue(user.check_password('TestPassword!'))


def tearDownModule():
    shutil.rmtree(TEST_DIR, ignore_errors=True)