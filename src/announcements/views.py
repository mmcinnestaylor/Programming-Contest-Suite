from django.shortcuts import render
from django.utils import timezone
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from .models import Announcement
from contestsuite.settings import CACHE_TIMEOUT

# Create your views here.


class AnnouncementListView(ListView):

    model = Announcement
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        context['cache_timeout'] = CACHE_TIMEOUT
        return context


class AnnouncementDetailView(DetailView):

    model = Announcement

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        context['cache_timeout'] = CACHE_TIMEOUT
        return context
