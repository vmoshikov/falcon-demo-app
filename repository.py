import json
from logger import logger



class JsonRepository:
    """
    Класс репозиторий для работы с JSON файлом
    """

    def __init__(self, json_file='books.json'):
        with open(json_file) as f:
            self.__json_file = json_file
            self._file = json.load(f)
            f.close()

    def __iter__(self):
        for item in self._file:
            yield item

    def __str__(self):
        return f"В классе {len(self._file)} объектов"

    def get_list(self, offset: int = 0, limit: int = 10):
        return self._file[offset:offset + limit]

    def get_by_id(self, id: int):
        logger.debug(f"Получаем объект по ID:{id}")
        for item in self._file:
            if item.get('id') == id:
                logger.info(f"Объект найден")
                return item

        return None

    def get_last_id(self):
        logger.debug("Поулчаем ID последнего элемента")
        return self._file[-1].get('id')

    def append(self, item: dict):
        logger.debug(f"Добавляем новый объект")
        self._file.append(item)

    def update(self, id: int, data: dict):
        logger.debug(f"Изменяем объект по ID:{id}")
        i = 0
        while i < len(self._file) and True:
            if self._file[i].get('id') == id:
                logger.info(f"Объект для изменения найден")
                break
            i += 1

        if i < len(self._file):
            self._file[i] = data

    def remove(self, id: int):
        logger.debug(f"Удаляем объект по ID:{id}")
        i = 0
        while i < len(self._file) and True:
            if self._file[i].get('id') == id:
                logger.info(f"Объект для удаления найден")
                break
            i += 1

        if i < len(self._file):
            del self._file[i]


    def commit(self):
        logger.debug(f"Сохраняем изменения в файл")
        with open(self.__json_file, 'w') as f:
            json.dump(self._file, f)
            f.close()

