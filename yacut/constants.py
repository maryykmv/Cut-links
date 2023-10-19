import re
import string


CHARACTERS = string.ascii_letters + string.digits
SHORT_LENGTH = 6
MAX_SHORT_LENGTH = 16
MAX_LONG_LENGTH = 2000
REDIRECT_VIEW = 'redirect_view'
INDEX_TEMPLATE = 'index.html'
VALID_CHARACTERS = f'[{re.compile(CHARACTERS)}]{{1,{SHORT_LENGTH}}}'
