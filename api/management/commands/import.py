from django.apps import apps
from django.core.management.base import BaseCommand

from utils.import_handler import ImportHandler


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--url', type=str, required=True, help='URL для запроса')
        parser.add_argument('--model', type=str, required=True, help='Модель для загрузки данных')
        parser.add_argument('--pageNum', type=str, help='Номер страницы')
        parser.add_argument('--pageSize', type=str, help='Размер страницы')
        parser.add_argument('--order', type=str, help='Поле сортировки')
        parser.add_argument('--orderDirection', type=str, choices=['asc', 'desc'],
                            help='Сортировка по возрастанию или по убыванию')
        parser.add_argument('--filterstatus', type=str, choices=['ACTIVE', 'ARCHIVE'], help='Фильтрация по статусу')
        parser.add_argument('--offset', type=int, help='Смещение порции данных блока')

    def handle(self, *args, **options):
        url = options.pop('url')
        model_name = options.pop('model')
        model = apps.get_model('api', model_name)
        # Создаём словарь с "непустыми" значениями
        filtered_options = {k: v for k, v in options.items() if v}
        import_handler = ImportHandler(url, model, **filtered_options)
        import_handler.import_data()
