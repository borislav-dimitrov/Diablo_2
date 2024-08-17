class Appearances:
    LIGHT = 'light'
    DARK = 'dark'
    SYSTEM = 'system'


class Themes:
    BLUE = 'blue'
    DARK_BLUE = 'dark-blue'
    GREEN = 'green'


FONTS = {
    'header_1': ('Consolas', 22, 'bold'),
    'header_2': ('Consolas', 20, 'bold'),
    'header_3': ('Consolas', 18, 'bold'),
    'label': ('Consolas', 15, 'normal')
}

THEME_COLORS = {
    Themes.BLUE: {'normal': '#1F6AA5', 'hover': '#144870'},
    Themes.DARK_BLUE: {'normal': '#1F538D', 'hover': '#14375E'},
    Themes.GREEN: {'normal': '#2FA572', 'hover': '#106A43'}
}
