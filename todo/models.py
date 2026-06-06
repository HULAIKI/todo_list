from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    STATUS = (
        ('Pending', 'Pending'),
        ('Progress', 'Progress'),
        ('Done', 'Done'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS, default='Pending')

    # 🔥 TAMBAHAN: otomatis isi waktu saat task dibuat
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title