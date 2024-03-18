from django.contrib import messages
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView

from authentication.decorators import secretary_required, staff_required
from authentication.models import User
from dashboard.models import Notification
from ecf_applications.models import CODES as ECF_CODES
from ecf_applications.models import ECFApplication, ECFApplicationAssessment

from .forms import MeetingForm
from .models import Meeting, MeetingAgenda
from django.views.generic import UpdateView


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
        if request.POST.get("category") == "1":
            applications = ECFApplication.objects.filter(
                status=ECF_CODES["PENDING"],
                applicant__department=self.request.user.department
            )
        else:
            applications = self.get_exam_apps()

        if not applications.exists():
            messages.error(request, "Cannot create meeting with no agenda items")
            return redirect("meetings:new")
        
        form = MeetingForm(request.POST)

        if form.is_valid():
            meeting = MeetingForm(request.POST).save(commit=False)
            meeting.creator = request.user
            meeting.save()


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

            messages.success(request, "Meeting created successfully")
            return redirect("meetings:detail", pk=meeting.pk)
        
        return super().post(request, *args, **kwargs)

@method_decorator(staff_required, name="dispatch")
class MeetingDetailView(DetailView):
    model = Meeting
    template_name = "meetings/detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["agendas"] = MeetingAgenda.objects.filter(meeting=self.object)

        return context


@method_decorator(staff_required, name="dispatch")
class MeetingListView(ListView):
    model = Meeting
    template_name = "meetings/list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["scrutiny_meetings"] = Meeting.objects.filter(
            category=Meeting.SCRUTINY_PANEL,
            creator__department=self.request.user.department
        ).order_by("date_time")

        scrutiny_meeting_agendas_dict = {
            meeting.id: MeetingAgenda.objects.filter(meeting=meeting).count()
            for meeting in context["scrutiny_meetings"]
        }
        context["scrutiny_meeting_agendas"] = scrutiny_meeting_agendas_dict

        context["exam_meetings"] = Meeting.objects.filter(
            category=Meeting.EXAM_BOARD,
            creator__department=self.request.user.department
        ).order_by("date_time")

        exam_meeting_agendas_dict = {
            meeting.id: MeetingAgenda.objects.filter(meeting=meeting).count()
            for meeting in context["exam_meetings"]
        }
        context["exam_meeting_agendas"] = exam_meeting_agendas_dict

        return context
    

@method_decorator(secretary_required, name="dispatch")
class MeetingUpdateView(UpdateView):
    model = Meeting
    template_name = "meetings/update.html"
    form_class = MeetingForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["agenda_count"] = MeetingAgenda.objects.filter(
            meeting=self.object).count()

        return context
    
    def get_success_url(self):
        messages.success(self.request, "Meeting updated successfully")
        return super().get_success_url()