import datetime

from django.db import models


class KBKStatus(models.TextChoices):
    ACTIVE = "ACTIVE", 'Актуальная запись'
    ARCHIVE = "ARCHIVE", 'Архивная запись'


class BudgetType(models.TextChoices):
    """Код типа бюджета"""
    OTHER = "00", 'Прочие бюджеты'
    FEDERAL = "01", 'Федеральный бюджет'
    SUBJECT = "02", 'Бюджет субъекта РФ'
    CAPITALS = "03", 'Бюджеты внутригородских МО г. Москвы и г. Санкт-Петербурга'
    CITY = "04", 'Бюджет городского округа'
    MUNICIPAL = "05", 'Бюджет муниципального района'
    PENSION = "06", 'Бюджет Пенсионного фонда РФ'
    FSS = "07", 'Бюджет ФСС РФ'
    FFOMS = "08", 'Бюджет ФФОМС'
    TFOMS = "09", 'Бюджет ТФОМС'
    LOCAL = "10", 'Бюджет поселения'
    # Есть 13 код в документации не описан, возможно есть и другие
    DISTRIBUTED = "98", 'Распределяемый доход'
    ORGANIZATION = "99", 'Доход организации (только для ПДИ)'

    __empty__ = '(Unknown)'


class BaseModel(models.Model):
    code = models.CharField(
        "Код",
        max_length=8,
        blank=False,
        null=False
    )
    name = models.TextField(
        "Полное наименование",
        max_length=2000,
        blank=False,
        null=False)
    startdate = models.DateTimeField(
        "Дата начала действия записи",
        blank=False,
        null=False,
        default=datetime.datetime.now)
    enddate = models.DateTimeField(
        "Дата окончания действия записи",
        blank=True,
        null=True,
        default=None
    )

    class Meta:
        abstract = True

    @classmethod
    def get_by_code(cls, code):
        return cls.objects.filter(code=code).first() or None

    @classmethod
    def get_by_name(cls, name):
        return cls.objects.filter(name=name).first()

    @classmethod
    def get_field_names(cls):
        return [f.name for f in cls._meta.fields if not f.primary_key]


class Budget(BaseModel):
    parentcode = models.ForeignKey(
        'self',
        verbose_name="Вышестоящий бюджет",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
    status = models.CharField(
        "Статус записи",
        max_length=7,
        choices=KBKStatus.choices,
        blank=False,
        null=False,
        default=KBKStatus.ACTIVE
    )
    budgtypecode = models.CharField(
        "Тип бюджета",
        max_length=2,
        choices=BudgetType.choices,
        blank=False,
        null=False,
        default=BudgetType.OTHER)

    class Meta:
        verbose_name = 'Справочник бюджетов'
        verbose_name_plural = 'Справочники бюджетов'

    def __str__(self):
        return f"{self.code}: {self.name}"


class GlavBudgetClass(BaseModel):
    """Справочник главы по бюджетной классификации."""
    budgetname = models.ForeignKey(
        Budget,
        verbose_name="Бюджет",
        blank=False,
        null=False,
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'Справочник главы по бюджетной классификации'
        verbose_name_plural = 'Справочники главы по бюджетной классификации'

    def __str__(self):
        return f"{self.code}: {self.name}"
