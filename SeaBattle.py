import random
import time

class Error(Exception):
    pass
class SeaBattleError(Error):
    '''Исключение пустого ввода'''
    #expression - выражение где произошла ошибка
    #message - объяснение ошибки
    def __init__(self, expression, message):
        self.expression = expression
        self.message = message

    
class Dot:                              #Класс Точка
    def __init__(self):
        self.x = 0
        self.y = 0
    def set_x(self, x):                 #присваивание значения для x
        self.x = x
    def set_y(self, y):                 #присваивание значения для y
        self.y = y
    @property
    def get_x(self):                    #получение значения для x
        return self.x
    @property
    def get_y(self):                    #получение значения для y
        return self.y
    def input_xy(self):                 #проверка ввода координат
        try:
            x = int(input('Введите координату x: ', ))
            y = int(input('Введите координату y: ', ))
            if 0 > x > 5 or 0 > y > 5:  #условия диапазона поля
                raise SeaBattleError(f'!!! x = {x}, y = {y}', '-> Точка за границами поля.')
        except SeaBattleError as e:
            print(e.args[0])
            print(e.args[1])
            self.input_xy()             #цикличный вызов функции, пока не получим верные координаты
        except (TypeError, ValueError):
            print(f'Введите целые числа от 0 - 5!')
            self.input_xy()             #цикличный вызов функции, пока не получим верные координаты
        else:
            self.set_x(x)               #сохраняем верные координаты
            self.set_y(y)
            return True
               
class Ship:                                                 #Класс Корабль                                                               
    def __init__(self, lenght):
        self.lenght = lenght                                #Длина корабля                       
        self.dotStart = Dot()                               #Точка начала корабля
        self.direction = 0                                  #направление: 0 - горизонтальное, 1 - вертикальное
        self.count_life = lenght                            #количество жизней, изначально равно lenght
        self.listShip = []                                  #список координат корабля  
    
    def set_listShip(self, dot):                            #сохранение списков координат корабля в список
        self.listShip.append([dot.get_x, dot.get_y])
    @property
    def get_listShip(self):                                 #получение списка координат корабля 
        return self.listShip
    def set_direction(self, direction):                     #сохранение направления корабля
        self.direction = direction
    @property
    def get_direction(self):                                #получение направления корабля
        return self.direction
    
