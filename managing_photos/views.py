import json
import tempfile
import urllib
import urllib.request
from io import BytesIO
import traceback
from rest_framework.renderers import JSONRenderer
import requests
from django.views.generic import ListView, UpdateView, TemplateView
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.core import files
from django.shortcuts import redirect, render
import imageio
import numpy as np
from .models import Photo
from .serializers import PhotoSerializer
from .forms import PhotoForm

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

class UploadFail(TemplateView):
    template_name = 'managing_photos/upload_fail.html'

class ConfirmAllDelete(TemplateView):
    template_name = 'managing_photos/confirm_all_delete.html'

class ObjectsView(TemplateView):
    template_name = 'managing_photos/objects_view.html'

    def get(self, request):
        query = Photo.objects.all()
        serializer = PhotoSerializer(query, many = True)
        json_data = JSONRenderer().render(serializer.data)
        return HttpResponse(json_data, content_type='application/json')

def create_object_from_json(json_data):
    '''
    The function creates a Photo model object and obtains
    information about photos (dominant color, width, height).
    '''

    for i in range(len(json_data)):
        response = requests.get(json_data[i]['thumbnailUrl'])
        file_name = json_data[i]['url'].split('/')[-1]
        lf = tempfile.NamedTemporaryFile()

        for block in response.iter_content():
            lf.write(block)

        try:
            img = np.asarray(imageio.imread(BytesIO(response.content)))
            img_temp = img.copy()
            unique, counts = np.unique(img_temp.reshape(-1, 3), axis=0, return_counts=True)
            img_temp[:,:,0], img_temp[:,:,1], img_temp[:,:,2] = unique[np.argmax(counts)]
            hex_dominat = ('#{:X}{:X}{:X}').format(
                img_temp[0][0][0], img_temp[0][0][1], img_temp[0][0][1])
        except:
            hex_dominat = '-------'
            img = np.array([[0,0]])

        photo = Photo(
            albumId = json_data[i]['albumId'],
            id = json_data[i]['id'],
            title = json_data[i]['title'],
            url = json_data[i]['url'],
            thumbnailUrl = json_data[i]['thumbnailUrl'],
            width = img.shape[1], height = img.shape[0],
            hexcolorDominant = hex_dominat)

        photo.image.save(file_name, files.File(lf))
        photo.save()
    return True

def api_link(request):
    """
    The function loads the json data from the external api.
    """
    try:
        url = request.GET.get('document')
        with urllib.request.urlopen(url) as url:
            json_data = json.load(url)
            if create_object_from_json(json_data):
                return redirect('managing_photos:list_photo')
    except:
        print(traceback.format_exc())
        return redirect('managing_photos:upload_fail')

def upload(request):
    """
    The function loads json data from the form.
    """
    try:
        if request.method == 'POST':
            json_raw = request.FILES['document']
            json_data = json_raw.read().decode()
            json_data = json.loads(json_data)
            if create_object_from_json(json_data):
                return redirect('managing_photos:list_photo')
    except:
        print(traceback.format_exc())
        return redirect('managing_photos:upload_fail')

def error_404_view(request, exception):
    return render(request, "404.html")

def create_photo(request):
    if request.method == 'POST':
        form = PhotoForm(request.POST)
        if form.is_valid():
            form.save()
    return redirect('managing_photos:list_photo')

def delete_all(request):
    """
    The function removes all objects from the Photo model along with photos from the media/img folder.
    """
    for photo in Photo.objects.all():
        photo.image.delete(save=True)
    Photo.objects.all().delete()
    return redirect('managing_photos:list_photo')

def delete_photo(request, id):
    Photo.objects.get(id=id).image.delete(save=True)
    Photo.objects.get(id=id).delete()
    return redirect('managing_photos:list_photo')
