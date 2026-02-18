from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    patronymic = models.CharField(
        max_length=150,
        verbose_name='Patronymic',
        blank=True
    )

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profile'

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


def validate_image_size(image):
    if image.size > 2 * 1024 * 1024:
        raise ValidationError('The image size must not exceed 2 MB.')


def validate_image_extension(value):
    allowed = ['jpg', 'jpeg', 'png', 'bmp']
    ext = value.name.split('.')[-1].lower()
    if ext not in allowed:
        raise ValidationError('Invalid image format')


class Category(models.Model):
    name = models.CharField(
        'Category name',
        max_length=100,
        unique=True
    )

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

class DesignRequest(models.Model):
    class Status(models.TextChoices):
        NEW = 'new', 'New'
        IN_PROGRESS = 'in_progress', 'In Progress'
        DONE = 'done', 'Done'

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='User'
    )

    title = models.CharField('Name', max_length=200)
    description = models.TextField('Description')

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name='Category'
    )

    photo = models.ImageField(
        'Photo of the room / plan',
        upload_to='design_requests/photos/',
        validators=[validate_image_size, validate_image_extension]
    )

    result_image = models.ImageField(
        'Photo of the completed work',
        upload_to='design_requests/results/',
        blank=True,
        null=True
    )

    admin_comment = models.TextField(
        'Administrators comment',
        blank=True,
        null=True
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.NEW,
        verbose_name='Status'
    )

    created_at = models.DateTimeField(
        'Creation date',
        auto_now_add=True
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Design request'
        verbose_name_plural = 'Design requests'

    def __str__(self):
        return self.title