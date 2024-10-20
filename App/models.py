from django.db import models
from django.conf import settings
from cities_light.models import City,Country
# Create your models here.

from .manager import CustomUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.conf import settings




class myuser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=40,blank=False)
    last_name = models.CharField(max_length=40,blank=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_student = models.BooleanField(default=True)
    is_teacher = models.BooleanField(default=False)
    is_company = models.BooleanField(default=False)



    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','last_name',]
    objects = CustomUserManager()

    def __str__(self):
        return f'{self.first_name} {self.last_name}'



    


class Categories(models.Model):
    title = models.CharField(max_length=200)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.title


class SubCategories(models.Model):
    category = models.ForeignKey(Categories,on_delete=models.CASCADE,null=True)
    title = models.CharField(max_length=200)
    
    class Meta:
        verbose_name_plural = 'SubCategories'

    def __str__(self):
        return self.title


class Course(models.Model):
    instructor = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    category = models.ForeignKey(Categories,on_delete=models.CASCADE)
    sub_category = models.ForeignKey(SubCategories,on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    thumbnail = models.ImageField(upload_to ='thumbnail')
    preview_video = models.FileField(upload_to='course-preview-video/', null=True, blank=True)
    overview = models.CharField(max_length=100)
    description = models.TextField(null=True)
    created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now_add=True,null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Add this line for the price field

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.title

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    number_of_employees = models.CharField(max_length=200,null = True)
    phone = models.CharField(max_length=200)
    website = models.CharField(max_length=200,null = True)
    picture = models.ImageField(upload_to ='profile/')

    def __str__(self):
        return f'{self.title}'

class CompanyProfile(models.Model):
    EMPLOYEES_CHOICES = [
        ('1- 49', '1-49'),
        ('50 - 100', '50 - 99'),
        ('100 - 150', '100 - 150'),
        
        # Add more choices as needed
    ]
    INDUSTRY_CHOICES = [
        ('Technology', 'Technology'),
        ('Finance', 'Finance'),
        ('Healthcare', 'Healthcare'),
        ('Education', 'Education'),
        ('Retail', 'Retail'),
        # Add more industry choices as needed
    ]
    EMPLOYEE_COUNT_CHOICES = [
        ('1-10', '1-10'),
        ('11-50', '11-50'),
        ('51-200', '51-200'),
        ('201-500', '201-500'),
        ('501-1000', '501-1000'),
        ('1001-5000', '1001-5000'),
        ('5001-10000', '5001-10000'),
        ('10001+', '10001+'),
    ]
    
    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    company_name = models.CharField(max_length=200)
    City = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True)
    Country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, blank=True)
    phone = models.CharField(max_length=200)
    website = models.CharField(max_length=200)
    logo = models.ImageField(upload_to ='company-logo/')
    employee_count = models.CharField(max_length=20, choices=EMPLOYEE_COUNT_CHOICES, null=True, blank=True)
    company_industry = models.CharField(max_length=50, choices=INDUSTRY_CHOICES)

    def __str__(self):
        return f'{self.company_name}'



