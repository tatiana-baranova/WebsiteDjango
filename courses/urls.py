from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomePage.as_view(), name='home'),
    path('tariffs/', views.TariffsPage, name='tariffs'),
    path('course/<slug>', views.CourseDetailPage.as_view(), name='course-detail'),
    path('course/<slug>/<lesson_slug>', views.LessonDetailPage.as_view(), name='lesson-detail'),
    path('course/add/', views.AddCoursePage.as_view(), name='course-add')
]
