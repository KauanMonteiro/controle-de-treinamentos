from django.db import models

class Company(models.Model):
    name = models.CharField(max_length=100)
    cnpj = models.CharField(max_length=14)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('user.User', on_delete=models.CASCADE)

    def __str__(self):
        return self.name
