from django.contrib import admin
from fcc_opif.models import FileForm

@admin.register(FileForm)
class FileFormAdmin(admin.ModelAdmin):
	list_display = (
		'name',
		'created_at',
		'last_updated_at',
		)