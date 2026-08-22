from django.views.generic import ListView, DetailView
from django.shortcuts import render

from .models import Course


class HomePage(ListView):
    model = Course
    template_name = 'courses/home.html'
    context_object_name = 'courses'
    ordering = ['-id']

    def get_context_data(
        self, *, object_list = ..., **kwargs):
        ctx = super(HomePage, self).get_context_data(**kwargs)
        ctx['title'] = 'Головна сторінка'
        return ctx

class CourseDetailPage(DetailView):
    model = Course
    template_name = 'courses/course_detail.html'