class Board:                                                #Класс Игровое поле 
    def __init__(self):
        self.listBoard = [[' '] * 6 for i in range(6)]      #доска с кораблями
        self.boardShots = [[' '] * 6 for i in range(6)]     #доска с выстрелами по противнику   
        self.liststop = []                                  #список координат контура кораблей
        self.hid = True                                     #скрывать корабли или нет
        self.Ship3 = Ship(3)                                #объект корябля на 3 клетки
        self.Ship2_1 = Ship(2)                              #объект корябля на 2 клетки
        self.Ship2_2 = Ship(2)                              #объект корябля на 2 клетки, второй
        self.Ship1_1 = Ship(1)                              #объект корябля на 1 клетку
        self.Ship1_2 = Ship(1)                              #объект корябля на 1 клетку, второй
        self.Ship1_3 = Ship(1)                              #объект корябля на 1 клетку, третий
        self.Ship1_4 = Ship(1)                              #объект корябля на 1 клетку, четвертый
        self.listShips = [self.Ship3, self.Ship2_1,         #список всех кораблей доски
                     self.Ship2_2, self.Ship1_1,
                     self.Ship1_2, self.Ship1_3,
                     self.Ship1_4]                      
        self.liveShip = 7                                   #количество живых кораблей, изначально 7 штук

    def double_shot(self, dot):                             #проверка повторного выстрела
        if self.boardShots[dot.get_x][dot.get_y] == '*' or self.boardShots[dot.get_x][dot.get_y] == 'X':
            return True
        else:
            return False
    def not_countout_board(self, d):                        #проверка на пересечение с контуром или кораблем
        try:
            if [d.get_x, d.get_y] in self.liststop:         #если есть в списке координат контура
                raise SeaBattleError('', '')
            elif self.listBoard[d.get_x][d.get_y] == 'O':   #если координата занята кораблем
                raise SeaBattleError('', '')    
        except SeaBattleError:
            return False
        else:
            return True
        
    def add_list(self, d_list):                             #добавление координат в список координат контура
        if d_list not in self.liststop:
            self.liststop.append(d_list)
       
    def shot(self, dot):                                    #выстрел                     
        for ship in self.listShips:                         #проверка по координатам коралей
            if [dot.get_x, dot.get_y] in ship.get_listShip:
                print('УРАА!!! Точно в цель! Хорошо идем!')
                ship.count_life -=1
                time.sleep(4)
                if ship.count_life == 0:                    #проверка на убитый корабль
                    print('УРА!!! Убит!!!')
                    self.liveShip -=1
                    time.sleep(4)
                return True
        print('Промах, повезет в следующий раз!')
        time.sleep(4)
        return False
         
    def get_board(self, board):                             #вывод полей на экран
        def sample_for(ii, brd):                            #шаблон построчного вывода
            strT = '| '
            for i in brd[ii]:
                strT += i + ' | '
            return strT
        def sample_hid(userboard, aiboard):                 #шаблон вывода полей с учетом Hid
            strNP = '-'
            c = ' '
            print()
            print(f'{c*3}Поле Игрока:{c*26}Поле AI:')
            print()
            print(f'{c*5}0{c*3}1{c*3}2{c*3}3{c*3}4{c*3}5{c*17}0{c*3}1{c*3}2{c*3}3{c*3}4{c*3}5')
            print(f'{c*3}{strNP*25}{c*13}{strNP*25}')
            for i in range(6):
                print(f'{c}{i}{c}{sample_for(i, userboard)}{c*10}{i}{c}{sample_for(i, aiboard)}')
                print(f'{c*3}{strNP*25}{c*13}{strNP*25}')    
            print()
        
        if self.hid == True and board.hid == True:          #условия вызова шаблона вывода
            sample_hid(self.listBoard, board.listBoard)
        elif self.hid == False and board.hid == True:
            sample_hid(board.boardShots, board.listBoard)
        elif self.hid == True and board.hid == False:
            sample_hid(self.listBoard, self.boardShots)
        elif self.hid == False and board.hid == False:
            sample_hid(self.boardShots, self.boardShots)   
                       
    def add_ship(self, i):                                  #сохранение корабля на поле
        for dot in self.listShips[i].get_listShip:
            self.listBoard[dot[0]][dot[1]] = 'O'
        self.countour(self.listShips[i].get_listShip)       #вызов создания контура корабля
        
    def countour(self, ls):                                 #создание контура корабля
        def semple_add_listStop(listXY, spisok):            #шаблон проверки координаты на допустимость сохранения в контур
            if 0 > listXY[0] or  listXY[0] > 5:
                return False
            if 0 > listXY[1] or  listXY[1] > 5:
                return False
            elif [listXY[0], listXY[1]] in spisok:
                return False
            elif [listXY[0], listXY[1]] in self.liststop:
                return False
            else:
                return True
            
        for s in ls:                                        #перебор каждой координаты корабля
            if semple_add_listStop([s[0], s[1]-1], ls):     #координата левее
                self.liststop.append([s[0], s[1]-1])
            if semple_add_listStop([s[0]-1, s[1]], ls):     #координата выше
                self.liststop.append([s[0]-1, s[1]])
            if semple_add_listStop([s[0], s[1]+1], ls):     #координата правее
                self.liststop.append([s[0], s[1]+1])
            if semple_add_listStop([s[0]+1, s[1]], ls):     #координата ниже
                self.liststop.append([s[0]+1, s[1]])
                    
