# API Documentation

## Account API

### 1. Login User
- **URL**: `/api/v1/accounts/login/`
- **Method**: `POST`
- **Description**: Login (signIn) user.
- **Request Body**:
  ```json
  {
    "username": "string",
    "password": "string"
  }
**Note:** if the user is an admin, the response will include a field indicating their admin status.
### 2. Register User
- **URL**: `/api/v1/accounts/register/`
- **Method**: `POST`
- **Description**: Register (signUp) user.
- **Request Body**:
  ```json
  {
    "username": "string",
    "fullName": "string",
    "email": "string",
    "password": "string",
    "mobile": "string"
  }
- **Note**: After registering the user, they will be logged in automatically.
### 3. Logout User
- **URL**: `/api/v1/accounts/logout/`
- **Method**: `POST`
- **Description**: Logout user.
- **Request Body**: No body, just to be logged in
### 4. Send Email
- **URL**: `/api/v1/accounts/password_recovery/`
- **Method**: `POST`
- **Description**: send 4 digit code via email to check the email.
- **Request Body**:
  ```json
  {
    "email": "example@gmail.com",
  }
- **Response Body**
  ```json
  {
    "status": 200,
    "data": "xxxx",
    "error": None
  }
- **Method**: `PUT`
- **Description**: check the sent code is correct or not.
- **Request Body**:
  ```json
  {
    "digit": 0000 (int),
  }
### 6. Change Password
- **URL**: `/api/v1/accounts/change_password/`
- **Method**: `POST`
- **Description**: change (reset) user password.
- **Request Body**:
  ```json
  {
    "new_password": "string",
    "confirm_password": "string"
  }
### 7. All User
- **URL**: `/api/v1/accounts/all_users/`
- **Method**: `GET`
- **Description**: get the list of all users
- **Response Body**:
  ```json
  {
      "status": 200,
      "data": [
          {
              "user": 1,
              "profile_img": "/media/userProfile/",
              "fullName": "string",
              "age": int,
              "phoneNumber": "string",
              "email": "email",
              "country": "string",
              "gender": "string"
          }
      ],
      "error": null
  }
### 8. All Specialist Users
- **URL**: `/api/v1/accounts/all_specialist/`
- **Method**: `GET`
- **Description**: get the list of all Specialist users (admin)
- **Response Body**:
  ```json
  {
      "status": 200,
      "data": [
          {
              "user": 2,
              "profile_img": "/media/userProfile/",
              "fullName": "string",
              "age": int,
              "phoneNumber": "string",
              "email": "email",
              "country": "string",
              "gender": "string",
              "position": "string",
              "specialties": "string",
              "experience_years": int,
              "last_login": date
          }
      ],
      "error": null
  }

- **Note**: After registering the user, they will be logged in automatically.
- **Note**: This api is just for admin (web page not mobile)

### 10. Admin Update
- **URL**: `/api/v1/accounts/me_update_admin/`
- **Method**: `PUT`
- **Description**: Each admin can update him/her self.
- **Request Body**:
  ```json
  {
    "fullName": "string",
    "email": "string",
    "phoneNumber": "string",
    "experience_years": int,
    "profile_img": File
  }
### 11. Add Admin
- **URL**: `/api/v1/accounts/add_specialist/`
- **Method**: `POST`
- **Description**: Modir add admin. (admin register)
- **Request Body**:
  ```json
  {
    "fullName": "string",
    "email": "string",
    "mobile": "string",
    "password": "string",
    "specialties": "string"
  }
### 12. Update UserProfile
- **URL**: `/api/v1/accounts/me_update/`
- **Method**: `PUT`
- **Description**: update user profile. see the items that can be update.
- **Request Body**:
  ```json
  {
    "fullName": "string",
    "email": "string",
    "phoneNumber": "string",
    "age": int,
    "profile_img": File,
    "Expenses": int
  }
### 13. Delete user
- **URL**: `/api/v1/accounts/delete_user/<int:user_id>/`
- **Method**: `DELETE`
- **Description**: For admin and **FrontEnd Developer** to delete a specific user. jsut set the user id in the <> in the url.
- **Request Body**:
  ```json
  {

  }
### 14. Delete List of users or admins
- **URL**: `/api/v1/accounts/delete_group/`
- **Method**: `DELETE`
- **Description**: get a list of ids to delete them together.
- **Request Body**:
  ```json
  {
    "user_ids": [0, 0, 0, 0, ...]
  }
### 14. Delete List of users or admins
- **URL**: `/api/v1/accounts/me_admin/`
- **Method**: `GET`
- **Description**: get the profile of admin
- **Response Body**:
  ```json
  {
    "status": 200,
    "data": {
      "fullName": "string",
      "phoneNumber": "string",
      "email": "string",
      "profile_img": "/media/userProfile/default.png",
      "experience_years": int,
      "income": int,
      "is_admin": true
    },
    "error": null
  }