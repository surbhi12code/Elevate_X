

from django.db import models
# from django.contrib.auth.models import User
from django.conf import settings

class Certificate(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    test_name = models.CharField(max_length=255)
    score = models.DecimalField(max_digits=5, decimal_places=2)
    certificate_file = models.FileField(upload_to='certificates/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Certificate for {self.user.username} - {self.test_name}"
