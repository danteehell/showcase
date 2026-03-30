from django.db import models
from django.utils.text import slugify


class TaskCategory(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name='Название категории')
    slug = models.SlugField(unique=True, verbose_name='Slug')

    class Meta:
        verbose_name = 'Категория задачи'
        verbose_name_plural = 'Категории задач'
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Task(models.Model):

    class Difficulty(models.TextChoices):
        EASY = 'easy', 'Лёгкая'
        MEDIUM = 'medium', 'Средняя'
        HARD = 'hard', 'Сложная'

    class Status(models.TextChoices):
        DRAFT = 'draft', 'Черновик'
        PUBLISHED = 'published', 'Опубликована'
        CLOSED = 'closed', 'Закрыта'
        ARCHIVED = 'archived', 'Архив'

    title = models.CharField(max_length=255, verbose_name='Название задачи')
    short_description = models.TextField(verbose_name='Краткое описание')
    description = models.TextField(blank=True, null=True, verbose_name='Полное описание')

    project = models.ForeignKey(
        'showcase.Project',
        on_delete=models.CASCADE,
        related_name='tasks',
        verbose_name='Проект'
    )

    category = models.ForeignKey(
        TaskCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='tasks',
        verbose_name='Категория'
    )

    difficulty = models.CharField(
        max_length=10,
        choices=Difficulty.choices,
        default=Difficulty.MEDIUM,
        db_index=True,
        verbose_name='Сложность'
    )

    points = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        verbose_name='Баллы'
    )

    deadline = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='Дедлайн'
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.DRAFT,
        db_index=True,
        verbose_name='Статус'
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создано')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлено')

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['difficulty']),
        ]

    def __str__(self):
        return self.title


class TaskSkill(models.Model):
    class SkillLevel(models.TextChoices):
        BEGINNER = 'beginner', 'Начальный'
        INTERMEDIATE = 'intermediate', 'Средний'
        ADVANCED = 'advanced', 'Продвинутый'

    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='task_skills', verbose_name='Задача')
    skill = models.CharField(max_length=250, verbose_name='Навык')
    level_required = models.CharField(
        max_length=20,
        choices=SkillLevel.choices,
        default=SkillLevel.BEGINNER,
        verbose_name='Уровень',
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = 'Навык задачи'
        verbose_name_plural = 'Навыки задач'
        unique_together = ('task', 'skill')

    def __str__(self):
        return f'{self.task} - {self.skill}'