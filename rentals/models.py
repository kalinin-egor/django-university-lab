from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models


class Car(models.Model):
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.PositiveIntegerField()
    vin = models.CharField(max_length=17, unique=True)
    color = models.CharField(max_length=50)
    daily_rental_price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        ordering = ['brand', 'model', 'year']

    def __str__(self) -> str:
        return f"{self.brand} {self.model} ({self.year})"


class Client(models.Model):
    full_name = models.CharField(max_length=255)
    driver_license_number = models.CharField(max_length=50, unique=True)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField(unique=True)

    class Meta:
        ordering = ['full_name']

    def __str__(self) -> str:
        return self.full_name


class ExtraService(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = 'extra service'
        verbose_name_plural = 'extra services'
        ordering = ['name']

    def __str__(self) -> str:
        return self.name


class Rental(models.Model):
    class RentalStatus(models.TextChoices):
        RESERVED = 'reserved', 'Reserved'
        ACTIVE = 'active', 'Active'
        COMPLETED = 'completed', 'Completed'
        CANCELLED = 'cancelled', 'Cancelled'

    car = models.ForeignKey(Car, on_delete=models.PROTECT, related_name='rentals')
    client = models.ForeignKey(Client, on_delete=models.PROTECT, related_name='rentals')
    extra_services = models.ManyToManyField(ExtraService, related_name='rentals', blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=RentalStatus.choices, default=RentalStatus.RESERVED)

    class Meta:
        ordering = ['-start_date']

    def __str__(self) -> str:
        return f"Rental #{self.pk} - {self.car}"

    def clean(self) -> None:
        if self.end_date < self.start_date:
            raise ValidationError('End date cannot be earlier than start date.')


class ekexam(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    exam_date = models.DateField()
    task_image = models.ImageField(upload_to='exam_tasks/')
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='ek_exams', blank=True)
    is_public = models.BooleanField(default=False)

    class Meta:
        ordering = ['-exam_date', '-created_at']
        verbose_name = 'exam'
        verbose_name_plural = 'exams'

    def __str__(self) -> str:
        return self.name
