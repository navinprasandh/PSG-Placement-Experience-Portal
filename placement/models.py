from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, Group
from django.db import transaction
from django.utils.translation import gettext_lazy as _
from smart_selects.db_fields import ChainedForeignKey
from django.conf import settings
from django.core.mail import send_mail
from dynamic_forms.models import FormField, ResponseField
from crum import get_current_user

# Create your models here.
from django.utils import timezone


class Carausel(models.Model):
    image = models.ImageField(upload_to="pics/%y/%m/%d/")
    title = models.CharField(max_length=150)
    sub_title = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class User_Manager(BaseUserManager):
    use_in_migrations = True

    def _create_user(
        self,
        name,
        email,
        profile_pic=None,
        roll_number=None,
        department=None,
        course=None,
        contact=None,
        year_of_passing=None,
        placed_company=None,
        package=None,
        offer_type=None,
        password=None,
        **extra_fields
    ):
        # Create and save both users
        if not name:
            raise ValueError("The given name must be set")
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(
            name=name,
            profile_pic=None,
            roll_number=roll_number,
            email=email,
            department=department,
            course=course,
            contact=contact,
            year_of_passing=year_of_passing,
            placed_company=placed_company,
            package=package,
            offer_type=offer_type,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    # Create Student
    def create_user(
        self,
        name,
        email,
        profile_pic,
        roll_number,
        department,
        course,
        password=None,
        **extra_fields
    ):
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_active", False)
        return self._create_user(
            name,
            email,
            profile_pic,
            roll_number,
            department,
            course,
            password,
            **extra_fields
        )

    # Create Admin
    def create_superuser(self, name, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(
            name,
            email,
            profile_pic=None,
            roll_number=None,
            department=None,
            course=None,
            contact=None,
            year_of_passing=None,
            placed_company=None,
            package=None,
            offer_type=None,
            password=password,
            **extra_fields
        )


class Department(models.Model):
    class Meta:
        verbose_name_plural = "Departments"

    name = models.CharField(max_length=100, unique=True, verbose_name="Department Name")

    def __str__(self):
        return str(self.name)


class Course(models.Model):
    class Meta:
        verbose_name_plural = "Courses"

    department = models.ForeignKey(
        Department, on_delete=models.CASCADE, blank=True, null=True
    )
    name = models.CharField(max_length=100, unique=True, verbose_name="Course Name")

    def __str__(self):
        return str(str(self.department) + " - " + str(self.name))


class Users(AbstractUser):
    class Meta:
        verbose_name_plural = "User Details"

    username = None
    first_name = None
    last_name = None

    OFFER_TYPE_CHOICES = (
        ("Intern", "Intern"),
        ("Full-time", "Full-time"),
        ("Intern + Full-time", "Intern + Full-time"),
    )

    name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    roll_number = models.CharField(max_length=10, blank=True, null=True)
    department = models.ForeignKey(
        Department, on_delete=models.CASCADE, blank=True, null=True
    )
    course = ChainedForeignKey(
        Course,
        chained_field="department",
        chained_model_field="department",
        show_all=False,
        sort=True,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="student_course",
    )
    contact = models.CharField(max_length=13, blank=True, null=True)
    year_of_passing = models.CharField(max_length=4, blank=True, null=True)
    placed_company = models.CharField(max_length=100, blank=True, null=True)
    package = models.CharField(max_length=20, blank=True, null=True)
    offer_type = models.CharField(
        max_length=20, choices=OFFER_TYPE_CHOICES, blank=True, null=True
    )
    profile_pic = models.ImageField(upload_to="pics/%y/%m/%d/", blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    objects = User_Manager()

    def __str__(self):
        return str(self.email)

    def save(self, **kwargs):
        if self.is_superuser == False and self.is_staff == False and self.pk is None:
            self.statusMail()
        super().save()
        transaction.on_commit(self.addingGroup)

    def addingGroup(self):
        if self.is_superuser == False and self.is_staff == False:
            self.groups.add(Group.objects.get(name="students"))
        super().save()

    def statusMail(self):
        self.is_active = False
        subject = "Welcome to the Student Portal"
        message = (
            "Hello "
            + self.name
            + ",\n\nWelcome to the Student Portal. Your account has been created. Please wait for the admin to activate your account.\n\nRegards,\nStudent Portal"
        )
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [
            self.email,
        ]
        send_mail(subject, message, email_from, recipient_list)
        super().save()


class Survey(models.Model):
    topic = models.CharField(
        max_length=100,
        verbose_name="Placement Round Name",
        help_text="Eg. Aptitude, Technical, HR, etc. (must be unique)",
    )

    form = FormField()

    def __str__(self):
        return "{} Round".format(self.topic)


class SurveyResponse(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    user = models.ForeignKey(Users, on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now, null=True, blank=True)
    response = ResponseField()

    def __str__(self):
        return "Response for {} by {}".format(self.survey, self.user.name)

    def save(self, *args, **kwargs):
        if self.user is None:
            self.user = get_current_user()
        return super().save(*args, **kwargs)
