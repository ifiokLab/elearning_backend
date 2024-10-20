from rest_framework import serializers
from .models import *
from cities_light.models import City,Country




class CompanyProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyProfile
        fields = '__all__'
        
class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = '__all__'
        #fields = ['title','description','location','preferred_employee_city','preferred_employee_country','company','posted_at','salary','job_type','company_industry','number_of_people_to_hire']

class InterviewQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = InterviewQuestion
        fields = '__all__'


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['id', 'name']

class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['id', 'name', 'country']

class MyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = myuser
        fields = ('id', 'email', 'first_name', 'last_name',)


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['category','sub_category','title','thumbnail','overview','description','preview_video','price']


class CourseListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'

class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategories
        fields = ['id', 'title']

class CategorySerializer(serializers.ModelSerializer):
    subcategories = SubCategorySerializer(many=True, read_only=True)

    class Meta:
        model = Categories
        fields = ['id', 'title', 'subcategories']


class InstructorCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'

    
class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = ['id', 'title', 'description']

class ContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = ['id', 'title', 'content_type', 'content_file','content']



class CourseDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"

class RequirementsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Requirements
        fields = ['id', 'title', 'course']


class ObjectivesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Objectives
        fields = ['id', 'title', 'course']

    
class ContentTypeCountSerializer(serializers.Serializer):
    content_type = serializers.CharField()
    count = serializers.IntegerField()



class ShoppingCartSerializer(serializers.ModelSerializer):
    courses = CourseListSerializer(many=True, read_only=True)

    class Meta:
        model = ShoppingCart
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    courses = CourseSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = '__all__'

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'

class EnrollmentSerializer(serializers.ModelSerializer):
    course_title = serializers.CharField(source='course.title', read_only=True)
    course_thumbnail = serializers.ImageField(source='course.thumbnail', read_only=True)
    # Add more fields as needed

    class Meta:
        model = Enrollment
        fields = ['id', 'course', 'course_title', 'course_thumbnail', 'enrollment_date']




class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'



class CourseSerializerNew(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['category','sub_category','title','thumbnail','overview','description','price']