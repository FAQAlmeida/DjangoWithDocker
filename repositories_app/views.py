from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView

# Create your views here.

class RepositoriesView(generic.View):
    template_name="repositories_app/repositories.html"
    def get(self, request):
        return render(request, self.template_name)
