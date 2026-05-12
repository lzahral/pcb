from django.shortcuts import render
from django.views.generic import CreateView, ListView
from django.urls import reverse_lazy

from .models import *

class PCBCreateView(CreateView):
    model = Board
    fields = "__all__"
    template_name = 'pcb_board/pcb_form.html'
    success_url = reverse_lazy('index')


class OrdersListView(ListView):
    template_name = 'pcb_board/orders_list.html'
    context_object_name = "data"
    model = Board

    # def get_queryset(self):
    #     # queryset = Board.objects.filter(is_deleted = False)
    #     return queryset