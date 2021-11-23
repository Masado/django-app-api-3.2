from django.db import models

# Create your models here.


class Run(models.Model):
    id = models.BigAutoField(primary_key=True)
    run_id = models.CharField(max_length=100)
    pipeline = models.CharField(max_length=100)
    exit_status = models.CharField(max_length=50, blank=True, null=True)
    pipeline_command = models.CharField(max_length=200, blank=True, null=True)
    start_time = models.DateTimeField('date started', auto_now_add=True)

    def __str__(self):
        return self.run_id
