# @Aleksandr Kristal v0.0.1 || create all
import ast
from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, HttpResponseRedirect

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from app1.views import \
    sendEmail
from sitedata.models import SiteBlock, SiteBlockVersionList
from app1.config import \
    getRandomCode, \
    dictStatus
import shutil
import os


def addSiteBlockVersionList(siteBlock):
    siteBlockVersionList = SiteBlockVersionList(
                    value=siteBlock.value,
                    name=siteBlock.name,
                    description=siteBlock.description,
                    version=siteBlock.getVersion()
                )
    siteBlockVersionList.save()
    return siteBlockVersionList.version


@csrf_exempt
def index_add_version(request):
    if request.method == 'POST':
        action = request.POST['action']
        if action in ["addSmall", "addMiddle", "addBig"]:
            name = request.POST['name']
            value = request.POST['value']
            description = request.POST['description']
            if len(SiteBlock.objects.filter(name=name)) == 1:
                siteBlock = SiteBlock.objects.get(name=name)
                if action == "addSmall":
                    siteBlock.addSmall(value, description)
                elif action == "addMiddle":
                    siteBlock.addMiddle(value, description)
                elif action == "addBig":
                    siteBlock.addBig(value, description)
                siteBlock.save()
                addSiteBlockVersionList(siteBlock)
                return JsonResponse({"result": True,
                                     "siteBlock": siteBlock.name,
                                     "version": siteBlock.version})
            elif len(SiteBlock.objects.filter(name=name)) == 0:
                siteBlock = SiteBlock(name=name,
                            value=value,
                            description=description)
                siteBlock.save()
                return JsonResponse({"result": True,
                                     "siteBlock": siteBlock.name,
                                     "value": siteBlock.value,
                                     "version": addSiteBlockVersionList(siteBlock)})
            else:
                return JsonResponse({"result": dictStatus.get(411)})
    return render(request, 'sitedata/index_versions.html')


@csrf_exempt
def index_get(request):
    if request.method == 'POST':
        action = request.POST['action']
        if action == "getName":
            name = request.POST['name']
            if len(SiteBlock.objects.filter(name=name)) == 1:
                siteBlock = SiteBlock.objects.get(name=name)
                return JsonResponse({"result": True,
                                     "name": siteBlock.name,
                                     "value": siteBlock.value,
                                     "description": siteBlock.description,
                                     "version": siteBlock.version})
            else:
                return JsonResponse({"result": dictStatus.get(411)})
        if action == "getAll":
            result = {}
            for siteBlock in SiteBlock.objects.all():
                siteBlockDict = {
                            "name": siteBlock.name,
                            "value": siteBlock.value,
                            "description": siteBlock.description,
                            "version": siteBlock.version}
                result[siteBlock.name] = siteBlockDict
            return JsonResponse({"result": True,
                                 "allSiteBlocks": result})
    return render(request, 'sitedata/index_get.html')
