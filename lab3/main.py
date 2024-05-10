import random

from faker import Faker
from faker.providers.lorem.ru_RU import Provider

fake = Faker()
fake.add_provider(Provider)

LETTERS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"


def gen_random_words(char_number):
    return fake.text(max_nb_chars=char_number + 0.1 * char_number)[:char_number]


def gen_random_letters(char_number):
    return "".join([random.choice(LETTERS) for _ in range(char_number)])


def compare(text1, text2):
    c = 0
    for i in range(len(text1)):
        if text1[i] == text2[i]:
            c += 1
    return c / len(text1)


def main():
    char_numbers = [1000, 5000, 10000, 15000, 20000]
    with open("foundation.txt") as f:
        text1 = f.read()
    with open("glavred_news.txt") as f:
        text2 = f.read()
    random_words = gen_random_words(char_numbers[-1])
    random_words2 = gen_random_words(char_numbers[-1])
    random_letters = gen_random_letters(char_numbers[-1])
    random_letters2 = gen_random_letters(char_numbers[-1])
    answers = []

    for n in char_numbers:
        answers.append(compare(text1[:n], text2[:n]))

    for n in char_numbers:
        answers.append(compare(text1[:n], random_letters[:n]))

    for n in char_numbers:
        answers.append(compare(text1[:n], random_words[:n]))

    for n in char_numbers:
        answers.append(compare(random_letters[:n], random_letters2[:n]))

    for n in char_numbers:
        answers.append(compare(random_words[:n], random_words2[:n]))

    print(text1[:1000])
    print()
    print(text2[:1000])
    print()
    print(random_words[:1000])
    print()
    print(random_words2[:1000])
    print()
    print(random_letters[:1000])
    print()
    print(random_letters2[:1000])

    print("""
|--------------------------------------------------------------------------------------------
|                                              |  1000  |  5000  | 10000  | 15000  | 20000  |
|----------------------------------------------|--------|--------|--------|--------|--------|
| Два осмысленных текста на естественном языке | {:.4f} | {:.4f} | {:.4f} | {:.4f} | {:.4f} |
| Осмысленный текст и текст из случайных букв  | {:.4f} | {:.4f} | {:.4f} | {:.4f} | {:.4f} |
| Осмысленный текст и текст из случайных слов  | {:.4f} | {:.4f} | {:.4f} | {:.4f} | {:.4f} |
| Два текста из случайных букв                 | {:.4f} | {:.4f} | {:.4f} | {:.4f} | {:.4f} |
| Два текста из случайных слов                 | {:.4f} | {:.4f} | {:.4f} | {:.4f} | {:.4f} |
|--------------------------------------------------------------------------------------------
""".format(*answers))


main()
