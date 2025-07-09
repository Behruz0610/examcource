from django.shortcuts import render, redirect
from .models import Topic, Course, Enroll
from django.contrib import messages
from django.contrib.auth.decorators import login_required # for Access Control
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Course
from .serializers import CourseSerializer
from rest_framework.generics import ListAPIView,ListCreateAPIView,RetrieveUpdateDestroyAPIView
from .models import Subject,Course
from .serializers import SubjectModelSerializers,CourseModelSerializers
from rest_framework.generics import ListAPIView,ListCreateAPIView,RetrieveUpdateDestroyAPIView
from rest_framework import viewsets
from .models import Course, Category
from .serializers import CourseSerializer, CategorySerializer
from .permissions import IsAdminForPremiumCourse
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework_simplejwt.tokens import RefreshToken, TokenError




def index(request):
    courses = Course.objects.filter(course_is_active='Yes', course_is_featured="Yes")
    context = {
        'courses': courses,
    }
    return render(request, 'courses/index.html', context)


def courses(request):
    courses = Course.objects.filter(course_is_active='Yes')
    context = {
        'courses': courses,
    }
    return render(request, 'courses/courses.html', context)


def topic_courses(request, topic_slug):
    topic = Topic.objects.get(topic_slug=topic_slug)
    courses = Course.objects.filter(course_is_active='Yes', course_topic=topic)
    context = {
        'courses': courses,
        'topic': topic,
    }
    return render(request, 'courses/topic_courses.html', context)


def search_courses(request):
    if request.method == "GET":
        keyword = request.GET.get('q')
        courses = Course.objects.filter(course_is_active='Yes')
        searched_courses = courses.filter(course_title__icontains=keyword) | courses.filter(course_description__icontains=keyword)
        
        context = {
            'courses': searched_courses,
            'keyword': keyword,
        }
        return render(request, 'courses/search_courses.html', context)

def course_detail(request, course_slug):
    try:
        course = Course.objects.get(course_slug=course_slug)
        modules = course.modules.all()  # Endi modullarni olamiz

        if request.user.is_authenticated:
            enrolled = Enroll.objects.filter(course=course, user=request.user)
        else:
            enrolled = None

        context = {
            'course': course,
            'modules': modules,  # lectures emas, modules!
            'enrolled': enrolled,
        }
        return render(request, 'courses/course_detail.html', context)

    except:
        messages.error(request, "Course Does not Exist.")
        return redirect(index)

@login_required(login_url='account_login')
def lecture(request, course_slug):
    try:
        course = Course.objects.get(course_slug=course_slug)
        modules = course.modules.all()
        first_module = modules.first()
        first_lecture = first_module.lectures.first() if first_module else None
        enrolled = Enroll.objects.filter(course=course, user=request.user)

        context = {
            'course': course,
            'modules': modules,
            'first_lecture': first_lecture,
            'enrolled': enrolled,
        }
        if enrolled:
            return render(request, 'courses/lecture.html', context)
        else:
            messages.error(request, "Enroll Now to access this course.")
            return render(request, 'courses/course_detail.html', context)

    except:
        messages.error(request, "Course Does not Exist.")
        return redirect(index)


@login_required(login_url='account_login')
def lecture_selected(request, course_slug, lecture_slug):
    try:
        course = Course.objects.get(course_slug=course_slug)
        modules = course.modules.all()
        lecture_selected = Lecture.objects.get(lecture_slug=lecture_slug, module__course=course)
        enrolled = Enroll.objects.filter(course=course, user=request.user)

        context = {
            'course': course,
            'modules': modules,
            'lecture_selected': lecture_selected,
            'enrolled': enrolled,
        }
        if enrolled:
            return render(request, 'courses/lecture_selected.html', context)
        else:
            messages.error(request, "Enroll Now to access this course.")
            return render(request, 'courses/course_detail.html', context)

    except:
        messages.error(request, "Course Does not Exist.")
        return redirect(index)


@login_required(login_url='account_login')
def enroll(request, course_id):
    user = request.user
    course = Course.objects.get(id=course_id)

    try:
        Enroll.objects.create(user=user, course=course)
        messages.success(request, "Successfully enrolled to the Course.")
        return redirect(index)

    except:
        messages.error(request, "Couldn't Enroll to the course. Please try again later.")
        return redirect(index)


@login_required(login_url='account_login')
def enrolled_courses(request):

    try:
        courses = Enroll.objects.filter(user=request.user)
        context = {
            'courses': courses,
        }
        return render(request, 'courses/enrolled_courses.html', context)

    except:
        messages.error(request, "Couldn't Enroll to the course. Please try again later.")
        return redirect(index)
    




class SubjectListCreateAPIView(ListCreateAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectModelSerializers
    
    def get_queryset(self):
        queryset = Subject.objects.all()
        queryset = queryset.annotate(course_count=Count('courses'))
        queryset = queryset.order_by('course_count')
        return queryset
    
    
class SubjectDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectModelSerializers
    # lookup_field = 'subject_id'
    lookup_url_kwarg = 'subject_id'



class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminForPremiumCourse]


# from rest_framework import viewsets
# from .models import Course, Category
# from .serializers import CourseSerializer, CategorySerializer

# class CourseViewSet(viewsets.ModelViewSet):
#     queryset = Course.objects.all()
#     serializer_class = CourseSerializer

# class CategoryViewSet(viewsets.ModelViewSet):
#     queryset = Category.objects.all()
#     serializer_class = CategorySerializer


@api_view(['GET'])
def course_list_api(request):
    courses = Course.objects.all()
    serializer = CourseSerializer(courses, many=True)
    return Response(serializer.data)


# class CourseListCreateAPIView(ListCreateAPIView):
#     queryset = Course.objects.all()
#     serializer_class = CourseSerializer

#     def get_queryset(self):
#         queryset = Course.objects.all()
#         return queryset
    



# class CourseDetailAPIView(RetrieveUpdateDestroyAPIView):
#     queryset = Course.objects.all()
#     serializer_class = CourseSerializer

#     lookup_url_kwarg= 'course_slug'



# from .permissions import IsAdminOrManager

# class CourseListView(ListAPIView):
#     queryset = Course.objects.all()
#     serializer_class = CourseSerializer
#     permission_classes = [IsAdminOrManager]


from .permissions import IsAdminForPremiumCourse, IsEvenYear, IsSuperUser, PutPatchOnly

# Misol uchun:
class PremiumCourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.filter(is_premium=True)
    serializer_class = CourseSerializer
    permission_classes = [IsAdminForPremiumCourse]


from .permissions import PutPatchOnly

class CourseUpdateView(APIView):
    permission_classes = [PutPatchOnly]


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data['username'] = self.user.username
        # qo‘shimcha ma’lumotlar qo‘shish mumkin
        return data

class CustomObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except KeyError:
            return Response({"error": "refresh token kerak"}, status=400)
        except TokenError:
            return Response({"error": "Notogri token"}, status=400)