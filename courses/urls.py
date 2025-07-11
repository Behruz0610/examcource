from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from .views import CourseViewSet, CategoryViewSet
from django.urls import path
from .views import CustomObtainPairView, LogoutView
from rest_framework_simplejwt.views import TokenRefreshView


router = DefaultRouter()
router.register(r'courses', CourseViewSet)
router.register(r'categories', CategoryViewSet)


urlpatterns = [
    path('', views.index, name="home"),
    path('courses/', views.courses, name="courses"),
    path('courses/search/', views.search_courses, name="search-courses"),
    path('courses/enrolled-courses/', views.enrolled_courses, name="enrolled-courses"),

    path('courses/<slug:topic_slug>/', views.topic_courses, name="topic-courses"),
    path('course/<slug:course_slug>/', views.course_detail, name="course-detail"),
    path('course/<slug:course_slug>/lecture/', views.lecture, name="lecture"),
    path('course/<slug:course_slug>/lecture/<slug:lecture_slug>/', views.lecture_selected, name="lecture-selected"),

    path('course/enroll/<int:course_id>/', views.enroll, name="enroll"),
    path('api/', include(router.urls)),  # <-- REST API endpointlari uchun
    path('api/token/', CustomObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/logout/', LogoutView.as_view(), name='logout'),
    

    
]
