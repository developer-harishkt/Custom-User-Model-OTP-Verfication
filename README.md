# Custom-User-Model-OTP-Verfication
This is a Django Application, featuring:

- Registration of a user into the application after verifying the mobile phone with OTP.
- TokenBased Login & Logout with django-rest-knox authentication 

API's:

- http://localhost:8000/api/validate_phone (POST):
  
  Request-Parameters:
  
  {
    "phone": <10-digit-Mobile-Number>
  }
  
  Response:

  {
    "status" : True/False
    "detail": OTP Sent / Bad Request
  }
  
  // OTP will be sent using the 2factor.io API's
  
- http://localhost:8000/api/validate_otp (POST):

  Request-Parameters:
  
  {
    "phone": <10-digit-Mobile-Number>
    "otp" : <4-digit>
  }
  
  Response:

  {
    "status" : True/False
    "detail": Verified / Bad Request
  }

- http://localhost:8000/api/register (POST):

  Request-Parameters:
  
  {
    "phone": <10-digit-Mobile-Number>
    "password" : <password>
  }
  
  Response:

  {
    "status" : True/False
    "detail": Account Created / Bad Request
  }
