from django.test import TestCase
from ecf_applications.forms import ECFApplicationForm

class ECFApplicationFormTest(TestCase):
    def test_start_date_in_future_raises_error(self):
        form = ECFApplicationForm(data={
            'circumstance': 1,
            'start_date': '3000-01-01',
            'ongoing': True,
            'description': 'Test description'
        })
        self.assertFalse(form.is_valid())
        self.assertTrue(form.errors['start_date'])

    def test_end_date_before_start_date_raises_error(self):
        form = ECFApplicationForm(data={
            'circumstance': 1,
            'start_date': '2000-01-01',
            'ongoing': False,
            'end_date': '1950-01-01',
            'description': 'Test description'
        })
        self.assertFalse(form.is_valid())
        self.assertTrue(form.errors['end_date'])

    def test_end_date_after_start_date_does_not_raise_error(self):
        form = ECFApplicationForm(data={
            'circumstance': 1,
            'start_date': '1950-01-01',
            'ongoing': False,
            'end_date': '2000-01-01',
            'description': 'Test description'
        })
        self.assertTrue(form.is_valid())
