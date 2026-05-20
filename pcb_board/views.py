from django.shortcuts import render
from django.views.generic import CreateView, ListView, DetailView
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

    def get_queryset(self):
        queryset = Board.objects.filter(user = self.request.user.profile)
        return queryset
    

class InvoiceDetailView(DetailView):
    model = Board
    template_name = 'pcb_board/invoice_detail.html'
    context_object_name = "data"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["profile"] = self.request.user.profile 
        return context
        

    
