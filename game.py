import pygame
import time
import os
import sys
from constants import *

class Game:
    def __init__(self, size=9, level=1, show_rules=False, emoji_font=None):
        self.size = size
        self.level = level
        self.show_rules = show_rules
        self.emoji_font = emoji_font
        from levels import LevelSystem
        self.level_system = LevelSystem()
        self.board = self.level_system.get_level(size, level)
        self.original_board = [row[:] for row in self.board]
        self.selected = None
        self.start_time = time.time()
        self.completed = False
        self.stars = 0
        self.rules_shown = False
        self.check_mode = False
        self.victory_shown = False
        self.highlight_cells = {}
        self.game_mode = 'trial'
        
        if size == 3:
            self.max_number = 6
            self.grid_offset_x = GRID_OFFSET_X_3
            self.cell_size = CELL_SIZE
        elif size == 6:
            self.max_number = 6
            self.grid_offset_x = GRID_OFFSET_X_6
            self.cell_size = CELL_SIZE
        elif size == 9:
            self.max_number = 9
            self.grid_offset_x = GRID_OFFSET_X_9
            self.cell_size = CELL_SIZE
        else:  # size == 12
            self.max_number = 12
            self.grid_offset_x = GRID_OFFSET_X_12
            self.cell_size = CELL_SIZE_12  # Используем уменьшенный размер
        
        self.grid_offset_y = GRID_OFFSET_Y if size != 12 else GRID_OFFSET_Y_12
        
        # Загружаем шрифт с эмодзи
        self.emoji_font = self.load_emoji_font()
        
    def load_emoji_font(self):
        """Загружает шрифт с эмодзи"""
        if getattr(sys, 'frozen', False):
            base_path = os.path.dirname(sys.executable)
        else:
            base_path = os.path.dirname(__file__)
        
        font_path = os.path.join(base_path, "assets", "fonts", "segoe-ui-emoji_0.ttf")
        
        if os.path.exists(font_path):
            try:
                return pygame.font.Font(font_path, 24)
            except:
                return None
        return None
    
    def calculate_stars(self, elapsed):
        if self.size == 3:
            if elapsed < 10:
                return 3
            elif elapsed < 15:
                return 2
            elif elapsed < 20:
                return 1
            return 0
        elif self.size == 6:
            if elapsed < 25:
                return 3
            elif elapsed < 35:
                return 2
            elif elapsed < 45:
                return 1
            return 0
        elif self.size == 9:
            if elapsed < 45:
                return 3
            elif elapsed < 55:
                return 2
            elif elapsed < 65:
                return 1
            return 0
        else:
            if elapsed < 60:
                return 3
            elif elapsed < 80:
                return 2
            elif elapsed < 100:
                return 1
            return 0
    
    def draw(self, screen, font):
        # КАЖДЫЙ КАДР берем свежую тему из constants
        theme = get_theme()
        
        screen.fill(theme.bg_color)
        
        # Левая информация в рамке
        field_text = f"{self.size}x{self.size}  Уровень: {self.level}"
        field_surface = font.render(field_text, True, theme.text_color)
        
        field_padding = 15
        field_width = field_surface.get_width() + field_padding * 2
        field_height = field_surface.get_height() + field_padding
        field_x = 50 - field_padding//2
        field_y = 30 - field_padding//2
        
        pygame.draw.rect(screen, theme.button_color, (field_x, field_y, field_width, field_height), border_radius=15)
        pygame.draw.rect(screen, theme.accent_color, (field_x, field_y, field_width, field_height), 3, border_radius=15)
        screen.blit(field_surface, (50, 30))
        
        # Таймер в рамке (ТОЛЬКО если не режим изучения)
        if hasattr(self, 'game_mode') and self.game_mode != 'study':
            if hasattr(self, 'start_time'):
                elapsed = int(time.time() - self.start_time)
                minutes = elapsed // 60
                seconds = elapsed % 60
                timer_text = f"{minutes:02d}:{seconds:02d}"
                timer = font.render(timer_text, True, theme.text_color)
                
                timer_padding = 15
                timer_width = timer.get_width() + timer_padding * 2
                timer_height = timer.get_height() + timer_padding
                timer_x = 1150 - timer_width + timer_padding
                timer_y = 30 - timer_padding//2
                
                pygame.draw.rect(screen, theme.button_color, (timer_x, timer_y, timer_width, timer_height), border_radius=15)
                pygame.draw.rect(screen, theme.accent_color, (timer_x, timer_y, timer_width, timer_height), 3, border_radius=15)
                
                timer_rect = timer.get_rect()
                timer_rect.topright = (1150, 30)
                screen.blit(timer, timer_rect)
        else:
            # В режиме изучения показываем иконку 📚 вместо таймера
            study_icon = self.emoji_font.render("📚", True, theme.accent_color)
            icon_rect = study_icon.get_rect(topright=(1150, 30))
            screen.blit(study_icon, icon_rect)
        
        # Кнопки
        button_width = 280
        button_height = 80
        button_x = 900
        button_start_y = 80
        button_spacing = 90
        
        back = pygame.Rect(button_x, button_start_y, button_width, button_height)
        pygame.draw.rect(screen, theme.button_color, back, border_radius=20)
        pygame.draw.rect(screen, theme.grid_color, back, 4, border_radius=20)
        back_text = pygame.font.Font(None, 54).render("МЕНЮ", True, WHITE)
        back_rect = back_text.get_rect(center=back.center)
        screen.blit(back_text, back_rect)
        
        rules = pygame.Rect(button_x, button_start_y + button_spacing, button_width, button_height)
        pygame.draw.rect(screen, theme.button_color, rules, border_radius=20)
        pygame.draw.rect(screen, theme.grid_color, rules, 4, border_radius=20)
        rules_text = pygame.font.Font(None, 54).render("ПРАВИЛА", True, WHITE)
        rules_rect = rules_text.get_rect(center=rules.center)
        screen.blit(rules_text, rules_rect)
        
        check_btn = pygame.Rect(button_x, button_start_y + button_spacing * 2, button_width, button_height)
        color = GREEN if self.check_mode else theme.button_color
        pygame.draw.rect(screen, color, check_btn, border_radius=20)
        pygame.draw.rect(screen, theme.grid_color, check_btn, 4, border_radius=20)
        check_text = pygame.font.Font(None, 54).render("ПРОВЕРКА", True, WHITE)
        check_rect = check_text.get_rect(center=check_btn.center)
        screen.blit(check_text, check_rect)
        
        # Сетка
        self.draw_grid(screen)
        self.draw_highlights(screen)
        self.draw_numbers(screen, font)
        if self.selected: 
            self.draw_selected(screen)
        
        # Подсказка для 12x12
        if self.size == 12:
            hint_font = pygame.font.Font(None, 20)
            hint_text = hint_font.render("0=10  -=11  ==12", True, theme.accent_color)
            screen.blit(hint_text, (self.grid_offset_x, self.grid_offset_y + self.size*self.cell_size + 10))
        
        if self.show_rules and not self.rules_shown:
            self.show_rules_popup(screen, font)
            self.rules_shown = True
            
        return back, rules, check_btn
    
    def draw_grid(self, screen):
        # КАЖДЫЙ КАДР берем свежую тему
        theme = get_theme()
        start_x = self.grid_offset_x
        start_y = self.grid_offset_y
        
        if self.size == 9:
            block_size = 3
        elif self.size == 6:
            block_size = 2
        elif self.size == 12:
            block_size = 4
        else:
            block_size = 1
        
        for i in range(self.size + 1):
            w = 3 if i % block_size == 0 else 1
            pygame.draw.line(screen, theme.grid_color,
                        (start_x, start_y + i * self.cell_size), 
                        (start_x + self.size * self.cell_size, start_y + i * self.cell_size), w)
            pygame.draw.line(screen, theme.grid_color,
                        (start_x + i * self.cell_size, start_y), 
                        (start_x + i * self.cell_size, start_y + self.size * self.cell_size), w)
        
    def draw_highlights(self, screen):
            if not self.check_mode:
                return
                
            start_x = self.grid_offset_x
            start_y = self.grid_offset_y
            
            for r in range(self.size):
                for c in range(self.size):
                    if (r, c) in self.highlight_cells:
                        color = self.highlight_cells[(r, c)]
                        s = pygame.Surface((self.cell_size-2, self.cell_size-2))
                        s.set_alpha(150)
                        s.fill(color)
                        screen.blit(s, (start_x + 1 + c*self.cell_size, start_y + 1 + r*self.cell_size))
            
    def draw_numbers(self, screen, font):
        theme = get_theme()
        start_x = self.grid_offset_x
        start_y = self.grid_offset_y
        
        for r in range(self.size):
            for c in range(self.size):
                n = self.board[r][c]
                if n != 0:
                    if theme.name == "Темная":
                        color = WHITE if self.original_board[r][c] != 0 else theme.accent_color
                    else:
                        color = BLACK if self.original_board[r][c] != 0 else theme.button_color
                    
                    # Для чисел 10, 11, 12 используем чуть меньший шрифт
                    if n >= 10:
                        text = pygame.font.Font(None, 40).render(str(n), True, color)
                    else:
                        text = font.render(str(n), True, color)
                    
                    x = start_x + c*self.cell_size + (self.cell_size - text.get_width())//2
                    y = start_y + r*self.cell_size + (self.cell_size - text.get_height())//2
                    screen.blit(text, (x, y))
        # ;d
        if theme.name == "Фиолетовая" and self.size == 9:
            self.draw_easter_egg(screen)

    def draw_easter_egg(self, screen):
        """Рисует пасхалку в фиолетовой теме на 9x9"""
        start_x = self.grid_offset_x
        start_y = self.grid_offset_y
        
        small_font = pygame.font.Font(None, 16)
        
        if self.board[0][0] == 0:
            hint1 = small_font.render("V", True, (200, 150, 255))
            screen.blit(hint1, (start_x + 5, start_y + 5))
        
        if self.board[0][8] == 0:
            hint2 = small_font.render("I", True, (200, 150, 255))
            screen.blit(hint2, (start_x + 8*self.cell_size + 5, start_y + 5))
        
        if self.board[8][0] == 0:
            hint3 = small_font.render("N", True, (200, 150, 255))
            screen.blit(hint3, (start_x + 5, start_y + 8*self.cell_size + 5))
        
        if self.board[8][8] == 0:
            hint4 = small_font.render("D", True, (200, 150, 255))
            screen.blit(hint4, (start_x + 8*self.cell_size + 5, start_y + 8*self.cell_size + 5))
    
    def draw_selected(self, screen):
        r, c = self.selected
        start_x = self.grid_offset_x
        start_y = self.grid_offset_y
        pygame.draw.rect(screen, (255,200,200), 
                        (start_x + c*self.cell_size, start_y + r*self.cell_size, 
                        self.cell_size, self.cell_size), 3)
    
    def handle_click(self, pos):
        x, y = pos
        start_x = self.grid_offset_x
        start_y = self.grid_offset_y
        
        if (start_x <= x <= start_x + self.size*self.cell_size and 
            start_y <= y <= start_y + self.size*self.cell_size):
            c = (x - start_x) // self.cell_size
            r = (y - start_y) // self.cell_size
            if r < self.size and c < self.size and self.original_board[r][c] == 0:
                self.selected = (r, c)
            else: 
                self.selected = None
            return True
        return False
    
    def place_number(self, num):
        if num < 1 or num > self.max_number:
            return
            
        if self.selected and not self.completed:
            r, c = self.selected
            if self.original_board[r][c] == 0:
                self.board[r][c] = num
                if self.check_mode:
                    self.check_board()
                else:
                    self.highlight_cells.clear()
    
    def delete_number(self):
        if self.selected and not self.completed:
            r, c = self.selected
            if self.original_board[r][c] == 0:
                self.board[r][c] = 0
                if self.check_mode:
                    self.check_board()
                else:
                    self.highlight_cells.clear()
    
    def is_valid_move(self, row, col, num):
        for x in range(self.size):
            if x != col and self.board[row][x] == num:
                return False
        
        for x in range(self.size):
            if x != row and self.board[x][col] == num:
                return False
        
        if self.size == 9:
            box_size = 3
            start_row = row - row % 3
            start_col = col - col % 3
        elif self.size == 6:
            box_size = 2
            start_row = row - row % 2
            start_col = col - col % 3
        elif self.size == 3:
            box_size = 1
            start_row = row
            start_col = col
        else:
            box_size = 4
            start_row = row - row % 4
            start_col = col - col % 3
        
        for i in range(box_size):
            for j in range(3 if self.size in [6,12] else box_size):
                r = start_row + i
                c = start_col + j
                if r < self.size and c < self.size:
                    if (r != row or c != col) and self.board[r][c] == num:
                        return False
        return True
    
    def check_board(self):
        self.highlight_cells.clear()
        for r in range(self.size):
            for c in range(self.size):
                if self.board[r][c] != 0 and self.original_board[r][c] == 0:
                    num = self.board[r][c]
                    self.board[r][c] = 0
                    if not self.is_valid_move(r, c, num):
                        self.highlight_cells[(r, c)] = LIGHT_RED
                    else:
                        self.highlight_cells[(r, c)] = LIGHT_GREEN
                    self.board[r][c] = num
    
    def check_win_condition(self):
        if not self.check_mode:
            return False
        
        for r in range(self.size):
            for c in range(self.size):
                if self.board[r][c] == 0:
                    return False
        
        for r in range(self.size):
            for c in range(self.size):
                num = self.board[r][c]
                if not self.is_valid_move(r, c, num):
                    return False
        
        self.completed = True
        t = time.time() - self.start_time
        self.stars = self.calculate_stars(t)
            
        self.victory_shown = True
        return True
    
    def check_victory_condition(self):
        """Проверяет, решено ли судоку правильно"""
        # Проверяем заполненность
        for r in range(self.size):
            for c in range(self.size):
                if self.board[r][c] == 0:
                    return False
        
        # Проверяем правильность
        for r in range(self.size):
            for c in range(self.size):
                num = self.board[r][c]
                if not self.is_valid_move(r, c, num):
                    return False
        
        return True
    
    def check_defeat_condition(self, elapsed):
        """Проверяет, проиграл ли игрок (только для trial и tournament)"""
        from constants import STAR_TIMES, DEFEAT_MULTIPLIER
        
        # В режиме изучения поражения нет
        if not hasattr(self, 'game_mode') or self.game_mode == 'study':
            return False
        
        # Базовое время на поражение (в 2 раза больше бронзы)
        if self.size == 3:
            defeat_time = 20 * DEFEAT_MULTIPLIER
        elif self.size == 6:
            defeat_time = 45 * DEFEAT_MULTIPLIER
        elif self.size == 9:
            defeat_time = 65 * DEFEAT_MULTIPLIER
        else:
            defeat_time = 100 * DEFEAT_MULTIPLIER
        
        # Для турнирного режима времени еще меньше
        if self.game_mode == 'tournament':
            defeat_time = defeat_time * 0.7
        
        return elapsed > defeat_time
    
    def show_rules_popup(self, screen, font):
        # КАЖДЫЙ КАДР берем свежую тему
        theme = get_theme()
        
        # Размеры окна правил
        popup_width = 800
        popup_height = 850
        popup_x = (WIDTH - popup_width) // 2
        popup_y = 50
        
        popup_rect = pygame.Rect(popup_x, popup_y, popup_width, popup_height)
        pygame.draw.rect(screen, WHITE, popup_rect)
        pygame.draw.rect(screen, theme.accent_color, popup_rect, 5)
        
        if theme.name == "Фиолетовая" and self.size == 9:
            # В самом низу правил, мелким шрифтом
            easter_font = pygame.font.Font(None, 16)
            easter_text = easter_font.render("PS: VINDIGO4 - это ключ...", True, (200, 150, 255))
            screen.blit(easter_text, (400, 820))

        # Заголовок
        title = pygame.font.Font(None, 48).render("ПРАВИЛА ИГРЫ СУДОКУ", True, theme.accent_color)
        title_rect = title.get_rect(center=(WIDTH//2, popup_y + 50))
        screen.blit(title, title_rect)
        
        # Время для звезд
        if self.size == 3:
            time_texts = [
                "ВРЕМЯ ДЛЯ 3x3",
                "Золото: < 10 сек (3 звезды)",
                "Серебро: 10-14 сек (2 звезды)",
                "Бронза: 15-19 сек (1 звезда)",
                "Без звезд: ≥ 20 сек"
            ]
        elif self.size == 6:
            time_texts = [
                "ВРЕМЯ ДЛЯ 6x6",
                "Золото: < 25 сек (3 звезды)",
                "Серебро: 25-34 сек (2 звезды)",
                "Бронза: 35-44 сек (1 звезда)",
                "Без звезд: ≥ 45 сек"
            ]
        elif self.size == 9:
            time_texts = [
                "ВРЕМЯ ДЛЯ 9x9",
                "Золото: < 45 сек (3 звезды)",
                "Серебро: 45-54 сек (2 звезды)",
                "Бронза: 55-64 сек (1 звезда)",
                "Без звезд: ≥ 65 сек"
            ]
        else:
            time_texts = [
                "ВРЕМЯ ДЛЯ 12x12",
                "Золото: < 60 сек (3 звезды)",
                "Серебро: 60-79 сек (2 звезды)",
                "Бронза: 80-99 сек (1 звезда)",
                "Без звезд: ≥ 100 сек"
            ]
        
        # Весь текст правил
        rules_texts = [
            "ОСНОВНЫЕ ПРАВИЛА:",
            "",
            "1. ЦЕЛЬ ИГРЫ:",
            "   Заполнить всю сетку цифрами так, чтобы в каждой строке,",
            "   каждом столбце и каждом блоке цифры не повторялись.",
            "",
            "2. ИГРОВОЕ ПОЛЕ:",
            "   • 9x9 - классическое судоку (блоки 3x3, цифры 1-9)",
            "   • 6x6 - уменьшенная версия (блоки 2x3, цифры 1-6)",
            "   • 3x3 - для начинающих (блок 3x3, цифры 1-6)",
            "   • 12x12 - бонусный режим (блоки 4x3, цифры 1-12)",
            "",
            "3. ЦИФРЫ:",
            "   • Черные цифры - изначальные (нельзя менять)",
            "   • Синие цифры - введены игроком",
            "",
            "УПРАВЛЕНИЕ:",
            "4. МЫШЬ:",
            "   • Левый клик - выбрать клетку",
            "",
            "5. КЛАВИАТУРА:",
            "   • Цифры 1-9 - ввести цифру",
            "   • DELETE/BACKSPACE - стереть цифру",
        ]

        # Добавляем правила для 12x12 если нужно
        if self.size == 12:
            rules_texts.extend([
                "",
                "ДЛЯ 12x12:",
                "   • 0 - ввести 10",
                "   • - (минус) - ввести 11",
                "   • = (равно) - ввести 12"
            ])

        # Продолжаем основной список
        rules_texts.extend([
            "",
            "6. КНОПКИ:",
            "   • МЕНЮ - вернуться в главное меню",
            "   • ПРАВИЛА - открыть это окно",
            "   • ПРОВЕРКА - подсветить ошибки",
            "",
            "СИСТЕМА ПРОГРЕССА",
            "7. УРОВНИ:",
            "   • 30 уровней для каждого размера",
            "   • Новый уровень открывается после прохождения",
            "",
            "8. ЗВЕЗДЫ ЗА СКОРОСТЬ:",
            time_texts[0],
            time_texts[1],
            time_texts[2],
            time_texts[3],
            time_texts[4],
            "",
            "ЖЕЛАЕМ УДАЧИ!",
            "",
            "Над проектом работали",
            "Ученики 9г класса:",
            "Бортников А.С. и Ломтев А.И."
        ])
        
        # Параметры прокрутки
        scroll_y = 0
        line_height = 30
        start_y = popup_y + 100
        visible_height = 650
        total_height = len(rules_texts) * line_height
        max_scroll = max(0, total_height - visible_height)
        
        # Кнопка ОК
        ok_btn = pygame.Rect(WIDTH//2 - 100, popup_y + popup_height - 70, 200, 50)
        
        # Ползунок
        scroll_bar_x = popup_x + popup_width - 30
        scroll_bar_y = popup_y + 100
        scroll_bar_height = visible_height
        scroll_thumb_height = max(40, int(scroll_bar_height * visible_height / total_height))
        scroll_thumb = pygame.Rect(scroll_bar_x, scroll_bar_y, 15, scroll_thumb_height)
        
        # Шрифты
        text_font = pygame.font.Font(None, 24)
        
        waiting = True
        dragging = False
        
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if ok_btn.collidepoint(event.pos):
                        waiting = False
                    
                    # Проверка клика по ползунку
                    if scroll_bar_x <= event.pos[0] <= scroll_bar_x + 15 and \
                       scroll_bar_y <= event.pos[1] <= scroll_bar_y + scroll_bar_height:
                        dragging = True
                        # Перемещение ползунка к месту клика
                        rel_y = event.pos[1] - scroll_bar_y
                        rel_y = max(0, min(rel_y, scroll_bar_height - scroll_thumb_height))
                        scroll_thumb.y = scroll_bar_y + rel_y
                        progress = (scroll_thumb.y - scroll_bar_y) / (scroll_bar_height - scroll_thumb_height)
                        scroll_y = -progress * max_scroll
                
                if event.type == pygame.MOUSEBUTTONUP:
                    dragging = False
                
                if event.type == pygame.MOUSEMOTION and dragging:
                    rel_y = event.pos[1] - scroll_bar_y
                    rel_y = max(0, min(rel_y, scroll_bar_height - scroll_thumb_height))
                    scroll_thumb.y = scroll_bar_y + rel_y
                    progress = (scroll_thumb.y - scroll_bar_y) / (scroll_bar_height - scroll_thumb_height)
                    scroll_y = -progress * max_scroll
                
                if event.type == pygame.MOUSEWHEEL:
                    scroll_y += event.y * 30
                    scroll_y = min(0, max(scroll_y, -max_scroll))
                    if max_scroll > 0:
                        progress = -scroll_y / max_scroll
                        scroll_thumb.y = scroll_bar_y + progress * (scroll_bar_height - scroll_thumb_height)
            
            # Отрисовка фона
            pygame.draw.rect(screen, WHITE, popup_rect)
            pygame.draw.rect(screen, theme.accent_color, popup_rect, 5)
            screen.blit(title, title_rect)
            
            # Отрисовка текста с прокруткой
            y_offset = 0
            for rule in rules_texts:
                text_y_pos = start_y + y_offset + scroll_y
                # Рисуем только видимые строки
                if start_y <= text_y_pos <= start_y + visible_height:
                    if "Золото" in rule:
                        color = GOLD
                    elif "Серебро" in rule:
                        color = SILVER
                    elif "Бронза" in rule:
                        color = BRONZE
                    elif rule.startswith("   "):
                        color = BLACK
                    else:
                        color = theme.accent_color
                    
                    text_surface = text_font.render(rule, True, color)
                    screen.blit(text_surface, (popup_x + 30, text_y_pos))
                y_offset += line_height
            
            # Отрисовка ползунка
            if max_scroll > 0:
                pygame.draw.rect(screen, LIGHT_GRAY, (scroll_bar_x, scroll_bar_y, 15, scroll_bar_height))
                pygame.draw.rect(screen, theme.accent_color, scroll_thumb)
                pygame.draw.rect(screen, DARK_GRAY, scroll_thumb, 1)
            
            # Отрисовка кнопки ОК
            pygame.draw.rect(screen, theme.button_color, ok_btn, border_radius=10)
            pygame.draw.rect(screen, theme.accent_color, ok_btn, 3, border_radius=10)
            ok_text = text_font.render("ОК", True, WHITE)
            ok_text_rect = ok_text.get_rect(center=ok_btn.center)
            screen.blit(ok_text, ok_text_rect)
            
            pygame.display.flip()