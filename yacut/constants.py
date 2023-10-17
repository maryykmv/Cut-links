import string


CHARACTERS = string.ascii_letters + string.digits
LENGTH_SHORT = 6
MAX_LENGTH_SHORT = 16
MAX_LENGTH_LONG_LINK = 2000
INDEX_TEMPLATE = 'index.html'
REDIRECT_VIEW = 'redirect_view'
MESSAGE_INVALID_VALUE = 'Указано недопустимое имя для короткой ссылки'
MESSAGE_EXISTS_SHORT = (
    'Предложенный вариант короткой ссылки уже существует.')
CHAR_SET = r'[a-zA-Z0-9]+'
