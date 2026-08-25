from django.template.context_processors import request
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView
from django.shortcuts import render
from .forms import CourseAddForm
from .models import Course, Lesson


def TariffsPage(request):
    return render(request, 'courses/tariffs.html', {'title': 'Тарифи на сайті'})

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

class AddCoursePage(CreateView):
    model = Course
    form_class = CourseAddForm
    template_name = 'courses/add_course.html'

    def get_absolute_url(self):
        return reverse('course-detail', kwargs={'slug': self.slug})

class CourseDetailPage(DetailView):
    model = Course
    template_name = 'courses/course_detail.html'
    def get_context_data(
        self, *, object_list = ..., **kwargs):
        ctx = super(CourseDetailPage, self).get_context_data(**kwargs)
        course = Course.objects.filter(slug=self.kwargs['slug']).first()
        ctx['title'] = course
        ctx['lessons'] = Lesson.objects.filter(course=course).order_by('number')
        return ctx



class LessonDetailPage(DetailView):
    model = Course
    template_name = 'courses/lesson_detail.html'
    def get_context_data(
        self, *, object_list = ..., **kwargs):
        ctx = super(LessonDetailPage, self).get_context_data(**kwargs)
        course = Course.objects.filter(slug=self.kwargs['slug']).first()
        lesson = Lesson.objects.filter(slug=self.kwargs['lesson_slug']).first()

        if lesson and lesson.video:
            # lesson.video = lesson.video.split('=')[1]
            lesson.video = lesson.video.split('v=')[1].split('&')[0]

        ctx['title'] = lesson
        ctx['lesson'] = lesson
        return ctx

