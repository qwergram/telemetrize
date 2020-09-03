from django.shortcuts import render
from django.http import HttpResponse
from django import forms
from django.views.decorators.csrf import csrf_exempt
from base.models import TelemetryRecord

# Create your views here.

class PayloadReader(forms.Form):
    telemetryid = forms.CharField(max_length=255)
    runtime = forms.FloatField()
    time = forms.FloatField()
    args = forms.CharField(max_length=255)
    kwargs = forms.CharField(max_length=255)
    runid = forms.UUIDField()
    pwd = forms.CharField()
    path = forms.CharField()
    executable = forms.CharField()
    ver = forms.CharField(max_length=255)
    host = forms.CharField(max_length=255)
    user = forms.CharField(max_length=255)


@csrf_exempt
def get_payload(request):
    form = PayloadReader(request.POST)
    if form.is_valid():
        TelemetryRecord.objects.create(**form.cleaned_data)
        return HttpResponse('done')
    print(form.errors)