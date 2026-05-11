from django.shortcuts import render
from django.views.generic import CreateView
from django.urls import reverse_lazy

from .models import *

class PCBCreateView(CreateView):
    model = Board
    fields = "__all__"
    template_name = 'pcb_board/pcb_form.html'
    success_url = reverse_lazy('index')
