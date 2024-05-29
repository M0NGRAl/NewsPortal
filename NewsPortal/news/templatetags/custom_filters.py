from django import template

register = template.Library()

CENSOR_WORDS = {
    'text1': 't****',
    'title2': 't*****',
}


@register.filter(name='censor')
def censor(value):
    if not isinstance(value, str):
        return value

    words = value.split()
    for i, word in enumerate(words):
        if word in CENSOR_WORDS:
            words[i] = CENSOR_WORDS[word]

    return ' '.join(words)