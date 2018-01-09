from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from upload import UploadDownloadAPI
from django.http import JsonResponse


def index(request):
    return render(request, "index.html")

@csrf_exempt
def upload(request):
    if request.method == "GET":
        contextDict = {
            "requestObj": request,
        }
        return render(request, "upload.html", context=contextDict)
    elif request.method == "POST":
        return UploadDownloadAPI.upload(request)


