# ЗАДАНИЕ ПО ТЕМЕ "Очереди для обмена данными между потоками"

import threading
from queue import Queue
from time import sleep
from random import randint


# Класс Table (столы) / объект класса содержит информацию о находящемся за ним госте (guest)
class Table:
    def __init__(self, number):
        self.number = number  # номер стола
        self.guest = None


# Класс Guest (гости) / создается поток, при запуске которого происходит задержка от 3 до 10 сек.
class Guest(threading.Thread):

    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name  # имя гостя

    def run(self):
        threading.Thread.run(self)
        time_lag = randint(3, 10)  # Время задержки - случайное число от 3 до 10 сек.
        sleep(time_lag)


# Класс Cafe / В экземпляре класса есть список столов и реализованы два метода:
# прием гостей (guest_arrival) и обслуживание гостей (discuss_guests)
class Cafe:

    def __init__(self, *args):
        self.tables = list(args)  # Список столов
        self.queue = Queue()  # Очередь гостей

    # Прием и рассаживание гостей за столами
    def guest_arrival(self, *args):
        list_tables = self.tables  # Список свободных столов
        quantity_tables = len(self.tables)  # Количество свободных столов
        list_guests = list(args)  # Список гостей
        # Для каждого гостя из списка гостей
        for guest in list_guests:
            # Проверяем, есть ли свободные столы
            if quantity_tables > 0:  # Если имеются свободные столы
                # Для каждого стола из списка столов проверяем
                for table in list_tables:
                    if table.guest is None:  # Если стол свободен
                        table.guest = guest  # Усаживаем гостя за стол
                        guest.start()  # Запускаем поток гостя
                        print(f'{guest.name} сел(-а) за стол номер {table.number}')
                        quantity_tables -= 1  # Уменьшаем количество свободных столов
                        break  # Переходим к следующему гостю
            else:  # Если свободных столов нет
                self.queue.put(guest)  # Ставим (помещаем) гостя в очередь
                print(f'{guest.name} в очереди')
                continue  # Переходим к следующему гостю

    # Обслуживание гостей кафе
    def discuss_guests(self):
        # Выполняем до тех пор, пока очередь не пустая или хотя бы один из столов занят гостем
        while not self.queue.empty() or any(table.guest is not None for table in self.tables):
            for table in self.tables:
                # Если текущий стол занят и поток гостя завершил работу (гость закончил приём пищи)
                if table.guest is not None and not table.guest.is_alive():
                    print(f'{table.guest.name} покушал(-а) и ушёл(ушла)')
                    print(f'Стол номер {table.number} свободен')
                    table.guest = None  # Текущий стол свободен
                    if not self.queue.empty():  # Если очередь не пустая
                        table.guest = self.queue.get()  # Берем гостя из очереди и усаживаем за текущий стол
                        table.guest.start()  # Запускаем поток гостя
                        print(f'{table.guest.name} вышел(-ла) из очереди и сел(-а) за стол номер {table.number}')


# Создание столов
tables = [Table(number) for number in range(1, 6)]
# Имена гостей
guests_names = [
    'Maria', 'Oleg', 'Vakhtang', 'Sergey', 'Darya', 'Arman',
    'Vitoria', 'Nikita', 'Galina', 'Pavel', 'Ilya', 'Alexandra'
]
# Создание гостей
guests = [Guest(name) for name in guests_names]
# Заполнение кафе столами
cafe = Cafe(*tables)
# Приём гостей
cafe.guest_arrival(*guests)
# Обслуживание гостей
cafe.discuss_guests()
