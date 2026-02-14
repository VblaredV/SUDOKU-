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
    # Импортируем main внутри функции для музыки
    import main
    
    s = player_settings['sound']
    m = player_settings['music']
    exp = player_settings['experience']
    show_p = player_settings.get('show_player', True)
    current_theme = player_settings.get('theme', 'light')
    
    theme_names = {
        'light': 'Светлая',
        'dark': 'Темная',
        'blue': 'Синяя',
        'green': 'Зеленая',
        'purple': 'Фиолетовая'
    }
    
    # Список тем для циклического переключения
    theme_list = ['light', 'dark', 'blue', 'green', 'purple']
    theme_index = theme_list.index(current_theme) if current_theme in theme_list else 0
    
    btns = [
        Button(400, 120, 400, 60, f"Музыка: {'ВКЛ' if m else 'ВЫКЛ'}", DARK_BLUE, BLUE, 40),
        Button(400, 190, 400, 60, f"Звуки: {'ВКЛ' if s else 'ВЫКЛ'}", DARK_BLUE, BLUE, 40),
        Button(400, 260, 400, 60, f"Режим: {'Новичок' if exp=='novice' else 'Опытный'}", DARK_BLUE, BLUE, 40),
        Button(400, 330, 400, 60, f"Тема: {theme_names[current_theme]}", DARK_BLUE, BLUE, 40),
        Button(400, 400, 400, 60, f"Плеер: {'ПОКАЗЫВАТЬ' if show_p else 'СКРЫТЬ'}", DARK_BLUE, BLUE, 40),
        Button(400, 470, 400, 60, "СОХРАНИТЬ И ВЫЙТИ", GRAY, DARK_GRAY, 40),
    ]
    
    while True:
        screen.fill(WHITE)
        mouse = pygame.mouse.get_pos()
        
        title = font.render("НАСТРОЙКИ", True, BLACK)
        title_rect = title.get_rect(center=(600, 50))
        screen.blit(title, title_rect)
        
        # Маленькая пасхалка для внимательных
        hint = small_font.render("v0.1 - 2026", True, (220, 220, 220))
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
                        exp = 'expert' if exp == 'novice' else 'novice'
                        player_settings['experience'] = exp
                        btns[i].text = f"Режим: {'Новичок' if exp=='novice' else 'Опытный'}"
                    elif i == 3:
                        # Переключение темы
                        theme_index = (theme_index + 1) % len(theme_list)
                        current_theme = theme_list[theme_index]
                        player_settings['theme'] = current_theme
                        
                        # Устанавливаем тему через функцию из constants
                        from constants import set_theme
                        set_theme(current_theme)
                        
                        btns[i].text = f"Тема: {theme_names[current_theme]}"
                        
                        # ПРИНУДИТЕЛЬНО перерисовываем фон настроек с новой темой
                        screen.fill(WHITE)
                        title = font.render("НАСТРОЙКИ", True, BLACK)
                        screen.blit(title, title_rect)
                        
                        # Перерисовываем все кнопки
                        for b in btns:
                            b.draw(screen)
                        
                        pygame.display.flip()
                        
                    elif i == 4:
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
                    elif i == 5:
                        save_system.save_settings(player_settings)
                        return
        
        for btn in btns:
            btn.check_hover(mouse)
            btn.draw(screen)
        pygame.display.flip()
        clock.tick(60)