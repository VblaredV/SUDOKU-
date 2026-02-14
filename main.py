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
    while True:
        draw_bg()
        mouse = pygame.mouse.get_pos()
        theme = get_theme()
        
        btns = [
            Button(400, 300, 400, 80, "ИГРАТЬ", theme.button_color, theme.button_hover),
            Button(400, 400, 400, 80, "УРОВНИ", theme.button_color, theme.button_hover),
            Button(400, 500, 400, 80, "НАСТРОЙКИ", theme.button_color, theme.button_hover),
            Button(400, 600, 400, 80, "ВЫХОД", theme.button_color, theme.button_hover)
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
            
            for btn in btns:
                if btn.is_clicked(mouse, e):
                    if btn.text == "ИГРАТЬ": 
                        size_menu()
                    elif btn.text == "УРОВНИ": 
                        progress_menu()
                    elif btn.text == "НАСТРОЙКИ": 
                        settings.show_settings(screen, clock, font_mid, font_small, player_settings, save_system)
                    elif btn.text == "ВЫХОД":
                        save_system.save_settings(player_settings)
                        pygame.quit()
                        sys.exit()
            
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
        
        # Определяем цвет заголовка в зависимости от темы
        if theme.name == "Темная":
            title_color = WHITE
            frame_bg_color = DARK_GRAY  # Темный фон рамки
        else:
            title_color = theme.text_color
            frame_bg_color = WHITE  # Белый фон рамки
        
        title = font_mid.render(title_text, True, title_color)
        
        text_height = title.get_height()
        padding = int(text_height * 0.5)
        
        title_width = title.get_width() + padding * 2
        title_height = text_height + padding * 2
        title_x = center_x - title_width // 2
        title_y = 80
        
        # Тень
        shadow_rect = pygame.Rect(title_x + 3, title_y + 3, title_width, title_height)
        pygame.draw.rect(screen, (50,50,50,100), shadow_rect, border_radius=10)
        
        # Основная рамка - цвет фона зависит от темы
        title_rect = pygame.Rect(title_x, title_y, title_width, title_height)
        pygame.draw.rect(screen, frame_bg_color, title_rect, border_radius=10)
        pygame.draw.rect(screen, theme.accent_color, title_rect, 2, border_radius=10)
        
        # Текст заголовка по центру рамки
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
            stars = level_system.get_total_stars(s)
            unlocked = level_system.unlocked_levels[s]
            
            y = start_y + i * (text_height + padding)
            
            # Размер и количество уровней
            size_text = font_small.render(f"{s}x{s}: {completed}/30 уровней", True, theme.text_color)
            screen.blit(size_text, (inner_x + 50, y))
            
            # Звезды
            star_text = font_emoji_small.render(f"⭐ {stars}", True, theme.accent_color)
            star_rect = star_text.get_rect(center=(center_x, y + text_height//2))
            screen.blit(star_text, star_rect)
            
            # ===== СТАТУС =====
            if s == 12:
                total_stars_all = level_system.get_total_stars()
                if total_stars_all >= 270:
                    status_emoji = font_emoji_small.render("🔓", True, theme.accent_color)
                    status_text = font_small.render(f"{unlocked}/30", True, theme.text_color)
                else:
                    status_emoji = font_emoji_small.render("🔒", True, GRAY)
                    status_text = font_small.render("???", True, GRAY)
            else:
                status_emoji = font_emoji_small.render("🔓", True, theme.text_color)
                status_text = font_small.render(f"{unlocked}/30", True, theme.text_color)
                
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
        
        # ===== ЗАГОЛОВОК В РАМКЕ =====
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
            
            stats_12x12 = font_tiny.render(f"{len(level_system.stars[12])}/30", True, BLACK)
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
        
        # ===== ЗАГОЛОВОК ПО ЦЕНТРУ =====
        title_text = f"УРОВНИ {size}x{size}"
        title = font_big.render(title_text, True, theme.accent_color)
        title_rect = title.get_rect(center=(WIDTH//2, 80))
        screen.blit(title, title_rect)
        
        # ===== ИНФОРМАЦИЯ О ЗВЕЗДАХ СПРАВА =====
        stars_total = level_system.get_total_stars(size)
        
        # Увеличили размер до 38 и опустили ниже (120 вместо 110)
        big_font = pygame.font.Font(None, 38)  # Размер 38
        
        star = font_emoji.render("⭐", True, GOLD)
        text1 = big_font.render("Звёзд:", True, theme.text_color)
        text2 = big_font.render(f"{stars_total}/90", True, theme.accent_color)
        
        # Считаем общую ширину
        total_width = star.get_width() + text1.get_width() + text2.get_width() + 10
        start_x = 1150 - total_width  # Отступ от правого края
        
        screen.blit(star, (start_x, 120))  # Опустил ниже (было 120), идеал 126
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
    # Создаем игру
    game = Game(size, level, show_rules=False, emoji_font=font_emoji)
    
    timer_paused = False
    paused_time = 0
    
    # Проверяем режим игрока
    if player_settings['experience'] == 'novice':
        # НОВИЧОК - показываем правила перед каждым уровнем
        timer_paused = True
        print(f"⏸️ Таймер на паузе (новичок, уровень {level})")
        # Показываем правила
        game.show_rules_popup(screen, font_mid)
        # После закрытия правил запускаем таймер
        game.start_time = time.time()
        timer_paused = False
        print(f"▶️ Таймер запущен (новичок, уровень {level})")
    else:
        # ОПЫТНЫЙ - сразу запускаем таймер
        game.start_time = time.time()
        print(f"⏱️ Таймер запущен (опытный, уровень {level})")
    
    victory_timer = None
    victory_delay = 0.5
    last_state = None
    
    # Для проверки завершения 12x12
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
                        # Открытие правил по кнопке (для всех режимов)
                        if not timer_paused and hasattr(game, 'start_time'):
                            paused_time = time.time() - game.start_time
                            timer_paused = True
                            print(f"⏸️ Таймер на паузе: {paused_time:.2f} сек")
                        
                        # Показываем правила
                        game.show_rules_popup(screen, font_mid)
                        
                        # Возобновляем
                        if hasattr(game, 'start_time'):
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
            
            if e.type == pygame.KEYDOWN and game.selected:
                if e.key in [pygame.K_1, pygame.K_KP1]: game.place_number(1)
                elif e.key in [pygame.K_2, pygame.K_KP2]: game.place_number(2)
                elif e.key in [pygame.K_3, pygame.K_KP3]: game.place_number(3)
                elif e.key in [pygame.K_4, pygame.K_KP4]: game.place_number(4)
                elif e.key in [pygame.K_5, pygame.K_KP5]: game.place_number(5)
                elif e.key in [pygame.K_6, pygame.K_KP6]: game.place_number(6)
                elif e.key in [pygame.K_7, pygame.K_KP7]: game.place_number(7) if size > 6 else None
                elif e.key in [pygame.K_8, pygame.K_KP8]: game.place_number(8) if size > 6 else None
                elif e.key in [pygame.K_9, pygame.K_KP9]: game.place_number(9) if size > 6 else None
                elif e.key in [pygame.K_DELETE, pygame.K_BACKSPACE]: game.delete_number()
                victory_timer = None
            
            if music_btns:
                prev, play, next_btn = music_btns
                if prev.collidepoint(mouse) and e.type == pygame.MOUSEBUTTONDOWN:
                    prev_track()
                if play.collidepoint(mouse) and e.type == pygame.MOUSEBUTTONDOWN:
                    toggle_music()
                if next_btn.collidepoint(mouse) and e.type == pygame.MOUSEBUTTONDOWN:
                    next_track()
        
        # Проверяем победу только если таймер существует и не на паузе
        if hasattr(game, 'start_time') and not timer_paused:
            if game.check_mode:
                game.check_board()
                
                all_filled = True
                for r in range(size):
                    for c in range(size):
                        if game.board[r][c] == 0:
                            all_filled = False
                            break
                    if not all_filled:
                        break
                
                has_errors = False
                for r in range(size):
                    for c in range(size):
                        if (r, c) in game.highlight_cells and game.highlight_cells[(r, c)] == LIGHT_RED:
                            has_errors = True
                            break
                    if has_errors:
                        break
                
                is_correct = game.check_win_condition()
                
                current_state = (all_filled, has_errors, is_correct)
                if last_state != current_state:
                    print(f"all_filled: {all_filled}, has_errors: {has_errors}, is_correct: {is_correct}")
                    last_state = current_state
                
                if all_filled and not has_errors and is_correct:
                    if victory_timer is None:
                        victory_timer = time.time()
                        print(f"🎉 Условия победы выполнены! Таймер запущен")
                    
                    elif time.time() - victory_timer >= victory_delay:
                        elapsed = time.time() - game.start_time
                        
                        if size == 3:
                            if elapsed < 10:
                                game.stars = 3
                            elif elapsed < 15:
                                game.stars = 2
                            elif elapsed < 20:
                                game.stars = 1
                            else:
                                game.stars = 0
                        elif size == 6:
                            if elapsed < 25:
                                game.stars = 3
                            elif elapsed < 35:
                                game.stars = 2
                            elif elapsed < 45:
                                game.stars = 1
                            else:
                                game.stars = 0
                        elif size == 9:
                            if elapsed < 45:
                                game.stars = 3
                            elif elapsed < 55:
                                game.stars = 2
                            elif elapsed < 65:
                                game.stars = 1
                            else:
                                game.stars = 0
                        else:  # size == 12
                            if elapsed < 60:
                                game.stars = 3
                            elif elapsed < 80:
                                game.stars = 2
                            elif elapsed < 100:
                                game.stars = 1
                            else:
                                game.stars = 0
                        
                        print(f"🏆 {size}x{size} Время: {elapsed:.2f} сек -> {game.stars} ⭐")
                        
                        theme = get_theme()
                        
                        # Проверяем, не завершена ли игра полностью
                        if size == 12 and level == 30 and game.stars > 0:
                            # Проверяем, все ли 30 уровней 12x12 пройдены
                            all_12x12_done = len(level_system.stars[12]) >= 30
                            if all_12x12_done and not game_completed:
                                game_completed = True
                                # Показываем титры
                                show_credits(screen, font_big, font_mid, font_small, theme)
                                return
                        
                        if game.stars > 0:
                            play_victory_sound()
                            win_text = f"ПОБЕДА! {game.stars}"
                            win = font_mid.render(win_text, True, theme.accent_color)
                            star_text = font_emoji_big.render("⭐", True, theme.accent_color)
                            next_level = level + 1 if level < 30 else 1
                            next_text = f"СЛЕДУЮЩИЙ УРОВЕНЬ {next_level}"
                            window_width, window_height = 500, 320
                        else:
                            play_defeat_sound()
                            win_text = "ВЫ ПРОИГРАЛИ"
                            win = font_mid.render(win_text, True, RED)
                            star_text = None
                            next_text = "ПОПРОБУЙТЕ ЕЩЕ РАЗ"
                            window_width, window_height = 500, 280
                        
                        window_x = (WIDTH - window_width) // 2
                        window_y = (HEIGHT - window_height) // 2
                        
                        s = pygame.Surface((WIDTH, HEIGHT))
                        s.set_alpha(180)
                        s.fill(BLACK)
                        screen.blit(s, (0,0))
                        
                        border_color = theme.accent_color if game.stars > 0 else RED
                        pygame.draw.rect(screen, WHITE, (window_x, window_y, window_width, window_height), border_radius=15)
                        pygame.draw.rect(screen, border_color, (window_x, window_y, window_width, window_height), 4, border_radius=15)
                        
                        if game.stars > 0:
                            win_rect = win.get_rect(center=(WIDTH//2 - 20, window_y + 70))
                            screen.blit(win, win_rect)
                            star_rect = star_text.get_rect(midleft=(win_rect.right + 5, win_rect.centery))
                            screen.blit(star_text, star_rect)
                        else:
                            win_rect = win.get_rect(center=(WIDTH//2, window_y + 70))
                            screen.blit(win, win_rect)
                        
                        next_surface = font_small.render(next_text, True, theme.text_color if game.stars > 0 else RED)
                        next_rect = next_surface.get_rect(center=(WIDTH//2, window_y + 130))
                        screen.blit(next_surface, next_rect)
                        
                        if game.stars > 0:
                            continue_btn = pygame.Rect(WIDTH//2 - 120, window_y + 170, 240, 50)
                            restart_btn = pygame.Rect(WIDTH//2 - 120, window_y + 230, 240, 50)
                            
                            pygame.draw.rect(screen, theme.button_color, continue_btn, border_radius=10)
                            pygame.draw.rect(screen, WHITE, continue_btn, 3, border_radius=10)
                            continue_text = font_small.render("ДАЛЕЕ", True, WHITE)
                            continue_rect = continue_text.get_rect(center=continue_btn.center)
                            screen.blit(continue_text, continue_rect)
                            
                            pygame.draw.rect(screen, theme.button_color, restart_btn, border_radius=10)
                            pygame.draw.rect(screen, WHITE, restart_btn, 3, border_radius=10)
                            restart_text = font_small.render("ЗАНОВО", True, WHITE)
                            restart_rect = restart_text.get_rect(center=restart_btn.center)
                            screen.blit(restart_text, restart_rect)
                        else:
                            restart_btn = pygame.Rect(WIDTH//2 - 100, window_y + 170, 200, 50)
                            pygame.draw.rect(screen, RED, restart_btn, border_radius=10)
                            pygame.draw.rect(screen, WHITE, restart_btn, 3, border_radius=10)
                            restart_text = font_small.render("ЗАНОВО", True, WHITE)
                            restart_rect = restart_text.get_rect(center=restart_btn.center)
                            screen.blit(restart_text, restart_rect)
                            continue_btn = None
                        
                        pygame.display.flip()
                        
                        waiting = True
                        while waiting:
                            for event in pygame.event.get():
                                if event.type == pygame.QUIT:
                                    pygame.quit()
                                    sys.exit()
                                if event.type == pygame.MOUSEBUTTONDOWN:
                                    if game.stars > 0 and continue_btn and continue_btn.collidepoint(event.pos):
                                        waiting = False
                                        level_system.complete_level(size, level, game.stars)
                                        if level < 30:
                                            start_game(size, level + 1)
                                            return
                                        else:
                                            return
                                    if restart_btn and restart_btn.collidepoint(event.pos):
                                        waiting = False
                                        start_game(size, level)
                                        return
                                if event.type == pygame.KEYDOWN:
                                    if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                                        if game.stars > 0:
                                            waiting = False
                                            level_system.complete_level(size, level, game.stars)
                                            if level < 30:
                                                start_game(size, level + 1)
                                                return
                                            else:
                                                return
                                        else:
                                            waiting = False
                                            start_game(size, level)
                                            return
            else:
                victory_timer = None
        
        pygame.display.flip()
        clock.tick(60)

def show_credits(screen, font_big, font_mid, font_small, theme):
    """Показывает титры после прохождения игры"""
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(200)
    overlay.fill(BLACK)
    screen.blit(overlay, (0,0))
    
    # Белое окно для титров
    credit_width = 700
    credit_height = 500
    credit_x = (WIDTH - credit_width) // 2
    credit_y = (HEIGHT - credit_height) // 2
    
    pygame.draw.rect(screen, WHITE, (credit_x, credit_y, credit_width, credit_height), border_radius=20)
    pygame.draw.rect(screen, GOLD, (credit_x, credit_y, credit_width, credit_height), 5, border_radius=20)
    
    # Заголовок
    title = font_big.render("СПАСИБО ЗА ИГРУ!", True, DARK_BLUE)
    title_rect = title.get_rect(center=(WIDTH//2, credit_y + 80))
    screen.blit(title, title_rect)
    
    # Основной текст
    line1 = font_mid.render("Над проектом работали", True, BLACK)
    line1_rect = line1.get_rect(center=(WIDTH//2, credit_y + 180))
    screen.blit(line1, line1_rect)

    line2 = font_small.render("ученики 9Г класса:", True, GRAY)
    line2_rect = line2.get_rect(center=(WIDTH//2, credit_y + 250))
    screen.blit(line2, line2_rect)
    
    line3 = font_mid.render("Бортников А.С.", True, DARK_BLUE)
    line3_rect = line3.get_rect(center=(WIDTH//2, credit_y + 310))
    screen.blit(line3, line3_rect)
    
    line4 = font_mid.render("Ломтев А.И.", True, DARK_BLUE)
    line4_rect = line4.get_rect(center=(WIDTH//2, credit_y + 370))
    screen.blit(line4, line4_rect)

    # Звезды
    stars_text = font_emoji_big.render("⭐⭐⭐⭐⭐", True, GOLD)
    stars_rect = stars_text.get_rect(center=(WIDTH//2, credit_y + 440))
    screen.blit(stars_text, stars_rect)
    
    # Кнопка выхода
    exit_btn = pygame.Rect(WIDTH//2 - 100, credit_y + 500, 200, 50)
    pygame.draw.rect(screen, DARK_BLUE, exit_btn, border_radius=10)
    pygame.draw.rect(screen, WHITE, exit_btn, 3, border_radius=10)
    exit_text = font_small.render("В МЕНЮ", True, WHITE)
    exit_rect = exit_text.get_rect(center=exit_btn.center)
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
                if exit_btn.collidepoint(event.pos):
                    waiting = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN or event.key == pygame.K_ESCAPE:
                    waiting = False

if __name__ == "__main__":
    exp_choice()
    main_menu()