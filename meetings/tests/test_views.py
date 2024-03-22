from django.test import TestCase
from django.urls import reverse

from authentication.models import User
from meetings.models import Meeting, MeetingAgenda
from ecf_applications.models import ECFApplication, ECFApplicationAssessment, CODES
from django.utils import timezone


class MeetingCreateViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        student = User.objects.create(
            email="test@test.com",
            password="testpassword",
            role=User.STUDENT,
            department="COM"
        )

        cls.secretary = User.objects.create(
            email="test@secretary.com",
            password="testpassword",
            role=User.SECRETARY,
            department="COM"
        )

        cls.scrutiny_app = ECFApplication.objects.create(
            applicant=student,
            start_date='2021-01-01',
            circumstance=1,
            description='Test description'
        )

        app = ECFApplication.objects.create(
            applicant=student,
            start_date='2021-01-01',
            circumstance=1,
            description='Test description',
            status=CODES["UNDER_REVIEW"]
        )

        ECFApplicationAssessment.objects.create(
            application=app,
            module='test',
            assessment='test',
            action=2,
            description='test'
        )
            

    def setUp(self):
        self.client.force_login(self.secretary)

    def test_correct_template_used(self):
        response = self.client.get(reverse('meetings:new'))
        self.assertTemplateUsed(response, 'meetings/new.html')

    def test_can_create_scrutiny_panel_meeting(self):
        response = self.client.post(reverse('meetings:new'), {
            'creator': self.secretary.id,
            'date_time': '3000-01-01',
            'category': Meeting.SCRUTINY_PANEL,
        })
        self.assertEqual(response.status_code, 302)

    def test_can_create_exam_board_meeting(self):
        response = self.client.post(reverse('meetings:new'), {
            'creator': self.secretary.id,
            'date_time': '3000-01-01',
            'category': Meeting.EXAM_BOARD,
        })
        self.assertEqual(response.status_code, 302)

    def test_cannot_create_meeting_without_applications(self):
        self.scrutiny_app.delete()
        response = self.client.post(reverse('meetings:new'), {
            'creator': self.secretary.id,
            'date_time': '3000-01-01',
            'category': Meeting.SCRUTINY_PANEL,
        })
        self.assertRedirects(response, reverse('meetings:new'))

    def test_invalid_form_returns_error(self):
        response = self.client.post(reverse('meetings:new'), {
            'creator': self.secretary.id,
            'date_time': 'invalid',
            'category': Meeting.EXAM_BOARD,
        })
        self.assertEqual(response.status_code, 200)


class MeetingDetailViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.secretary = User.objects.create(
            email="test@secretary.com",
            password="testpassword",
            role=User.SECRETARY,
            department="COM"
        )

        cls.meeting = Meeting.objects.create(
            creator=cls.secretary,
            date_time=timezone.now(),
            category=Meeting.SCRUTINY_PANEL,
        )

        MeetingAgenda.objects.create(
            meeting=cls.meeting,
            application=ECFApplication.objects.create(
                applicant=cls.secretary,
                start_date='2021-01-01',
                circumstance=1,
                description='Test description'
            ),
        )

    def setUp(self):
        self.client.force_login(self.secretary)

    def test_correct_template_used(self):
        response = self.client.get(reverse('meetings:detail', args=[self.meeting.id]))
        self.assertTemplateUsed(response, 'meetings/detail.html')

    def test_meeting_in_future_adjusts_info(self):
        self.meeting.date_time = timezone.now() + timezone.timedelta(days=1)
        self.meeting.save()
        response = self.client.get(reverse('meetings:detail', args=[self.meeting.id]))
        self.assertContains(response, 'This meeting is on')


class MeetingListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.secretary = User.objects.create(
            email="test@secretary.com",
            password="testpassword",
            role=User.SECRETARY,
            department="COM"
        )

        Meeting.objects.create(
            creator=cls.secretary,
            date_time=timezone.now(),
            category=Meeting.SCRUTINY_PANEL,
        )

        Meeting.objects.create(
            creator=cls.secretary,
            date_time=timezone.now(),
            category=Meeting.EXAM_BOARD,
        )

    def setUp(self):
        self.client.force_login(self.secretary)

    def test_correct_template_used(self):
        response = self.client.get(reverse('meetings:list'))
        self.assertTemplateUsed(response, 'meetings/list.html')

    def test_no_meetings_shows_message(self):
        Meeting.objects.all().delete()
        response = self.client.get(reverse('meetings:list'))
        self.assertContains(response, 'There are no meetings.')


class MeetingUpdateViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.secretary = User.objects.create(
            email="test@secretary.com",
            password="testpassword",
            role=User.SECRETARY,
            department="COM"
        )

        cls.meeting = Meeting.objects.create(
            creator=cls.secretary,
            date_time=timezone.now(),
            category=Meeting.SCRUTINY_PANEL,
        )

    def setUp(self):
        self.client.force_login(self.secretary)

    def test_correct_template_used(self):
        response = self.client.get(reverse('meetings:update', args=[self.meeting.id]))
        self.assertTemplateUsed(response, 'meetings/update.html')

    def test_can_update_meeting(self):
        response = self.client.post(reverse('meetings:update', args=[self.meeting.id]), {
            'creator': self.secretary.id,
            'date_time': '3000-01-01',
            'category': Meeting.SCRUTINY_PANEL,
        })
        self.assertEqual(response.status_code, 302)