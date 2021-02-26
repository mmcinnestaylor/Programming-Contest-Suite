from django.contrib.admin.views.decorators import staff_member_required
from django.urls import path

from . import views

urlpatterns = [
    path('', views.dashboard, name='admin_dashboard'),
    path('dj_tsv/download', staff_member_required(views.DownloadTSVFiles.as_view()), name='download_dj_files'),
    path('dj_tsv/generate', staff_member_required(views.GenerateDomJudgeTSV.as_view()), name='gen_dj_files'),
    path('ec_files/download', staff_member_required(views.DownloadExtraCreditFiles.as_view()), name='download_ec_files'),
    path('ec_files/email_faculty', staff_member_required(views.EmailFaculty.as_view()), name='email_faculty'),
    path('ec_files/generate', staff_member_required(views.GenerateExtraCreditReports.as_view()), name='gen_ec_reports'),
    path('faculty/<uidb64>/', views.FacultyDashboard.as_view(), name='fac_ec_dashboard'),
    path('faculty/<uidb64>/download', views.FacultyDashboard.download, name='fac_ec_files_dl'),
]
