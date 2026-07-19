from django.core.exceptions import ValidationError
from django.db import models
from core.models import TimeStampedModel
from .university import University
from apps.academic.models.enums import (
    DegreeType,
    StudySystem,
    CourseCategory,
    SessionTerm,
    RepeatPolicy,
)



class GradingScheme(TimeStampedModel):
    """
    Defines a grading policy used by a university.

    A university may have multiple grading schemes over time,
    but only one grading scheme can be active at any given moment.
    """

    university = models.ForeignKey(
        University,
        on_delete=models.CASCADE,
        related_name="grading_schemes",
    )

    name = models.CharField(
        max_length=100,
    )

    repeat_policy = models.CharField(
        max_length=30,
        choices=RepeatPolicy.choices,
        default=RepeatPolicy.LATEST_ATTEMPT,
    )

    effective_from = models.DateField()

    effective_to = models.DateField(
        null=True,
        blank=True,
    )

    is_active = models.BooleanField(
        default=False,
    )

    class Meta:
        ordering = (
            "-effective_from",
        )

        verbose_name = "Grading Scheme"
        verbose_name_plural = "Grading Schemes"

    def clean(self):
        """
        Validate the grading scheme.
        """

        self._validate_effective_dates()
        self._validate_single_active_scheme()

    def _validate_effective_dates(self):
        """
        Ensure effective_from is not after effective_to.
        """

        if (
            self.effective_to
            and self.effective_from > self.effective_to
        ):
            raise ValidationError(
                {
                    "effective_from": (
                        "Effective from date cannot be after effective to date."
                    )
                }
            )

    def _validate_single_active_scheme(self):
        """
        Ensure a university has only one active grading scheme.
        """

        if not self.is_active:
            return

        active_scheme = (
            GradingScheme.objects.filter(
                university=self.university,
                is_active=True,
            )
            .exclude(
                pk=self.pk,
            )
        )

        if active_scheme.exists():
            raise ValidationError(
                {
                    "is_active": (
                        "A university can only have one active grading scheme."
                    )
                }
            )

    def __str__(self):
        return (
            f"{self.university.name} - {self.name}"
        )