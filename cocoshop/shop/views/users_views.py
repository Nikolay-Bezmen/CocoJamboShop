from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView
from django.contrib.auth.models import User
from shop.forms import UserRegistrationForm, UserUpdateForm
from django.urls import reverse_lazy


class UserListView(ListView):
    model = User
    template_name = 'users/user_list.html'
    context_object_name = 'users'


class UserCreateView(CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'users/user_form.html'
    success_url = reverse_lazy('user_list')


class UserUpdateView(UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'users/user_form.html'
    success_url = reverse_lazy('user_list')


class UserDetailView(DetailView):
    model = User
    template_name = 'users/user_detail.html'
    context_object_name = 'user'


class UserDeleteView(DeleteView):
    model = User
    template_name = 'users/user_confirm_delete.html'
    success_url = reverse_lazy('user_list')
