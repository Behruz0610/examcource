from rest_framework import serializers
from .models import Course
from rest_framework import serializers
from .models import Subject, Course



class SubjectModelSerializers(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'

class CourseModelSerializers(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'

from rest_framework import serializers
from .models import Course, Category

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'

class CategoryCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    courses = CategoryCourseSerializer(many=True, read_only=True, source='course_set')
    course_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = '__all__'  

    def get_course_count(self, obj):
        return obj.course_set.count()