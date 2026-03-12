from django.db import models

class Branch(models.Model):
    name = models.CharField(max_length=120)  # city name
    code = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Level(models.Model):
    # Global levels (same across branches)
    name = models.CharField(max_length=120)  # e.g., Grade 10 / Level 2
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "name"]
        unique_together = [("name", "order")]

    def __str__(self):
        return self.name

class Batch(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.PROTECT, related_name="batches")
    level = models.ForeignKey(Level, on_delete=models.PROTECT, related_name="batches")
    name = models.CharField(max_length=120)  # e.g., Batch A
    year = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = [("branch", "level", "name", "year")]
        ordering = ["-year", "name"]

    def __str__(self):
        return f"{self.branch} - {self.level} - {self.name} ({self.year})"
