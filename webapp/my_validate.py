from django.core.exceptions import ValidationError

SPECIAL_WORDS = ['bullshit', 'fuck', 'motherfucker', 'wtf']
SPECIAL_CHARS = ['%', '*', '@', '#']


def special_words(text):
    for i in SPECIAL_WORDS:
        if i.lower() in text.lower():
            raise ValidationError(f'Description should not contain "{i}!". Forbidden words {SPECIAL_WORDS}')


def special_chars(name):
    for i in SPECIAL_CHARS:
        if i in name:
            raise ValidationError(f'Summary should not contain "{i}"!. Forbidden symbols {SPECIAL_CHARS}')


def check_count(list):
    if len(list) == 3:
        raise ValidationError(f'"type" cannot be equal to 3')
