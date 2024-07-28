from django.contrib.auth import get_user_model
from django.db import models
from tinymce.models import HTMLField

User = get_user_model()


class AlgorithmCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    parent = models.ForeignKey(
        to='self',
        null=True,
        blank=True,
        related_name='children',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'algorithm_categories'
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Algorithm(models.Model):
    category = models.ForeignKey(
        to=AlgorithmCategory,
        null=False,
        blank=False,
        related_name='algorithm_algorithms',
        on_delete=models.PROTECT
    )
    name = models.CharField(max_length=255)
    description = HTMLField()
    slug = models.SlugField(max_length=255, unique=True)
    component = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'algorithm_algorithms'
        ordering = ['-created_at']


class Comment(models.Model):
    user = models.ForeignKey(
        to=User,
        null=False,
        blank=False,
        related_name='comments',
        on_delete=models.CASCADE
    )
    algorithm = models.ForeignKey(
        to=Algorithm,
        null=False,
        blank=False,
        related_name='comments',
        on_delete=models.CASCADE
    )
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.first_name} {self.user.last_name} on {self.algorithm.name}"

    class Meta:
        db_table = 'algorithm_comments'
        ordering = ['-created_at']


class UserProgress(models.Model):
    user = models.ForeignKey(
        to=User,
        null=False,
        blank=False,
        related_name='user_progress',
        on_delete=models.CASCADE
    )
    algorithm = models.ForeignKey(
        to=Algorithm,
        null=False,
        blank=False,
        related_name='user_progress',
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'algorithm_user_progress'
        unique_together = (('user', 'algorithm'),)
