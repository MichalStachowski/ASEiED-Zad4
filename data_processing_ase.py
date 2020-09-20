# Natalia Brochocka, 171659
# Stanisław Ebertowski, 171919
# Michał Stachowski, 171570

import matplotlib.pyplot as plt
import codecs
import numpy as np
import os
import pandas as pd
from tabulate import tabulate


def sort_by_date(arr):
    return arr[0]


def get_data(path):
    _input = []
    file_list = os.listdir(path)
    for file in file_list:
        current_file = os.path.join(path, file)
        with codecs.open(current_file, "r", encoding='utf-8') as f:
            data = f.readlines()
        for line in data:
            words = line.split(',')
            words[-1] = int(words[-1].replace('\n', ''))
            _input.append(words)

    return _input


def find_category(keywords):
    metakeywords = ' '.join(keywords)
    metakeywords = metakeywords.lower()

    for word in edukacja:
        if metakeywords.find(word) != -1:
            return 'edukacja'

    for word in zdrowie:
        if metakeywords.find(word) != -1:
            return 'zdrowie'

    for word in polityka:
        if metakeywords.find(word) != -1:
            return 'polityka'

    for word in technologia:
        if metakeywords.find(word) != -1:
            return 'technologia'

    for word in rozrywka:
        if metakeywords.find(word) != -1:
            return 'rozrywka'

    return 'pozostałe'


def sort_by_keywords():
    _word_cat2019 = [
        ['edukacja', 0, 0, 0, 0],
        ['zdrowie', 0, 0, 0, 0],
        ['polityka', 0, 0, 0, 0],
        ['technologia', 0, 0, 0, 0],
        ['rozrywka', 0, 0, 0, 0],
        ['pozostałe', 0, 0, 0, 0],
    ]

    _word_cat2020 = [
        ['edukacja', 0, 0, 0, 0],
        ['zdrowie', 0, 0, 0, 0],
        ['polityka', 0, 0, 0, 0],
        ['technologia', 0, 0, 0, 0],
        ['rozrywka', 0, 0, 0, 0],
        ['pozostałe', 0, 0, 0, 0],
    ]

    for d19 in data_2019:
        keywords = d19[1:-2]
        category = find_category(keywords)

        for item in _word_cat2019:
            if item[0] == category:
                if d19[-2] == 'pandemia':
                    item[1] += d19[-1]
                elif d19[-2] == 'wirus':
                    item[2] += d19[-1]
                elif d19[-2] == 'covid':
                    item[3] += d19[-1]
                elif d19[-2] == 'covid19':
                    item[4] += d19[-1]

    for d20 in data_2020:
        keywords = d20[1:-2]
        category = find_category(keywords)

        for item in _word_cat2020:
            if item[0] == category:
                if d20[-2] == 'pandemia':
                    item[1] += d20[-1]
                elif d20[-2] == 'wirus':
                    item[2] += d20[-1]
                elif d20[-2] == 'covid':
                    item[3] += d20[-1]
                elif d20[-2] == 'covid19':
                    item[4] += d20[-1]

    return _word_cat2019, _word_cat2020


def autolabel(ax, rects):
    for rect in rects:
        height = rect.get_height()
        ax.annotate('{}'.format(int(height)),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha='center', va='bottom')


def plot_word_by_date(word):
    days = []
    for d19 in data_2019:
        if d19[-2] == word:
            data = d19[0].replace('2019-', '')
            try:
                days.index(data)
            except:
                days.append(data)

    for d20 in data_2020:
        if d20[-2] == word:
            data = d20[0].replace('2020-', '')
            try:
                days.index(data)
            except:
                days.append(data)

    days = sorted(days)
    count_19 = np.zeros(len(days))
    count_20 = np.zeros(len(days))

    for d19 in data_2019:
        if d19[-2] == word:
            data = d19[0].replace('2019-', '')
            index = days.index(data)
            count_19[index] += d19[-1]

    for d20 in data_2020:
        if d20[-2] == word:
            data = d20[0].replace('2020-', '')
            index = days.index(data)
            count_20[index] += d20[-1]

    fig, ax = plt.subplots()
    x = np.arange(len(days))
    width = 0.2
    rects1 = ax.bar(x - width / 2, count_19, width, label=word + ' 2019')
    rects2 = ax.bar(x + width / 2, count_20, width, label=word + ' 2020')
    ax.set_ylabel('ilość wystąpień')
    ax.set_xlabel('dzień')
    ax.set_title('Ilość wystąpień słowa ' + word + ' w poszególne dni w roku 2019 i 2020')
    ax.set_xticks(x)
    ax.set_xticklabels(days)
    ax.legend()
    autolabel(ax, rects1)
    autolabel(ax, rects2)
    fig.tight_layout()
    plt.xticks(fontsize=7, rotation=90)
    plt.show()


def print_table(words_2019, words_2020):
    data = []
    words_general = list(zip(words_2019, words_2020))
    for word in words_general:
        word[0].insert(1, '2019')
        word[1].insert(1, '2020')
        data.append(word[0])
        data.append(word[1])
        if word[0][0] != "pozostałe":
            data.append(["-----------", "-----", "-----------", "--------", "-------", "---------"])
    df = pd.DataFrame(data, columns=['Kategoria', 'Rok', 'Pandemia', 'Wirus', 'Covid', "Covid19"])
    print(tabulate(df, headers='keys', tablefmt='psql', showindex=False))


