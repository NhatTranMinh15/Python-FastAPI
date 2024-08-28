from random import random, randrange

from services.name_generator.name import (
    word,
    female,
    female_length,
    last_name,
    last_name_length,
    male,
    male_length,
    word_length,
)


def get_first_name(gender: str = None):
    if not gender:
        gender = "male"
        if random() > 0.5:
            gender = "female"
    if gender.lower() == "male":
        return male[randrange(male_length)]
    if gender.lower() == "female":
        return female[randrange(female_length)]


def get_last_name():
    return last_name[randrange(last_name_length)]


def get_full_name(gender: str = None):
    if not gender:
        gender = "male"
        if random() > 0.5:
            gender = "female"
    return f"{get_first_name(gender)} {get_last_name()}"


def get_email(full_name: str = None):
    if full_name:
        return full_name.lower().replace(" ", "")


def get_username(fullname: str = None):
    if not fullname:
        num_of_word = randrange(2, 4)
        username = (
            word[randrange(word_length)]
            if random() > 0.5
            else word[randrange(word_length)].lower()
        )
        underscore = "_" if random() > 0.5 else ""
        for i in range(num_of_word):
            next_word = (
                word[randrange(word_length)]
                if random() > 0.5
                else word[randrange(word_length)].lower()
            )
            username = username + underscore + next_word
        return username + ("_" + str(randrange(9999)) if random() > 0.7 else "")
    else:
        return fullname.lower().replace(" ", "_") + (
            "_" + str(randrange(9999)) if random() > 0.7 else ""
        )


def get_random_word(min=1, max=20):
    d = word[randrange(word_length)]
    for i in range(randrange(min, max)):
        d += " " + word[randrange(word_length)]
    return d
