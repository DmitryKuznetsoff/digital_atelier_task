from urllib.parse import urlsplit, urlencode, parse_qs

import requests

from utils.fix_naive_tz import fix_naive_tz
from api.models import Budget


class ImportHandler:
    def __init__(self, url, model, **kwargs):
        self.url = url
        self.model = model
        self.kwargs = kwargs

    def get_page_url(self):
        # Формирует url с указанными в **kwargs параметрами запроса:
        parsed_url = urlsplit(self.url)
        query = parse_qs(parsed_url.query)
        query.update(**self.kwargs)
        new_query = urlencode(query, doseq=True)
        parsed_url = parsed_url._replace(query=new_query)
        return parsed_url.geturl()

    def get_page_data(self):
        page_url = self.get_page_url()
        response = requests.get(page_url)
        return response.json()['data']

    def get_import_data(self):
        # Возвращает данные только с одной страницы, если её номер передан в параметрах запроса:
        if 'pageNum' in self.kwargs:
            data = self.get_page_data()
            yield data
        # Возвращает данные с каждой страницы:
        else:
            page_num = 1
            while True:
                self.kwargs.update({'pageNum': page_num})
                data = self.get_page_data()
                if not data:
                    break
                yield data
                page_num += 1

    def validate_import_data(self, data):
        import_data = self.filter_data_fields(data)
        self.handle_empty_field(import_data, 'startdate')
        self.handle_empty_field(import_data, 'enddate')
        # Обработка поля paretncode:
        if 'parentcode' in import_data:
            self.replace_parentcode(import_data)
        # Обработка поля budgetname:
        if 'budgetname' in import_data:
            self.replace_budgetname(import_data)
        # От сервера могут прийти даты без часового пояса, фиксим их:
        startdate = import_data.get('startdate')
        enddate = import_data.get('enddate')
        if startdate:
            import_data['startdate'] = fix_naive_tz(startdate)
        if enddate:
            import_data['enddate'] = fix_naive_tz(enddate)
        return import_data

    @staticmethod
    def handle_empty_field(data, field):
        # Обрабатывает пустые поля в data, присваивает им значение = None
        if not data[field]:
            data[field] = None
        return data

    def replace_parentcode(self, data):
        # Обрабатывает поле parentcode: заменяет его на соответствующий id в БД приложения
        parentcode = data.get('parentcode')
        new_parentcode = self.model.get_by_code(parentcode)
        data['parentcode'] = new_parentcode
        self.handle_empty_field(data, 'parentcode')
        return data

    def replace_budgetname(self, data):
        budgetname = data['budgetname'].capitalize()
        new_budgetname = Budget.get_by_name(budgetname)
        data['budgetname'] = new_budgetname
        return data

    def filter_data_fields(self, data):
        # Оставляет в data только те поля, которые соответствуют полям модели model
        model_fields = self.model.get_field_names()
        return {k: data[k] for k in model_fields}

    def compare_db_obj_with_import_data(self, obj_from_db, import_data):
        obj_attrs = {attr: getattr(obj_from_db, attr) for attr in self.model.get_field_names()}
        return obj_attrs == import_data

    def import_data(self):
        data = self.get_import_data()
        for d in data:
            for i in d:
                import_data = self.validate_import_data(i)
                code = import_data['code']
                obj_from_db = self.model.get_by_code(code)
                if not obj_from_db:
                    self.model.objects.create(**import_data)
                else:
                    if not self.compare_db_obj_with_import_data(obj_from_db, import_data):
                        self.model.objects.filter(id=obj_from_db.id).update(**import_data)
                    continue
