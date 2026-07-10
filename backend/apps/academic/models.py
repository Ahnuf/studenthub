from django.db import models
from core.models import TimeStampedModel



class University(TimeStampedModel):
    name = models.CharField(
        max_length=255,
        unique=True,
    )

    short_name = models.CharField(
        max_length=20,
        unique=True,
    )

    country = models.CharField(
        max_length=100,
        default="Pakistan",
    )

    city = models.CharField(
        max_length=100,
    )

    website = models.URLField(
        blank=True,
    )

    logo = models.ImageField(
        upload_to="universities/logos/",
        blank=True,
        null=True,
    )

    is_active = models.BooleanField(
        default=True,
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "University"
        verbose_name_plural = "Universities"

    def __str__(self):
        return self.short_name
