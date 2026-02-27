import json
from django.db import IntegrityError
from django.http import JsonResponse
from django.views import View
from .models import Project, Bug, User
from django.contrib.auth import get_user_model
from django.forms.models import model_to_dict
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from django.contrib.auth import authenticate, login
# Create your views here.

User = get_user_model()


@method_decorator(csrf_exempt, name='dispatch')
class SignupView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            name = data.get('name')
            email = data.get('email')
            mobile_number = data.get('mobile_number')
            password = data.get('password')
            confirm_password = data.get('confirm_password')
            user_type = data.get('user_type')

            if password != confirm_password:
                return JsonResponse({"error": "Password do not match"}, status=400)

            if not all([name, email, password, user_type]):
                return JsonResponse({"error": "All fields are required"}, status=400)

            # add data to user model & hash the password

            user = User.objects.create_user(
                username=email,
                name=name,
                email=email,
                password=password,
                user_type=user_type.lower()
            )

            user_data = model_to_dict(user)

            return JsonResponse({"message": "User Created Successfully", "User": user_data}, status=200, safe=False)
        except IntegrityError:
            return JsonResponse({"error": "Email already exists"}, status=400)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)


@method_decorator(csrf_exempt, name='dispatch')
class LoginView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            email = data.get('email')
            password = data.get('password')

            user = authenticate(request, email=email, password=password)

            if user is not None:
                login(request, user)
                return JsonResponse({"message": "Login Successfuly",
                                     "user": user.name,
                                     "email": user.email,
                                     "user_type": user.user_type}, status=200)
            else:
                return JsonResponse({"error": "Invalid email or password"}, status=401)

        except Exception as e:
            return JsonResponse({"error": "Something went wrong"}, status=500)


@method_decorator(csrf_exempt, name='dispatch')
class ProjectListCreateView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return JsonResponse({"error": "Login required"}, status=401)

        user = request.user

        if user.user_type == "manager":
            projects = Project.objects.filter(manager=user).values()
        else:
            projects = Project.objects.filter(members=user).values()

        return JsonResponse(list(projects), safe=False)

    def post(self, request):
        if request.user.user_type != 'manager':
            return JsonResponse({"error": "Only Managers can create projects"}, status=403)

        name = request.POST.get('name')
        short_detail = request.POST.get('short_detail')
        logo = request.FILES.get('logo')
        member_ids = request.POST.getlist('members')

        try:
            project = Project.objects.create(
                name=name,
                short_detail=short_detail,
                logo=logo,
                manager=request.user
            )
            if member_ids:
                project.members.set(member_ids)

            return JsonResponse({"message": "Project Created Successfully", "id": project.id}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)


@method_decorator(csrf_exempt, name='dispatch')
class ProjectDetailView(View):
    def post(self, request, pk):
        try:
            project = get_object_or_404(Project, pk=pk, manager=request.user)

            project.name = request.POST.get('name', project.name)
            project.short_detail = request.POST.get(
                'short_detail', project.short_detail)
            project.logo = request.FILES.get('logo')
            members_ids = request.POST.getlist('members')
            if members_ids:
                project.members.set(members_ids)

            project.save()
            return JsonResponse({"error": "Project Updated Successfully"}, status=200)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    def delete(self, request, pk):
        project = get_object_or_404(Project, pk=pk, manager=request.user)
        project.delete()
        return JsonResponse({"message": "Project deleted"}, status=204)

