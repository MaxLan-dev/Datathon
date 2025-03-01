from django.shortcuts import render
import csv
from django.conf import settings
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import io
import base64
from django.http import JsonResponse
from django.template.loader import render_to_string

def home_page_view(request):
    template_name = 'website/home.html'
    
    return render(request, template_name)
