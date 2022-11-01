import json
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, TemplateView
from django.http import HttpResponse
from rest_framework.renderers import JSONRenderer
from django.shortcuts import redirect
from .models import Photo
from .serializers import PhotoSerializer
from .forms import PhotoForm
import urllib.request

def create_photo(request):
    if request.method == 'POST':
        form = PhotoForm(request.POST)
        if form.is_valid():
            form.save()
    return redirect('managing_photos:list_photo')

def delete_all(request):
    Photo.objects.all().delete()
    return redirect('managing_photos:list_photo')

def delete_photo(request, id):
    Photo.objects.filter(id=id).delete()
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

def api_link(request):

    try:
        url = request.GET.get('document')
        print(url)
        with urllib.request.urlopen(url) as url:
            json_data = json.load(url)
            for i in range(len(json_data)):
                print(i)
                serializer = PhotoSerializer(data=json_data[i])
                if serializer.is_valid():
                    serializer.save()
        return redirect('managing_photos:list_photo')
    except:
        return redirect('managing_photos:upload_fail')

def upload(request):
    try:
        if request.method == 'POST':
            json_raw = request.FILES['document']
            json_data = json_raw.read().decode()
            json_data = json.loads(json_data)
            for i in range(len(json_data)):
                print(i)
                serializer = PhotoSerializer(data=json_data[i])
                if serializer.is_valid():
                    serializer.save()
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
