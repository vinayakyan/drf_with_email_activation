from django.contrib import admin
from django.urls import path
from api.views import SignUpApi, VerifyEmail

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', SignUpApi.as_view()),
    path('verify/', VerifyEmail.as_view(), name='email-verify'),
]
