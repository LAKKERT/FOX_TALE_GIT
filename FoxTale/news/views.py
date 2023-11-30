from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .forms import NewsForm
from .models import NewsContent
from django.urls import reverse_lazy, reverse

# Create your views here.
class newsView(ListView):
    model = NewsContent
    template_name = 'news.html'
    ordering = ['-date_add']


def newsDetailView(request, pk):
    try:
        newsDetail = NewsContent.objects.get(pk=pk)
    except NewsContent.DoesNotExist:
        return HttpResponse("Object doesn't exist", status=404)

    if request.method == 'POST':
        NewsContent.objects.filter(pk=pk).delete()
        return redirect('news')
    
    return render(request, 'new_detail.html', {'newsDetail': newsDetail})

class newsCreateView(UserPassesTestMixin, CreateView):
    model = NewsContent
    form_class = NewsForm
    template_name = "add_news.html"
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        return self.request.user.is_staff

class newsUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = NewsContent
    form_class = NewsForm
    template_name = "new_update.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        return self.request.user.is_staff
    
    def get_absolute_url(self):
        return reverse('new_update', kwargs={'pk': self.pk})