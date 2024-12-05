from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from accounts import serializer, models
from rest_framework import viewsets
from random import randint
from django.conf import settings
from django.core.mail import send_mail
from django.core.exceptions import ObjectDoesNotExist
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        current_user = request.user
        try:
            user_profile = models.UserProfile.objects.get(user=current_user)
            serializer_ = serializer.UserProfileSerializer(user_profile)
            context = {
                "status": 200,
                "data": serializer_.data,
                "error": None
            }
            return Response(context, status=status.HTTP_200_OK)
        except models.UserProfile.DoesNotExist:
            context = {
                "status": 404,
                "data": None,
                "error": "User profile not found."
            }
            return Response(context, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            context = {
                "status": 500,
                "data": None,
                "error": f"An unexpected error occurred: {str(e)}"
            }
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# logout user
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # Get the token from the request
            token = request.auth
            # Delete the token
            token.delete()
            context = {
                "status": 202,
                "data": "Successfully logged out.",
                "error": None
            }
            return Response(context, status=status.HTTP_200_OK)
        except Exception as e:
            context = {
                "status": 400,
                "data": None,
                "error": str(e)
            }
            return Response(context, status=status.HTTP_200_OK)


# register user
class RegisterView(APIView):
    def post(self, request):
        pass


# password recovery and send mail

class PasswordRecoveryViewSet(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')

        try:
            validate_email(email)
        except ValidationError:
            return Response({"status": 400, "data": None, "error": "Invalid email format"},
                            status=status.HTTP_200_OK)

        try:
            user = models.UserProfile.objects.get(email=email)
        except models.UserProfile.DoesNotExist:
            return Response({"status": 200,
                             "data": "If the email exists, a recovery code has been sent.",
                             "error": None},
                            status=status.HTTP_200_OK)

        random_number = randint(1000, 9999)
        request.session['random_number'] = random_number
        request.session['email'] = email

        subject = "Reset Password"
        message = "Your reset code is below."
        from_mail = settings.EMAIL_HOST_USER
        to_list = [email]
        html_content = f"""
            <html>
            <head>
                <style>
                    body {{
                        font-family: Arial, sans-serif;
                        background-color: #C7EBDC;
                        margin: 0;
                        padding: 0;
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        height: 100vh;
                    }}
                    .email-container {{
                        width: 80%;
                        max-width: 400px;
                        background-color: white;
                        padding: 20px;
                        border-radius: 10px;
                        text-align: center;
                        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
                    }}
                    .welcome-text {{
                        color: #024227;
                        font-size: 2rem;
                        margin-bottom: 20px;
                    }}
                    .instruction-text {{
                        font-size: 1.2rem;
                        margin-bottom: 30px;
                        color: #024227;
                    }}
                    .code {{
                        background-color: #024227;
                        color: #fff;
                        padding: 10px;
                        border-radius: 20px;
                        font-size: 2rem;
                        font-weight: bold;
                    }}
                </style>
            </head>
            <body>
                <div class="email-container">
                    <h1 class="welcome-text">به گیاهپزشک خوش آمدید</h1>
                    <p class="instruction-text">لطفاً این کد را وارد کنید:</p>
                    <h1 class="code">{random_number}</h1>
                </div>
            </body>
            </html>
        """

        try:
            send_mail(subject, message, from_mail, to_list,
                      fail_silently=False, html_message=html_content)
        except Exception as e:
            return Response({"status": 500, "data": None, "error": str(e)},
                            status=status.HTTP_200_OK)

        return Response({"status": 200, "data": "Code sent to email", "error": None},
                        status=status.HTTP_200_OK)
    # check the sent code is correct or not

    def put(self, request):
        # get the 4 digit numbr from request
        digit_number = request.data.get('digit')
        # check if the given code is correct in the form
        if 'random_number' in request.session and int(digit_number) == request.session['random_number']:
            context = {
                'status': 200,
                "data": "code is correct",
                "error": "null"
            }
            return Response(context, status=status.HTTP_200_OK)
        else:
            context = {
                'status': 404,
                "data": "null",
                "error": "Code is incorrect"
            }
            return Response(context, status=status.HTTP_200_OK)


# change password
class ChangePasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        new_password = request.data.get("new_password")
        confirm_password = request.data.get("confirm_password")
        email = request.session.get("email")

        if not new_password or not confirm_password:
            return Response({"status": 400, "data": "null", "error": "Both password and confirmation are required"}, status.HTTP_200_OK)

        if new_password != confirm_password:
            return Response({"status": 400, "data": "null", "error": "Passwords do not match"}, status.HTTP_200_OK)

        user_ = models.UserProfile.objects.filter(email=email).first()
        if user_:
            user_.user.set_password(new_password)
            user_.user.save()

            if 'random_number' in request.session:
                del request.session['random_number']
            if 'email' in request.session:
                del request.session['email']

            context = {
                "status": 200,
                "data": "Password changed successfully",
                "error": "null"
            }
            return Response(context, status=status.HTTP_200_OK)
        else:
            context = {
                "status": 404,
                "data": "null",
                "error": "User not found"
            }
            return Response(context, status=status.HTTP_200_OK)


# all users
class AllUserProfilesView(APIView):
    def get(self, request):
        usersProfile = models.UserProfile.objects.all()
        serializer_ = serializer.UserProfileSerializer(usersProfile, many=True)

        context = {
            "status": 200,
            "data": serializer_.data,
            "error": None
        }

        return Response(context, status.HTTP_200_OK)

# view all admins (pecialist)
class AllSpecialistView(APIView):
    def get(self, request):
        specialistProfile = models.Specialist.objects.all()
        serializer_ = serializer.SpecialistProfileSerializer(
            specialistProfile, many=True)
        context = {
            "status": 200,
            "data": serializer_.data,
            "error": None
        }
        return Response(context, status.HTTP_200_OK)


# add admin (pecialist)
class AddSpecialistView(APIView):
    def post(self, request):
        serializer_ = serializer.SpecialistProfileSerializer(data=request.data)
        if serializer_.is_valid():
            serializer_.save()
            return Response({
                "status": 201,
                "data": serializer_.data,
                "error": None,
                "success": True
            }, status=status.HTTP_200_OK)
        return Response({
            "status": 400,
            "data": None,
            "error": serializer_.errors,
            "success": False
        }, status=status.HTTP_200_OK)
