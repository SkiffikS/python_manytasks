""" 
Завдання 1.
Заданий малюнок, що являє собою матрицю, в якій частина клітинок зафарбована білою
фарбою (має знаення ' ' (пробіл)), інша частина зафарбована іорною фарбою (має значення
'Х'). Фігурою на такому малюнку називається сукупність чорних клітин ('X'), для довільної
пари яких центри клітин можнна з'єднати ламаною, що повністю міститься у чорних клітинках
('X'). Різними фінурами називають такі, які неможливосумістити послідовним
застосуванням паралельних переносів, поворотів на 90° і симетрії відносно вертикальної чи
горизонтальної прямої. Визначте кількість усіх фігур на малюнку та кількість різних фігур.
"""

from rich import print

MATRIX = [ # Основна матриця
    ["X", " ", "X", " ", "X", " ", " ", "X"],
    ["X", "X", " ", "X", "X", "X", "X", "X"],
    ["X", "X", "X", " ", " ", "X", " ", " "],
    [" ", " ", "X", " ", "X", " ", "X", " "],
    [" ", "X", "X", "X", " ", "X", "X", "X"],
    ["X", "X", "X", "X", "X", " ", "X", " "],
    [" ", "X", " ", " ", "X", "X", "X", " "],
    [" ", " ", "X", " ", "X", " ", " ", "X"]
]

def isuppertriangular(M): # перевірка чи існує у матриці прямокутний трикутник
    count = 0
    for i in range(1, len(M)):
        for j in range(0, i):
            if(M[i][j] != " "): 
                pass
            else:
                count += 1
    return count

def count_squares(mat): # перевірка на квадрати
    m = len(mat)
    n = len(mat[0])
    count = 0
    for i in range(m-1):
        for j in range(n-1):
            if len(set([mat[i][j],mat[i][j+1],mat[i+1][j],mat[i+1][j+1]])) == 1:
                count += 1
    return count

def simetry_figurs(mat): # перевіка на фігури симетричні по горизонтальній осі
    count = 0
    for i in range(len(mat)):
        for j in range(len(mat[i])):
            try:
                if mat[i][j] == "X":
                    if mat[i + 1][j] == "X" and mat[i + 1][j - 1] == "X" and mat[i + 1][j + 1] == "X":
                        count += 1
            except:
                pass
    return count


def main():

    right_triangles = isuppertriangular(MATRIX)
    square = count_squares(MATRIX)
    simetry_fig = simetry_figurs(MATRIX)
    sum = right_triangles + square + simetry_fig

    print(f"[bold green]На матриці знайдено {sum} фігур, із яких:\n{right_triangles} \
рівнобедрених трикутників\n{square} Квадратів\n{simetry_fig} фігур симетричних \
відносно своєї осі\nусього 3 види різноманітних фігур[bold green]")


if __name__ == "__main__":

    main() 