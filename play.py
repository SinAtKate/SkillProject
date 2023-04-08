# Игра в крестики нолики

def output_table(listL):
    print('   0 | 1 | 2')
    print(f'0| {listL[0][0]} | {listL[0][1]} | {listL[0][2]}')
    print(f'1| {listL[1][0]} | {listL[1][1]} | {listL[1][2]}')
    print(f'2| {listL[2][0]} | {listL[2][1]} | {listL[2][2]}')

def test_Int_In(x, y):
    if 0 <= x <= 2 and 0 <= y <= 2:
        return True
    else:
        print('ОШИБКА!!! Ведите координаты в диапазоне о 0 до 2!')
        return False
def test_empty_position(x, y, listL):
    if listL[x][y] != 'X' and listL[x][y] != 'O':
        return True
    else:
        print('Ошибка!!! Клетка уже занята, выберите другие координаты!')
        return False
def test_victory_move(x, y, listL):
    if listL[0][0] == listL[0][1] == listL[0][2] != '':
        return True
    elif listL[1][0] == listL[1][1] == listL[1][2] != '':
        return True
    elif listL[2][0] == listL[2][1] == listL[2][2] != '':
        return True
    elif listL[0][0] == listL[1][0] == listL[2][0] != '':
        return True
    elif listL[0][1] == listL[1][1] == listL[2][1] != '':
        return True
    elif listL[0][2] == listL[1][2] == listL[2][2] != '':
        return True
    elif listL[0][0] == listL[1][1] == listL[2][2] != '':
        return True
    elif listL[2][0] == listL[1][1] == listL[0][2] != '':
        return True
    else:
        return False

#необходимые переменные, конст-ты и пр.
lib_play = ('Игра в крестики нолики',
            'Правила игры:',
            'Ввод хода производится путем указывания координат разделяемых одним пробелом.',
            'Игра окончена! НИЧЬЯ!',
            'ОШИБКА!!! Введите челые числа!',
            'ОШИБКА ВВОДА!!!')

listL = [['', '', ''], ['', '', ''], ['', '', '']]
counter_move = 0 #счетчик хода
step = 0 # 0 - ход крестика? 1 - нолик

#начало игры
#Вывод поля и заголовка

for iter in range(3):
    print(lib_play[iter])
    print()
output_table(listL)
#цикл хода
while True:
    #проверка количества ходов
    if counter_move == 9:
        print(lib_play[3])
        break
    #условие для вызова проверки победителя
    if counter_move >= 3:
        #проверка на победу
        if test_victory_move(int(x), int(y), listL) == True:
            print(f'УРА!!! Победил {listL[int(x)][int(y)]} -ик, игра окончена!')
            break
    #чей ход
    if step == 0:
        print('Ходит крестик!')
    else:
        print('Ходит нолик!')
    #Исключение на неверный ввод координат
    try:
        x, y = (input('Введите координаты: ')).split()
        #Проверка что ввели числа
        if x.isdigit() and y.isdigit():
            #попадают ли они в диапазон координат
            if test_Int_In(int(x), int(y)) == False:
                continue
            #проверка на пустую клетку со второго хода
            if (counter_move != 0) and (test_empty_position(int(x), int(y), listL) == False):
                continue
        else:
            print(lib_play[4])
            continue
        #фиксация хода X
        if step == 0:
            step = 1
            listL[int(x)][int(y)] = 'X'
            output_table(listL)
            counter_move += 1
            continue
        # фиксация хода O
        else:
            step = 0
            listL[int(x)][int(y)] = 'O'
            output_table(listL)
            counter_move += 1
            continue
    #отработка исключения
    except ValueError:
        print(lib_play[5])
        continue




