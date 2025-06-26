from django.db import models
from courses.models import Course
from django.utils.text import slugify
from django.conf import settings


class Module(models.Model):
    module_title = models.CharField(max_length=200, verbose_name="Module Title")
    course = models.ForeignKey(Course, related_name="modules", on_delete=models.CASCADE)
    module_order = models.PositiveIntegerField(default=1, verbose_name="Module Order")
    module_description = models.TextField(blank=True, null=True, verbose_name="Module Description")

    def __str__(self):
        return self.module_title

class Lecture(models.Model):
    lecture_title = models.CharField(max_length=255, verbose_name="Lecture Title")
    lecture_slug = models.SlugField(verbose_name="Lecture Slug", blank=True)
    lecture_description = models.TextField(blank=True, null=True, verbose_name="Lecture Description")
    module = models.ForeignKey(Module, related_name="lectures", on_delete=models.CASCADE)
    lecture_file = models.FileField(upload_to="files/", blank=True, null=True)
    lecture_video = models.CharField(max_length=150, blank=True, null=True, verbose_name="Video ID")
    lecture_previewable = models.CharField(
        choices = (('Yes', 'Yes'), ('No', 'No')),
        default = 'Yes',
        max_length=50,
        verbose_name="Is Previewable?"
    )
    lecture_created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created Date")
    lecture_updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated Date")
    seo_lecture_title = models.CharField(max_length=60, blank=True, null=True, verbose_name="SEO Lecture Title (60 Characters Long)")
    seo_lecture_keyword = models.TextField(blank=True, null=True, verbose_name="SEO Lecture Keywords, Separated by Comma")
    seo_lecture_description = models.TextField(blank=True, null=True, verbose_name="SEO Lecture Description (160 Characters Long)")

    def __str__(self):
        return self.lecture_title
    

    def save(self, *args, **kwargs):
        if not self.lecture_slug:
            self.lecture_slug = slugify(self.lecture_title)
        super().save(*args, **kwargs)
    

class ModuleComment(models.Model):
    module = models.ForeignKey(Module, related_name="comments", on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    comment = models.TextField(verbose_name="Comment")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.module}"

class ModuleRating(models.Model):
    module = models.ForeignKey(Module, related_name="ratings", on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(verbose_name="Rating (1-5)")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.module} - {self.rating}"