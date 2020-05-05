from django.shortcuts import render, get_object_or_404
from fcc_opif.models import FacilityFile, CableFile, FileForm
from django.views import generic
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.contrib.auth.decorators import login_required
from django.forms.models import model_to_dict
from django.conf import settings
from .forms import FileFormForm

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

class FileFormList(ListView):

    model = FileForm
    paginate_by = 100
    template = 'fcc_opic/fileform_list.html'

class FileFormCreate(CreateView):

    model = FileForm
    fields = ['name']
    template_name_suffix = '_create'
    success_url = '/fcc_opif/fileform_list'

def update_form(request):
    if request.method == 'POST':
        form = FileFormForm(request.POST)
        if form.is_valid():
            relative_url = form.data['url'].lstrip(settings.MEDIA_URL)
            file = FacilityFile.objects.get(stored_file = relative_url)
            fileform = FileForm.objects.get(name=form.data['name'])
            fileform.proto_file_field = file.file_id
            fileform.boxes = form.data['boxes']
            fileform.save()
    else:
        form = FileFormForm()

    return render(request, 'fcc_opif/form_maker.html', {'form': form})
