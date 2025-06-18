from django.urls import path
from invoiceGeneratorApp import views


urlpatterns=[
    path('',views.renderDashBoard,name="dashBoard"),
    path('product/AddProduct/',views.addProduct,name="AddProduct"),
    path('product/edit/<int:id>/',views.renderEdit,name="editProduct"),
    path('product/',views.renderProduct,name="product"),
    path('product/deleteProduct/<int:id>/',views.deleteProduct,name="deleteProduct"),
    path('product/edit/<int:id>/EditProduct/',views.EditProduct,name="EditProduct"),
    path('generateInvoice/', views.generateInvoice, name='generateInvoice'),
    path('product/searchProduct/',views.searchProduct,name="searchProduct"),
    path('invoice/deleteInvoice/<int:id>/',views.deleteInvoice,name="deleteInvoice"),
    path('invoice_details/<int:id>/', views.invoice_details, name='invoice_details'),
    path('invoice/', views.renderInvoice, name='invoice'),  
    path('invoice/download_pdf/<int:id>/', views.download_invoice_pdf, name='download_invoice_pdf'),
]