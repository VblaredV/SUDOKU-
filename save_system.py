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
    
    def save_progress(self, unlocked_levels, stars):
        try:
            save_data = {
                "unlocked_levels": {str(k): v for k, v in unlocked_levels.items()},
                "stars": {str(s): {str(l): stars[s][l] for l in stars[s]} for s in stars},
                "last_save": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            with open(self.progress_file, 'w', encoding='utf-8') as f:
                json.dump(save_data, f, indent=4, ensure_ascii=False)
            print(f"💾 Прогресс сохранен в {self.progress_file}")
            return True
        except Exception as e:
            print(f"❌ Ошибка сохранения: {e}")
            return False
    
    def load_progress(self):
        default_unlocked = {3: 1, 6: 1, 9: 1, 12: 0}
        default_stars = {3: {}, 6: {}, 9: {}, 12: {}}
        
        if not self.progress_file.exists():
            print("🆕 Файл сохранения не найден. Новая игра!")
            return default_unlocked, default_stars
        
        try:
            with open(self.progress_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            unlocked = {int(k): v for k, v in data["unlocked_levels"].items()}
            
            stars = {}
            for s in data["stars"]:
                size = int(s)
                stars[size] = {int(l): data["stars"][s][l] for l in data["stars"][s]}
            
            print(f"✅ Прогресс загружен из {self.progress_file}")
            return unlocked, stars
        except Exception as e:
            print(f"❌ Ошибка загрузки: {e}")
            return default_unlocked, default_stars
    
    def save_settings(self, settings):
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
        default = {'sound': True, 'music': True, 'experience': 'novice', 'show_player': True}
        if not self.settings_file.exists():
            return default
        try:
            with open(self.settings_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            if 'last_save' in data: del data['last_save']
            if 'show_player' not in data:
                data['show_player'] = True
            return data
        except Exception as e:
            print(f"❌ Ошибка загрузки настроек: {e}")
            return default
    
    def reset_progress(self):
        try:
            if self.progress_file.exists(): 
                os.remove(self.progress_file)
            print("🔄 Прогресс сброшен")
            return {3: 1, 6: 1, 9: 1, 12: 0}, {3: {}, 6: {}, 9: {}, 12: {}}
        except Exception as e:
            print(f"❌ Ошибка сброса: {e}")
            return None

save_system = SaveSystem()