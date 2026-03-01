from generator import generate_unique_level
from save_system import save_system

class LevelSystem:
    def __init__(self):
        self.unlocked_levels, self.stars, self.mode_stats = save_system.load_progress()
        # Для 12x12 максимум 1 уровень
        if 12 in self.unlocked_levels and self.unlocked_levels[12] > 1:
            self.unlocked_levels[12] = min(self.unlocked_levels[12], 1)
    
    def get_level(self, size, level_num):
        # Для 12x12 всегда уровень 1
        if size == 12:
            level_num = 1
        return generate_unique_level(size, level_num)
    
    def complete_level(self, size, level, stars_count, game_mode='trial', elapsed_time=None):
        # Сохраняем звезды за уровень
        old = self.stars[size].get(level, 0)
        if stars_count > old:
            self.stars[size][level] = stars_count
        
        # Открываем следующий уровень (кроме 12x12)
        if size != 12 and level < 30 and level == self.unlocked_levels[size]:
            self.unlocked_levels[size] = level + 1
        
        # Открываем 12x12 если нужно
        if self.is_bonus_unlocked() and self.unlocked_levels[12] == 0:
            self.unlocked_levels[12] = 1
            print("🎉 Бонусный уровень 12x12 открыт!")
        
        # Обновляем статистику режима
        if game_mode in self.mode_stats:
            self.mode_stats[game_mode]['games'] += 1
            if stars_count > 0:
                self.mode_stats[game_mode]['wins'] += 1
            
            if game_mode != 'study' and elapsed_time:
                best = self.mode_stats[game_mode].get('best_time')
                if best is None or elapsed_time < best:
                    self.mode_stats[game_mode]['best_time'] = round(elapsed_time, 1)
                
                self.mode_stats[game_mode]['total_stars'] = \
                    self.mode_stats[game_mode].get('total_stars', 0) + stars_count
        
        save_system.save_progress(self.unlocked_levels, self.stars, self.mode_stats)
    
    def get_total_stars(self, size=None):
        if size: 
            return sum(self.stars[size].values())
        return sum(sum(s.values()) for s in self.stars.values())
    
    def is_bonus_unlocked(self):
        # Для открытия 12x12 нужно 270 звезд
        return self.get_total_stars() >= 270
    
    def reset_progress(self):
        result = save_system.reset_progress()
        if result: 
            self.unlocked_levels, self.stars, self.mode_stats = result