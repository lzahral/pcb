from django.urls import path
from .views import *

urlpatterns = [
    path('3D-form/', view=PrintForm.as_view(), name='3D-form'),
    path('orders/', view=PrintOrder.as_view(), name='3D-orders'),
    path('orders/admin/', view=OrdersAdminListView.as_view(), name='3D-admin'),
    path('print/<int:print_id>/change-state/<str:state_key>/', change_print_state, name='change_print_state'),
    path('print/<int:pk>/upload-receipt/', UploadReceiptView.as_view(), name='upload_print_receipt'),
    path("invoice/<int:pk>/", InvoiceDetailView.as_view(), name="invoice_print_detail"),
    path('add-service/<int:pk>', view=AddItem.as_view(), name="add-service"),
    path("delete-print-order/<int:id>/<str:type>",
         DeleteItem.as_view(), name="delete-print-order"),
]


