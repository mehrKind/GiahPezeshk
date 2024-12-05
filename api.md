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
### 2. Register User
- **URL**: `/api/v1/accounts/register/`
- **Method**: `POST`
- **Description**: Register (signUp) user.
- **Request Body**:
  ```json
  {
    "username": "string",
    "password": "string"
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
    "digit": "xxxx",
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
              "age": 0,
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
              "age": 0,
              "phoneNumber": "string",
              "email": "email",
              "country": "string",
              "gender": "string",
              "position": "string",
              "specialties": 0,
              "experience_years": 0
          }
      ],
      "error": null
  }