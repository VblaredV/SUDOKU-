import pygame
import sys
import os
import time
from constants import *
from game import Game
from levels import LevelSystem
from save_system import save_system
import settings
from constants import get_theme, set_theme, get_theme_name, THEMES

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SUDOKU BV")
clock = pygame.time.Clock()

cheat_code = []

CHEAT_SEQUENCE = [pygame.K_v, pygame.K_i, pygame.K_n, pygame.K_d, 
                  pygame.K_i, pygame.K_g, pygame.K_o, pygame.K_4]

# ===== МУЗЫКА =====
pygame.mixer.init()
MUSIC_FOLDER = os.path.join("assets", "music")
playlist = []
if os.path.exists(MUSIC_FOLDER):
    for file in os.listdir(MUSIC_FOLDER):
        if file.endswith('.mp3'):
            playlist.append(os.path.join(MUSIC_FOLDER, file))
    print(f"✅ Найдено треков: {len(playlist)}")

current_track = 0
music_playing = False

# ===== ЗВУКОВЫЕ ЭФФЕКТЫ =====
SOUND_FOLDER = os.path.join("assets", "sounds")
victory_sound = None
defeat_sound = None

victory_path = os.path.join(SOUND_FOLDER, "victory.wav")
defeat_path = os.path.join(SOUND_FOLDER, "defeat.wav")

if os.path.exists(victory_path):
    try:
        victory_sound = pygame.mixer.Sound(victory_path)
        print("✅ Звук победы загружен")
    except Exception as e:
        print(f"❌ Ошибка загрузки victory.wav: {e}")

if os.path.exists(defeat_path):
    try:
        defeat_sound = pygame.mixer.Sound(defeat_path)
        print("✅ Звук поражения загружен")
    except Exception as e:
        print(f"❌ Ошибка загрузки defeat.wav: {e}")

def play_victory_sound():
    if player_settings.get('sound', True) and victory_sound:
        victory_sound.play()

def play_defeat_sound():
    if player_settings.get('sound', True) and defeat_sound:
        defeat_sound.play()

def play_track(index):
    global current_track, music_playing
    if playlist and 0 <= index < len(playlist):
        try:
            pygame.mixer.music.load(playlist[index])
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play(-1)
            current_track = index
            music_playing = True
            print(f"🎵 Играет трек {index+1}")
        except Exception as e:
            print(f"❌ Ошибка музыки: {e}")

def stop_music():
    global music_playing
    pygame.mixer.music.stop()
    music_playing = False
    print("🎵 Музыка остановлена")

def pause_music():
    global music_playing
    pygame.mixer.music.pause()
    music_playing = False
    print("🎵 Музыка на паузе")

def unpause_music():
    global music_playing
    pygame.mixer.music.unpause()
    music_playing = True
    print("🎵 Музыка возобновлена")

def next_track():
    if playlist:
        next_index = (current_track + 1) % len(playlist)
        play_track(next_index)

def prev_track():
    if playlist:
        prev_index = (current_track - 1) % len(playlist)
        play_track(prev_index)

def toggle_music():
    global music_playing
    if music_playing:
        pause_music()
    else:
        unpause_music()


# ===== ШРИФТЫ =====
# Системные шрифты (ДЛЯ ОБЫЧНОГО ТЕКСТА)
font_big = pygame.font.Font(None, 80)
font_mid = pygame.font.Font(None, 54)
font_small = pygame.font.Font(None, 42)
font_tiny = pygame.font.Font(None, 30)

# Шрифт с эмодзи (ТОЛЬКО ДЛЯ ЭМОДЗИ)
emoji_font_path = None
fonts_folder = os.path.join("assets", "fonts")
if os.path.exists(fonts_folder):
    for file in os.listdir(fonts_folder):
        if file.endswith('.ttf'):
            emoji_font_path = os.path.join(fonts_folder, file)
            print(f"✅ Найден шрифт: {file}")
            break

if emoji_font_path:
    try:
        font_emoji = pygame.font.Font(emoji_font_path, 30)
        font_emoji_big = pygame.font.Font(emoji_font_path, 40)
        font_emoji_small = pygame.font.Font(emoji_font_path, 24)
        print("✅ Шрифт с эмодзи загружен!")
    except Exception as e:
        print(f"❌ Ошибка загрузки шрифта: {e}")
        font_emoji = font_tiny
        font_emoji_big = font_small
        font_emoji_small = font_tiny
else:
    print("⚠️ Шрифт не найден, эмодзи не будут работать")
    font_emoji = font_tiny
    font_emoji_big = font_small
    font_emoji_small = font_tiny

level_system = LevelSystem()
player_settings = save_system.load_settings()

if 'show_player' not in player_settings:
    player_settings['show_player'] = True

if 'theme' in player_settings:
    set_theme(player_settings['theme'])

# ;3
FULLSCREEN_READY = False
if FULLSCREEN_READY:
    print("🖥️ Режим полного экрана скоро будет доступен...")

if playlist:
    if player_settings.get('show_player', True) and player_settings.get('music', True):
        play_track(0)
        print("🎵 Музыка включена (плеер показан)")
    else:
        print("🎵 Музыка не играет (плеер скрыт или музыка выключена)")

class Button:
    def __init__(self, x, y, w, h, t, c, hc, fs=54):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = t
        self.color = c
        self.hover_color = hc
        self.current = c
        self.font = pygame.font.Font(None, fs)
    
    def draw(self, s):
        theme = get_theme()
        pygame.draw.rect(s, self.current, self.rect, border_radius=15)
        pygame.draw.rect(s, theme.grid_color, self.rect, 4, border_radius=15)
        txt = self.font.render(self.text, True, WHITE)
        txt_rect = txt.get_rect(center=self.rect.center)
        s.blit(txt, txt_rect)
    
    def check_hover(self, pos):
        self.current = self.hover_color if self.rect.collidepoint(pos) else self.color
        return self.rect.collidepoint(pos)
    
    def is_clicked(self, pos, e):
        return e.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(pos)

def draw_bg():
    theme = get_theme()
    screen.fill(theme.bg_color)
    for i in range(0, WIDTH, 50):
        pygame.draw.line(screen, (theme.grid_color[0], theme.grid_color[1], theme.grid_color[2], 30), (i, 0), (i, HEIGHT), 1)
    for i in range(0, HEIGHT, 50):
        pygame.draw.line(screen, (theme.grid_color[0], theme.grid_color[1], theme.grid_color[2], 30), (0, i), (WIDTH, i), 1)

