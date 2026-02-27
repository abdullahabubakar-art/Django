from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator
from django.forms import ValidationError

# User Model


class User(AbstractUser):

    MANAGER = 'manager'
    QA = 'qa'
    DEVELOPER = 'developer'

    USER_TYPE_CHOICES = [
        (MANAGER, 'Manager'),
        (QA, 'QA'),
        (DEVELOPER, 'Developer'),
    ]

    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    user_type = models.CharField(max_length=50, choices=USER_TYPE_CHOICES)

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['name', 'user_type']

    def __str__(self):
        return f"{self.name} ({self.get_user_type_display()})"

# Project Model


class Project(models.Model):
    name = models.CharField(max_length=100, unique=True)
    short_detail = models.TextField(blank=True, null=True)
    logo = models.ImageField(upload_to='project_logos/', null=True, blank=True)
    manager = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='managed_projects', limit_choices_to={'user_type': User.MANAGER})

    members = models.ManyToManyField(User, related_name='assigned_projects')

    def __str__(self):
        return self.name

# Bug Model


class Bug(models.Model):
    FEATURE = 'feature'
    BUG = 'bug'
    TYPE_CHOICES = [(FEATURE, 'Feature'), (BUG, 'Bug')]

    NEW = 'new'
    STARTED = 'started'
    COMPLETED = 'completed'
    RESOLVED = 'resolved'

    STATUS_CHOICES = [
        (NEW, 'New'),
        (STARTED, 'Started'),
        (COMPLETED, 'Completed'),  # For Features
        (RESOLVED, 'Resolved'),   # For Bugs
    ]

    title = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    deadline = models.DateField(null=True, blank=True)
    screenshot = models.ImageField(
        upload_to='bugs/',
        null=True,
        blank=True,
        validators=[FileExtensionValidator(allowed_extensions=['png', 'gif'])]
    )
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='New')

    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name='bugs')
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='created_bugs', limit_choices_to={'user_type': User.QA})
    assigned_to = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, related_name='assigned_bugs', limit_choices_to={'user_type': User.DEVELOPER})

    REQUIRED_FIELDS = ['title', 'status', 'type']

    def clean(self):
        if self.type == self.FEATURE and self.status == self.RESOLVED:
            raise ValidationError(
                {'status': "Features cannot have 'Resolved' status. Use 'Completed'."})
        if self.type == self.BUG and self.status == self.COMPLETED:
            raise ValidationError(
                {'status': "Bugs cannot have 'Completed' status. Use 'Resolved'."})

    def __str__(self):
        return self.title
