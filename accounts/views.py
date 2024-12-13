from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from accounts import serializer, models
from random import randint
from django.conf import settings
from django.core.mail import send_mail
from django.core.exceptions import ObjectDoesNotExist
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from rest_framework_simplejwt.tokens import RefreshToken


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        # Authenticate the user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)  # Log the user in
            refresh = RefreshToken.for_user(user)

            # Check if the user is an admin (or specialist in your case)
            is_admin = models.Specialist.objects.filter(user=user).exists()

            # Prepare the response context
            context = {
                "status": 200,
                "data": {
                    "access": str(refresh.access_token),  # Access token
                    "refresh": str(refresh),  # Refresh token
                    "is_admin": is_admin
                },
                "error": None
            }
            return Response(context, status=status.HTTP_200_OK)
        else:
            # User authentication failed
            context = {
                "status": 401,
                "data": None,
                "error": "Invalid username or password."
            }
            return Response(context, status=status.HTTP_200_OK)


# current profile user
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
                "error": "User profile not found"
            }
            return Response(context, status=status.HTTP_200_OK)
        except Exception as e:
            context = {
                "status": 500,
                "data": None,
                "error": f"An unexpected error occurred: {str(e)}"
            }
            return Response(context, status=status.HTTP_200_OK)


# logout user
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
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

# register


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        # Extract user data from the request
        username_data = request.data.get("username", "")
        email_data = request.data.get("email", "")
        password_data = request.data.get("password", "")
        phone_data = request.data.get("mobile", "")
        name_data = request.data.get('fullName', "Null")

        try:
            # Create the user
            user = User.objects.create_user(
                username=username_data,
                email=email_data,  # Save email in User model
                password=password_data
            )

            # Create the user profile
            profile_data = {
                'user': user.pk,  # Pass the primary key of the user
                'fullName': name_data,
                'email': email_data,
                'phoneNumber': phone_data
            }

            user_profile_serializer = serializer.RegisterSerializer(
                data=profile_data)

            if user_profile_serializer.is_valid():
                user_profile_serializer.save()
                # Log in the user
                login(request, user)

                refresh = RefreshToken.for_user(user)

                # Prepare the response context
                context = {
                    "status": 201,
                    "data": {
                        "access": str(refresh.access_token),  # Access token
                        "refresh": str(refresh),  # Refresh token
                        "user": user_profile_serializer.data  # User profile data
                    },
                    "error": None
                }

                return Response(context, status=status.HTTP_201_CREATED)
            else:
                # If the profile data is invalid, delete the user
                user.delete()
                context = {
                    "status": 400,
                    "data": None,
                    "error": user_profile_serializer.errors
                }
                return Response(context, status=status.HTTP_200_OK)

        except Exception as e:
            # Handle exceptions (e.g., duplicate username)
            context = {
                "status": 400,
                "data": None,
                "error": str(e)
            }
            return Response(context, status=status.HTTP_200_OK)


class AdminRegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        # Extract user data from the request
        # username_data = request.data.get("username", "")
        email_data = request.data.get("email", "")
        password_data = request.data.get("password", "")
        phone_data = request.data.get("mobile", "")
        name_data = request.data.get('fullName', "Null")
        specialties_data = request.data.get('specialties', "Null")

        try:
            # Create the user
            user = User.objects.create_user(
                username=email_data,
                email=email_data,  # Save email in User model
                password=password_data
            )

            # Create the user profile
            profile_data = {
                'user': user.pk,  # Pass the primary key of the user
                'fullName': name_data,
                'email': email_data,
                'phoneNumber': phone_data,
                "specialties": specialties_data

            }

            user_profile_serializer = serializer.AdminRegisterSerializer(
                data=profile_data)

            if user_profile_serializer.is_valid():
                user_profile_serializer.save()
                # Log in the user
                login(request, user)

                refresh = RefreshToken.for_user(user)

                # Prepare the response context
                context = {
                    "status": 201,
                    "data": {
                        "access": str(refresh.access_token),  # Access token
                        "refresh": str(refresh),  # Refresh token
                        "user": user_profile_serializer.data  # User profile data
                    },
                    "error": None
                }

                return Response(context, status=status.HTTP_201_CREATED)
            else:
                # If the profile data is invalid, delete the user
                user.delete()
                context = {
                    "status": 400,
                    "data": None,
                    "error": user_profile_serializer.errors
                }
                return Response(context, status=status.HTTP_200_OK)

        except Exception as e:
            # Handle exceptions (e.g., duplicate username)
            context = {
                "status": 400,
                "data": None,
                "error": str(e)
            }
            return Response(context, status=status.HTTP_200_OK)


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
                    <p class="instruction-text">کد فراموشی شما:</p>
                    <h1 class="code">{random_number}</h1>
                    <p>کلینیک تخصصی و مرکز مشاوره کشاورزی دانشگاه جهرم</p>
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


# update user
class UserProfileUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user_profile = models.UserProfile.objects.get(user=request.user)
        serializer_ = serializer.UserProfileUpdateSerializer(
            user_profile, data=request.data)
        if serializer_.is_valid():  # Validate the data
            serializer_.save()  # Save the updated profile
            context = {
                "status": 200,
                "data": serializer_.data,
                "error": None
            }
            return Response(context, status=status.HTTP_200_OK)
        context = {
            "status": 400,
            "data": None,
            "error": serializer_.errors
        }
        return Response(context, status=status.HTTP_200_OK)


# update admin
class SelfAdminUpdateProfile(APIView):
    def put(self, request):
        user_profile = models.Specialist.objects.get(user=request.user)
        serialiser_ = serializer.AdminProfileUpdate(
            user_profile, data=request.data)
        if serialiser_.is_valid():
            serialiser_.save()
            context = {
                "status": 200,
                "data": serialiser_.data,
                "error": None
            }
            return Response(context, status.HTTP_200_OK)
        else:
            context = {
                "status": 404,
                "data": None,
                "error": serialiser_.errors
            }
            return Response(context, status.HTTP_200_OK)


# todo: modir can edit
class ModirAdminUpdateView(APIView):
    def put(self, request):
        pass


class UserDeleteView(APIView):
    permission_classes = [IsAuthenticated]  # Ensure the user is authenticated

    def delete(self, request, user_id):
        """Delete a user account."""
        try:
            if user_id:
                user = User.objects.get(id=user_id)
                user.delete()
                context = {
                    "status": 204, "message": "User deleted successfully.", "error": None}
                return Response(context, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            {"status": 404, "data": None, "error": "User not found."}
            return Response(context, status=status.HTTP_200_OK)
