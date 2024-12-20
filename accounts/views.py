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
            admin_user = models.Specialist.objects.filter(user=current_user)
            print(f"admin_user: {admin_user}")
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

                return Response(context, status=status.HTTP_200_OK)
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

class UserRegisterView(APIView):
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
                # login(request, user)

                # refresh = RefreshToken.for_user(user)

                # Prepare the response context
                context = {
                    "status": 201,
                    "data": {
                        # "access": str(refresh.access_token),  # Access token
                        # "refresh": str(refresh),  # Refresh token
                        "user": user_profile_serializer.data  # User profile data
                    },
                    "error": None
                }

                return Response(context, status=status.HTTP_200_OK)
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
                "specialties": specialties_data,
                "is_admin": True
            }

            user_profile_serializer = serializer.AdminRegisterSerializer(
                data=profile_data)

            if user_profile_serializer.is_valid():

                user_profile_serializer.save()
                # Prepare the response context
                context = {
                    "status": 201,
                    "data": {
                        "user": user_profile_serializer.data  # User profile data
                    },
                    "error": None
                }

                return Response(context, status=status.HTTP_200_OK)
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

class AdminProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            # Retrieve the admin profile associated with the authenticated user
            admin_profile = models.Specialist.objects.get(user=request.user)
            admin_profile_serializer = serializer.AdminProfileSerializer(admin_profile)

            context = {
                "status": 200,
                "data": admin_profile_serializer.data,
                "error": None
            }
            return Response(context, status=status.HTTP_200_OK)

        except models.Specialist.DoesNotExist:
            context = {
                "status": 404,
                "data": None,
                "error": "Admin profile not found."
            }
            return Response(context, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            context = {
                "status": 500,
                "data": None,
                "error": str(e)
            }
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
        
# password recovery and send mail

class PasswordRecoveryViewSet(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')

        # Validate email format
        try:
            validate_email(email)
            if not User.objects.filter(email=email).exists():
                return Response({
                    "status": 404,
                    "data": None,
                    "error": "Email is not in our database"
                }, status=status.HTTP_200_OK)
        except ValidationError:
            return Response({
                "status": 400,
                "data": None,
                "error": "Email is not valid"
            }, status=status.HTTP_200_OK)

        # Check if the user exists
        try:
            user = models.UserProfile.objects.get(email=email)
        except models.UserProfile.DoesNotExist:
            # Obfuscate the error for non-existing users
            return Response({
                "status": 200,
                "data": "If the email exists, a recovery code has been sent.",
                "error": None
            }, status=status.HTTP_200_OK)

        # Generate a recovery code
        random_number = randint(1000, 9999)
        request.session['random_number'] = random_number
        request.session['email'] = email
        request.session.save()

        # Prepare email content
        subject = "Reset Your Password"
        message = "Your password recovery code is below."
        from_mail = settings.EMAIL_HOST_USER
        to_list = [email]
        html_content = f"""
        <html>
        <head>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    background-color: #f5f5f5;
                    margin: 0;
                    padding: 0;
                }}
                .email-container {{
                    max-width: 600px;
                    margin: 30px auto;
                    background-color: white;
                    border-radius: 8px;
                    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
                    overflow: hidden;
                }}
                .header {{
                    background-color: #024227;
                    color: white;
                    text-align: center;
                    padding: 20px;
                }}
                .header h1 {{
                    margin: 0;
                    font-size: 1.5rem;
                }}
                .content {{
                    padding: 20px;
                    text-align: center;
                }}
                .content p {{
                    color: #333;
                    font-size: 1rem;
                    margin-bottom: 20px;
                }}
                .code {{
                    display: inline-block;
                    padding: 10px 20px;
                    font-size: 1.5rem;
                    color: white;
                    background-color: #024227;
                    border-radius: 5px;
                    font-weight: bold;
                }}
                .footer {{
                    text-align: center;
                    padding: 10px;
                    font-size: 0.8rem;
                    color: #666;
                }}
            </style>
        </head>
        <body>
            <div class="email-container">
                <div class="header">
                    <h1>Reset Your Password</h1>
                </div>
                <div class="content">
                    <p>کاربر عزیز</p>
                    <p>کد بازیابی رمز عبور شما:</p>
                    <div class="code">{random_number}</div>
                    <p>لطفا از این کد برای بازیابی رمز عبور خود استفاده کنید. این کد پس از گذشت 5 دقیقه منقضی خواهد شد.</p>
                </div>
                <div class="footer">
                    <p>&copy; 2024 Jahrom University - Agricultural Clinic</p>
                </div>
            </div>
        </body>
        </html>
        """

        # Send email
        try:
            send_mail(subject, message, from_mail, to_list,
                      fail_silently=False, html_message=html_content)
        except Exception as e:
            return Response({
                "status": 500,
                "data": None,
                "error": str(e)
            }, status=status.HTTP_200_OK)

        return Response({
            "status": 200,
            "data": "Code sent to email",
            "error": None
        }, status=status.HTTP_200_OK)

    def put(self, request):
        digit_number = request.data.get('digit')
        print(f"Session data: {request.session.items()}")

        if 'random_number' in request.session and int(digit_number) == request.session['random_number']:
            return Response({"status": 200, "data": "code is correct", "error": None},
                            status=status.HTTP_200_OK)
        else:
            return Response({"status": 404, "data": None, "error": "Code is incorrect"},
                            status=status.HTTP_200_OK)
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


class DeleteAdminListView(APIView):
    def delete(self, request):
        user_ids = request.data.get('user_ids', [])

        if not user_ids:
            return Response({
                "status": 400,
                "data": "No user IDs provided.",
                "error": "user_ids field is required."
            }, status=status.HTTP_200_OK)

        deleted_users = []
        not_found_users = []

        for user_id in user_ids:
            try:
                user = User.objects.get(id=user_id)
                user.delete()
                deleted_users.append(user_id)
            except User.DoesNotExist:
                not_found_users.append(user_id)

        if deleted_users:
            context = {
                "status": 204,
                "data": f"Users with IDs {deleted_users} deleted successfully.",
                "error": None    
            }
            return Response(context, status=status.HTTP_204_NO_CONTENT)

        if not_found_users:
            context = {
                "status": 404,
                "data": f"Users with IDs {not_found_users} not found.",
                "error": None    
            }
            return Response(context, status=status.HTTP_404_NOT_FOUND)

        return Response({
            "status": 400,
            "data": "No users were deleted.",
            "error": "No valid user IDs provided."
        }, status=status.HTTP_400_BAD_REQUEST)
        
        