from django.db import models
import uuid
from django.contrib.postgres.fields import JSONField

class FileForm(models.Model):
	name = models.CharField(max_length = 200)
	created_at = models.DateTimeField(auto_now_add = True)
	last_updated_at = models.DateTimeField(auto_now = True)
	boxes = JSONField(null=True)
	ocr_data = JSONField(null=True)
	proto_file_field = models.UUIDField(
        editable=False, max_length=200, null=True
    )