class Player:                                               #Класс Игра
    def __init__(self):
        self.boardUser = Board()                            #объект доска игрока
        self.boardAI = Board()                              #объект доска AI
        self.dot = Dot()                                    #объект точка
    
    def ask(self, user):                                    #запрос координат для выстрела
        if user == 'user':
            self.dot.input_xy()
        else:
            self.dot.set_x(random.randrange(0, 6))          #генерация координат для AI
            self.dot.set_y(random.randrange(0, 6))
        return self.dot
    
    def move(self, user, play):                             #вызов выстрела с проверкой
        self.dot = self.ask(user)                           #запрос координат
        if user == 'user':                                  #если стреляет игрок
            if self.boardUser.double_shot(self.dot):        #вызов проверки на повторный выстрел
                print('Произошел порвторный выстрел в одну цель!!! Повторите попытку')
                time.sleep(4)
                return True
            elif play.boardAI.shot(self.dot):               #вызов выстрела
                self.boardUser.boardShots[self.dot.get_x][self.dot.get_y] = 'X'
                play.boardAI.listBoard[self.dot.get_x][self.dot.get_y] = 'X'
                return True
            else:                                           #промах
                self.boardUser.boardShots[self.dot.get_x][self.dot.get_y] = '*'
                play.boardAI.listBoard[self.dot.get_x][self.dot.get_y] = '*'
                return False
        else:                                               #если стреляет AI
            if self.boardAI.double_shot(self.dot):          #вызов проверки на повторный выстрел
                print('Произошел порвторный выстрел в одну цель!!! Повторите попытку')
                time.sleep(4)
                return True
            elif play.boardUser.shot(self.dot):             #вызов выстрела
                self.boardAI.boardShots[self.dot.get_x][self.dot.get_y] = 'X'
                play.boardUser.listBoard[self.dot.get_x][self.dot.get_y] = 'X'
                return True
            else:                                           #промах
                self.boardAI.boardShots[self.dot.get_x][self.dot.get_y] = '*'
                play.boardUser.listBoard[self.dot.get_x][self.dot.get_y] = '*'
                return False
            
class AI(Player):                                           #Класс AI
    def __init__(self):
        self.play = Player()                                #объект наследования класса Игра
        self.dot = Dot()                                    #объект точка
    
    def rand_ship(self, i):                                 #генерация кораблей
        try:
            self.play.boardAI.listShips[i].set_direction(random.randrange(0, 2))                    #рандомное направление
            if self.play.boardAI.listShips[i].get_direction == 0:                                   #направление горизонтальное, тогда
                self.play.boardAI.listShips[i].dotStart.set_x(random.randrange(0, 6))                                           #рандомная точка начала корабля с условием:                                                                                     
                self.play.boardAI.listShips[i].dotStart.set_y(random.randrange(0, (7-self.play.boardAI.listShips[i].lenght)))   #длина корабля должна поместиться по направлению
                if self.play.boardAI.not_countout_board(self.play.boardAI.listShips[i].dotStart) == False:      #вызов проверки на пересечение кораблей
                    raise SeaBattleError('', '')
                self.play.boardAI.listShips[i].set_listShip(self.play.boardAI.listShips[i].dotStart)            #сохранение координаты прошедшей все условия
                                                                                                                #в список координат корабля
                for n in range(self.play.boardAI.listShips[i].lenght-1):                                        #создание последующих точек корабля в зависимости от длины
                    self.dot.set_x(self.play.boardAI.listShips[i].dotStart.get_x)
                    self.dot.set_y(self.play.boardAI.listShips[i].dotStart.get_y+(n+1))
                    self.play.boardAI.listShips[i].set_listShip(self.dot)                                       #сохранение точки в список
                    if self.play.boardAI.not_countout_board(self.dot) == False:                                 #вызов проверки на пересечение для каждой точки
                        raise SeaBattleError('', '')
            else:                                                                                               #направление вертикальное, тогда
                self.play.boardAI.listShips[i].dotStart.set_x(random.randrange(0, (7-self.play.boardAI.listShips[i].lenght)))   #рандомная точка начала корабля с условием:                                                                                                                
                self.play.boardAI.listShips[i].dotStart.set_y(random.randrange(0, 6))                                           #длина корабля должна поместиться по направлению
                if self.play.boardAI.not_countout_board(self.play.boardAI.listShips[i].dotStart) == False:      #вызов проверки на пересечение кораблей
                    raise SeaBattleError('', '')
                self.play.boardAI.listShips[i].set_listShip(self.play.boardAI.listShips[i].dotStart)            #сохранение координаты прошедшей все условия
                                                                                                                #в список координат корабля
                for n in range(self.play.boardAI.listShips[i].lenght-1):                                        #создание последующих точек корабля в зависимости от длины
                    self.dot.set_x(self.play.boardAI.listShips[i].dotStart.get_x+(n+1))
                    self.dot.set_y(self.play.boardAI.listShips[i].dotStart.get_y)
                    self.play.boardAI.listShips[i].set_listShip(self.dot)                                       #сохранение точки в список
                    if self.play.boardAI.not_countout_board(self.dot) == False:                                 #вызов проверки на пересечение для каждой точки
                        raise SeaBattleError('', '')
        except SeaBattleError as e:
            self.play.boardAI.listShips[i].get_listShip.clear()                                     #чистить список, если координата не подходит
            self.rand_ship(i)                                                                       #цикличный вызов при неудачном создании корабля
        else:
            return self.play.boardAI.listShips[i].get_listShip                                      #вернет список точек удачного корабля
                      
