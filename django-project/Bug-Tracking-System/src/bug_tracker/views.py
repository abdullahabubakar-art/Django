import json

from django.db import IntegrityError
from django.http import JsonResponse
from django.views import View
from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
# Create your views here.

User = get_user_model()


@method_decorator(csrf_exempt, name='dispatch')
class SignupView(View):
    def post(self, request):
        try:
            data = json.load(request.body)

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
                password=password,
                user_type=user_type.lower()
            )

            return JsonResponse(user, {"message": "User Created Successfully,"})
        except IntegrityError:
            return JsonResponse({"error": "Email already exists"}, status=400)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
