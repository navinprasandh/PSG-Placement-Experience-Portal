from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, Group
from django.db import transaction
from django.utils.translation import gettext_lazy as _
from smart_selects.db_fields import ChainedForeignKey
from django.conf import settings
from django.core.mail import send_mail
# Create your models here.

class Carausel(models.Model):
	image = models.ImageField(upload_to='pics/%y/%m/%d/')
	title = models.CharField(max_length=150)
	sub_title = models.CharField(max_length=100)

	def __str__(self):
		return self.title

class User_Manager(BaseUserManager):
	use_in_migrations = True
	def _create_user(self, name, email, roll_number=None, department=None, course=None, password=None, **extra_fields):
		# Create and save both users
		if not name:
			raise ValueError('The given name must be set')
		if not email:
			raise ValueError('The given email must be set')
		email = self.normalize_email(email)
		user = self.model(name=name, roll_number=roll_number, email=email, department=department, course=course, **extra_fields)
		user.set_password(password)
		user.save(using=self._db)
		return user

	#Create Student
	def create_user(self, name, email, roll_number, department, course, password=None, **extra_fields):
		extra_fields.setdefault('is_superuser', False)
		extra_fields.setdefault('is_staff', False)
		extra_fields.setdefault('is_active', True)
		return self._create_user(name, email, roll_number, department, course, password, **extra_fields)

	#Create Admin
	def create_superuser(self, name, email, password=None, **extra_fields):
		extra_fields.setdefault('is_staff', True)
		extra_fields.setdefault('is_superuser', True)
		extra_fields.setdefault('is_active', True)

		if extra_fields.get('is_staff') is not True:
			raise ValueError('Superuser must have is_staff=True.')
		if extra_fields.get('is_superuser') is not True:
			raise ValueError('Superuser must have is_superuser=True.')

		return self._create_user(name, email, roll_number=None, department=None, course=None, password=password, **extra_fields)

class Department(models.Model):
	class Meta:
		verbose_name_plural = "Departments and Courses"

	name = models.CharField(max_length=100, unique=True, verbose_name="Department Name")
	course = models.CharField(max_length=100, verbose_name="Course Name")

	def __str__(self):
		return str(str(self.name) + " - " + str(self.course))

class Users(AbstractUser):
	class Meta:
		verbose_name_plural = "User Details"

	username = None
	first_name = None
	last_name = None

	name = models.CharField(max_length=50)
	email = models.EmailField(unique=True)
	roll_number = models.CharField(max_length=10, blank=True, null=True)
	department = models.ForeignKey(Department, on_delete=models.CASCADE, blank=True, null=True)
	# course = models.CharField(max_length=100, blank=True, null=True)
	course = ChainedForeignKey(Department, chained_field="department", chained_model_field="name", show_all=False, sort=True, on_delete=models.CASCADE, blank=True, null=True,related_name="student_course")
	USERNAME_FIELD='email'
	REQUIRED_FIELDS = ['name']


	objects = User_Manager()

	def __str__(self):
		return str(self.email)

	# def save(self, **kwargs):
	# 	if self.is_superuser == False and self.is_staff == False:
	# 		self.statusMail()
	# 	super().save()
	# 	transaction.on_commit(self.addingGroup)

	# def addingGroup(self):
	# 	if self.is_superuser == False and self.is_staff == False:
	# 		self.groups.add(Group.objects.get(name='students'))
	# 	super().save()

	def statusMail(self):
		# self.is_active = False
		subject = "Welcome to the Student Portal"
		message = "Hello " + self.name + ",\n\nWelcome to the Student Portal. Your account has been created. Please wait for the admin to activate your account.\n\nRegards,\nStudent Portal"
		email_from = settings.EMAIL_HOST_USER
		recipient_list = [self.email,]
		send_mail(subject, message, email_from, recipient_list)
		super().save()
