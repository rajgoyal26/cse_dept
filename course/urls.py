from . import views
from django.urls import path


app_name = 'course'

urlpatterns = [
     path('', views.IndexView.as_view(), name='index'),
     path('<int:pk>/', views.DetailView , name='detail'),
     path('course/add/', views.CourseCreate, name='course-add'),
     path('course/<int:pk>/update/',views.CourseUpdate, name='course-update'),
     path('course/<int:pk>/delete/',views.CourseDelete, name='course-delete'),
     path('search/', views.search, name='course-search'),
     path('<int:pk>/add-co/', views.Add_CO, name='co-new'),
     path('<int:co>/select-po/', views.Select_PO, name='po-select'),
     path('availableCourses/', views.OfferCoursesIndex , name='course-offeredlist'),
     path('offerCourses/', views.OfferCourses, name='course-offer'),
     path('enroll|std/', views.Enroll_Student, name='enroll-student'),
     path('enroll|faculty/', views.Enroll_Faculty, name='enroll-faculty'),
     path('<int:co>/see-links/', views.See_Links , name='see-links'),
     #path('<int:pk>/add-co/', views.Add_CO, name='co-add'),

]
