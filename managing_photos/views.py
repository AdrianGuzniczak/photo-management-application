import json
import tempfile
import urllib
import urllib.request
from rest_framework.renderers import JSONRenderer
import requests
from django.views.generic import ListView, UpdateView, TemplateView
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.core import files
from django.shortcuts import redirect
from .models import Photo
from .serializers import PhotoSerializer
from .forms import PhotoForm




def create_photo(request):
    if request.method == 'POST':
        form = PhotoForm(request.POST)
        if form.is_valid():
            form.save()
    return redirect('managing_photos:list_photo')

def delete_all(request):
    for photo in Photo.objects.all():
        photo.image.delete(save=True)
    Photo.objects.all().delete()

    return redirect('managing_photos:list_photo')

def delete_photo(request, id):
    Photo.objects.get(id=id).image.delete(save=True)
    Photo.objects.get(id=id).delete()
    return redirect('managing_photos:list_photo')

class PhotoListView(ListView):
    model = Photo
    paginate_by = 4

    def get_queryset(self):
        return Photo.objects.all()

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = PhotoForm()
        return context

class PhotoUpdateView(UpdateView):
    model = Photo
    fields = ['title', 'albumId', 'url']
    success_url = reverse_lazy('managing_photos:list_photo')

def create_object_from_json(json_data):
    for i in range(len(json_data)):
        response = requests.get(json_data[i]['url'], stream=True)
        file_name = json_data[i]['url'].split('/')[-1]
        lf = tempfile.NamedTemporaryFile()

        for block in response.iter_content(1024 * 8):
            lf.write(block)

        photo = Photo(albumId = json_data[i]['albumId'], id = json_data[i]['id'],\
            title = json_data[i]['title'], url = json_data[i]['url'],thumbnailUrl = json_data[i]['thumbnailUrl'],\
                width = 1111,height = 3333, hexcolorDominant = '#234567')
        photo.image.save(file_name, files.File(lf))

        photo.save()
    return True



def api_link(request):

    try:
        url = request.GET.get('document')
        print(url)
        with urllib.request.urlopen(url) as url:
            json_data = json.load(url)
            if create_object_from_json(json_data):
                return redirect('managing_photos:list_photo')

    except:
        return redirect('managing_photos:upload_fail')


def upload(request):
    try:
        if request.method == 'POST':
            json_raw = request.FILES['document']
            json_data = json_raw.read().decode()
            json_data = json.loads(json_data)
            if create_object_from_json(json_data):
                return redirect('managing_photos:list_photo')

    except:
        return redirect('managing_photos:upload_fail')


class UploadFail(TemplateView):
    template_name = 'managing_photos/upload_fail.html'

class ObjectsView(TemplateView):
    template_name = 'managing_photos/objects_view.html'

    def get(self, request):
        query = Photo.objects.all()
        serializer = PhotoSerializer(query, many = True)
        json_data = JSONRenderer().render(serializer.data)
        return HttpResponse(json_data, content_type='application/json')
