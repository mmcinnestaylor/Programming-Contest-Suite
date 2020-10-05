import os

from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.shortcuts import redirect, render

from io import BytesIO
from zipfile import ZipFile

from . import forms
from . import tasks
from contestsuite.settings import MEDIA_ROOT
from manager.models import Course, Profile
from register.models import Team

# Create your views here.


class FacExtraCreditFiles(View):

    def serve(self, request, uidb64):
        try:
            faculty_member = force_text(urlsafe_base64_decode(uidb64))
            #user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            faculty_member = None

        if faculty_member is not None:
            in_memory = BytesIO()
            zip = ZipFile(in_memory, 'a')

            fpath = MEDIA_ROOT + '/ec_files/'
            for fname in os.listdir(fpath):
                    if faculty_member in fname:
                        zip.write(fpath+fname, fname)

                # fix for Linux zip files read in Windows
                for file in zip.filelist:
                    file.create_system = 0

                zip.close()

                response = HttpResponse(content_type='application/zip')
                response['Content-Disposition'] = 'attachment; filename=' + faculty_member + '_ec_files.zip'

                in_memory.seek(0)
                response.write(in_memory.read())

                return response
        else:
            return HttpResponse('Unable to serve extra credit files. Please try again later or contact the ACM team.')


@staff_member_required
def dashboard(request):
    context = {}

    if request.method == 'POST':
        walkin_form = forms.GenerateWalkinForm(request.POST)

        if walkin_form.is_valid():
            if walkin_form.cleaned_data['total'] and walkin_form.cleaned_data['division']:
                tasks.create_walkin_teams.delay(int(walkin_form.cleaned_data['division']), int(walkin_form.cleaned_data['total']))
                
                messages.info(request, 'Create teams task scheduled.', fail_silently=True)
                return redirect('admin_dashboard')

    else:
        forms.GenerateWalkinForm()

    context['users_registered'] = User.objects.all().count()
    context['users_verified'] = User.objects.filter(is_active=True).count()
    context['added_fsu_num'] = Profile.objects.exclude(fsu_num=None).count()
    context['added_fsu_id'] = Profile.objects.exclude(fsu_id=None).count()
    context['added_courses'] = Profile.objects.exclude(courses=None).count()

    context['total_teams'] = Team.objects.all().count()
    context['registered_teams'] = Team.objects.exclude(name__contains='Walk-in-').count()
    context['total_walkin'] = Team.objects.filter(name__contains='Walk-in-').count()
    context['walkin_used'] = Team.objects.filter(name__contains='Walk-in-').exclude(num_members=0).count()

    context['num_upper_teams'] = Team.objects.filter(division=1).exclude(name__contains='Walk-in-').count()
    context['num_upper_reg_participants'] = Profile.objects.filter(team__division=1).exclude(team__name__contains='Walk-in-').count()
    context['num_upper_walkin_participants'] = Profile.objects.filter(team__division=1).filter(team__name__contains='Walk-in-').count()

    context['num_lower_teams'] = Team.objects.filter(division=2).exclude(name__contains='Walk-in-').count()
    context['num_lower_reg_participants'] = Profile.objects.filter(team__division=2).exclude(team__name__contains='Walk-in-').count()
    context['num_lower_walkin_participants'] = Profile.objects.filter(team__division=2).filter(team__name__contains='Walk-in-').count()

    context['gen_walkin_form'] = forms.GenerateWalkinForm()
    context['courses'] = Course.objects.all()
    return render(request, 'contestadmin/dashboard.html', context)


@staff_member_required
def download_ec_files(request):
    in_memory = BytesIO()
    zip = ZipFile(in_memory, "a")
    
    fpath = MEDIA_ROOT + '/ec_files/'
    for fname in os.listdir(fpath):
        zip.write(fpath+fname, fname)

    # fix for Linux zip files read in Windows
    for file in zip.filelist:
        file.create_system = 0 

    zip.close()

    response = HttpResponse(content_type="application/zip")
    response["Content-Disposition"] = "attachment; filename=all_ec_files.zip"
    
    in_memory.seek(0)    
    response.write(in_memory.read())
    
    return response
