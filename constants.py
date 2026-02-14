# РАЗМЕРЫ
WIDTH = 1200
HEIGHT = 1000

# Размеры сетки - разные для разных размеров
CELL_SIZE = 70

# Для 3x3 и 6x6 - по центру
GRID_OFFSET_X_3 = (WIDTH - 3*CELL_SIZE) // 2
GRID_OFFSET_X_6 = (WIDTH - 6*CELL_SIZE) // 2

# Для 9x9 - смещаем левее
GRID_OFFSET_X_9 = 200

# Для 12x12 - тоже чуть левее
GRID_OFFSET_X_12 = 150

# Вертикальный отступ для всех
GRID_OFFSET_Y = 200

# ЦВЕТА БАЗОВЫЕ
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
LIGHT_GRAY = (200, 200, 200)
DARK_GRAY = (64, 64, 64)
RED = (255, 99, 71)
LIGHT_RED = (255, 200, 200)
GREEN = (144, 238, 144)
LIGHT_GREEN = (200, 255, 200)

# ЦВЕТА ДЛЯ ЗВЕЗД
GOLD = (255, 215, 0)
SILVER = (192, 192, 192)
BRONZE = (205, 127, 50)

# ЦВЕТА ДЛЯ КНОПОК (ВОЗВРАЩАЕМ!)
DARK_BLUE = (70, 130, 180)
BLUE = (100, 149, 237)

# ВРЕМЯ ДЛЯ ЗВЕЗД В ЗАВИСИМОСТИ ОТ РАЗМЕРА ПОЛЯ
STAR_TIMES_3 = {3: 10, 2: 15, 1: 20}
STAR_TIMES_6 = {3: 25, 2: 35, 1: 45}
STAR_TIMES_9 = {3: 45, 2: 55, 1: 65}
STAR_TIMES_12 = {3: 60, 2: 80, 1: 100}

# ===== ТЕМЫ =====
class Theme:
    def __init__(self, name, bg_color, grid_color, text_color, button_color, button_hover, accent_color):
        self.name = name
        self.bg_color = bg_color
        self.grid_color = grid_color
        self.text_color = text_color
        self.button_color = button_color
        self.button_hover = button_hover
        self.accent_color = accent_color

# Словарь всех тем
THEMES = {
    'light': Theme("Светлая", (255,255,255), (0,0,0), (0,0,0), (70,130,180), (100,149,237), (255,215,0)),
    'dark': Theme("Темная", (30,30,30), (200,200,200), (255,255,255), (100,100,150), (130,130,180), (255,215,0)),
    'blue': Theme("Синяя", (230,240,255), (0,50,100), (0,20,50), (0,100,200), (30,130,230), (255,200,0)),
    'green': Theme("Зеленая", (230,255,230), (0,80,0), (0,40,0), (0,120,0), (30,150,30), (255,215,0)),
    'purple': Theme("Фиолетовая", (245,230,255), (80,0,80), (40,0,40), (120,0,120), (150,30,150), (255,215,0))
}

# Текущая тема (глобальная переменная)
_current_theme = 'light'

def get_theme():
    """Возвращает текущую тему"""
    return THEMES[_current_theme]

def set_theme(theme_name):
    """Устанавливает новую тему"""
    global _current_theme
    if theme_name in THEMES:
        _current_theme = theme_name
        print(f"🎨 Тема изменена на {THEMES[theme_name].name}")
        return True
    return False

def get_theme_name():
    """Возвращает название текущей темы"""
    return _current_theme