import json

from django.db import IntegrityError
from django.http import JsonResponse
from django.views import View
from django.contrib.auth import get_user_model
from django.forms.models import model_to_dict
from django.utils.decorators import method_decorator
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

            # add data to user model

            user = User.objects.create_user(
                username=email,
                name=name,
                email=email,
                password=password,
                user_type=user_type.lower()
            )

            user_data = model_to_dict(user)

            return JsonResponse({"message": "User Created Successfully", "User": user_data}, status=201, safe=False)
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