def draw_music_player():
    if not playlist or not player_settings.get('show_player', True):
        return None
    
    theme = get_theme()
    
    player_width = 700
    player_height = 70
    player_x = WIDTH//2 - player_width//2
    player_y = HEIGHT - 90
    
    player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
    pygame.draw.rect(screen, theme.button_color, player_rect, border_radius=15)
    pygame.draw.rect(screen, theme.accent_color, player_rect, 3, border_radius=15)
    
    track_name = os.path.basename(playlist[current_track])
    if len(track_name) > 25:
        track_name = track_name[:22] + "..."
    
    track_text = font_tiny.render(track_name, True, WHITE)
    track_rect = track_text.get_rect(midleft=(player_x + 20, player_y + player_height//2))
    screen.blit(track_text, track_rect)
    
    button_size = 50
    button_y = player_y + (player_height - button_size) // 2
    
    # Отступ от правого края - 20 пикселей
    right_margin = 20
    
    # Кнопка NEXT (самая правая)
    next_btn = pygame.Rect(player_x + player_width - button_size - right_margin, 
                          button_y, button_size, button_size)
    pygame.draw.rect(screen, theme.button_hover, next_btn, border_radius=10)
    pygame.draw.rect(screen, WHITE, next_btn, 2, border_radius=10)
    next_text = font_emoji_big.render("⏭️", True, WHITE)
    next_rect = next_text.get_rect(center=next_btn.center)
    screen.blit(next_text, next_rect)
    
    # Кнопка PLAY/PAUSE (слева от NEXT)
    play_btn = pygame.Rect(player_x + player_width - button_size * 2 - right_margin - 10, 
                          button_y, button_size, button_size)
    color = GREEN if music_playing else RED
    pygame.draw.rect(screen, color, play_btn, border_radius=10)
    pygame.draw.rect(screen, WHITE, play_btn, 2, border_radius=10)
    play_text = font_emoji_big.render("⏸️" if music_playing else "▶️", True, WHITE)
    play_rect = play_text.get_rect(center=play_btn.center)
    screen.blit(play_text, play_rect)
    
    # Кнопка PREV (слева от PLAY)
    prev_btn = pygame.Rect(player_x + player_width - button_size * 3 - right_margin - 20, 
                          button_y, button_size, button_size)
    pygame.draw.rect(screen, theme.button_hover, prev_btn, border_radius=10)
    pygame.draw.rect(screen, WHITE, prev_btn, 2, border_radius=10)
    prev_text = font_emoji_big.render("⏮️", True, WHITE)
    prev_rect = prev_text.get_rect(center=prev_btn.center)
    screen.blit(prev_text, prev_rect)
    
    return prev_btn, play_btn, next_btn

def exp_choice():
    if save_system.settings_file.exists(): return
    
    center_x = WIDTH // 2
    
    btns = [
        Button(400, 400, 400, 80, "Я НОВИЧОК", DARK_BLUE, BLUE, 50),
        Button(400, 500, 400, 80, "Я ОПЫТНЫЙ", DARK_BLUE, BLUE, 50)
    ]
    
    while True:
        draw_bg()
        mouse = pygame.mouse.get_pos()
        theme = get_theme()
        
        # ===== ЗАГОЛОВОК В РАМКЕ =====
        title_text = "SUDOKU BV"
        title = font_big.render(title_text, True, theme.accent_color)
        
        # Рамка для заголовка
        title_padding = 30
        title_width = title.get_width() + title_padding * 2
        title_height = title.get_height() + title_padding
        title_x = center_x - title_width // 2
        title_y = 120
        
        # Тень
        shadow_rect = pygame.Rect(title_x + 4, title_y + 4, title_width, title_height)
        pygame.draw.rect(screen, (50,50,50,150), shadow_rect, border_radius=20)
        
        # Основная рамка
        title_rect = pygame.Rect(title_x, title_y, title_width, title_height)
        pygame.draw.rect(screen, theme.button_color, title_rect, border_radius=20)
        pygame.draw.rect(screen, theme.accent_color, title_rect, 4, border_radius=20)
        
        # Текст заголовка
        title_rect = title.get_rect(center=(center_x, title_y + title_height//2))
        screen.blit(title, title_rect)
        
        # ===== ПОДЗАГОЛОВОК =====
        subtitle_text = "Выберите ваш уровень опыта"
        subtitle = font_mid.render(subtitle_text, True, theme.text_color)
        
        # Рамка для подзаголовка
        sub_padding = 20
        sub_width = subtitle.get_width() + sub_padding * 2
        sub_height = subtitle.get_height() + sub_padding
        sub_x = center_x - sub_width // 2
        sub_y = 220
        
        shadow_sub = pygame.Rect(sub_x + 3, sub_y + 3, sub_width, sub_height)
        pygame.draw.rect(screen, (50,50,50,100), shadow_sub, border_radius=15)
        
        sub_rect = pygame.Rect(sub_x, sub_y, sub_width, sub_height)
        pygame.draw.rect(screen, theme.button_hover, sub_rect, border_radius=15)
        pygame.draw.rect(screen, theme.accent_color, sub_rect, 2, border_radius=15)
        
        sub_rect = subtitle.get_rect(center=(center_x, sub_y + sub_height//2))
        screen.blit(subtitle, sub_rect)
        
        # ===== ОПИСАНИЯ РЕЖИМОВ =====
        desc_y = 600
        desc_spacing = 30
        
        if btns[0].check_hover(mouse):
            # Описание для новичка
            desc_title = font_small.render("РЕЖИМ НОВИЧКА:", True, theme.accent_color)
            screen.blit(desc_title, (center_x - 200, desc_y))
            
            desc1 = font_tiny.render("• Правила показываются перед игрой", True, theme.text_color)
            screen.blit(desc1, (center_x - 200, desc_y + desc_spacing))
            
            desc2 = font_tiny.render("• Подсветка ошибок включена", True, theme.text_color)
            screen.blit(desc2, (center_x - 200, desc_y + desc_spacing * 2))
            
            desc3 = font_tiny.render("• Больше времени на получение звезд", True, theme.text_color)
            screen.blit(desc3, (center_x - 200, desc_y + desc_spacing * 3))
            
        elif btns[1].check_hover(mouse):
            # Описание для опытного
            desc_title = font_small.render("РЕЖИМ ОПЫТНОГО:", True, theme.accent_color)
            screen.blit(desc_title, (center_x - 200, desc_y))
            
            desc1 = font_tiny.render("• Правила показываются один раз", True, theme.text_color)
            screen.blit(desc1, (center_x - 200, desc_y + desc_spacing))
            
            desc2 = font_tiny.render("• Подсветка ошибок по желанию", True, theme.text_color)
            screen.blit(desc2, (center_x - 200, desc_y + desc_spacing * 2))
            
            desc3 = font_tiny.render("• Меньше времени на звезды", True, theme.text_color)
            screen.blit(desc3, (center_x - 200, desc_y + desc_spacing * 3))
        
        # ===== КНОПКИ =====
        for i, btn in enumerate(btns):
            # Центрируем кнопки
            btn.rect.x = center_x - btn.rect.width // 2
            btn.rect.y = 350 + i * 100
            
            btn.check_hover(mouse)
            btn.draw(screen)
        
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            for btn in btns:
                if btn.is_clicked(mouse, e):
                    player_settings['experience'] = 'novice' if btn.text == "Я НОВИЧОК" else 'expert'
                    save_system.save_settings(player_settings)
                    return
        
        pygame.display.flip()
        clock.tick(60)

def main_menu():
    global cheat_code  # Добавляем глобальную переменную
    
    while True:
        draw_bg()
        mouse = pygame.mouse.get_pos()
        theme = get_theme()
        
        btns = [
            Button(400, 250, 400, 80, "ИГРАТЬ", theme.button_color, theme.button_hover),
            Button(400, 350, 400, 80, "УРОВНИ", theme.button_color, theme.button_hover),
            Button(400, 450, 400, 80, "СТАТИСТИКА", theme.button_color, theme.button_hover),
            Button(400, 550, 400, 80, "НАСТРОЙКИ", theme.button_color, theme.button_hover),
            Button(400, 650, 400, 80, "ВЫХОД", theme.button_color, theme.button_hover)
        ]
        
        # ===== УКРАШЕННЫЙ ЗАГОЛОВОК =====
        shadow = font_big.render("SUDOKU BV", True, (50, 50, 50, 128))
        shadow_rect = shadow.get_rect(center=(602, 182))
        screen.blit(shadow, shadow_rect)
        
        title = font_big.render("SUDOKU BV", True, theme.accent_color)
        title_rect = title.get_rect(center=(600, 180))
        
        for dx, dy in [(-2,-2), (2,-2), (-2,2), (2,2)]:
            outline = font_big.render("SUDOKU BV", True, theme.grid_color)
            screen.blit(outline, (title_rect.x + dx, title_rect.y + dy))
        
        screen.blit(title, title_rect)
        
        line_y = title_rect.bottom + 10
        pygame.draw.line(screen, theme.accent_color, (400, line_y), (800, line_y), 3)
        pygame.draw.line(screen, theme.grid_color, (400, line_y + 2), (800, line_y + 2), 1)
        
        # ===== ЛЕВАЯ ПАНЕЛЬ =====
        total_stars = level_system.get_total_stars()
        
        left_panel = pygame.Rect(30, 20, 230, 50)
        pygame.draw.rect(screen, theme.button_color, left_panel, border_radius=10)
        pygame.draw.rect(screen, theme.accent_color, left_panel, 2, border_radius=10)
        
        stars_text = font_tiny.render("Всего звезд:", True, WHITE)
        stars_text_rect = stars_text.get_rect(midleft=(left_panel.x + 10, left_panel.centery))
        screen.blit(stars_text, stars_text_rect)
        
        stars_value = font_emoji_small.render(f"⭐ {total_stars}", True, WHITE)
        stars_value_rect = stars_value.get_rect(midright=(left_panel.right - 15, left_panel.centery))
        screen.blit(stars_value, stars_value_rect)
        
        # ===== ПРАВАЯ ПАНЕЛЬ =====
        mode = "Новичок" if player_settings['experience'] == 'novice' else "Опытный"
        
        right_panel = pygame.Rect(950, 20, 220, 50)
        pygame.draw.rect(screen, theme.button_color, right_panel, border_radius=10)
        pygame.draw.rect(screen, theme.accent_color, right_panel, 2, border_radius=10)
        
        mode_emoji = font_emoji_small.render("👤", True, WHITE)
        mode_emoji_rect = mode_emoji.get_rect(midleft=(right_panel.x + 10, right_panel.centery))
        screen.blit(mode_emoji, mode_emoji_rect)
        
        mode_text = font_tiny.render(f"Режим: {mode}", True, WHITE)
        mode_text_rect = mode_text.get_rect(midright=(right_panel.right - 10, right_panel.centery))
        screen.blit(mode_text, mode_text_rect)
        
        # ===== ДЕКОРАТИВНЫЕ УГЛЫ =====
        corner_size = 40
        line_width = 4
        
        pygame.draw.line(screen, theme.accent_color, (0, 0), (corner_size, 0), line_width)
        pygame.draw.line(screen, theme.accent_color, (0, 0), (0, corner_size), line_width)
        pygame.draw.line(screen, theme.accent_color, (WIDTH, 0), (WIDTH - corner_size, 0), line_width)
        pygame.draw.line(screen, theme.accent_color, (WIDTH, 0), (WIDTH, corner_size), line_width)
        pygame.draw.line(screen, theme.accent_color, (0, HEIGHT), (corner_size, HEIGHT), line_width)
        pygame.draw.line(screen, theme.accent_color, (0, HEIGHT), (0, HEIGHT - corner_size), line_width)
        pygame.draw.line(screen, theme.accent_color, (WIDTH, HEIGHT), (WIDTH - corner_size, HEIGHT), line_width)
        pygame.draw.line(screen, theme.accent_color, (WIDTH, HEIGHT), (WIDTH, HEIGHT - corner_size), line_width)
        
        music_btns = draw_music_player()
        
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                save_system.save_settings(player_settings)
                pygame.quit()
                sys.exit()
            
            
            if e.type == pygame.KEYDOWN:
                cheat_code.append(e.key)
                # Оставляем только последние 8 нажатий
                if len(cheat_code) > len(CHEAT_SEQUENCE):
                    cheat_code.pop(0)
                
                # Проверяем, совпадает ли код
                if cheat_code == CHEAT_SEQUENCE:
                    activate_cheat()
                    cheat_code.clear()
                    print("🎮 ЧИТ-КОД НА ВСЁ АКТИВИРОВАН!")
            
            # ===== ОБРАБОТКА КНОПОК =====
            for btn in btns:
                if btn.is_clicked(mouse, e):
                    if btn.text == "ИГРАТЬ": 
                        size_menu()
                    elif btn.text == "УРОВНИ": 
                        progress_menu()
                    elif btn.text == "СТАТИСТИКА":
                        show_mode_stats()
                    elif btn.text == "НАСТРОЙКИ": 
                        settings.show_settings(screen, clock, font_mid, font_small, player_settings, save_system)
                    elif btn.text == "ВЫХОД":
                        save_system.save_settings(player_settings)
                        pygame.quit()
                        sys.exit()
            
            # ===== ОБРАБОТКА МУЗЫКАЛЬНОГО ПЛЕЕРА =====
            if music_btns:
                prev, play, next_btn = music_btns
                if prev.collidepoint(mouse) and e.type == pygame.MOUSEBUTTONDOWN:
                    prev_track()
                if play.collidepoint(mouse) and e.type == pygame.MOUSEBUTTONDOWN:
                    toggle_music()
                if next_btn.collidepoint(mouse) and e.type == pygame.MOUSEBUTTONDOWN:
                    next_track()
        
        # ===== ОТРИСОВКА КНОПОК =====
        for btn in btns:
            btn.check_hover(mouse)
            btn.draw(screen)
        
        pygame.display.flip()
        clock.tick(60)


def progress_menu():
    while True:
        draw_bg()
        mouse = pygame.mouse.get_pos()
        theme = get_theme()
        
        center_x = WIDTH // 2
        
        # ===== ЗАГОЛОВОК В РАМКЕ =====
        title_text = "ТВОЙ ПРОГРЕСС"
        
        if theme.name == "Темная":
            title_color = WHITE
            frame_bg_color = DARK_GRAY
        else:
            title_color = theme.text_color
            frame_bg_color = WHITE
        
        title = font_mid.render(title_text, True, title_color)
        
        text_height = title.get_height()
        padding = int(text_height * 0.5)
        
        title_width = title.get_width() + padding * 2
        title_height = text_height + padding * 2
        title_x = center_x - title_width // 2
        title_y = 80
        
        shadow_rect = pygame.Rect(title_x + 3, title_y + 3, title_width, title_height)
        pygame.draw.rect(screen, (50,50,50,100), shadow_rect, border_radius=10)
        
        title_rect = pygame.Rect(title_x, title_y, title_width, title_height)
        pygame.draw.rect(screen, frame_bg_color, title_rect, border_radius=10)
        pygame.draw.rect(screen, theme.accent_color, title_rect, 2, border_radius=10)
        
        title_rect = title.get_rect(center=(center_x, title_y + title_height//2))
        screen.blit(title, title_rect)
        
        # ===== РАМКА ДЛЯ СТАТИСТИКИ =====
        sample_text = font_small.render("3x3: 00/30 уровней", True, theme.text_color)
        text_height = sample_text.get_height()
        padding = int(text_height * 0.5)
        
        frame_width = 900
        frame_height = (text_height + padding) * 4 + padding * 2
        frame_x = center_x - frame_width // 2
        frame_y = title_y + title_height + 25
        
        pygame.draw.rect(screen, theme.button_color, (frame_x, frame_y, frame_width, frame_height), border_radius=12)
        pygame.draw.rect(screen, theme.accent_color, (frame_x, frame_y, frame_width, frame_height), 2, border_radius=12)
        
        inner_x = frame_x + 5
        inner_y = frame_y + 5
        inner_width = frame_width - 10
        inner_height = frame_height - 10
        pygame.draw.rect(screen, theme.bg_color, (inner_x, inner_y, inner_width, inner_height), border_radius=10)
        
        start_y = inner_y + padding
        
        for i, s in enumerate([3,6,9,12]):
            completed = len(level_system.stars[s])
            unlocked = level_system.unlocked_levels[s]  # <-- ЭТА СТРОКА БЫЛА ПРОПУЩЕНА
            stars = level_system.get_total_stars(s)
            
            # Для 12x12 максимальное значение 1, для остальных 30
            if s == 12:
                max_levels = 1
                completed_display = 1 if completed > 0 else 0
                unlocked_display = 1 if unlocked > 0 else 0
            else:
                max_levels = 30
                completed_display = completed
                unlocked_display = unlocked
            
            y = start_y + i * (text_height + padding)
            
            # Размер и количество уровней
            if s == 12:
                size_text = font_small.render(f"{s}x{s}: {completed_display}/{max_levels} уровень", True, theme.text_color)
            else:
                size_text = font_small.render(f"{s}x{s}: {completed_display}/{max_levels} уровней", True, theme.text_color)
            screen.blit(size_text, (inner_x + 50, y))
            
            # Звезды
            star_text = font_emoji_small.render(f"⭐ {stars}", True, theme.accent_color)
            star_rect = star_text.get_rect(center=(center_x, y + text_height//2))
            screen.blit(star_text, star_rect)
            
            # ===== СТАТУС =====
            if s == 12:
                status_emoji = font_emoji_small.render("🔓" if unlocked_display > 0 else "🔒", True, theme.accent_color if unlocked_display > 0 else GRAY)
                status_text = font_small.render(f"{unlocked_display}/1", True, theme.text_color if unlocked_display > 0 else GRAY)
            else:
                status_emoji = font_emoji_small.render("🔓", True, theme.text_color)
                status_text = font_small.render(f"{unlocked_display}/30", True, theme.text_color)
                
            # Позиционирование справа
            status_right_x = inner_x + inner_width - 50
            status_y = y + text_height//2
            
            status_emoji_rect = status_emoji.get_rect(midright=(status_right_x - 40, status_y))
            screen.blit(status_emoji, status_emoji_rect)
            
            status_text_rect = status_text.get_rect(midleft=(status_right_x - 30, status_y))
            screen.blit(status_text, status_text_rect)
        
        # ===== ОБЩЕЕ КОЛИЧЕСТВО ЗВЕЗД =====
        total_stars = level_system.get_total_stars()
        
        total_frame_width = 400
        total_frame_height = 50
        total_frame_x = center_x - total_frame_width // 2
        total_frame_y = frame_y + frame_height + 25
        
        pygame.draw.rect(screen, theme.button_color, (total_frame_x, total_frame_y, total_frame_width, total_frame_height), border_radius=10)
        pygame.draw.rect(screen, theme.accent_color, (total_frame_x, total_frame_y, total_frame_width, total_frame_height), 2, border_radius=10)
        
        # Звезда и текст
        star_symbol = font_emoji_small.render("⭐", True, theme.accent_color)
        total_text = font_small.render(f"ВСЕГО ЗВЕЗД: {total_stars}", True, theme.accent_color)
        
        total_width = star_symbol.get_width() + 10 + total_text.get_width()
        start_x = center_x - total_width // 2
        text_y = total_frame_y + 15
        
        screen.blit(star_symbol, (start_x, text_y))
        screen.blit(total_text, (start_x + star_symbol.get_width() + 10, text_y))
        
        # ===== КНОПКА НОВАЯ ИГРА =====
        reset_btn = pygame.Rect(center_x - 200, total_frame_y + 70, 400, 70)
        pygame.draw.rect(screen, RED, reset_btn, border_radius=15)
        pygame.draw.rect(screen, WHITE, reset_btn, 3, border_radius=15)
        
        reset_emoji = font_emoji_small.render("🔄", True, WHITE)
        reset_text = font_small.render("НОВАЯ ИГРА", True, WHITE)
        
        total_width = reset_emoji.get_width() + 15 + reset_text.get_width()
        start_x = center_x - total_width // 2
        text_y = reset_btn.y + reset_btn.height//2 - reset_text.get_height()//2
        
        screen.blit(reset_emoji, (start_x, text_y))
        screen.blit(reset_text, (start_x + reset_emoji.get_width() + 15, text_y))
        
        # ===== КНОПКА НАЗАД =====
        back_btn = pygame.Rect(center_x - 200, reset_btn.y + 85, 400, 70)
        pygame.draw.rect(screen, GRAY, back_btn, border_radius=15)
        pygame.draw.rect(screen, DARK_GRAY, back_btn, 3, border_radius=15)
        back_text = font_small.render("НАЗАД", True, WHITE)
        back_text_rect = back_text.get_rect(center=back_btn.center)
        screen.blit(back_text, back_text_rect)
        
        music_btns = draw_music_player()
        
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if e.type == pygame.MOUSEBUTTONDOWN:
                if reset_btn.collidepoint(e.pos):
                    level_system.reset_progress()
                    return
                if back_btn.collidepoint(e.pos):
                    return
            
            if music_btns:
                prev, play, next_btn = music_btns
                if prev.collidepoint(mouse) and e.type == pygame.MOUSEBUTTONDOWN:
                    prev_track()
                if play.collidepoint(mouse) and e.type == pygame.MOUSEBUTTONDOWN:
                    toggle_music()
                if next_btn.collidepoint(mouse) and e.type == pygame.MOUSEBUTTONDOWN:
                    next_track()
        
        pygame.display.flip()
        clock.tick(60)
        
def size_menu():
    center_x = WIDTH // 2
    btn_width = 220
    btn_height = 80
    
    center_btn_x = center_x - btn_width // 2
    left_center_x = center_x // 2 - btn_width // 2
    right_center_x = center_x + (center_x // 2) - btn_width // 2
    
    while True:
        draw_bg()
        mouse = pygame.mouse.get_pos()
        theme = get_theme()
        
        # Заголовок
        title_text = "ВЫБЕРИ ПОЛЕ"
        title = font_mid.render(title_text, True, theme.accent_color)
        
        title_padding = 40
        title_width = title.get_width() + title_padding * 2
        title_height = title.get_height() + title_padding
        title_x = center_x - title_width // 2
        title_y = 40
        
        shadow_rect = pygame.Rect(title_x + 4, title_y + 4, title_width, title_height)
        pygame.draw.rect(screen, (50,50,50,150), shadow_rect, border_radius=20)
        
        title_rect = pygame.Rect(title_x, title_y, title_width, title_height)
        pygame.draw.rect(screen, theme.button_color, title_rect, border_radius=20)
        pygame.draw.rect(screen, theme.accent_color, title_rect, 4, border_radius=20)
        
        title_rect = title.get_rect(center=(center_x, title_y + title_height//2))
        screen.blit(title, title_rect)
        
        # Кнопки полей
        btns = [
            Button(left_center_x, 230, btn_width, btn_height, "3x3", theme.button_color, theme.button_hover, 54),
            Button(center_btn_x, 230, btn_width, btn_height, "6x6", theme.button_color, theme.button_hover, 54),
            Button(right_center_x, 230, btn_width, btn_height, "9x9", theme.button_color, theme.button_hover, 54),
        ]
        
        back_btn = Button(center_btn_x, 570, btn_width, btn_height, "НАЗАД", GRAY, DARK_GRAY, 54)
        
        # Бонусный уровень 12x12
        btn_12x12 = None
        if level_system.is_bonus_unlocked():
            btn_12x12 = Button(center_btn_x, 130, btn_width, btn_height, "12x12", GOLD, (255,215,0), 54)
        
        # Статистика под кнопками
        stats_y = 370
        stats_width = btn_width
        stats_height = 70
        
        # Статистика для 3x3
        stats_3x3_x = left_center_x
        stats_3x3_rect = pygame.Rect(stats_3x3_x, stats_y, stats_width, stats_height)
        pygame.draw.rect(screen, theme.button_color, stats_3x3_rect, border_radius=12)
        pygame.draw.rect(screen, theme.accent_color, stats_3x3_rect, 2, border_radius=12)
        
        stats_3x3 = font_tiny.render(f"{len(level_system.stars[3])}/30", True, WHITE)
        stats_3x3_rect = stats_3x3.get_rect(midleft=(stats_3x3_x + 15, stats_y + 20))
        screen.blit(stats_3x3, stats_3x3_rect)
        
        stars_3x3 = font_emoji_small.render(f"⭐{level_system.get_total_stars(3)}", True, WHITE)
        stars_3x3_rect = stars_3x3.get_rect(midright=(stats_3x3_x + stats_width - 15, stats_y + 45))
        screen.blit(stars_3x3, stars_3x3_rect)
        
        # Статистика для 6x6
        stats_6x6_x = center_btn_x
        stats_6x6_rect = pygame.Rect(stats_6x6_x, stats_y, stats_width, stats_height)
        pygame.draw.rect(screen, theme.button_color, stats_6x6_rect, border_radius=12)
        pygame.draw.rect(screen, theme.accent_color, stats_6x6_rect, 2, border_radius=12)
        
        stats_6x6 = font_tiny.render(f"{len(level_system.stars[6])}/30", True, WHITE)
        stats_6x6_rect = stats_6x6.get_rect(midleft=(stats_6x6_x + 15, stats_y + 20))
        screen.blit(stats_6x6, stats_6x6_rect)
        
        stars_6x6 = font_emoji_small.render(f"⭐{level_system.get_total_stars(6)}", True, WHITE)
        stars_6x6_rect = stars_6x6.get_rect(midright=(stats_6x6_x + stats_width - 15, stats_y + 45))
        screen.blit(stars_6x6, stars_6x6_rect)
        
        # Статистика для 9x9
        stats_9x9_x = right_center_x
        stats_9x9_rect = pygame.Rect(stats_9x9_x, stats_y, stats_width, stats_height)
        pygame.draw.rect(screen, theme.button_color, stats_9x9_rect, border_radius=12)
        pygame.draw.rect(screen, theme.accent_color, stats_9x9_rect, 2, border_radius=12)
        
        stats_9x9 = font_tiny.render(f"{len(level_system.stars[9])}/30", True, WHITE)
        stats_9x9_rect = stats_9x9.get_rect(midleft=(stats_9x9_x + 15, stats_y + 20))
        screen.blit(stats_9x9, stats_9x9_rect)
        
        stars_9x9 = font_emoji_small.render(f"⭐{level_system.get_total_stars(9)}", True, WHITE)
        stars_9x9_rect = stars_9x9.get_rect(midright=(stats_9x9_x + stats_width - 15, stats_y + 45))
        screen.blit(stars_9x9, stars_9x9_rect)
        
        # Статистика для 12x12 если доступен
        if level_system.is_bonus_unlocked():
            stats_12x12_x = center_btn_x
            stats_12x12_rect = pygame.Rect(stats_12x12_x, 460, stats_width, stats_height)
            pygame.draw.rect(screen, GOLD, stats_12x12_rect, border_radius=12)
            pygame.draw.rect(screen, theme.accent_color, stats_12x12_rect, 2, border_radius=12)
            
            # Для 12x12 показываем 0/1 или 1/1
            completed = 1 if len(level_system.stars[12]) > 0 else 0
            stats_12x12 = font_tiny.render(f"{completed}/1", True, BLACK)
            stats_12x12_rect = stats_12x12.get_rect(midleft=(stats_12x12_x + 15, 480))
            screen.blit(stats_12x12, stats_12x12_rect)
            
            stars_12x12 = font_emoji_small.render(f"⭐{level_system.get_total_stars(12)}", True, BLACK)
            stars_12x12_rect = stars_12x12.get_rect(midright=(stats_12x12_x + stats_width - 15, 505))
            screen.blit(stars_12x12, stars_12x12_rect)
        
        music_btns = draw_music_player()
        
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            for btn in btns:
                if btn.is_clicked(mouse, e):
                    if btn.text == "3x3": 
                        level_select(3)
                        return
                    elif btn.text == "6x6": 
                        level_select(6)
                        return
                    elif btn.text == "9x9": 
                        level_select(9)
                        return
            if btn_12x12 and btn_12x12.is_clicked(mouse, e):
                start_game(12, 1)
                return
            if back_btn.is_clicked(mouse, e):
                return
            
            if music_btns:
                prev, play, next_btn = music_btns
                if prev.collidepoint(mouse) and e.type == pygame.MOUSEBUTTONDOWN:
                    prev_track()
                if play.collidepoint(mouse) and e.type == pygame.MOUSEBUTTONDOWN:
                    toggle_music()
                if next_btn.collidepoint(mouse) and e.type == pygame.MOUSEBUTTONDOWN:
                    next_track()
        
        for btn in btns:
            btn.check_hover(mouse)
            btn.draw(screen)
        if btn_12x12:
            btn_12x12.check_hover(mouse)
            btn_12x12.draw(screen)
        back_btn.check_hover(mouse)
        back_btn.draw(screen)
        pygame.display.flip()
        clock.tick(60)

def level_select(size):
    if size == 12:
        # Для 12x12 сразу запускаем игру (только 1 уровень)
        start_game(12, 1)
        return
    
    unlocked = level_system.unlocked_levels[size]
    
    while True:
        draw_bg()
        mouse = pygame.mouse.get_pos()
        theme = get_theme()
        
        btns = []
        start_x = 350
        start_y = 250
        for i in range(30):
            r, c = i//6, i%6
            x = start_x + c * 90
            y = start_y + r * 80
            if i+1 <= unlocked:
                stars = level_system.stars[size].get(i+1, 0)
                if stars == 3: color = GOLD
                elif stars == 2: color = SILVER
                elif stars == 1: color = BRONZE
                else: color = theme.button_color
                hc = theme.button_hover
            else:
                color = GRAY
                hc = DARK_GRAY
            btns.append(Button(x, y, 70, 60, str(i+1), color, hc, 40))
        
        back = Button(500, 750, 200, 60, "НАЗАД", GRAY, DARK_GRAY, 48)
        
        # Заголовок
        title_text = f"УРОВНИ {size}x{size}"
        title = font_big.render(title_text, True, theme.accent_color)
        title_rect = title.get_rect(center=(WIDTH//2, 80))
        screen.blit(title, title_rect)
        
        # Информация о звездах
        stars_total = level_system.get_total_stars(size)
        big_font = pygame.font.Font(None, 38)
        
        star = font_emoji.render("⭐", True, GOLD)
        text1 = big_font.render("Звёзд:", True, theme.text_color)
        text2 = big_font.render(f"{stars_total}/90", True, theme.accent_color)
        
        total_width = star.get_width() + text1.get_width() + text2.get_width() + 10
        start_x = 1150 - total_width
        
        screen.blit(star, (start_x, 120))
        screen.blit(text1, (start_x + star.get_width() + 5, 126))
        screen.blit(text2, (start_x + star.get_width() + text1.get_width() + 10, 126))
        
        music_btns = draw_music_player()
        
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            for i, btn in enumerate(btns):
                if btn.is_clicked(mouse, e) and i+1 <= unlocked:
                    start_game(size, i+1)
                    return
            if back.is_clicked(mouse, e): 
                return
            
            if music_btns:
                prev, play, next_btn = music_btns
                if prev.collidepoint(mouse) and e.type == pygame.MOUSEBUTTONDOWN:
                    prev_track()
                if play.collidepoint(mouse) and e.type == pygame.MOUSEBUTTONDOWN:
                    toggle_music()
                if next_btn.collidepoint(mouse) and e.type == pygame.MOUSEBUTTONDOWN:
                    next_track()
        
        for btn in btns + [back]:
            btn.check_hover(mouse)
            btn.draw(screen)
        pygame.display.flip()
        clock.tick(60)

def start_game(size, level):
    # Получаем режим игры из настроек
    game_mode = player_settings.get('mode', 'trial')
    
    # Создаем игру и передаем ей режим
    game = Game(size, level, show_rules=False, emoji_font=font_emoji)
    game.game_mode = game_mode  # Передаем режим в игру
    
    timer_paused = False
    paused_time = 0
    game_started = False
    
    # Проверяем режим
    if game_mode == 'study':
        # Режим изучения - таймер не нужен, сразу показываем победу при решении
        print("📚 Режим изучения - таймер отключен")
        game_started = True
        # В режиме изучения не создаем start_time
    else:
        # Для trial и tournament - таймер нужен
        if player_settings['experience'] == 'novice' and not hasattr(start_game, 'rules_shown'):
            # Показываем правила для новичка
            timer_paused = True
            game.show_rules_popup(screen, font_mid)
            setattr(start_game, 'rules_shown', True)
            game.start_time = time.time()
            timer_paused = False
            game_started = True
            print(f"⚡ {game_mode} режим - таймер запущен после правил")
        else:
            game.start_time = time.time()
            game_started = True
            print(f"⚡ {game_mode} режим - таймер запущен")
    
    victory_timer = None
    victory_delay = 0.5
    last_check_time = 0
    check_interval = 0.5
    
    game_completed = False
    
    while True:
        theme = get_theme()
        back, rules, check = game.draw(screen, font_mid)
        mouse = pygame.mouse.get_pos()
        
        music_btns = draw_music_player()
        
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if e.type == pygame.MOUSEBUTTONDOWN:
                if not game.handle_click(mouse):
                    if back.collidepoint(mouse): 
                        return
                    if rules.collidepoint(mouse):
                        if game_mode != 'study' and game_started and not timer_paused and hasattr(game, 'start_time'):
                            paused_time = time.time() - game.start_time
                            timer_paused = True
                            print(f"⏸️ Таймер на паузе: {paused_time:.2f} сек")
                        
                        game.show_rules_popup(screen, font_mid)
                        
                        if game_mode != 'study' and game_started and hasattr(game, 'start_time') and timer_paused:
                            game.start_time = time.time() - paused_time
                            timer_paused = False
                            print(f"▶️ Таймер возобновлен: {paused_time:.2f} сек")
                        
                    if check.collidepoint(mouse): 
                        game.check_mode = not game.check_mode
                        if game.check_mode:
                            game.check_board()
                        else:
                            game.highlight_cells.clear()
                            victory_timer = None
            
            if e.type == pygame.KEYDOWN and game.selected and game_started:
                if e.key in [pygame.K_1, pygame.K_KP1]: game.place_number(1)
                elif e.key in [pygame.K_2, pygame.K_KP2]: game.place_number(2)
                elif e.key in [pygame.K_3, pygame.K_KP3]: game.place_number(3)
                elif e.key in [pygame.K_4, pygame.K_KP4]: game.place_number(4)
                elif e.key in [pygame.K_5, pygame.K_KP5]: game.place_number(5)
                elif e.key in [pygame.K_6, pygame.K_KP6]: game.place_number(6)
                elif e.key in [pygame.K_7, pygame.K_KP7]: game.place_number(7) if size > 6 else None
                elif e.key in [pygame.K_8, pygame.K_KP8]: game.place_number(8) if size > 6 else None
                elif e.key in [pygame.K_9, pygame.K_KP9]: game.place_number(9) if size > 6 else None
                # Для 12x12 - поддержка 10, 11, 12 через комбинации
                elif size == 12:
                    if e.key == pygame.K_0:  # 0 = 10
                        game.place_number(10)
                    elif e.key == pygame.K_MINUS:  # - = 11
                        game.place_number(11)
                    elif e.key == pygame.K_EQUALS:  # = = 12
                        game.place_number(12)
                elif e.key in [pygame.K_DELETE, pygame.K_BACKSPACE]:
                    game.delete_number()
                victory_timer = None
            
            if music_btns:
                prev, play, next_btn = music_btns
                if prev.collidepoint(mouse) and e.type == pygame.MOUSEBUTTONDOWN:
                    prev_track()
                if play.collidepoint(mouse) and e.type == pygame.MOUSEBUTTONDOWN:
                    toggle_music()
                if next_btn.collidepoint(mouse) and e.type == pygame.MOUSEBUTTONDOWN:
                    next_track()
        
        # Проверяем состояние игры
        current_time = time.time()
        if game_started and not timer_paused and current_time - last_check_time > check_interval:
            last_check_time = current_time
            
            # Проверяем победу (для всех режимов)
            if game.check_victory_condition():
                print(f"✅ Условие победы выполнено! Поле заполнено правильно")
                if victory_timer is None:
                    victory_timer = time.time()
                    print(f"🎉 Таймер победы запущен: {victory_timer}")
                elif time.time() - victory_timer >= victory_delay:
                    print(f"🎊 ПОБЕДА! Прошло {time.time() - victory_timer:.2f} сек")
                    # Победа!
                    if game_mode == 'study':
                        game.stars = 3
                        win_message = "ПОБЕДА! +3 ⭐"
                        elapsed = 0
                    elif game_mode == 'tournament':
                        elapsed = time.time() - game.start_time
                        base_stars = game.calculate_stars(elapsed)
                        game.stars = min(base_stars * 2, 3)
                        win_message = f"ТУРНИРНАЯ ПОБЕДА! +{game.stars} ⭐⭐"
                    else:  # trial
                        elapsed = time.time() - game.start_time
                        game.stars = game.calculate_stars(elapsed)
                        win_message = f"ПОБЕДА! {game.stars} ⭐"
                    
                    # Для 12x12 после победы показываем титры
                    if size == 12 and game.stars > 0:
                        # Отмечаем, что бонусный уровень пройден
                        if 12 not in level_system.stars or level_system.stars[12].get(1, 0) < game.stars:
                            level_system.complete_level(size, level, game.stars, game_mode, elapsed)
                        
                        # Показываем титры
                        show_credits(screen, font_big, font_mid, font_small, theme)
                        return
                    
                    # Передаем время в функцию победы
                    show_victory_screen(size, level, game.stars, win_message, game_mode, elapsed)
                    return
                else:
                    print(f"⏳ Ожидание победы: {time.time() - victory_timer:.2f}/{victory_delay}")
            else:
                if victory_timer is not None:
                    print("❌ Условие победы нарушено, сброс таймера")
                    victory_timer = None
            
            # Проверяем поражение (только для trial и tournament)
            if game_mode != 'study' and hasattr(game, 'start_time'):
                elapsed = time.time() - game.start_time
                if game.check_defeat_condition(elapsed):
                    print(f"💀 Поражение! Время вышло: {elapsed:.1f} сек")
                    show_defeat_screen(size, level)
                    return
        
        pygame.display.flip()
        clock.tick(60)

def show_victory_screen(size, level, stars, message, game_mode, elapsed):
    """Показывает экран победы"""
    theme = get_theme()
    
    # Затемнение
    s = pygame.Surface((WIDTH, HEIGHT))
    s.set_alpha(180)
    s.fill(BLACK)
    screen.blit(s, (0,0))
    
    # Белое окно
    window_width, window_height = 550, 420
    window_x = (WIDTH - window_width) // 2
    window_y = (HEIGHT - window_height) // 2
    
    pygame.draw.rect(screen, WHITE, (window_x, window_y, window_width, window_height), border_radius=15)
    pygame.draw.rect(screen, GOLD, (window_x, window_y, window_width, window_height), 4, border_radius=15)
    
    # Сообщение о победе
    win_text = font_big.render("ПОБЕДА!", True, GOLD)
    win_rect = win_text.get_rect(center=(WIDTH//2, window_y + 60))
    screen.blit(win_text, win_rect)
    
    # Звезды
    star_text = font_emoji_big.render("⭐" * stars, True, GOLD)
    star_rect = star_text.get_rect(center=(WIDTH//2, window_y + 120))
    screen.blit(star_text, star_rect)
    
    # Время (если не режим изучения)
    if game_mode != 'study':
        time_text = font_small.render(f"Время: {elapsed:.1f} сек", True, DARK_BLUE)
        time_rect = time_text.get_rect(center=(WIDTH//2, window_y + 170))
        screen.blit(time_text, time_rect)
        next_level_y = 230
        restart_y = 290
        menu_y = 350
    else:
        next_level_y = 200
        restart_y = 260
        menu_y = 320
    
    # Кнопки
    next_level = level + 1 if level < 30 else 1
    
    # Кнопка "УРОВЕНЬ 2"
    continue_btn = pygame.Rect(WIDTH//2 - 150, window_y + next_level_y, 300, 50)
    pygame.draw.rect(screen, theme.button_color, continue_btn, border_radius=12)
    pygame.draw.rect(screen, WHITE, continue_btn, 3, border_radius=12)
    continue_text = font_mid.render(f"УРОВЕНЬ {next_level}", True, WHITE)
    continue_rect = continue_text.get_rect(center=continue_btn.center)
    screen.blit(continue_text, continue_rect)
    
    # Кнопка "ЗАНОВО"
    restart_btn = pygame.Rect(WIDTH//2 - 150, window_y + restart_y, 300, 50)
    pygame.draw.rect(screen, theme.button_color, restart_btn, border_radius=12)
    pygame.draw.rect(screen, WHITE, restart_btn, 3, border_radius=12)
    restart_text = font_mid.render("ЗАНОВО", True, WHITE)
    restart_rect = restart_text.get_rect(center=restart_btn.center)
    screen.blit(restart_text, restart_rect)
    
    # Кнопка "В МЕНЮ"
    menu_btn = pygame.Rect(WIDTH//2 - 150, window_y + menu_y, 300, 50)
    pygame.draw.rect(screen, GRAY, menu_btn, border_radius=12)
    pygame.draw.rect(screen, WHITE, menu_btn, 3, border_radius=12)
    menu_text = font_mid.render("В МЕНЮ", True, WHITE)
    menu_rect = menu_text.get_rect(center=menu_btn.center)
    screen.blit(menu_text, menu_rect)
    
    pygame.display.flip()
    
    play_victory_sound()
    
    # Сохраняем прогресс и статистику
    if game_mode == 'study':
        level_system.complete_level(size, level, stars, game_mode)
    else:
        level_system.complete_level(size, level, stars, game_mode, elapsed)
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if continue_btn.collidepoint(event.pos):
                    waiting = False
                    if level < 30:
                        start_game(size, level + 1)
                    else:
                        return
                if restart_btn.collidepoint(event.pos):
                    waiting = False
                    start_game(size, level)
                if menu_btn.collidepoint(event.pos):
                    waiting = False
                    return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    waiting = False
                    if level < 30:
                        start_game(size, level + 1)
                    else:
                        return

def show_defeat_screen(size, level):
    """Показывает экран поражения"""
    theme = get_theme()
    
    # Затемнение
    s = pygame.Surface((WIDTH, HEIGHT))
    s.set_alpha(180)
    s.fill(BLACK)
    screen.blit(s, (0,0))
    
    # Красное окно
    window_width, window_height = 400, 250
    window_x = (WIDTH - window_width) // 2
    window_y = (HEIGHT - window_height) // 2
    
    pygame.draw.rect(screen, WHITE, (window_x, window_y, window_width, window_height), border_radius=15)
    pygame.draw.rect(screen, RED, (window_x, window_y, window_width, window_height), 4, border_radius=15)
    
    # Сообщение о поражении
    defeat_text = font_big.render("ПОРАЖЕНИЕ!", True, RED)
    defeat_rect = defeat_text.get_rect(center=(WIDTH//2, window_y + 80))
    screen.blit(defeat_text, defeat_rect)
    
    # Пояснение
    info_text = font_small.render("Время вышло...", True, BLACK)
    info_rect = info_text.get_rect(center=(WIDTH//2, window_y + 140))
    screen.blit(info_text, info_rect)
    
    # Кнопка заново
    restart_btn = pygame.Rect(WIDTH//2 - 100, window_y + 180, 200, 50)
    pygame.draw.rect(screen, RED, restart_btn, border_radius=10)
    pygame.draw.rect(screen, WHITE, restart_btn, 3, border_radius=10)
    restart_text = font_small.render("ЗАНОВО", True, WHITE)
    restart_rect = restart_text.get_rect(center=restart_btn.center)
    screen.blit(restart_text, restart_rect)
    
    pygame.display.flip()
    
    play_defeat_sound()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if restart_btn.collidepoint(event.pos):
                    waiting = False
                    start_game(size, level)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    waiting = False
                    start_game(size, level)

def show_credits(screen, font_big, font_mid, font_small, theme):
    """Показывает титры после прохождения игры"""
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(200)
    overlay.fill(BLACK)
    screen.blit(overlay, (0,0))
    
    # Белое окно для титров
    credit_width = 700
    credit_height = 450  # Чуть уменьшил высоту
    credit_x = (WIDTH - credit_width) // 2
    credit_y = (HEIGHT - credit_height) // 2 - 30  # Поднял выше, чтобы освободить место для кнопки
    
    pygame.draw.rect(screen, WHITE, (credit_x, credit_y, credit_width, credit_height), border_radius=20)
    pygame.draw.rect(screen, GOLD, (credit_x, credit_y, credit_width, credit_height), 5, border_radius=20)
    
    # Заголовок
    title = font_big.render("СПАСИБО ЗА ИГРУ!", True, DARK_BLUE)
    title_rect = title.get_rect(center=(WIDTH//2, credit_y + 60))
    screen.blit(title, title_rect)
    
    # Основной текст
    line1 = font_mid.render("Над проектом работали", True, BLACK)
    line1_rect = line1.get_rect(center=(WIDTH//2, credit_y + 130))
    screen.blit(line1, line1_rect)

    line2 = font_small.render("ученики 9Г класса:", True, GRAY)
    line2_rect = line2.get_rect(center=(WIDTH//2, credit_y + 180))
    screen.blit(line2, line2_rect)
    
    line3 = font_mid.render("Бортников А.С.", True, DARK_BLUE)
    line3_rect = line3.get_rect(center=(WIDTH//2, credit_y + 230))
    screen.blit(line3, line3_rect)
    
    line4 = font_mid.render("Ломтев А.И.", True, DARK_BLUE)
    line4_rect = line4.get_rect(center=(WIDTH//2, credit_y + 280))
    screen.blit(line4, line4_rect)

    # Звезды
    stars_text = font_emoji_big.render("⭐⭐⭐⭐⭐", True, GOLD)
    stars_rect = stars_text.get_rect(center=(WIDTH//2, credit_y + 340))
    screen.blit(stars_text, stars_rect)
    
    # ===== ОТДЕЛЬНАЯ РАМКА ДЛЯ КНОПКИ =====
    button_width = 220
    button_height = 60
    button_x = WIDTH//2 - button_width//2
    button_y = credit_y + credit_height + 20  # 20 пикселей отступа от основной рамки
    
    # Рамка для кнопки
    pygame.draw.rect(screen, DARK_BLUE, (button_x, button_y, button_width, button_height), border_radius=15)
    pygame.draw.rect(screen, GOLD, (button_x, button_y, button_width, button_height), 3, border_radius=15)
    
    # Текст кнопки
    exit_text = font_small.render("В МЕНЮ", True, WHITE)
    exit_rect = exit_text.get_rect(center=(button_x + button_width//2, button_y + button_height//2))
    screen.blit(exit_text, exit_rect)
    
    pygame.display.flip()
    
    # Ждем нажатия
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Проверяем клик по кнопке
                if button_x <= event.pos[0] <= button_x + button_width and \
                   button_y <= event.pos[1] <= button_y + button_height:
                    waiting = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN or event.key == pygame.K_ESCAPE:
                    waiting = False

def show_mode_stats():
    """Показывает статистику по режимам"""
    while True:
        draw_bg()
        mouse = pygame.mouse.get_pos()
        theme = get_theme()
        
        center_x = WIDTH // 2
        
        # ===== ЗАГОЛОВОК В РАМКЕ =====
        title_text = "СТАТИСТИКА РЕЖИМОВ"
        
        if theme.name == "Темная":
            title_color = WHITE
            frame_bg_color = DARK_GRAY
        else:
            title_color = theme.text_color
            frame_bg_color = WHITE
        
        title = font_mid.render(title_text, True, title_color)
        
        text_height = title.get_height()
        padding = int(text_height * 0.5)
        
        title_width = title.get_width() + padding * 2
        title_height = text_height + padding * 2
        title_x = center_x - title_width // 2
        title_y = 40
        
        shadow_rect = pygame.Rect(title_x + 3, title_y + 3, title_width, title_height)
        pygame.draw.rect(screen, (50,50,50,100), shadow_rect, border_radius=10)
        
        title_rect = pygame.Rect(title_x, title_y, title_width, title_height)
        pygame.draw.rect(screen, frame_bg_color, title_rect, border_radius=10)
        pygame.draw.rect(screen, theme.accent_color, title_rect, 2, border_radius=10)
        
        title_rect = title.get_rect(center=(center_x, title_y + title_height//2))
        screen.blit(title, title_rect)
        
        # ===== РАМКА =====
        frame_width = 950
        frame_height = 430  # Уменьшил высоту
        frame_x = center_x - frame_width // 2
        frame_y = title_y + title_height + 25
        
        pygame.draw.rect(screen, theme.button_color, (frame_x, frame_y, frame_width, frame_height), border_radius=15)
        pygame.draw.rect(screen, theme.accent_color, (frame_x, frame_y, frame_width, frame_height), 3, border_radius=15)
        
        inner_x = frame_x + 25
        inner_y = frame_y + 25
        inner_width = frame_width - 50
        inner_height = frame_height - 50
        
        # ===== ШАПКА ТАБЛИЦЫ =====
        study_col_x = inner_x + 230
        trial_col_x = inner_x + 470
        tour_col_x = inner_x + 710
        
        study_title_surf = font_tiny.render("ИЗУЧЕНИЕ", True, (100, 150, 255))
        trial_title_surf = font_tiny.render("ИСПЫТАТЕЛЬНЫЙ", True, (255, 200, 50))
        tour_title_surf = font_tiny.render("ТУРНИРНЫЙ", True, (255, 100, 100))
        
        header_y = inner_y + 10
        
        study_title_rect = study_title_surf.get_rect(center=(study_col_x, header_y))
        trial_title_rect = trial_title_surf.get_rect(center=(trial_col_x, header_y))
        tour_title_rect = tour_title_surf.get_rect(center=(tour_col_x, header_y))
        
        screen.blit(study_title_surf, study_title_rect)
        screen.blit(trial_title_surf, trial_title_rect)
        screen.blit(tour_title_surf, tour_title_rect)
        
        header_line_y = header_y + 15
        pygame.draw.line(screen, theme.accent_color, (inner_x, header_line_y), (inner_x + inner_width, header_line_y), 2)
        
        # ===== СТАТИСТИКА =====
        start_y = header_line_y + 15
        row_height = 55
        
        study_stats = level_system.mode_stats.get('study', {'games': 0, 'wins': 0})
        trial_stats = level_system.mode_stats.get('trial', {'games': 0, 'wins': 0, 'best_time': None, 'total_stars': 0, 'best_stars': 0})
        tour_stats = level_system.mode_stats.get('tournament', {'games': 0, 'wins': 0, 'best_time': None, 'total_stars': 0, 'best_stars': 0})
        
        label_x = inner_x
        
        study_pct = (study_stats.get('wins', 0) / study_stats.get('games', 1) * 100) if study_stats.get('games', 0) > 0 else 0
        trial_pct = (trial_stats.get('wins', 0) / trial_stats.get('games', 1) * 100) if trial_stats.get('games', 0) > 0 else 0
        tour_pct = (tour_stats.get('wins', 0) / tour_stats.get('games', 1) * 100) if tour_stats.get('games', 0) > 0 else 0
        
        rows = [
            {'label': "Игр сыграно:", 'study': str(study_stats.get('games', 0)), 'trial': str(trial_stats.get('games', 0)), 'tour': str(tour_stats.get('games', 0)), 'type': 'number'},
            {'label': "Побед:", 'study': str(study_stats.get('wins', 0)), 'trial': str(trial_stats.get('wins', 0)), 'tour': str(tour_stats.get('wins', 0)), 'type': 'number'},
            {'label': "Процент побед:", 'study': f"{study_pct:.1f}%", 'trial': f"{trial_pct:.1f}%", 'tour': f"{tour_pct:.1f}%", 'type': 'percent'},
            {'label': "Лучшее время:", 'study': "—", 'trial': f"{trial_stats.get('best_time', 0):.1f}с" if trial_stats.get('best_time') else "—", 'tour': f"{tour_stats.get('best_time', 0):.1f}с" if tour_stats.get('best_time') else "—", 'type': 'time'},
            {'label': "Всего звезд:", 'study': "—", 'trial': f"⭐ {trial_stats.get('total_stars', 0)}" if trial_stats.get('total_stars', 0) > 0 else "—", 'tour': f"⭐ {tour_stats.get('total_stars', 0)}" if tour_stats.get('total_stars', 0) > 0 else "—", 'type': 'stars'},
            {'label': "Лучший результат:", 'study': "—", 'trial': f"⭐ {trial_stats.get('best_stars', 0)}" if trial_stats.get('best_stars', 0) > 0 else "—", 'tour': f"⭐ {tour_stats.get('best_stars', 0)}" if tour_stats.get('best_stars', 0) > 0 else "—", 'type': 'stars'}
        ]
        
        for i, row in enumerate(rows):
            row_center_y = start_y + i * row_height + row_height // 2
            
            if i > 0:
                line_y = start_y + i * row_height
                pygame.draw.line(screen, theme.accent_color, (inner_x + 20, line_y), (inner_x + inner_width - 20, line_y), 1)
            
            label_surf = font_tiny.render(row['label'], True, theme.text_color)
            label_rect = label_surf.get_rect(midleft=(label_x, row_center_y))
            screen.blit(label_surf, label_rect)
            
            if row['study'] != "—":
                study_surf = font_tiny.render(row['study'], True, theme.accent_color)
            else:
                study_surf = font_tiny.render(row['study'], True, theme.text_color)
            study_rect = study_surf.get_rect(center=(study_col_x, row_center_y))
            screen.blit(study_surf, study_rect)
            
            if row['type'] == 'stars' and row['trial'] != "—":
                trial_surf = font_emoji_small.render(row['trial'], True, GOLD)
            elif row['trial'] != "—":
                trial_surf = font_tiny.render(row['trial'], True, theme.accent_color)
            else:
                trial_surf = font_tiny.render(row['trial'], True, theme.text_color)
            trial_rect = trial_surf.get_rect(center=(trial_col_x, row_center_y))
            screen.blit(trial_surf, trial_rect)
            
            if row['type'] == 'stars' and row['tour'] != "—":
                tour_surf = font_emoji_small.render(row['tour'], True, GOLD)
            elif row['tour'] != "—":
                tour_surf = font_tiny.render(row['tour'], True, theme.accent_color)
            else:
                tour_surf = font_tiny.render(row['tour'], True, theme.text_color)
            tour_rect = tour_surf.get_rect(center=(tour_col_x, row_center_y))
            screen.blit(tour_surf, tour_rect)
        
        # ===== КНОПКА НАЗАД (ПОДНЯТА) =====
        back_btn = pygame.Rect(center_x - 100, frame_y + frame_height + 5, 200, 60)
        pygame.draw.rect(screen, GRAY, back_btn, border_radius=15)
        pygame.draw.rect(screen, DARK_GRAY, back_btn, 3, border_radius=15)
        back_text = font_small.render("НАЗАД", True, WHITE)
        back_rect = back_text.get_rect(center=back_btn.center)
        screen.blit(back_text, back_rect)
        
        music_btns = draw_music_player()
        
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if e.type == pygame.MOUSEBUTTONDOWN:
                if back_btn.collidepoint(e.pos):
                    return
                
                if music_btns:
                    prev, play, next_btn = music_btns
                    if prev.collidepoint(e.pos):
                        prev_track()
                    if play.collidepoint(e.pos):
                        toggle_music()
                    if next_btn.collidepoint(e.pos):
                        next_track()
        
        pygame.display.flip()
        clock.tick(60)

# ===== ФУНКЦИЯ УВЕДОМЛЕНИЯ (ОПРЕДЕЛЯЕМ ПЕРВОЙ) =====
def show_cheat_notification():
    """Показывает уведомление об активации чита"""
    theme = get_theme()
    
    s = pygame.Surface((WIDTH, HEIGHT))
    s.set_alpha(180)
    s.fill(BLACK)
    screen.blit(s, (0,0))
    
    # Окно
    window_width, window_height = 600, 380
    window_x = (WIDTH - window_width) // 2
    window_y = (HEIGHT - window_height) // 2
    
    pygame.draw.rect(screen, WHITE, (window_x, window_y, window_width, window_height), border_radius=15)
    pygame.draw.rect(screen, (200, 150, 255), (window_x, window_y, window_width, window_height), 4, border_radius=15)
    
    # Заголовок (обычный шрифт)
    title = font_mid.render("ЧИТ-КОД АКТИВИРОВАН!", True, (200, 150, 255))
    title_rect = title.get_rect(center=(WIDTH//2, window_y + 50))
    screen.blit(title, title_rect)
    
    # Код VINDIGO4 (обычный шрифт, крупно)
    code = font_big.render("VINDIGO4", True, GOLD)
    code_rect = code.get_rect(center=(WIDTH//2, window_y + 110))
    screen.blit(code, code_rect)
    
    # Строка 1: галочка через эмодзи-шрифт, текст через обычный
    check = font_emoji.render("✅", True, (0, 200, 0))
    screen.blit(check, (window_x + 150, window_y + 160))
    line1 = font_small.render("Все уровни открыты", True, BLACK)
    screen.blit(line1, (window_x + 190, window_y + 160))
    
    # Строка 2: звезда через эмодзи-шрифт, текст через обычный
    star = font_emoji.render("⭐", True, GOLD)
    screen.blit(star, (window_x + 150, window_y + 200))
    line2 = font_small.render("270 звезд получено", True, GOLD)
    screen.blit(line2, (window_x + 190, window_y + 200))
    
    # Строка 3: замочек через эмодзи-шрифт, текст через обычный
    lock = font_emoji.render("🔓", True, DARK_BLUE)
    screen.blit(lock, (window_x + 150, window_y + 240))
    line3 = font_small.render("Режим 12x12 доступен!", True, DARK_BLUE)
    screen.blit(line3, (window_x + 190, window_y + 240))
    
    # Строка 4: сердечко через эмодзи-шрифт
    heart = font_emoji.render("❤️", True, RED)
    screen.blit(heart, (window_x + 150, window_y + 280))
    line4 = font_tiny.render("Спасибо за игру!", True, GRAY)
    screen.blit(line4, (window_x + 190, window_y + 280))
    
    pygame.display.flip()
    time.sleep(2.5)

# ===== ФУНКЦИЯ АКТИВАЦИИ ЧИТА =====
def activate_cheat():
    """Активирует чит-код VINDIGO4: все уровни открыты, 270 звезд"""
    
    # Открываем все уровни
    for size in [3, 6, 9, 12]:
        level_system.unlocked_levels[size] = 30
    
    # Даем по 90 звезд на каждый размер
    for size in [3, 6, 9, 12]:
        for level in range(1, 31):
            level_system.stars[size][level] = 3
    
    # Обновляем статистику режимов
    level_system.mode_stats['study']['games'] = 30
    level_system.mode_stats['study']['wins'] = 30
    
    level_system.mode_stats['trial']['games'] = 30
    level_system.mode_stats['trial']['wins'] = 30
    level_system.mode_stats['trial']['total_stars'] = 90
    level_system.mode_stats['trial']['best_stars'] = 3
    level_system.mode_stats['trial']['best_time'] = 5.0
    
    level_system.mode_stats['tournament']['games'] = 30
    level_system.mode_stats['tournament']['wins'] = 30
    level_system.mode_stats['tournament']['total_stars'] = 90
    level_system.mode_stats['tournament']['best_stars'] = 3
    level_system.mode_stats['tournament']['best_time'] = 4.5
    
    save_system.save_progress(level_system.unlocked_levels, level_system.stars, level_system.mode_stats)
    show_cheat_notification()  # Теперь функция определена выше


if __name__ == "__main__":
    exp_choice()
    main_menu()