from django.db import models

# Create your models here.
class SpaceDucksData(models.Model):
    created_at = models.TextField()
    updated_at = models.TextField()
    event_type = models.IntegerField()
    payload = models.TextField()
    device_id = models.TextField()
    uuid = models.TextField()
    device_type = models.TextField()
    company_id = models.TextField()

    class Meta:
        db_table = "SpaceDucksData"