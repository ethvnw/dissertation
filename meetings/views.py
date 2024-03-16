from typing import Any
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView

from authentication.decorators import scrutiny_required, secretary_required
from ecf_applications.models import CODES as ECF_CODES
from ecf_applications.models import ECFApplication, ECFApplicationAssessment

from .forms import MeetingForm
from .models import Meeting, MeetingAgenda


@method_decorator(secretary_required, name="dispatch")
class MeetingCreateView(CreateView):
    model = Meeting
    template_name = "meetings/new.html"
    form_class = MeetingForm

    def get_exam_apps(self):
        exam_assessments = ECFApplicationAssessment.objects.filter(
            action=ECFApplicationAssessment.EXAM_BOARD_CONSIDERATION,
            application__status=ECF_CODES["UNDER_REVIEW"],
            application__applicant__department=self.request.user.department
        )

        applications = ECFApplication.objects.filter(
            id__in=[assessment.application.id for assessment in exam_assessments]
        )

        return applications


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        num_scrutiny_apps = ECFApplication.objects.filter(
            status=ECF_CODES["PENDING"],
            applicant__department=self.request.user.department
        ).count()
        context["num_scrutiny_apps"] = num_scrutiny_apps

        num_exam_apps = self.get_exam_apps().count()
        context["num_exam_apps"] = num_exam_apps

        return context
            

    def post(self, request, *args, **kwargs):
        meeting = MeetingForm(request.POST).save(commit=False)
        meeting.creator = request.user
        meeting.save()

        if meeting.category == Meeting.SCRUTINY_PANEL:
            applications = ECFApplication.objects.filter(
                status=ECF_CODES["PENDING"],
                applicant__department=self.request.user.department
            )

        else:
            applications = self.get_exam_apps()

        MeetingAgenda.objects.bulk_create([
            MeetingAgenda(
                application=app,
                meeting=meeting
            )
            for app in applications
        ])

        if meeting.category == Meeting.SCRUTINY_PANEL:
            applications.update(status=ECF_CODES["UNDER_REVIEW"])
        else:
           applications.update(status=ECF_CODES["UNDER_EXAM_REVIEW"])

        return redirect("meetings:detail", pk=meeting.pk)
        

@method_decorator(secretary_required, name="dispatch")
class MeetingDetailView(DetailView):
    model = Meeting
    template_name = "meetings/detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["agendas"] = MeetingAgenda.objects.filter(meeting=self.object)

        return context


class MeetingListView(ListView):
    model = Meeting
    template_name = "meetings/list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["scrutiny_meetings"] = Meeting.objects.filter(
            category=Meeting.SCRUTINY_PANEL,
            creator__department=self.request.user.department
        )

        scrutiny_meeting_agendas_dict = {
            meeting.id: MeetingAgenda.objects.filter(meeting=meeting).count()
            for meeting in context["scrutiny_meetings"]
        }
        context["scrutiny_meeting_agendas"] = scrutiny_meeting_agendas_dict

        context["exam_meetings"] = Meeting.objects.filter(
            category=Meeting.EXAM_BOARD,
            creator__department=self.request.user.department
        )

        exam_meeting_agendas_dict = {
            meeting.id: MeetingAgenda.objects.filter(meeting=meeting).count()
            for meeting in context["exam_meetings"]
        }
        context["exam_meeting_agendas"] = exam_meeting_agendas_dict

        return context