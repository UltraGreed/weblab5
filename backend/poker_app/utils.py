import random


def make_path(_prefix, model=None, slug_length=7):
    allowed_chars = '1234567890qwertyuiopasdfghjklzxcvbnm'
    prefix = _prefix
    name = ''
    for _ in range(slug_length):
        name += allowed_chars[random.randint(0, len(allowed_chars) - 1)]
    path = prefix + name
    if model is not None:
        if model.objects.filter(path=path).exists():
            make_path(_prefix, model, slug_length)
    return path, name


def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]
