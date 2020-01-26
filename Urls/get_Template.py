# coding: utf-8
from django.shortcuts import render
from django.views.decorators.clickjacking import xframe_options_exempt, xframe_options_sameorigin, xframe_options_deny


@xframe_options_exempt
def redirect(request, page_name):
    return render(request, page_name)
