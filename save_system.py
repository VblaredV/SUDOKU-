import json
import os
import sys
from pathlib import Path
from datetime import datetime

class SaveSystem:
    def __init__(self):
        # Определяем правильную папку для сохранений
        if getattr(sys, 'frozen', False):
            # Если запущены как EXE
            self.game_folder = Path(os.path.dirname(sys.executable))
        else:
            # Если запущены как скрипт
            self.game_folder = Path(__file__).parent
            
        self.saves_folder = self.game_folder / "saves"
        if not self.saves_folder.exists():
            os.makedirs(self.saves_folder)
            print(f"✅ Создана папка для сохранений: {self.saves_folder}")
            
        self.progress_file = self.saves_folder / "progress.json"
        self.settings_file = self.saves_folder / "settings.json"
    
    def save_progress(self, unlocked_levels, stars, mode_stats=None):
        """Сохраняет прогресс игрока и статистику режимов"""
        try:
            # Если статистика не передана, загружаем существующую
            if mode_stats is None:
                _, _, mode_stats = self.load_progress()
            
            # Преобразуем ключи в строки для JSON
            unlocked_str = {str(k): v for k, v in unlocked_levels.items()}
            
            stars_str = {}
            for size_key, size_data in stars.items():
                size_str = str(size_key)
                stars_str[size_str] = {}
                for level_key, stars_count in size_data.items():
                    stars_str[size_str][str(level_key)] = stars_count
            
            save_data = {
                "unlocked_levels": unlocked_str,
                "stars": stars_str,
                "mode_stats": mode_stats,
                "last_save": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            with open(self.progress_file, 'w', encoding='utf-8') as f:
                json.dump(save_data, f, indent=4, ensure_ascii=False, default=str)
            
            print(f"💾 Прогресс сохранен в {self.progress_file}")
            return True
        except Exception as e:
            print(f"❌ Ошибка сохранения прогресса: {e}")
            return False
    
    def load_progress(self):
        """Загружает прогресс игрока и статистику режимов"""
        # Значения по умолчанию
        default_unlocked = {3: 1, 6: 1, 9: 1, 12: 0}
        default_stars = {3: {}, 6: {}, 9: {}, 12: {}}
        default_mode_stats = {
            'study': {
                'games': 0,           # Количество игр
                'wins': 0,             # Количество побед
                'best_time': None      # Лучшее время (не используется в study)
            },
            'trial': {
                'games': 0,             # Количество игр
                'wins': 0,               # Количество побед
                'best_time': None,        # Лучшее время в секундах
                'total_stars': 0,         # Всего заработано звезд
                'best_stars': 0           # Лучший результат звезд за уровень
            },
            'tournament': {
                'games': 0,               # Количество игр
                'wins': 0,                 # Количество побед
                'best_time': None,          # Лучшее время в секундах
                'total_stars': 0,           # Всего заработано звезд
                'best_stars': 0             # Лучший результат звезд за уровень
            }
        }
        
        # Если файл не существует, возвращаем значения по умолчанию
        if not self.progress_file.exists():
            print("🆕 Файл сохранения не найден. Новая игра!")
            return default_unlocked, default_stars, default_mode_stats
        
        try:
            with open(self.progress_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Загружаем открытые уровни
            unlocked = {}
            for k, v in data.get("unlocked_levels", {}).items():
                try:
                    unlocked[int(k)] = v
                except (ValueError, TypeError):
                    pass
            
            # Убеждаемся, что все размеры присутствуют
            for size in [3, 6, 9, 12]:
                if size not in unlocked:
                    unlocked[size] = 1 if size != 12 else 0
            
            # Загружаем звезды
            stars = {3: {}, 6: {}, 9: {}, 12: {}}
            stars_data = data.get("stars", {})
            for size_str, size_data in stars_data.items():
                try:
                    size = int(size_str)
                    if size in stars:
                        for level_str, stars_count in size_data.items():
                            try:
                                level = int(level_str)
                                stars[size][level] = int(stars_count)
                            except (ValueError, TypeError):
                                pass
                except (ValueError, TypeError):
                    pass
            
            # Загружаем статистику режимов
            mode_stats = data.get("mode_stats", default_mode_stats)
            
            # Убеждаемся, что все ключи режимов присутствуют
            for mode in ['study', 'trial', 'tournament']:
                if mode not in mode_stats:
                    mode_stats[mode] = default_mode_stats[mode]
                else:
                    # Добавляем недостающие поля
                    for key, value in default_mode_stats[mode].items():
                        if key not in mode_stats[mode]:
                            mode_stats[mode][key] = value
            
            print(f"✅ Прогресс загружен из {self.progress_file}")
            return unlocked, stars, mode_stats
            
        except Exception as e:
            print(f"❌ Ошибка загрузки прогресса: {e}")
            return default_unlocked, default_stars, default_mode_stats
    
    def update_mode_stats(self, mode, won=True, stars=0, elapsed_time=None):
        """Обновляет статистику для конкретного режима"""
        try:
            unlocked, stars_data, mode_stats = self.load_progress()
            
            if mode not in mode_stats:
                return False
            
            # Увеличиваем счетчик игр
            mode_stats[mode]['games'] += 1
            
            # Если победа
            if won:
                mode_stats[mode]['wins'] += 1
                
                # Для режимов с таймером
                if mode != 'study' and elapsed_time is not None:
                    # Обновляем лучшее время
                    best = mode_stats[mode].get('best_time')
                    if best is None or elapsed_time < best:
                        mode_stats[mode]['best_time'] = round(elapsed_time, 1)
                    
                    # Обновляем общее количество звезд
                    mode_stats[mode]['total_stars'] = mode_stats[mode].get('total_stars', 0) + stars
                    
                    # Обновляем лучший результат звезд
                    best_stars = mode_stats[mode].get('best_stars', 0)
                    if stars > best_stars:
                        mode_stats[mode]['best_stars'] = stars
            
            # Сохраняем обновленную статистику
            self.save_progress(unlocked, stars_data, mode_stats)
            return True
            
        except Exception as e:
            print(f"❌ Ошибка обновления статистики: {e}")
            return False
    
    def get_mode_stats(self, mode):
        """Возвращает статистику для конкретного режима"""
        try:
            _, _, mode_stats = self.load_progress()
            return mode_stats.get(mode, {})
        except:
            return {}
    
    def reset_mode_stats(self, mode=None):
        """Сбрасывает статистику для режима (или всех режимов)"""
        try:
            unlocked, stars_data, mode_stats = self.load_progress()
            
            default_mode_stats = {
                'study': {'games': 0, 'wins': 0, 'best_time': None},
                'trial': {'games': 0, 'wins': 0, 'best_time': None, 'total_stars': 0, 'best_stars': 0},
                'tournament': {'games': 0, 'wins': 0, 'best_time': None, 'total_stars': 0, 'best_stars': 0}
            }
            
            if mode and mode in mode_stats:
                # Сбрасываем только указанный режим
                mode_stats[mode] = default_mode_stats[mode]
            else:
                # Сбрасываем все режимы
                mode_stats = default_mode_stats.copy()
            
            self.save_progress(unlocked, stars_data, mode_stats)
            return True
            
        except Exception as e:
            print(f"❌ Ошибка сброса статистики: {e}")
            return False
    
    def save_settings(self, settings):
        """Сохраняет настройки игры"""
        try:
            data = settings.copy()
            data["last_save"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            
            print(f"⚙️ Настройки сохранены в {self.settings_file}")
            return True
        except Exception as e:
            print(f"❌ Ошибка сохранения настроек: {e}")
            return False
    
    def load_settings(self):
        """Загружает настройки игры"""
        default = {
            'sound': True, 
            'music': True, 
            'experience': 'novice', 
            'show_player': True,
            'mode': 'trial',  # По умолчанию испытательный режим
            'theme': 'light'
        }
        
        if not self.settings_file.exists():
            print("🆕 Файл настроек не найден. Создаем новые настройки.")
            return default
        
        try:
            with open(self.settings_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Удаляем временные метки
            if 'last_save' in data: 
                del data['last_save']
            
            # Добавляем недостающие поля
            if 'show_player' not in data:
                data['show_player'] = True
            if 'mode' not in data:
                data['mode'] = 'trial'
            if 'theme' not in data:
                data['theme'] = 'light'
            
            print(f"⚙️ Настройки загружены из {self.settings_file}")
            return data
            
        except Exception as e:
            print(f"❌ Ошибка загрузки настроек: {e}")
            return default
    
    def reset_progress(self):
        """Сбрасывает весь прогресс (уровни, звезды, статистику)"""
        try:
            if self.progress_file.exists(): 
                os.remove(self.progress_file)
            print("🔄 Прогресс сброшен")
            
            default_unlocked = {3: 1, 6: 1, 9: 1, 12: 0}
            default_stars = {3: {}, 6: {}, 9: {}, 12: {}}
            default_mode_stats = {
                'study': {'games': 0, 'wins': 0, 'best_time': None},
                'trial': {'games': 0, 'wins': 0, 'best_time': None, 'total_stars': 0, 'best_stars': 0},
                'tournament': {'games': 0, 'wins': 0, 'best_time': None, 'total_stars': 0, 'best_stars': 0}
            }
            
            return default_unlocked, default_stars, default_mode_stats
            
        except Exception as e:
            print(f"❌ Ошибка сброса прогресса: {e}")
            return None
    
    def get_total_stats(self):
        """Возвращает общую статистику по всем режимам"""
        try:
            _, _, mode_stats = self.load_progress()
            
            total = {
                'total_games': 0,
                'total_wins': 0,
                'total_stars': 0,
                'best_time_overall': None
            }
            
            for mode, stats in mode_stats.items():
                total['total_games'] += stats.get('games', 0)
                total['total_wins'] += stats.get('wins', 0)
                
                if mode != 'study':
                    total['total_stars'] += stats.get('total_stars', 0)
                    
                    best_time = stats.get('best_time')
                    if best_time:
                        if total['best_time_overall'] is None or best_time < total['best_time_overall']:
                            total['best_time_overall'] = best_time
            
            return total
            
        except Exception as e:
            print(f"❌ Ошибка получения общей статистики: {e}")
            return {}

# Создаем глобальный экземпляр
save_system = SaveSystem()