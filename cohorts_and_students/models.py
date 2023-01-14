from django.db import models
import uuid
from django.utils.text import slugify

class Cohort(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cohort_name = models.CharField(max_length=200)
    start_date = models.DateField(auto_now=True) 
    end_date = models.CharField(max_length=200)

    def __str__(self):
        return f"id={self.id}, cohort_name={self.cohort_name}, start_date={self.start_date}, end_date={self.end_date}"

class Student(models.Model):
    cohort = models.ForeignKey(Cohort, on_delete=models.CASCADE, related_name='students')
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=100)

    def save(self, *args, **kwargs):
        self.slug = slugify(f"{self.first_name} {self.last_name} {self.cohort.cohort_name}")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"id={self.id}, first_name={self.first_name}, last_name={self.last_name}"