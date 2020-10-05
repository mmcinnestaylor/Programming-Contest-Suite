import os

from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode

from io import BytesIO
from zipfile import ZipFile

from contestsuite.settings import MEDIA_ROOT

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
