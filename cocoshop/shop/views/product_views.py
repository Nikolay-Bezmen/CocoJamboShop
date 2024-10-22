from django.views.generic import ListView
from django.views.generic import DetailView
from django.views.generic import CreateView
from django.views.generic import UpdateView
from django.views.generic import DeleteView
from shop.forms import ProductForm
from shop.models import Products
from shop.services.services import ProductService
from django.urls import reverse_lazy
from rest_framework import viewsets
from shop.serializers import ProductSerializer


class ProductListView(viewsets.ModelViewSet):
    # model = Products
    # template_name = 'products/product_list.html'
    # context_object_name = 'products'
    queryset = ProductService.get_all_products()
    serializer_class = ProductSerializer


class ProductDetailView(DetailView):
    model = Products
    template_name = 'products/product_detail.html'
    context_object_name = 'product'


class ProductCreateView(CreateView):
    model = Products
    form_class = ProductForm
    template_name = 'products/product_form.html'
    success_url = reverse_lazy('product_list')


class ProductUpdateView(UpdateView):
    model = Products
    form_class = ProductForm
    template_name = 'products/product_form.html'
    success_url = reverse_lazy('product_list')


class ProductDeleteView(DeleteView):
    model = Products
    template_name = 'products/product_confirm_delete.html'
    success_url = reverse_lazy('product_list')