class User(Player):                                             #Класс Игрок
    def __init__(self):
        self.play = Player()                                    #объект наследования класса Игра
        self.dot = Dot()                                        #объект точка
        self.play.boardUser.hid = True                          #Индикатор вывода полей
    
    def add_ships(self, i):                                     #создание кораблей для игрока
        print()
        print(f'Создание корабля на {self.play.boardUser.listShips[i].lenght} клетку(и)')
        print()
        print('Укажите направление корабля:')
        print('0 - горизонтальное')
        print('1 - вертикальное')
        print()
        try:
            direction = int(input('Введите направление: '))
            if direction < 0 or direction > 1:
                raise SeaBattleError(f'!!! диапазон = {direction}', '-> Введите числа в указанном диапазоне.')
            
            self.play.boardUser.listShips[i].set_direction(int(direction))                          #сохранение направление корабля
            self.play.boardUser.listShips[i].dotStart.input_xy()                                    #вызов ввода координат точки начала корабля
            if self.play.boardUser.not_countout_board(self.play.boardUser.listShips[i].dotStart)==False:            #вызов проверки на пересечение
                    raise SeaBattleError(f'!!!Ошибка ', '-> С учетом начальной координаты корабля, он пересекается с другими кораблями!!!')
            if int(direction) == 0:                                                                 #горизонтальное направление
                if self.play.boardUser.listShips[i].dotStart.get_y <= (6 - self.play.boardUser.listShips[i].lenght):    #проверка на возможность размещения корабля с учетом: 
                                                                                                                        #точки начала и направления
                    self.play.boardUser.listShips[i].set_listShip(self.play.boardUser.listShips[i].dotStart)            #сохранение точки в список
                    for n in range(self.play.boardUser.listShips[i].lenght-1):                                          #создание последующих точек корабля в зависимости от длины
                        self.dot.set_x(self.play.boardUser.listShips[i].dotStart.get_x)
                        self.dot.set_y(self.play.boardUser.listShips[i].dotStart.get_y+(n+1))
                        self.play.boardUser.listShips[i].set_listShip(self.dot)                                         #сохранение точки в список
                        if self.play.boardUser.not_countout_board(self.dot) == False:                                   #вызов проверки на пересечение для каждой точки
                            raise SeaBattleError(f'!!!Ошибка ', '-> С учетом начальной координаты корабля, он пересекается с другими кораблями!!!')
                else:
                    raise SeaBattleError('!!!Ошибка ', '-> С учетом начальной координаты корабля, он не поместился на поле!!!')
            if int(direction) == 1:                                                                                     #вертикальное направление                           
                if self.play.boardUser.listShips[i].dotStart.get_x <= (6 - self.play.boardUser.listShips[i].lenght):    #проверка на возможность размещения корабля с учетом:
                                                                                                                        #точки начала и направления
                    self.play.boardUser.listShips[i].set_listShip(self.play.boardUser.listShips[i].dotStart)            #сохранение точки в список
                    for n in range(self.play.boardUser.listShips[i].lenght-1):                                          #создание последующих точек корабля в зависимости от длины
                        self.dot.set_x(self.play.boardUser.listShips[i].dotStart.get_x+(n+1))
                        self.dot.set_y(self.play.boardUser.listShips[i].dotStart.get_y)
                        self.play.boardUser.listShips[i].set_listShip(self.dot)                                         #сохранение точки в список
                        if self.play.boardUser.not_countout_board(self.dot) == False:                                   #вызов проверки на пересечение для каждой точки
                            raise SeaBattleError(f'!!!Ошибка ', '-> С учетом начальной координаты корабля, он пересекается с другими кораблями!!!')
                else:
                    raise SeaBattleError('!!!Ошибка ', '-> С учетом начальной координаты корабля, он не поместился на поле!!!')
        except SeaBattleError as e:
            print(e.args[0])
            print(e.args[1])
            print()
            time.sleep(4)
            self.play.boardUser.listShips[i].get_listShip.clear()                                   #чистить список, если координата не подходит
            self.add_ships(i)                                                                       #цикличный вызов при неудачном создании корабля
        except ValueError:
             print('Введите числа в указанном диапазоне.')
             time.sleep(4)
             self.play.boardUser.listShips[i].get_listShip.clear()                                  #чистить список, если координата не подходит
             self.add_ships(i)                                                                      #цикличный вызов при неудачном создании корабля
        else:    
            print('Корабль создан!')
            print()
            time.sleep(2)
            return self.play.boardUser.listShips[i].get_listShip                                    #вернет список точек удачного корабля
   
