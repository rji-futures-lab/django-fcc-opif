from django.shortcuts import render, get_object_or_404
from fcc_opif.models import FacilityFile
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.forms.models import model_to_dict

@login_required()
def facilityfile(request, file_id):
    print(file_id)
    file = get_object_or_404(FacilityFile, file_id=file_id)
    return render(request, 'fcc_opif/facility_file.html', {'file': model_to_dict(file)})

@login_required()
def cablefile(request, file_id):
    file = get_object_or_404(CableFile, file_id=file_id)
    return render(request, 'fcc_opif/cable_file.html', {'file': model_to_dict(file)})