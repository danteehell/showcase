from django.db import models

class Campus(models.Model):
    name=models.CharField(max_length=200,verbose_name="Корпус")
    address=models.CharField(max_length=400,blank=True,null=True,verbose_name="Адрес")
    abbreviation=models.CharField(max_length=2,blank=True,null=True,verbose_name="Аббревиатура")
    metro_station=models.CharField(max_length=20,blank=True,null=True,verbose_name="Станция метро")

    class Meta:
        verbose_name="Корпус"
        verbose_name_plural="Корпуса"

    def __str__(self):
        return self.name

class Partner(models.Model):
    name=models.CharField(max_length=200,verbose_name="Партнёр")
    website=models.URLField(blank=True,null=True,verbose_name="Сайт")
    email=models.EmailField(blank=True,null=True,verbose_name="Email")
    phone=models.CharField(max_length=50,blank=True,null=True,verbose_name="Телефон")
    internship=models.BooleanField(null=True,blank=True,verbose_name="Стажировка")

    class Meta:
        verbose_name="Партнёр"
        verbose_name_plural="Партнёры"

    def __str__(self):
        return self.name

class Curator(models.Model):
    first_name=models.CharField(max_length=100,verbose_name="Имя")
    last_name=models.CharField(max_length=100,verbose_name="Фамилия")
    email=models.EmailField(blank=True,null=True,verbose_name="Email")

    class Meta:
        verbose_name="Куратор"
        verbose_name_plural="Кураторы"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class FilterCategory(models.Model):
    TYPE_CHOICES=[
        ("theme","Тематика"),
        ("specialty","Специальность"),
        ("course","Курс"),
        ("campus","Корпус"),
        ("difficulty","Сложность"),
        ("partner","Партнёр"),
    ]
    category_type=models.CharField(max_length=20,choices=TYPE_CHOICES,blank=True,null=True)
    name=models.CharField(max_length=100,verbose_name="Название категории")

    class Meta:
        verbose_name="Категория фильтра"
        verbose_name_plural="Категории фильтров"

    def __str__(self):
        return self.name

class FilterOption(models.Model):
    category=models.ForeignKey(FilterCategory,on_delete=models.CASCADE,related_name="options",verbose_name="Категория")
    name=models.CharField(max_length=200,verbose_name="Опция фильтра")

    class Meta:
        verbose_name="Опция фильтра"
        verbose_name_plural="Опции фильтров"

    def __str__(self):
        return f"{self.category.name} - {self.name}"

class ScheduleItem(models.Model):
    DAYS=[
        (0,'Понедельник'),
        (1,'Вторник'),
        (2,'Среда'),
        (3,'Четверг'),
        (4,'Пятница'),
        (5,'Суббота'),
        (6,'Воскресенье')
    ]
    day_of_week=models.IntegerField(choices=DAYS,verbose_name="День недели")
    start_time=models.TimeField(verbose_name="Время начала")
    end_time=models.TimeField(blank=True,null=True,verbose_name="Время окончания")
    note=models.CharField(max_length=200,blank=True,null=True,verbose_name="Примечание")

    class Meta:
        verbose_name="Расписание"
        verbose_name_plural="Расписания"

    def __str__(self):
        return f"{self.get_day_of_week_display()} {self.start_time.strftime('%H:%M')} - {self.end_time.strftime('%H:%M') if self.end_time else ''}"

class CourseYear(models.Model):
    year=models.PositiveSmallIntegerField(verbose_name="Курс")

    class Meta:
        verbose_name="Курс студента"
        verbose_name_plural="Курсы студентов"

    def __str__(self):
        return str(self.year)

class Project(models.Model):
    title=models.CharField(max_length=300,verbose_name="Название проекта")
    theme=models.ForeignKey(FilterOption,on_delete=models.SET_NULL,null=True,blank=True,related_name="projects_as_theme",limit_choices_to={"category__category_type":"theme"},verbose_name="Тематика")
    specialties=models.ManyToManyField(FilterOption,blank=True,related_name="projects_as_specialty",limit_choices_to={"category__category_type":"specialty"},verbose_name="Специальности")
    campus=models.ForeignKey(FilterOption,on_delete=models.SET_NULL,null=True,blank=True,related_name="projects_as_campus",limit_choices_to={"category__category_type":"campus"},verbose_name="Корпус")
    courses=models.ManyToManyField(FilterOption,blank=True,related_name="projects_as_course",limit_choices_to={"category__category_type":"course"},verbose_name="Курсы студентов")
    difficulty=models.ForeignKey(FilterOption,on_delete=models.SET_NULL,null=True,blank=True,related_name="projects_as_difficulty",limit_choices_to={"category__category_type":"difficulty"},verbose_name="Сложность")
    partner=models.ForeignKey("Partner",on_delete=models.SET_NULL,null=True,blank=True,verbose_name="Партнёр")
    curator=models.ForeignKey("Curator",on_delete=models.SET_NULL,null=True,blank=True,verbose_name="Куратор")
    internship=models.BooleanField(default=False,verbose_name="Стажировка")
    spots_remaining=models.IntegerField(default=0,verbose_name="Оставшиеся места")
    short_description=models.TextField(blank=True,verbose_name="Короткое описание")
    long_description=models.TextField(blank=True,verbose_name="Расширенное описание")
    created_at=models.DateTimeField(auto_now_add=True,verbose_name="Дата создания")
    updated_at=models.DateTimeField(auto_now=True,verbose_name="Дата обновления")
    is_active=models.BooleanField(default=True,verbose_name="Доступен")

    class Meta:
        verbose_name="Проект"
        verbose_name_plural="Проекты"

    def __str__(self):
        return self.title
    
    @classmethod
    def get_total_count(cls):
        """
        Возвращает общее количество всех проектов
        """
        return cls.objects.count()
    
    @classmethod
    def get_active_count(cls):
        """
        Возвращает количество доступных проектов (is_active=True)
        """
        return cls.objects.filter(is_active=True).count()
    
    @classmethod
    def get_available_count(cls):
        """
        Возвращает количество доступных проектов со свободными местами
        """
        return cls.objects.filter(is_active=True, spots_remaining__gt=0).count()

class ProjectListItem(models.Model):
    TYPES=[
        ('requirement','Требование'),
        ('feature','Особенность'),
        ('motivation','Мотивация')
    ]
    project=models.ForeignKey(Project,on_delete=models.CASCADE,related_name='list_items',verbose_name="Проект")
    type=models.CharField(max_length=50,choices=TYPES,verbose_name="Тип элемента")
    position=models.PositiveIntegerField(default=0,verbose_name="Позиция")
    text=models.TextField(verbose_name="Текст")

    class Meta:
        verbose_name="Элемент списка проекта"
        verbose_name_plural="Элементы списков проектов"

    def __str__(self):
        return f"{self.project.title} - {self.get_type_display()} ({self.position})"