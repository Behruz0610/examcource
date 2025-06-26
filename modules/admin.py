from django.contrib import admin
from .models import Module, Lecture
from .models import ModuleComment, ModuleRating


class LectureAdmin(admin.ModelAdmin):
    prepopulated_fields = {"lecture_slug": ("lecture_title", )}

class ModuleAdmin(admin.ModelAdmin):
    prepopulated_fields = {"module_slug": ("module_title", )}

admin.site.register(Module)
admin.site.register(Lecture)

admin.site.register(ModuleComment)
admin.site.register(ModuleRating)