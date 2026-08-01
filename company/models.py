from django.db import models

class Company(models.Model):
    name = models.CharField(max_length=100)
    cnpj = models.CharField(max_length=14, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('user.User', on_delete=models.CASCADE)
    delete = models.BooleanField(default=False)

    def __str__(self):
        return self.name
