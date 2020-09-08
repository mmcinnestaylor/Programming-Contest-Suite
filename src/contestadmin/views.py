import os

from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse

from io import BytesIO
from zipfile import ZipFile

from contestsuite.settings import MEDIA_ROOT

# Create your views here.


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
    response["Content-Disposition"] = "attachment; filename=ec_files.zip"
    
    in_memory.seek(0)    
    response.write(in_memory.read())
    
    return response
