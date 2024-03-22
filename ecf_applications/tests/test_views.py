import shutil
from unittest import mock

from django.core.files import File
from django.test import TestCase, override_settings
from django.urls import reverse

from authentication.models import Student, User
from ecf_applications.models import CODES as ECF_CODES
from ecf_applications.models import (ECFApplication, ECFApplicationAssessment,
                                     ECFApplicationAssessmentComment,
                                     ECFApplicationComment)

TEST_DIR = 'test_files'

class NewECFApplicationWizardViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.student = User.objects.create(
            email="test@test.com",
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

    def setUp(self):
        self.client.force_login(self.student)

    def test_new_ecf_application_wizard_view_uses_correct_template(self):
        response = self.client.get(reverse('ecf_application:new'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'ecf_applications/new/application_form.html')

    def test_no_support_plan_shows_message(self):
        self.student_obj.support_plan = None
        self.student_obj.save()

        response = self.client.get(reverse('ecf_application:new'))
        self.assertContains(response, 'You do not have a learning support plan')

    def test_completing_first_form_displays_second_form(self):
        response = self.client.post(reverse('ecf_application:new'), {
            'new_ecf_application_wizard_view-current_step': 'application_form',
            'application_form-start_date': '2021-01-01',
            'application_form-ongoing': 'True',
            'application_form-circumstance': 1,
            'application_form-description': 'Test description'
        })

        self.assertTemplateUsed(response, 'ecf_applications/new/assessment_form.html')

    def test_no_support_plan_shows_message_on_second_form(self):
        self.student_obj.support_plan = None
        self.student_obj.save()
        response = self.client.post(reverse('ecf_application:new'), {
            'new_ecf_application_wizard_view-current_step': 'application_form',
            'application_form-start_date': '2021-01-01',
            'application_form-ongoing': 'True',
            'application_form-circumstance': 1,
            'application_form-description': 'Test description'
        })

        self.assertTemplateUsed(response, 'ecf_applications/new/assessment_form.html')

    def test_completing_second_form_redirects_to_success_page(self):
        self.client.post(reverse('ecf_application:new'), {
            'new_ecf_application_wizard_view-current_step': 'application_form',
            'application_form-start_date': '2021-01-01',
            'application_form-ongoing': 'True',
            'application_form-circumstance': 1,
            'application_form-description': 'Test description'
        })

        response = self.client.post(reverse('ecf_application:new'), {
            'new_ecf_application_wizard_view-current_step': 'assessment_formset',
            'assessment_formset-TOTAL_FORMS': 1,
            'assessment_formset-INITIAL_FORMS': 0,
            'assessment_formset-0-module':'test',
            'assessment_formset-0-assessment': 'test',
            'assessment_formset-0-action': 1,
            'assessment_formset-0-description': 'test'
        })

        self.assertRedirects(response, reverse('ecf_application:success'))

    def test_can_go_back_to_previous_step(self):
        self.client.post(reverse('ecf_application:new'), {
            'new_ecf_application_wizard_view-current_step': 'application_form',
            'application_form-start_date': '2021-01-01',
            'application_form-ongoing': 'True',
            'application_form-circumstance': 1,
            'application_form-description': 'Test description'
        })

        response = self.client.post(reverse('ecf_application:new'), {
            'new_ecf_application_wizard_view-current_step': 'assessment_formset',
            'assessment_formset-TOTAL_FORMS': 1,
            'assessment_formset-INITIAL_FORMS': 0,
            'assessment_formset-0-module':'test',
            'assessment_formset-0-assessment': 'test',
            'assessment_formset-0-action': 1,
            'assessment_formset-0-description': 'test',
            'wizard_goto_step': 'application_form'
        })

        self.assertContains(response, 'Test description')

    def test_cannot_go_back_to_previous_step_if_form_invalid(self):
        self.client.post(reverse('ecf_application:new'), {
            'new_ecf_application_wizard_view-current_step': 'application_form',
            'application_form-start_date': '2021-01-01',
            'application_form-ongoing': 'True',
            'application_form-circumstance': 1,
            'application_form-description': 'Test description'
        })

        response = self.client.post(reverse('ecf_application:new'), {
            'new_ecf_application_wizard_view-current_step': 'assessment_formset',
            'wizard_goto_step': 'application_form'
        })

        self.assertContains(response, 'error')

    @override_settings(MEDIA_ROOT=(TEST_DIR + '/media'))
    def test_evidence_file_is_renamed(self):
        file = mock.MagicMock(spec=File)
        file.name = 'evidence.pdf'

        self.client.post(reverse('ecf_application:new'), {
            'new_ecf_application_wizard_view-current_step': 'application_form',
            'application_form-start_date': '2021-01-01',
            'application_form-ongoing': 'True',
            'application_form-circumstance': 1,
            'application_form-description': 'Test description',
            'application_form-evidence': file
        })

        self.client.post(reverse('ecf_application:new'), {
            'new_ecf_application_wizard_view-current_step': 'assessment_formset',
            'assessment_formset-TOTAL_FORMS': 1,
            'assessment_formset-INITIAL_FORMS': 0,
            'assessment_formset-0-module':'test',
            'assessment_formset-0-assessment': 'test',
            'assessment_formset-0-action': 1,
            'assessment_formset-0-description': 'test'
        })

        application = ECFApplication.objects.get(applicant=self.student)
        self.assertNotEqual(application.evidence.name, file.name)


class ECFApplicationDetailViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.student = User.objects.create(
            email="test@test.com",
            password="testpassword",
            department="COM"
        )

        support_plan = mock.MagicMock(spec=File)
        support_plan.name = 'support_plan.pdf'

        cls.student_obj = Student.objects.create(
            user=cls.student,
            course="Test",
            study_level=1,
            support_plan=support_plan
        )

        cls.diff_student = User.objects.create(
            email="test@different.com",
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

        evidence = mock.MagicMock(spec=File)
        evidence.name = 'evidence.pdf'

        cls.app = ECFApplication.objects.create(
            applicant=cls.student,
            start_date='2021-01-01',
            circumstance=1,
            description='Test description',
            evidence=evidence
        )

        cls.assess = ECFApplicationAssessment.objects.create(
            application=cls.app,
            module='test',
            assessment='test',
            action=3,
            extension_date='2021-01-01',
            description='test'
        )

        ECFApplicationComment.objects.create(
            application=cls.app,
            user=cls.secretary,
            comment="Test comment"
        )

        ECFApplicationAssessmentComment.objects.create(
            assessment=cls.assess,
            user=cls.secretary,
            comment="Test comment"
        )


    def test_correct_template_used_for_student(self):
        self.client.force_login(self.student)
        response = self.client.get(reverse('ecf_application:detail', 
            args=[self.app.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'ecf_applications/detail/student_detail.html')

    def test_correct_template_used_for_secretary(self):
        self.client.force_login(self.secretary)
        response = self.client.get(reverse('ecf_application:detail', 
            args=[self.app.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'ecf_applications/detail/secretary_detail.html')

    def test_no_application_evidence_allows_secretary_to_send_reminder(self):
        self.app.evidence = None
        self.app.save()

        self.client.force_login(self.secretary)
        response = self.client.get(reverse('ecf_application:detail', 
            args=[self.app.id])
        )
        self.assertEqual(response.status_code, 200)

    def test_correct_template_used_for_scrutiny(self):
        self.client.force_login(self.scrutiny)
        response = self.client.get(reverse('ecf_application:detail', 
            args=[self.app.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'ecf_applications/detail/scrutiny_detail.html')

    def test_students_cannot_view_other_students_applications(self):
        self.client.force_login(self.diff_student)
        response = self.client.get(reverse('ecf_application:detail', 
            args=[self.app.id])
        )
        self.assertEqual(response.status_code, 403)

    def test_student_redirected_to_edit_view_if_application_not_action_required(self):
        self.client.force_login(self.student)
        self.app.status = ECF_CODES["ACTION_REQUIRED"]
        self.app.save()

        response = self.client.get(reverse('ecf_application:detail', args=[self.app.id]))
        self.assertRedirects(response, reverse('ecf_application:edit', args=[self.app.id]))

    def test_student_can_upload_evidence(self):
        self.client.force_login(self.student)
        self.app.status = ECF_CODES["ACTION_REQUIRED"]
        self.app.save()

        response = self.client.post(reverse('ecf_application:detail', args=[self.app.id]), {
            'evidence': mock.MagicMock(spec=File, name='evidence.pdf')
        })

        self.assertEqual(response.status_code, 302)


class EvidenceReminderViewTest(TestCase):
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

        cls.app = ECFApplication.objects.create(
            applicant=cls.student,
            start_date='2021-01-01',
            circumstance=1,
            description='Test description'
        )

    def test_can_send_reminder(self):
        self.client.force_login(self.secretary)
        response = self.client.post(reverse('ecf_application:reminder',
            args=[self.app.id])
        )
        self.assertEqual(response.status_code, 302)


class CommentSendViewTest(TestCase):
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

        cls.app = ECFApplication.objects.create(
            applicant=cls.student,
            start_date='2021-01-01',
            circumstance=1,
            description='Test description'
        )

        cls.assess = ECFApplicationAssessment.objects.create(
            application=cls.app,
            module='test',
            assessment='test',
            action=1,
            description='test'
        )

    def test_can_comment_on_main_application(self):
        self.client.force_login(self.secretary)
        response = self.client.post(
            reverse('ecf_application:comment',
            args=[self.app.id]),
            {"application-comment": "Test comment"}
        )
        self.assertEqual(response.status_code, 302)

    def test_can_comment_on_assessment(self):
        self.client.force_login(self.secretary)
        response = self.client.post(
            reverse('ecf_application:comment',
            args=[self.app.id]),
            {f"assessment-{self.assess.id}-comment": "Test comment"}
        )
        self.assertEqual(response.status_code, 302)

    def test_can_comment_on_main_application_and_assessment_with_garbage_data(self):
        self.client.force_login(self.secretary)
        response = self.client.post(
            reverse('ecf_application:comment',
            args=[self.app.id]),
            {
                "application-comment": "Test comment",
                f"assessment-{self.assess.id}-comment": "Test comment",
                "dsondas": "asdasd",
            }
        )
        self.assertEqual(response.status_code, 302)


class ECFApplicationEditViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.student = User.objects.create(
            email="test@test.com",
            password="testpassword",
            department="COM"
        )

        cls.diff_student = User.objects.create(
            email="test@diff.com",
            password="testpassword",
            department="COM"
        )

        cls.app = ECFApplication.objects.create(
            applicant=cls.student,
            start_date='2021-01-01',
            circumstance=1,
            description='Test description',
            status=ECF_CODES["ACTION_REQUIRED"]
        )

        cls.assess = ECFApplicationAssessment.objects.create(
            application=cls.app,
            module='test',
            assessment='test',
            action=1,
            description='test'
        )

        cls.assess2 = ECFApplicationAssessment.objects.create(
            application=cls.app,
            module='test2',
            assessment='test2',
            action=1,
            description='test2'
        )

        cls.app_comment = ECFApplicationComment.objects.create(
            application=cls.app,
            user=cls.student,
            comment="Test comment"
        )

        cls.assess_comment1 = ECFApplicationAssessmentComment.objects.create(
            assessment=cls.assess,
            user=cls.student,
            comment="Test comment"
        )

        cls.assess_comment2 = ECFApplicationAssessmentComment.objects.create(
            assessment=cls.assess,
            user=cls.student,
            comment="Test comment"
        )

        cls.assess_comment3 = ECFApplicationAssessmentComment.objects.create(
            assessment=cls.assess2,
            user=cls.student,
            comment="Test comment"
        )
        
    def test_correct_template_used_for_student(self):
        self.client.force_login(self.student)
        response = self.client.get(reverse('ecf_application:edit', 
            args=[self.app.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'ecf_applications/edit.html')
        
    def test_students_cannot_edit_other_students_applications(self):
        self.client.force_login(self.diff_student)
        response = self.client.get(reverse('ecf_application:edit', 
            args=[self.app.id])
        )
        self.assertEqual(response.status_code, 403)

    def test_cannot_edit_application_if_not_action_required(self):
        self.client.force_login(self.student)
        self.app.status = ECF_CODES["PENDING"]
        self.app.save()

        response = self.client.get(reverse('ecf_application:edit', args=[self.app.id]))
        self.assertRedirects(response, reverse('ecf_application:detail', args=[self.app.id]))

    def test_can_edit_application(self):
        self.client.force_login(self.student)
        response = self.client.post(reverse('ecf_application:edit', args=[self.app.id]), {
            'application_form-circumstance': 2,
            'application_form-start_date': '2021-01-01',
            'application_form-ongoing': 'True',
            'application_form-description': 'Test description',

            'form-TOTAL_FORMS': 2,
            'form-INITIAL_FORMS': 2,

            'form-0-id': self.assess.id,
            'form-0-module': 'test',
            'form-0-assessment': 'test',
            'form-0-action': 1,
            'form-0-description': 'test',

            'form-1-id': self.assess2.id,
            'form-1-module': 'test2',
            'form-1-assessment': 'test2',
            'form-1-action': 1,
            'form-1-description': 'test2'
        })
        self.assertEqual(response.status_code, 302)

    def test_invalid_application_form_throws_error(self):
        self.client.force_login(self.student)
        response = self.client.post(reverse('ecf_application:edit', args=[self.app.id]), {
        })
        self.assertEqual(response.status_code, 200)
        
    def test_invalid_assessment_formset_throws_error(self):
        self.client.force_login(self.student)
        response = self.client.post(reverse('ecf_application:edit', args=[self.app.id]), {
            'application_form-circumstance': 2,
            'application_form-start_date': '2021-01-01',
            'application_form-ongoing': 'True',
            'application_form-description': 'Test description',
        })
        self.assertEqual(response.status_code, 200)   

    def test_can_edit_without_application_comments(self):
        self.client.force_login(self.student)
        self.app_comment.delete()

        response = self.client.post(reverse('ecf_application:edit', args=[self.app.id]), {
            'form-TOTAL_FORMS': 2,
            'form-INITIAL_FORMS': 2,

            'form-0-id': self.assess.id,
            'form-0-module': 'test',
            'form-0-assessment': 'test',
            'form-0-action': 1,
            'form-0-description': 'test',

            'form-1-id': self.assess2.id,
            'form-1-module': 'test2',
            'form-1-assessment': 'test2',
            'form-1-action': 1,
            'form-1-description': 'test2'
        })
        self.assertEqual(response.status_code, 302)

    def test_can_edit_without_assessment_comments(self):
        self.client.force_login(self.student)
        self.assess_comment1.delete()
        self.assess_comment2.delete()
        self.assess_comment3.delete()

        response = self.client.post(reverse('ecf_application:edit', args=[self.app.id]), {
            'application_form-circumstance': 2,
            'application_form-start_date': '2021-01-01',
            'application_form-ongoing': 'True',
            'application_form-description': 'Test description',
        })
        self.assertEqual(response.status_code, 302)


class ECFApplicationListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.student = User.objects.create(
            email="test@test.com",
            password="testpassword",
            department="COM"
        )

        cls.app = ECFApplication.objects.create(
            applicant=cls.student,
            start_date='2021-01-01',
            circumstance=1,
            description='Test description'
        )

        cls.finalised_app = ECFApplication.objects.create(
            applicant=cls.student,
            start_date='2021-01-01',
            circumstance=1,
            description='Test description',
            status=ECF_CODES["APPROVED"]
        )

        cls.secretary = User.objects.create(
            email="test@secretary.com",
            password="testpassword",
            role=User.SECRETARY,
            department="COM"
        )

    def setUp(self):
        self.client.force_login(self.secretary)

    def test_correct_template_used(self):
        response = self.client.get(reverse('ecf_application:list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'ecf_applications/list.html')

    def test_no_applications_message(self):
        self.app.delete()
        self.finalised_app.delete()
        response = self.client.get(reverse('ecf_application:list'))
        self.assertContains(response, 'There are no ongoing applications')


class ECFApplicationDecisionViewTest(TestCase):
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

        cls.app = ECFApplication.objects.create(
            applicant=cls.student,
            start_date='2021-01-01',
            circumstance=1,
            description='Test description'
        )

        cls.assess = ECFApplicationAssessment.objects.create(
            application=cls.app,
            module='test',
            assessment='test',
            action=3,
            extension_date='2021-01-01',
            description='test'
        )

        cls.assess2 = ECFApplicationAssessment.objects.create(
            application=cls.app,
            module='test2',
            assessment='test2',
            action=1,
            description='test2'
        )

        ECFApplicationAssessmentComment.objects.create(
            assessment=cls.assess,
            user=cls.secretary,
            comment="Test comment"
        )


    def test_correct_template_used(self):
        self.client.force_login(self.secretary)
        response = self.client.get(reverse('ecf_application:decision', args=[self.app.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'ecf_applications/decision.html')

    def test_can_make_decisions(self):
        self.client.force_login(self.secretary)
        response = self.client.post(reverse('ecf_application:decision', args=[self.app.id]), {
            f'{self.assess.id}-decision': 'approve',
            f'{self.assess2.id}-decision': 'reject',
        })
        self.assertEqual(response.status_code, 302)

    def test_garbage_data_does_not_throw_error(self):
        self.client.force_login(self.secretary)
        response = self.client.post(reverse('ecf_application:decision', args=[self.app.id]), {
            'asdasd': 'asdasd'
        })
        self.assertEqual(response.status_code, 302)

    def test_all_assessments_approved_makes_application_approved(self):
        self.client.force_login(self.secretary)
        self.client.post(reverse('ecf_application:decision', args=[self.app.id]), {
            f'{self.assess.id}-decision': 'approve',
            f'{self.assess2.id}-decision': 'approve',
        })

        app = ECFApplication.objects.get(id=self.app.id)
        self.assertEqual(app.status, ECF_CODES["APPROVED"])
        
    def test_all_assessments_rejected_makes_application_rejected(self):
        self.client.force_login(self.secretary)
        self.client.post(reverse('ecf_application:decision', args=[self.app.id]), {
            f'{self.assess.id}-decision': 'reject',
            f'{self.assess2.id}-decision': 'reject',
        })

        app = ECFApplication.objects.get(id=self.app.id)
        self.assertEqual(app.status, ECF_CODES["REJECTED"])

def tearDownModule():
    shutil.rmtree(TEST_DIR, ignore_errors=True)