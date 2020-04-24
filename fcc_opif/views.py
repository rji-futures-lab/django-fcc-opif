from django.shortcuts import render, get_object_or_404
from fcc_opif.models import FacilityFile, CableFile
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.forms.models import model_to_dict
from django.conf import settings

@login_required()
def facilityfile(request, file_id):
    file = get_object_or_404(
        FacilityFile, file_id=file_id
    )

    return render(
        request,
        'fcc_opif/template_maker.html',
        {'file_url': file.stored_file.url, 'file_id': file_id}
    )

@login_required()
def cablesystemfile(request, file_id):
    file = get_object_or_404(
        CableFile, file_id=file_id
    )

    return render(
        request,
        'fcc_opif/template_maker.html',
        {'file_url': file.stored_file.url, 'file_id': file_id}
    )