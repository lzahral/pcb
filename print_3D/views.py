
from django.shortcuts import get_object_or_404, render
from django.views import View
from django.views.generic.edit import FormView, CreateView, UpdateView
from django.views.generic import  edit,CreateView, ListView , DetailView

from .models import *
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView
from django.shortcuts import redirect
from django.core.files.base import ContentFile
from django.shortcuts import render
# Create your views here.


# views.py
from django.shortcuts import render
from django.http import JsonResponse
from .forms import PaymentReceiptForm, PrintPriceForm, STLUploadForm

class OrdersAdminListView(View):
    template_name = 'print_3D/print3D_admin.html'

    def get(self, request, *args, **kwargs):
        orders = Print3D.objects.all()
        context = {
            "orders": orders
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        orders = Print3D.objects.all()
        price = request.POST.get('price')
        order_id = request.POST.get('id')

        item = Print3D.objects.get(id=order_id)
        item.price = price
        item.state='pending_payment'
        item.save()

        context = {
            "orders": orders
        }
        return render(request, self.template_name, context)

class PrintForm(LoginRequiredMixin,CreateView):
    model = Print3D
    template_name = "print_3D/print3D_form.html"
    success_url = reverse_lazy('3D-orders')
    fields ='__all__'
    fields = [ 'infill','material', 'qty', 'file', 'description']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['materials'] = Print3DMaterial.objects.filter()
        return context
    def form_valid(self, form):
        if self.request.user:
            form.instance.user = self.request.user.profile

            form.save()
            return super().form_valid(form)
        else:
            return redirect('login')
            
def change_print_state(request, print_id, state_key):
    print = get_object_or_404(Print3D, id=print_id)
    print.state = state_key
    print.save()

    return redirect('orders_admin')

    

class DeleteItem(View):
    def delete(self, request, id, type):
        Print3D.objects.get(id=id).delete()
        try:
            cart = self.request.session.get('cart')
            for item in cart['items']:
                if item['product_id'] == id and item['type']== type:
                    cart['price'] = cart['price']-item['quantity']*order.price
                    cart['items'].remove(item)
                    self.request.session['cart'] = cart
                    if not cart['items']:
                        del request.session['cart']
        except: 
            pass
        order = Print3D.objects.get(id=id)
        return JsonResponse({'message': 'successful'}, status=200)



class PrintOrder(LoginRequiredMixin, TemplateView):
    template_name = "print_3D/print3D_orders.html"

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        orders = Print3D.objects.filter(
            user=self.request.user.profile).order_by('-created_at')
        
        context['orders'] = orders
        return context
    

class UploadReceiptView(edit.UpdateView):
    model = Print3D
    form_class = PaymentReceiptForm

    def form_valid(self, form):
        board = form.save(commit=False)
        board.state = 'pending_receipt'  
        board.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('3D-orders')
    
class InvoiceDetailView(LoginRequiredMixin,DetailView):
    model = Print3D
    template_name = 'pcb_board/invoice_detail.html'
    context_object_name = "data"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["profile"] = self.request.user.profile 
        return context
    
    
class AddItem(View):
    def get(self, request, pk):
        item = get_object_or_404(Print3D, pk=pk)
        cart = self.request.session.get('cart')
        cart_items_ids = {
            item['product_id'] for item in cart.get('items', []) if item.get('type')
        } if cart else {}
        if not item.id in cart_items_ids:
            if cart:
                cart['items'].append({'product_id': item.id, 'quantity':1,'type':'print3D' })
                cart['price'] += item.price
                self.request.session['cart'] = cart
            else:
                self.request.session['cart'] = {'price': item.price, 'items': [{
                    'product_id': item.id,
                    'quantity':1,
                    'type': 'print3D'
                }]}


        return redirect('cart')