data_2019 = get_data("./2019")
data_2020 = get_data("./2020")

plot_word_by_date('wirus')
plot_word_by_date('pandemia')
plot_word_by_date('covid')
plot_word_by_date('covid19')

edukacja = ['kurs', 'lekcje', 'nauka', 'how to', "poradnik", 'liceum', 'biblioteka', 'edukacja', 'nauka', 'matematyka',
            'astronomia', 'geologia']
zdrowie = ['ks.', 'medytacja', 'adhd', 'epidemia', 'infekcja', 'szczepienia', 'usuwanie kurzajek', 'szpital',
           'sylwetki', 'dietetyka', 'medycyna', 'HIV', 'Airds', 'smartphone', 'netbook', 'choroby', 'cytomegalia',
           'WHO', 'lekarstwa', 'farmacja', 'rezonans', 'diagnostyka', 'minister', 'koronawirus', 'zdrowie', 'medycyna',
           "lekarz", "zdrowia", "pacjent", "kręgosłup", "bólu", "reumoatyczne", "reumatyzm", "rwa kulszowa", "gabinet",
           'zdrowotne', 'lifestyle', 'opryszczka', 'leczenie', 'lekarstwa', 'serce', 'profilaktyka', 'kardiologia',
           'dieta', 'szczepienia', 'grypa', 'grypy', 'HIV', "AIDS", "chirurg", "badania", "choroba"]
religia = ['katolicki', "szatan", "ksiądz", 'religia', 'Jan Paweł II', 'papież', 'chrześcijaństwo', 'zakonnik',
           'kościół']
technologia = ['tojan', 'windows', 'nvidia', 'huawei', 'intel', 'serwery', 'internet', 'antywirus', 'komputer',
               'skrypt', 'forum', 'ddos', 'dysk', 'ssd', 'festiwal', 'teatr', 'książka', 'Tokarczuk', 'sztuka',
               'samsung', 'nokia', 'apple', "virus", "wirus", "telefon", "antywirus", "whatsapp", "trojan", "webmaster",
               "freeware", "wtyczki", "windows", 'satelita', 'technologia', 'gnu', 'linux', 'system', "internet"]
rozrywka = ['wykop', 'muzyka', 'książk', 'czytanie', 'teatr', 'przedstawienia', 'koncert', 'czasopisa', 'autor',
            'thriller', 'fotografia', 'photo', 'foto', 'gry', 'hobby', 'film', 'gracz', 'gaming', 'gry', 'gier',
            'zombie', 'birthaday', 'party', 'urodziny', 'impreza', 'zabawki', 'bieszczady', 'turystyka', 'rekreacja',
            'marsz', 'kulturystyka', 'trening', 'sport', 'piłka', 'nożna', 'messi', 'ronaldo', 'neymar', 'wisła kraków',
            'cracovia', 'borussia', 'mistrzostwa', "facebook", "filmiki", "demotywatory", "humor", "zdjęcia",
            "rozrywka", "taniec", 'gra', 'gry', 'karty', 'plansza', 'przygoda', 'książki', "czytanie", "thriller",
            "książki", "podróże", "niusy", "newsy", "new", "komiks"]
zwierzeta = ['zwirzęta', 'owady', 'wścieklizna', 'weterynarz', "hodowla", "weterynaria", "psy", "koty", "terrier",
             "puppies"]
rodzina = ["dom", "rodzina", "kobiety", "mężczyźni", "ludzie", 'birthday', 'urodziny', 'dzieci']
finanse = ["biznes", "giełda", "giełdowe", "inwestycje", "akcje", "firma", "firmy", "biuro", 'dług', 'firma', 'bieda',
           'gospodarka', 'łapówki', 'finanse', 'fundusz', 'inwestycje']
zywienie = ['Kuchnia', 'delikatesy', "kulinaria", "potrawy", "eSpring", 'kebab', 'wegetarianizm', 'weganizm']
informacje = ['dziennikarstwo', 'reklama', 'wypadek', 'wiadomości', 'gazetacodzienna.pl', "radio", "reklama", "spoty",
              "aktualności", "informacje", "prognoza", "pogoda", "gazeta", 'feminizm', 'dorzeczy', 'wyborcza',
              'dziennik', 'news']
polityka = ["polityka", "Duda", 'Andzej Duda', 'Platforma Obywatelska', 'parlament', 'PiS', 'UE', 'konfederacja',
            'wybory', 'Krym',
            'Morawiecki', 'Schetyna', 'Ziemkiewicz', 'opozycja', 'PSL', 'Putin', 'burmistrz', 'prezydent',
            'Merkel', 'unia', 'hołownia', 'lewica', 'aborcja', 'komuniści', 'Sejm', 'ustawa', 'głosowanie',
            'Wałęsa', 'Korwin', 'Ziobro', 'Ministerstwo', 'protest', 'solidarność', 'MSZ', 'gmina', 'Obama',
            'Bosak']
motoryzacja = ["auto", "motoryzacja", 'transport', 'ferrari', 'lamborghini']
historia = ['kraj', 'historia', 'wojna', 'holokaust', 'Wołyń']

word_cat2019, word_cat2020 = sort_by_keywords()
print_table(word_cat2019, word_cat2020)

# print(word_cat2020)
# print(word_cat2019)
