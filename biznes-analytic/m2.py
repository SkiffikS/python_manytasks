"""
Завдання 2.
За допомогою генератора псевдрвипадкових чисел згенерувати реченння. Слова
вибираються із масивів артиклів, іменників, дієслів, прийменників у такому порядку: артикль,
іменник, дієслово, прийменник, артикль, іменник. Перше слово речення має починатися з
великої літери.
"""

from random import randint
from rich import print

articles = ["a", "oдин", "деякий", "кілька", "що", "ще", "той", "та", "чо", "цей"]
nouns = ["хлопчина", "чоловік", "Влад", "мужчика", "Андрій", "Олег"]
verbs = ["взяв", "зробив", "вийшов", "знайшов", "вкрав", "пожартував"]
prepositions = ["в", "у", "з", "на", "до", "від", "під", "над", "за", "крізь", "через", "при", "перед", "поза", "з-за", "біля", "обабіч", "коло", "по"]

art1 = articles[randint(0, len(articles) - 1)].title()
im1 = nouns[randint(0, len(nouns) - 1)]
ds = verbs[randint(0, len(verbs) - 1)]
pr = prepositions[randint(0, len(prepositions) - 1)]
art2 = articles[randint(0, len(articles)- 1)]
im2 = nouns[randint(0, len(nouns) - 1)]

sentence = art1 + " " + im1 + " " + ds + " " + pr + " " + art2 + " " + im2

print(f"[bold blue]{sentence}[/bold blue]")
