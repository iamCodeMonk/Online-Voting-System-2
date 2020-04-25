from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from .models import Post
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from blog.models import Society

# Create your views here.
class PostListView(LoginRequiredMixin,ListView):
    model = Society
    template_name = 'queries/home.html' #otherwise searches for <app>/<model>_<viewtype>.html
    context_object_name = 'society'
    ordering = ['-date_posted']
    paginate_by=5

    def get_queryset(self):
        s_name=get_object_or_404(Society,id=self.kwargs.get('pk'))
        return s_name.post_set.all().order_by('-date_posted')


class PostCreateView(LoginRequiredMixin, CreateView):
    model=Post
    fields = ['title', 'content']
# searches for <app>/<model>_form.html
    def form_valid(self,form):
        form.instance.author = self.request.user
        form.instance.society_id = self.kwargs.get('pk')
        return super().form_valid(form)
    # success_url = reverse_lazy('blog-home')