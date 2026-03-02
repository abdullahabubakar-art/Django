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
            return JsonResponse({"error": str(e)}, status=500)


@method_decorator(csrf_exempt, name='dispatch')
class ProjectListCreateView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return JsonResponse({"error": "Login required"}, status=401)

        user = request.user
        try:
            if user.user_type == "manager":
                projects = Project.objects.filter(manager=user).values()
            else:
                projects = Project.objects.filter(members=user).values()

            return JsonResponse(list(projects), safe=False)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

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
            return JsonResponse({"error": str(e)}, status=500)

    def delete(self, request, pk):
        project = get_object_or_404(Project, pk=pk, manager=request.user)
        project.delete()
        return JsonResponse({"message": "Project deleted"}, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class BugListCreateView(View):
    def get(self, request):
        try:
            user = request.user
            if not user.is_authenticated:
                return JsonResponse({"error": "Authantication required"})

            # project_id = request.POST.get('project_id')

            if user.user_type == 'manager':
                bugs = Bug.objects.filter(project__manager=user).values()
                print("manager see bugs in project they manage")
            elif user.user_type == 'developer':
                bugs = Bug.objects.filter(assigned_to=user).values()
                print(' bug assigned to developer')
            elif user.user_type == 'qa':
                bugs = Bug.objects.filter(project__members=user).values()
                print('bug created by QA or assign to project')

            return JsonResponse(list(bugs), safe=False)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    def post(self, request):
        if request.user.user_type != 'qa':
            return JsonResponse({"error": "Only QA can create bugs"}, status=403)

        project_id = request.POST.get('project')
        title = request.POST.get('title')
        description = request.POST.get('description')
        deadline = request.POST.get('deadline')
        bug_type = request.POST.get('type')
        status = request.POST.get('status')
        screenshot = request.FILES.get('screenshot')
        developer_id = request.POST.get('assigned_to')

        project = get_object_or_404(Project, id=project_id)
        user = get_object_or_404(User, id=developer_id)
        if request.user not in project.members.all():
            return JsonResponse({"error": "You are not assigned to this project"}, status=403)

        try:
            bug = Bug.objects.create(
                project=project,
                title=title,
                description=description,
                deadline=deadline,
                type=bug_type,
                status=status,
                screenshot=screenshot,
                created_by=request.user,
                assigned_to=user
            )

            return JsonResponse({"message": "Bug created Successfully", "id": bug.id}, status=200)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)


@method_decorator(csrf_exempt, name='dispatch')
class BugDetailView(View):
    def get(self, request, pk):
        try:
            bug = get_object_or_404(Bug, pk=pk)
            user = request.user
            if user.user_type != 'manager' and user not in bug.project.members.all():
                return JsonResponse({"error": "Access Denied"}, status=403)
            data = model_to_dict(bug, exclude=['screenshot'])
            # Object of type ImageFieldFile is not JSON serializable that why we exclude and manully add as  url.
            if bug.screenshot:
                data['screenshot'] = bug.screenshot.url
            return JsonResponse(data)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    def post(self, request, pk):
        try:

            bug = get_object_or_404(Bug, pk=pk)
            user = request.user
            if user.user_type == 'developer':
                if bug.assigned_to != user:
                    return JsonResponse({"error", "This bug is not assigned to you"}, status=403)
                bug.status = request.POST.get('status')
                bug.save()
                return JsonResponse({"message": "Status Updated Successfully"}, status=200)

            elif user.user_type == 'qa':
                if bug.created_by != user:
                    return JsonResponse({"error": "You can only update bugs you created"}, status=403)

                bug.title = request.POST.get('title', bug.title)
                bug.description = request.POST.get(
                    'description', bug.description)
                bug.deadline = request.POST.get('deadline', bug.deadline)
                bug.status = request.POST.get('status', bug.status)
                bug.type = request.POST.get('type', bug.type)
                bug.screenshot = request.FILES.get('screenshot')
                developer_id = request.POST.get('assigned_to', bug.assigned_to)
                user = get_object_or_404(User, id=developer_id)
                bug.assigned_to = user

                bug.save()
                return JsonResponse({"message": "Bug updated by QA Successfully"})
            return JsonResponse({'error': 'Action not allowed'}, status=403)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    def delete(self, request, pk):
        bug = get_object_or_404(Bug, pk=pk)
        user = request.user
        if bug.created_by == user or bug.project.manager == user:
            bug.delete()
            return JsonResponse({"message": "Bug deleted Successfully"}, status=200)
        return JsonResponse({"error": "You do not have permission to delete this bug"}, status=403)