class Section(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    course = models.ForeignKey('Course', on_delete=models.CASCADE, related_name='sections')

    def __str__(self):
        return f"{self.title} - {self.course.title}"


class Content(models.Model):
    CONTENT_TYPES = [
        ('video', 'Video'),
        ('audio', 'Audio'),
        ('document', 'Document'),
        ('quiz', 'Quiz'),
        ('assignment', 'Assignment'),
        # Add more content types as needed
    ]

    title = models.CharField(max_length=255)
    content_type = models.CharField(max_length=20, choices=CONTENT_TYPES)
    content_file = models.FileField(upload_to='content_files/', null=True, blank=True)
    content = models.TextField(null=True)
    section = models.ForeignKey('Section', on_delete=models.CASCADE, related_name='contents')

    def __str__(self):
        return f"{self.title} - {self.content_type} - {self.section.title}"


class Enrollment(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey('Course', on_delete=models.CASCADE, related_name='enrollments')
    enrollment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student} enrolled in {self.course}"



class Requirements(models.Model):
    title = models.CharField(max_length=255)
    course = models.ForeignKey('Course', on_delete=models.CASCADE, related_name='requirements')

    def __str__(self):
        return f"{self.title} - {self.course.title}"



class Objectives(models.Model):
    title = models.CharField(max_length=255)
    course = models.ForeignKey('Course', on_delete=models.CASCADE, related_name='objectives')

    def __str__(self):
        return f"{self.title} - {self.course.title}"


class ShoppingCart(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    courses = models.ManyToManyField(Course)

    def calculate_total_amount(self):
        return sum(course.price for course in self.courses.all())

    def clear(self):
        self.courses.clear()

class Order(models.Model):
    ORDER_STATUS = [
        ('pending', 'pending'),
        ('success', 'success'),
        ('cancel', 'cancel'),
        # Add more payment methods as needed
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    courses = models.ManyToManyField(Course)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    stripe_checkout_session_id = models.CharField(max_length=100,null=True,blank=True)
    order_status = models.CharField(max_length=20, choices=ORDER_STATUS,default='pending')
    
class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('credit_card', 'Credit Card'),
        ('paypal', 'PayPal'),
        # Add more payment methods as needed
    ]

    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    transaction_id = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

class Discount(models.Model):
    CHOICES = [
        (0.1, '10%'),
        (0.2, '20%'),
        (0.3, '30%'),
        (0.4, '40%'),
        (0.5, '50%'),
        (0.6, '60%'),
        (0.7, '70%'),
        (0.8, '80%'),
        # Add more discount options as needed
    ]
    amount = models.FloatField(choices=CHOICES, default=0.1)

    def __str__(self):
        return f'{self.get_amount_display()} Discount'
    class Meta:
        ordering = ['-id']





class Sample(models.Model):
   
    file = models.FileField(upload_to='sample/', null=True, blank=True)





#jobs started
class Company(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='company_profile')
    name = models.CharField(max_length=255)
    description = models.TextField()
    website = models.URLField(blank=True, null=True)
    logo = models.ImageField(upload_to='company_logos/', blank=True, null=True)

    def __str__(self):
        return self.name


class Staffs(models.Model):
    STATUS = [
        ('Active', 'Active'),
        ('Suspended', 'Suspended'),
        ('Inactive', 'Inctive'),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS, default='Active')
    date_joined = models.DateTimeField(auto_now_add=True,null=True)



class StaffCourseAssignment(models.Model):
    staff = models.ForeignKey(Staffs, related_name='assigned_courses', on_delete=models.CASCADE)
    course = models.ForeignKey(Course, related_name='assigned_staff', on_delete=models.CASCADE)
    assigned_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.staff.user.email} assigned to {self.course.title}"

class Job(models.Model):
    INDUSTRY_CHOICES = [
        ('Technology', 'Technology'),
        ('Finance', 'Finance'),
        ('Healthcare', 'Healthcare'),
        ('Education', 'Education'),
        ('Retail', 'Retail'),
        # Add more industry choices as needed
    ]

    LOCATION_CHOICES = [
        ('Remote', 'Remote'),
        ('Hybrid', 'Hybrid'),
        ('Onsite', 'Onsite'),
    ]

    OPENINGS_CHOICES = [
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
        ('6', '6'),
        # Add more choices as needed
    ]
    SALARY_RANGES = [
        ('0-20000', '£0 - £20,000'),
        ('20001-40000', '£20,001 - £40,000'),
        ('40001-60000', '£40,001 - £60,000'),
        ('60001-80000', '£60,001 - £80,000'),
        ('80001-100000', '£80,001 - £100,000'),
        ('100001-120000', '£100,001 - £120,000'),
        ('120001-140000', '£120,001 - £140,000'),
        ('140001-160000', '£140,001 - £160,000'),
        ('160001-180000', '£160,001 - £180,000'),
        ('180001-200000', '£180,001 - £200,000'),
        ('200001+', '£200,001 and above'),
    ]
    JOB_TYPE = [
        ('Full-time', 'Full-time'),
        ('Part-time', 'Part-time'),
        ('Contract', 'Contract'),
        ('Temporary', 'Temporary'),
        ('Internship', 'Internship'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=20, choices=LOCATION_CHOICES)
    preferred_employee_city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True)
    preferred_employee_country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, blank=True)
    company = models.ForeignKey(CompanyProfile, related_name='jobs', on_delete=models.CASCADE)
    posted_at = models.DateTimeField(auto_now_add=True)
    salary = models.CharField(max_length=50, choices = SALARY_RANGES)
    job_type = models.CharField(max_length=50, choices=JOB_TYPE, default='Full-time')
    company_industry = models.CharField(max_length=50, choices=INDUSTRY_CHOICES)
    number_of_people_to_hire = models.CharField(max_length=10, choices=OPENINGS_CHOICES)

    def __str__(self):
        return self.title


class InterviewQuestion(models.Model):
    job = models.ForeignKey(Job, related_name='interview_questions', on_delete=models.CASCADE)
    question = models.TextField()

    def __str__(self):
        return f"Question for {self.job.title}"

class Application(models.Model):
    job = models.ForeignKey(Job, related_name='applications', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='applications', on_delete=models.CASCADE)
    resume = models.FileField(upload_to='resumes/')
    cover_letter = models.TextField(blank=True, null=True)
    applied_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=[
        ('Applied', 'Applied'),
        ('In Review', 'In Review'),
        ('Interview', 'Interview'),
        ('Offered', 'Offered'),
        ('Rejected', 'Rejected'),
    ], default='Applied')

    def __str__(self):
        return f"{self.user.email} - {self.job.title}"

class Invitation(models.Model):
    company = models.ForeignKey(Company, related_name='invitations', on_delete=models.CASCADE)
    email = models.EmailField()
    role = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(default=False)

    

    def __str__(self):
        return f"Invitation to {self.email} for {self.role} at {self.company.name}"