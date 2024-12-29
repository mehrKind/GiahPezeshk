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
from rest_framework.parsers import MultiPartParser, FormParser


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

            # Fetch the user profile (UserProfile or Specialist)
            try:
                if models.Specialist.objects.filter(user=user).exists():
                    user_profile = models.Specialist.objects.get(user=user)
                else:
                    user_profile = models.UserProfile.objects.get(user=user)

                # Prepare the response context
                context = {
                    "status": 200,
                    "data": {
                        "access": str(refresh.access_token),  # Access token
                        "refresh": str(refresh),  # Refresh token
                        "is_admin": user_profile.is_admin,
                        "is_modir": user_profile.is_modir,
                    },
                    "error": None,
                }
                return Response(context, status=status.HTTP_200_OK)
            except models.UserProfile.DoesNotExist:
                # Handle case where UserProfile doesn't exist
                context = {
                    "status": 500,
                    "data": None,
                    "error": "User profile not found.",
                }
                return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            # User authentication failed
            context = {
                "status": 401,
                "data": None,
                "error": "Invalid username or password.",
            }
            return Response(context, status=status.HTTP_401_UNAUTHORIZED)



# current profile user
class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        current_user = request.user
        try:
            user_profile = models.UserProfile.objects.filter(is_admin = False).get(user = current_user)
            serializer_ = serializer.UserProfileSerializer(user_profile)
            # admin_user = models.Specialist.objects.filter(user=current_user)
            # print(f"admin_user: {admin_user}")
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


# ! ========================================
class UserRegisterView(APIView):
    permission_classes = [AllowAny]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        email_data = request.data.get("email", "")
        password_data = request.data.get("password", "")
        phone_data = request.data.get("mobile", "")
        name_data = request.data.get('fullName', "Null")
        profile_img_data = request.FILES.get("profile_img", None)  # Get profile_img if provided

        try:
            # Create the user
            user = User.objects.create_user(
                username=email_data,
                email=email_data,
                password=password_data
            )

            # Prepare the profile data
            profile_data = {
                'user': user.pk,
                'fullName': name_data,
                'email': email_data,
                'phoneNumber': phone_data,
                'profile_img': profile_img_data  # Include profile_img if provided
            }

            user_profile_serializer = serializer.RegisterSerializer(data=profile_data)

            if user_profile_serializer.is_valid():
                user_profile_serializer.save()
                context = {
                    "status": 201,
                    "data": {
                        "user": user_profile_serializer.data
                    },
                    "error": None
                }
                return Response(context, status=status.HTTP_200_OK)
            else:
                user.delete()  # Delete the user if profile data is invalid
                context = {
                    "status": 400,
                    "data": None,
                    "error": user_profile_serializer.errors
                }
                return Response(context, status=status.HTTP_200_OK)

        except Exception as e:
            context = {
                "status": 400,
                "data": None,
                "error": str(e)
            }
            return Response(context, status=status.HTTP_200_OK)

# ! ========================================


class AdminRegisterView(APIView):
    permission_classes = [AllowAny]
    parser_classes = [MultiPartParser, FormParser]  # Allow handling of form-data requests

    def post(self, request):
        # Extract user data from the request (including file)
        email_data = request.data.get("email", "")
        password_data = request.data.get("password", "")
        phone_data = request.data.get("mobile", "")
        name_data = request.data.get("fullName", "Null")
        specialties_data = request.data.get("specialties", "Null")
        profile_img_data = request.FILES.get("profile_img")

        try:
            # Create the user
            user = User.objects.create_user(
                username=email_data,
                email=email_data,
                password=password_data
            )

            # Create the user profile data
            profile_data = {
                'user': user.pk,
                'fullName': name_data,
                'email': email_data,
                'phoneNumber': phone_data,
                "specialties": specialties_data,
                "is_admin": True,
                "profile_img": profile_img_data
            }

            # Serialize and validate the profile data
            user_profile_serializer = serializer.AdminRegisterSerializer(data=profile_data)

            if user_profile_serializer.is_valid():
                user_profile_serializer.is_admin = True
                user_profile_serializer.save()
                # Return success response with user profile data
                context = {
                    "status": 201,
                    "data": {
                        "user": user_profile_serializer.data  # User profile data
                    },
                    "error": None
                }
                return Response(context, status=status.HTTP_200_OK)
            else:
                # If the profile data is invalid, delete the user and return the error
                user.delete()
                context = {
                    "status": 400,
                    "data": None,
                    "error": user_profile_serializer.errors
                }
                return Response(context, status=status.HTTP_200_OK)

        except Exception as e:
            # Handle any unexpected exceptions
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
        usersProfile = models.UserProfile.objects.filter(is_admin = False).all()
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

        try:
            # Fetch the Specialist instance for the current user
            all_specialist= models.Specialist.objects.all()
        except models.Specialist.DoesNotExist:
            context = {
                "status": 403,
                "data": None,
                "error": "no item is exists."
            }
            return Response(context, status=status.HTTP_200_OK)
        # Serialize the data
        serializer_ = serializer.SpecialistProfileSerializer(all_specialist, many=True)

        # Prepare the response context
        context = {
            "status": 200,
            "data": serializer_.data,
            "error": None
        }
        return Response(context, status=status.HTTP_200_OK)
    
    
