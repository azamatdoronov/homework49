from django.db import models

TYPES = [('Task', 'Задача'), ('Bug', 'Ошибка'), ('Enhancement', 'Улучшение')]
STATUSES = [('New', 'Новая'), ('In progress', 'В процессе'), ('Done', 'Выполнено')]


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата изменения")

    class Meta:
        abstract = True


class Status(models.Model):
    status = models.CharField(max_length=35, choices=STATUSES)

    def __str__(self):
        return f'{self.status}'

    class Meta:
        db_table = "status"
        verbose_name = 'Статус'
        verbose_name_plural = 'Статусы'


class Type(BaseModel):
    type = models.CharField(max_length=35, choices=TYPES)

    def __str__(self):
        return f'{self.type}'

    class Meta:
        db_table = "types"
        verbose_name = 'Тип'
        verbose_name_plural = 'Типы'


class Issue(BaseModel):
    summary = models.CharField(max_length=50, null=False, blank=False, verbose_name="Краткое описание")
    description = models.TextField(max_length=3000, null=True, blank=True, verbose_name="Описание")
    status = models.ForeignKey("webapp.Status", on_delete=models.PROTECT, related_name="status",
                               verbose_name='Статус')
    type = models.ForeignKey("webapp.Status", on_delete=models.PROTECT, related_name="type",
                             verbose_name='Тип')

    def __str__(self):
        return f"{self.id}. {self.summary}: {self.description}"

    class Meta:
        db_table = "issue"
        verbose_name = "задача"
        verbose_name_plural = "задачи"