class Game:                                                         #Класс Вызова игры
    def __init__(self):
        self.user = User()                                          #объект класса Игрок
        self.ai = AI()                                              #объект класса AI
        
    def random_board(self):                                         #генерация рандомного поля AI
        i = 0
        while i < 7:                                                #пока не создадим 7 кораблей
            self.ai.rand_ship(i)                                    #вызов создания рандомного корабля
            self.ai.play.boardAI.add_ship(i)                        #сохранение созданного корабля на поле
            i+=1
        time.sleep(10)
        
    def user_board(self):                                           #создание поля для игрока
        print('Создание боевого поля Игрока:')
        print()
        i = 0
        while i < 7:                                                        #пока не создадим 7 кораблей
            self.user.play.boardUser.get_board(self.ai.play.boardAI)        #вывод полей
            self.user.add_ships(i)                                          #вызов создания корабля
            self.user.play.boardUser.add_ship(i)                            #сохранение корабля на поле
            i+=1
            if i !=7:                                                       #выводить предупреждение пока не создали последний корабль
                print()
                print('!!!Предупреждение: Последующие корабли должны располагаться,')
                print('не менее чем на 1 клетку, дальше от созданных!')
                print()
            time.sleep(2)
        
    def greet(self):                                                        #описание игры
        print('Игра: МОРСКОЙ БОЙ')
        print()
        print('правила игры:')
        print('1. соперник - AI')
        print('2. ввод координат выстрела в диапазоне матрицы 6*6')
        print('3. следуйте подсказкам на экране')
        print()
        print('На экране отображаются 2 игровых поля')
        print('слева - Поле игрока, где:')
        print('в зависимости от выбора отображения, будут располагаться корабли')
        print('1 - корабли видны, 2 - корабли не видны')
        print('также на поле игрока будут фиксироваться выстрелы AI')
        print()
        print('справа - Поле AI, где:')
        print('в зависимости от выбора отображения, будут располагаться корабли')
        print('1 - корабли видны, 2 - корабли не видны')
        print('также на поле AI будут фиксироваться выстрелы игрока')
        print()
        print('УДАЧИ!')
        print()
        print('нажмите enter для начала игры...')
        input()
        
    def loop(self, count):                                                  #ходы игроков с учетом count - чей ход
        match count:
            case 1:                                                         #ход игрока
                print()
                self.user.play.boardUser.get_board(self.ai.play.boardAI)    #вывод полей
                print()
                print('Ваш ход: ')
                print()
                if self.user.play.move('user', self.ai.play):               #вызов выстрела
                    count = 1                                               #сохраняем индикатор если попали
                    if self.ai.play.boardAI.liveShip == 0:                  #проверяем возможную победу
                        print('УРА!!! Вы Выйграли!!!')                      #момент завершения игры
                    else:
                        self.loop(count)                                    #циклично вызываем повторный ход
                else:
                    count = 2                                               #иначе передаем ход сопернику
                    self.loop(count)                                        #циклично вызываем ход
                
            case 2:                                                         #ход AI
                print()
                self.user.play.boardUser.get_board(self.ai.play.boardAI)    #вывод полей
                print()
                print('Ходит AI: ')
                print()
                if self.ai.play.move('ai', self.user.play):                 #вызов выстрела
                    count = 2                                               #сохраняем индикатор если попали
                    if self.user.play.boardUser.liveShip == 0:              #проверяем возможную победу
                        print('УПС!!! Победил AI!!!')                       #момент завершения игры
                    else:
                        self.loop(count)                                    #циклично вызываем повторный ход
                else:
                    count = 1                                               #иначе передаем ход сопернику
                    self.loop(count)                                        #циклично вызываем ход
                    
    def start(self):                                    #старт игры
        us = 1                                          #индикатор вывода поля игрока
        ai = 1                                          #индикатор вывода поля AI
        self.greet()                                    #вызов описания
        self.user_board()                               #вызов создания поля для игрока
        print()
        print('Генерируем игровое поле AI')
        print()
        self.random_board()                             #вызов генерации поля AI
        for i in range(100):                            #отступ вместо чистки консоли
            print()
        print('Мы готовы начать игру!')
        print()
        while True:                                     #запрос на скрытие кораблей игрока и AI
            print('Скрыть ваши корабли на поле?')
            print('1 - Да')
            print('2 - Нет')
            try:
                us = int(input('Введите ответ: '))
                if us < 1 and us > 2:
                    raise SeaBattleError('!!!Ошибка ', '-> Введите числа: 1 или 2')
                print('Скрыть корабли AI на поле?')
                print('1 - Да')
                print('2 - Нет')
                ai = int(input('Введите ответ: '))
                if ai < 1 and ai > 2:
                    raise SeaBattleError('!!!Ошибка ', '-> Введите числа: 1 или 2')
            except SeaBattleError as e:
                print(e.args[0])
                print(e.args[1])
                print()
                time.sleep(4)
                continue
            except ValueError:
                print('!!!Ошибка ', '-> Введите целые числа: 1 или 2')
                time.sleep(4)
                continue
            else:
                break                                   #завершаем цикл при получении корректных данных

        if us == 1:                                     #установка индикатора hid для вывода полей на протяжении всей игры
            self.user.play.boardUser.hid = False        #True - отображать корабли, False - скрыть
        if ai == 2:
            self.ai.play.boardAI.hid = True
        else:
            self.ai.play.boardAI.hid = False
        self.loop(1)                                    #вызов ходов
        print()
        print('КОНЕЦ ИГРЫ!')
        
game = Game()                                           #объект класса вызова игры
game.start()                                            #запуск игры


