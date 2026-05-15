from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import CreateView, ListView , DetailView
from django.views import View
from django.urls import reverse_lazy

from pcb_board.forms import BoardPriceForm

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
    
class OrdersAdminListView(ListView):
    template_name = 'pcb_board/orders_admin.html'
    context_object_name = "data"
    model = Board

class BoardDetailView(DetailView):
    model = Board
    template_name = 'pcb_board/board_detail.html'
    context_object_name = 'board'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['fields'] = self.object._meta.fields
        return context

def change_board_state(request, board_id, state_key):
    board = get_object_or_404(Board, id=board_id)

    board.state = state_key
    board.save()

    return redirect('orders_admin')

class BoardPriceUpdateView(View):

    def post(self, request, pk):
        board = get_object_or_404(Board, pk=pk)

        form = BoardPriceForm(request.POST, instance=board)

        if form.is_valid():
            form.save()
            board.state='pending_payment'
            board.save()

        return redirect('orders_admin')