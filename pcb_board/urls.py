from django.urls import path
from .views import *

urlpatterns = [
    path("", PCBCreateView.as_view(), name="index_2"),
    path("orders/", OrdersListView.as_view(), name="orders_list"),
    path("orders/admin/", OrdersAdminListView.as_view(), name="orders_admin"),
    path('board/<int:pk>/', BoardDetailView.as_view(), name='board_detail'),
    path('board/<int:board_id>/change-state/<str:state_key>/', change_board_state, name='change_board_state'),
    path('board/<int:pk>/set-price/',BoardPriceUpdateView.as_view(),name='set_board_price'),
    path('board/<int:pk>/upload-receipt/', UploadReceiptView.as_view(), name='upload_receipt'),
    path("invoice/<int:pk>/", InvoiceDetailView.as_view(), name="invoice_detail"),
    path('board/<int:pk>/download/',download_board,name='board_download'),
]
