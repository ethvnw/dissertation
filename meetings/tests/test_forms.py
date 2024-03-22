from django.test import TestCase

from meetings.forms import MeetingForm
from meetings.models import Meeting


class MeetingFormTest(TestCase):
    def test_date_in_past_throws_error(self):
        form = MeetingForm(data={
            'creator': 'test',
            'date_time': '2019-01-01',
            'category': Meeting.EXAM_BOARD,
        })
        self.assertFalse(form.is_valid())
        self.assertTrue(form.errors['date_time'])
          
    def test_date_in_future_passes(self):
        form = MeetingForm(data={
            'creator': 'test',
            'date_time': '3000-01-01',
            'category': Meeting.EXAM_BOARD,
        })
        self.assertTrue(form.is_valid())        