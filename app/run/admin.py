from django.contrib import admin

from .models import Run

# Register your models here.


class RunAdmin(admin.ModelAdmin):
    list_display = ['id', 'run_id', 'pipeline', 'exit_status', 'pipeline_command', 'start_time']
    list_filter = ['id', 'pipeline', 'exit_status', 'pipeline_command', 'start_time']
    search_fields = ['id', 'run_id', 'pipeline', 'exit_status', 'pipeline_command', 'start_time']


admin.site.register(Run, RunAdmin)
