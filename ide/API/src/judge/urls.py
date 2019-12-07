from django.contrib import admin
from rest_framework import routers
from django.urls import path, include

from submission.views import Check, Submit, doc, apispec

router = routers.DefaultRouter()
# router.register(r'users', )

urlpatterns = [
    path('admin/', admin.site.urls),  # Admin site
    path('check/<int:subid>', Check.as_view()),  # Check API
    path('submit', Submit),          # Submit API
    path('', doc),
    path('apispec', apispec)
]
