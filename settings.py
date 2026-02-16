import pygame
import sys
from constants import *

# ===== КЛАСС Button ОПРЕДЕЛЯЕМ ПЕРВЫМ =====
class Button:
    def __init__(self, x, y, w, h, t, c, hc, fs=36):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = t
        self.color = c
        self.hover_color = hc
        self.current = c
        self.font = pygame.font.Font(None, fs)
    
    def draw(self, s):
        pygame.draw.rect(s, self.current, self.rect, border_radius=10)
        pygame.draw.rect(s, BLACK, self.rect, 3, border_radius=10)
        txt = self.font.render(self.text, True, WHITE)
        txt_rect = txt.get_rect(center=self.rect.center)
        s.blit(txt, txt_rect)
    
    def check_hover(self, pos):
        self.current = self.hover_color if self.rect.collidepoint(pos) else self.color
        return self.rect.collidepoint(pos)
    
    def is_clicked(self, pos, e):
        return e.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(pos)

# ===== ФУНКЦИЯ НАСТРОЕК =====
def show_settings(screen, clock, font, small_font, player_settings, save_system):
    import main
    
    # Получаем шрифты из main
    global font_emoji_small, font_tiny
    font_emoji_small = main.font_emoji_small
    font_tiny = main.font_tiny
    
    s = player_settings['sound']
    m = player_settings['music']
    exp = player_settings['experience']
    show_p = player_settings.get('show_player', True)
    current_theme = player_settings.get('theme', 'light')
    game_mode = player_settings.get('mode', 'trial')
    
    theme_names = {
        'light': 'Светлая',
        'dark': 'Темная',
        'blue': 'Синяя',
        'green': 'Зеленая',
        'purple': 'Фиолетовая'
    }
    
    mode_names = {
        'study': 'Изучения',
        'trial': 'Испытательный',
        'tournament': 'Турнирный'
    }
    
    theme_list = ['light', 'dark', 'blue', 'green', 'purple']
    mode_list = ['study', 'trial', 'tournament']
    
    theme_index = theme_list.index(current_theme) if current_theme in theme_list else 0
    mode_index = mode_list.index(game_mode) if game_mode in mode_list else 1
    
    btns = [
        Button(400, 120, 400, 60, f"Музыка: {'ВКЛ' if m else 'ВЫКЛ'}", DARK_BLUE, BLUE, 40),
        Button(400, 190, 400, 60, f"Звуки: {'ВКЛ' if s else 'ВЫКЛ'}", DARK_BLUE, BLUE, 40),
        Button(400, 260, 400, 60, f"Режим игры: {mode_names[game_mode]}", DARK_BLUE, BLUE, 40),
        Button(400, 330, 400, 60, f"Опыт: {'Новичок' if exp=='novice' else 'Опытный'}", DARK_BLUE, BLUE, 40),
        Button(400, 400, 400, 60, f"Тема: {theme_names[current_theme]}", DARK_BLUE, BLUE, 40),
        Button(400, 470, 400, 60, f"Плеер: {'ПОКАЗЫВАТЬ' if show_p else 'СКРЫТЬ'}", DARK_BLUE, BLUE, 40),
        Button(400, 540, 400, 60, "СОХРАНИТЬ И ВЫЙТИ", GRAY, DARK_GRAY, 40),
    ]
    
    while True:
        theme = get_theme()
        screen.fill(WHITE)
        mouse = pygame.mouse.get_pos()
        
        title = font.render("НАСТРОЙКИ", True, BLACK)
        title_rect = title.get_rect(center=(600, 50))
        screen.blit(title, title_rect)
        
        # ===== КРАСИВАЯ РАМКА ДЛЯ ОПИСАНИЯ =====
        desc_frame_x = 320
        desc_frame_y = 620
        desc_frame_width = 560
        desc_frame_height = 150
        
        # Определяем цвет рамки в зависимости от темы
        if theme.name == "Светлая":
            frame_color = (70, 130, 180)  # Синий для светлой темы
            inner_bg = (240, 248, 255)    # Светло-голубой внутри
        else:
            frame_color = theme.accent_color
            inner_bg = theme.bg_color
        
        # Внешняя рамка
        pygame.draw.rect(screen, frame_color, (desc_frame_x, desc_frame_y, desc_frame_width, desc_frame_height), border_radius=15)
        pygame.draw.rect(screen, theme.accent_color, (desc_frame_x, desc_frame_y, desc_frame_width, desc_frame_height), 3, border_radius=15)
        
        # Внутренняя подсветка
        inner_rect = pygame.Rect(desc_frame_x + 3, desc_frame_y + 3, desc_frame_width - 6, desc_frame_height - 6)
        pygame.draw.rect(screen, inner_bg, inner_rect, border_radius=12)
        
        # Заголовок и описание
        if game_mode == 'study':
            # Эмодзи для режима изучения
            emoji_study = font_emoji_small.render("📚", True, (100, 150, 255))
            screen.blit(emoji_study, (desc_frame_x + 20, desc_frame_y + 15))
            
            mode_title = small_font.render(" Режим изучения", True, (100, 150, 255))
            screen.blit(mode_title, (desc_frame_x + 60, desc_frame_y + 18))
            
            desc_lines = [
                "• Таймер отключен - играйте в своё удовольствие",
                "• Автоматическая победа при решении судоку",
                "• 3 звезды за любой правильный ответ"
            ]
        elif game_mode == 'trial':
            # Эмодзи для испытательного режима
            emoji_trial = font_emoji_small.render("⚡", True, (255, 200, 50))
            screen.blit(emoji_trial, (desc_frame_x + 20, desc_frame_y + 15))
            
            mode_title = small_font.render(" Испытательный режим", True, (255, 200, 50))
            screen.blit(mode_title, (desc_frame_x + 60, desc_frame_y + 18))
            
            desc_lines = [
                "• Таймер включен - на время",
                "• Звезды зависят от скорости решения",
                "• Поражение, если не уложиться в время"
            ]
        else:  # tournament
            # Эмодзи для турнирного режима
            emoji_tournament = font_emoji_small.render("🏆", True, (255, 100, 100))
            screen.blit(emoji_tournament, (desc_frame_x + 20, desc_frame_y + 15))
            
            mode_title = small_font.render(" Турнирный режим", True, (255, 100, 100))
            screen.blit(mode_title, (desc_frame_x + 60, desc_frame_y + 18))
            
            desc_lines = [
                "• Усложненный таймер (70% от обычного)",
                "• Двойные звезды за победу",
                "• Строгое поражение при просрочке"
            ]
        
        # Описание обычным шрифтом
        for i, line in enumerate(desc_lines):
            line_surface = pygame.font.Font(None, 22).render(line, True, theme.text_color)
            line_rect = line_surface.get_rect(midleft=(desc_frame_x + 40, desc_frame_y + 60 + i * 25))
            screen.blit(line_surface, line_rect)
        
        # Маленькая пасхалка
        hint = pygame.font.Font(None, 20).render("v0.3 - 2026", True, (220, 220, 220))
        hint_rect = hint.get_rect(bottomright=(1180, 980))
        screen.blit(hint, hint_rect)
        
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            for i, btn in enumerate(btns):
                if btn.is_clicked(mouse, e):
                    if i == 0:
                        m = not m
                        player_settings['music'] = m
                        btns[i].text = f"Музыка: {'ВКЛ' if m else 'ВЫКЛ'}"
                        if m:
                            if main.playlist:
                                main.play_track(main.current_track)
                        else:
                            pygame.mixer.music.pause()
                    elif i == 1:
                        s = not s
                        player_settings['sound'] = s
                        btns[i].text = f"Звуки: {'ВКЛ' if s else 'ВЫКЛ'}"
                    elif i == 2:
                        mode_index = (mode_index + 1) % len(mode_list)
                        game_mode = mode_list[mode_index]
                        player_settings['mode'] = game_mode
                        btns[i].text = f"Режим игры: {mode_names[game_mode]}"
                    elif i == 3:
                        exp = 'expert' if exp == 'novice' else 'novice'
                        player_settings['experience'] = exp
                        btns[i].text = f"Опыт: {'Новичок' if exp=='novice' else 'Опытный'}"
                    elif i == 4:
                        theme_index = (theme_index + 1) % len(theme_list)
                        current_theme = theme_list[theme_index]
                        player_settings['theme'] = current_theme
                        from constants import set_theme
                        set_theme(current_theme)
                        btns[i].text = f"Тема: {theme_names[current_theme]}"
                        
                        screen.fill(WHITE)
                        title = font.render("НАСТРОЙКИ", True, BLACK)
                        screen.blit(title, title_rect)
                        for b in btns:
                            b.draw(screen)
                        pygame.display.flip()
                    elif i == 5:
                        show_p = not show_p
                        player_settings['show_player'] = show_p
                        btns[i].text = f"Плеер: {'ПОКАЗЫВАТЬ' if show_p else 'СКРЫТЬ'}"
                        
                        if show_p:
                            if player_settings['music']:
                                if not pygame.mixer.music.get_busy():
                                    main.play_track(main.current_track)
                                else:
                                    pygame.mixer.music.unpause()
                        else:
                            pygame.mixer.music.pause()
                    elif i == 6:
                        save_system.save_settings(player_settings)
                        return
        
        for btn in btns:
            btn.check_hover(mouse)
            btn.draw(screen)
        pygame.display.flip()
        clock.tick(60)