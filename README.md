# ТЗ для backend разработчика

## Описание задачи:
Создать серверное приложение, которое должно реализовывать следующий функционал:

1. Импорт в модель Budget (Приложение 1) данных из [api](http://budget.gov.ru/epbs/faces/p/%D0%94%D0%B0%D0%BD%D0%BD%D1%8B%D0%B5%20%D0%B8%20%D1%81%D0%B5%D1%80%D0%B2%D0%B8%D1%81%D1%8B/opendata?code=7710568760-BUDGETS&_adf.ctrl-state=9j2lrpn45_123&regionId=66)

   Пример запроса: 
      ```http://budget.gov.ru/epbs/registry/7710568760-BUDGETS/data?pageSize=1000&filterstatus=ACTIVE&pageNum=1```
2. Данные могут импортироваться повторно, при этом в уже загруженных элементах поля должны обновляться   
3. api позволяет получать данные только постранично, для реализации импорта необходимо обеспечить автоматическое получение всех страниц
4. Необходимо загрузить все поля всех элементов справочника со статусом ACTIVE
5. Для элементов, у которых в данных, получаемых через API, указан parentcode,  при импорте это поле должно заполняться не оригинальным значением, а id элемента соответствующей записи в базе данных 
6. Механизм должен быть универсальным (класс или модуль) в который передаются настройки: url API, соответствие полей в API и модели данных, другое при необходимости
7. Реализованный механизм должен без изменений (меняются только настройки(параметры)) работать с иными схожими api и моделями.

   Например: ```http://budget.gov.ru/epbs/registry/7710568760-BUDGETCLASGRBSFB/data?pageSize=1000&pageNum=1```
   и моделью GlavBudgetClass
8. Способ вызова механизма импорта — на ваше усмотрение
9. Описание моделей дается для упрощения понимания задачи, обоснованные изменения для улучшения нейминга и оформления кода приветствуются. При этом id(PrimaryKey) в модели и в API это разные поля с разными кодами, а для перечислений значения используемые в системе и в api различаются
10. Необходимо уметь обосновать выбор того или иного алгоритма загрузки данных с точки зрения эффективности и универсальности, в частности так как загрузка выполняется на сервере, а объем загружаемых данных может быть достаточно велик, вероятно загрузка всех данных в память с последующей обработкой не является хорошим решением. Также стоит обратить внимание на то что первичная загрузка данных не является наиболее частым случаем использования и вероятно стоит в большей степени ориентироваться на основной сценарий когда большая часть данных загружена и происходит их “обновление” (“дозагрузка”)

## Обязательные требования:
1. Стек технологий:
   * Django
   * DRF
2. Максимально использовать возможности фреймворков
    
## Реализация:
1. Собрать и запустить docker-контейнеры с приложением и postgresql:```docker-compose up -d```
2. Выполнить импорт данных с типом ACTIVE для модели Budget: ```docker exec -it app python manage.py import --url http://budget.gov.ru/epbs/registry/7710568760-BUDGETS/data --filterstatus ACTIVE --model Budget```
3. Выполнить импорт данных для модели GlavBudgetClass: ```docker exec -it app python manage.py import --url http://budget.gov.ru/epbs/registry/7710568760-BUDGETCLASGRBSFB/data --model GlavBudgetClass```
4. Проверить загрузку данных, выполнив запросы: 
   * ```GET http://127.0.0.1:8000/api/budget/``` 
   * ```GET http://127.0.0.1:8000/api/glavbudgetclass/```
   
Все параметры команды можно узнать, выполнив ```python manage.py import --help```