# Trello-Tasks
Код к задачкам на Trello


## Review comments
1. Оформить как пакет
2. Вынести в отдельный модуль модели
3. Совет: добавить к моделям
```python
__mapper_args__ = {"eager_defaults": True}
```
4. Вынести создание `engine` в отдельный объект аля `SessionManager`
5. Использовать аннотации.
6. Юзать линтеры. Советую ruff + mypy
7. Для таких вещей
```python
Airport.city.like(f'%{name_fragment}%')
```
советую использовать индексы, [соответствующие](https://postgrespro.ru/docs/postgresql/9.6/pgtrgm)
8. МЕШАТЬ асинхронность (fastapi+uvicorn) вместе с синхронным кодом (sqlalchemy обычная) это блять ТАБУ.
9. Советую вместо `session.query(...)` использовать `select(...)`
10. Вообще весь код для работы с бд стоило бы выделить в отдельный класс, которому передавался бы какой-нибудь `SessionManager`
11. Все ошибки которые показывает mypy + ruff.