class AllSpecialistWebView(APIView):
    def get(self, request):
        current_user = request.user

        try:
            # Fetch the Specialist instance for the current user
            current_user_profile = models.Specialist.objects.get(user=current_user)
        except models.Specialist.DoesNotExist:
            context = {
                "status": 403,
                "data": None,
                "error": "Access denied. User does not have a specialist profile."
            }
            return Response(context, status=status.HTTP_200_OK)

        # Check if the current user is a "modir"
        if current_user_profile.is_modir:
            # If the user is a "modir", retrieve all specialists with is_admin=True
            specialist_profiles = models.Specialist.objects.filter(is_admin=True)
        else:
            # Otherwise, only return the current user's specialist profile
            specialist_profiles = models.Specialist.objects.filter(user=current_user)

        # Serialize the data
        serializer_ = serializer.SpecialistProfileSerializer(specialist_profiles, many=True)

        # Prepare the response context
        context = {
            "status": 200,
            "data": serializer_.data,
            "error": None
        }
        return Response(context, status=status.HTTP_200_OK)



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
    
    
class UserProfileUpdateViewFrom(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user_profile = models.UserProfile.objects.get(user=request.user)
        serializer_ = serializer.userprofileUpdateFromSerializer(
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
# class SelfAdminUpdateProfile(APIView):
#     def put(self, request):
#         user_profile = models.Specialist.objects.get(user=request.user)
#         serialiser_ = serializer.AdminProfileUpdate(
#             user_profile, data=request.data)
#         if serialiser_.is_valid():
#             serialiser_.save()
#             context = {
#                 "status": 200,
#                 "data": serialiser_.data,
#                 "error": None
#             }
#             return Response(context, status.HTTP_200_OK)
#         else:
#             context = {
#                 "status": 404,
#                 "data": None,
#                 "error": serialiser_.errors
#             }
#             return Response(context, status.HTTP_200_OK)


# todo: modir can edit

class ModirAdminUpdateView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def put(self, request, user_id):
        print(request.data)
        try:
            specialist_instance = models.Specialist.objects.get(user__id=user_id)
        except models.Specialist.DoesNotExist:
            return Response(
                {"status": 404, "data": None, "error": "Specialist with the provided user ID does not exist."},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer_ = serializer.AdminProfileUpdate(
            instance=specialist_instance, data=request.data, partial=True
        )

        if serializer_.is_valid():
            # Save the validated data, including profile_img if provided
            serializer_.save()

            return Response(
                {"status": 200, "data": serializer_.data, "error": None},
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {"status": 400, "data": None, "error": serializer_.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

class AdminUpdateUserView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def put(self, request, user_id):
        # Debug: Print the incoming request data
        print("Request Data:", request.data)

        try:
            # Retrieve the user profile instance based on user ID
            user_instance = models.UserProfile.objects.get(user__id=user_id)
        except models.UserProfile.DoesNotExist:
            return Response(
                {"status": 404, "data": None, "error": "UserProfile with the provided user ID does not exist."},
                status=status.HTTP_404_NOT_FOUND
            )

        # Make a copy of the incoming data
        data = request.data.copy()

        # Map `profile_image` field to `profile_img` in case of image upload
        if 'profile_image' in data:
            data['profile_img'] = data.pop('profile_image')

        # Debug: Print the modified data
        print("Data after modification:", data)

        # Serialize the data to validate and update the user profile
        serializer_ = serializer.UserProfileUpdateFromSerializer2(
            instance=user_instance, data=data, partial=True
        )

        if serializer_.is_valid():
            # Save the updated data
            serializer_.save()
            return Response(
                {"status": 200, "data": serializer_.data, "error": None},
                status=status.HTTP_200_OK
            )
        else:
            # Debug: Print validation errors
            print("Validation Errors:", serializer_.errors)
            return Response(
                {"status": 400, "data": None, "error": serializer_.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

# View: Handling incoming field 'profile_image' and mapping it to 'profile_img'
class AdminUpdateUserView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def put(self, request, user_id):
        # Debug the incoming request data
        print("Request Data:", request.data)

        try:
            user_instance = models.UserProfile.objects.get(user__id=user_id)
        except models.UserProfile.DoesNotExist:
            return Response(
                {
                    "status": 404,
                    "data": None,
                    "error": "UserProfile with the provided user ID does not exist."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        # Map the incoming data field `profile_image` to `profile_img` if needed
        data = request.data.copy()

        # Check if the incoming data contains 'profile_image' and map it to 'profile_img'
        if 'profile_image' in data:
            data['profile_img'] = data.pop('profile_image')

        # Use the serializer to validate and update the user profile
        serializer_ = serializer.UserProfileUpdateFromSerializer2(
            instance=user_instance, data=data, partial=True
        )

        if serializer_.is_valid():
            serializer_.save()  # Save the updated data
            return Response(
                {"status": 200, "data": serializer_.data, "error": None},
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {"status": 400, "data": None, "error": serializer_.errors},
                status=status.HTTP_400_BAD_REQUEST
            )



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
        
        

class SingleUserView(APIView):    
    def post(self, request):
        # Get email and phone_number from request data
        emails = request.data.get("email", [])  # Expecting a list
        phone_numbers = request.data.get("phoneNumber", [])  # Expecting a list
        
        userProfile = None
        
        # Initialize a queryset
        if emails:
            userProfile = models.UserProfile.objects.all().filter(email__in=emails)
        elif phone_numbers:
            userProfile = models.UserProfile.objects.all().filter(phoneNumber__in=phone_numbers)
        
        # If no userProfile found, return a 404 response
        if userProfile is None or not userProfile.exists():
            return Response({
                "status": 404,
                "data": None,
                "error": "User not found"
            }, status=status.HTTP_200_OK)

        # Serialize the user profile data
        userProfileSerializer = serializer.UserProfileSerializer(userProfile, many=True)
        
        # Return the user profile data
        context = {
            "status": 200,
            "data": userProfileSerializer.data,
            "error": None
        }
        
        return Response(context, status=status.HTTP_200_OK)