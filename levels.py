from generator import generate_unique_level
from save_system import save_system

class LevelSystem:
    def __init__(self):
        self.unlocked_levels, self.stars = save_system.load_progress()
    
    def get_level(self, size, level_num):
        return generate_unique_level(size, level_num)
    
    def complete_level(self, size, level, stars_count):
        old = self.stars[size].get(level, 0)
        if stars_count > old:
            self.stars[size][level] = stars_count
        if level < 30 and level == self.unlocked_levels[size]:
            self.unlocked_levels[size] = level + 1
        if self.is_bonus_unlocked():
            self.unlocked_levels[12] = 1
        save_system.save_progress(self.unlocked_levels, self.stars)
    
    def get_total_stars(self, size=None):
        if size: return sum(self.stars[size].values())
        return sum(sum(s.values()) for s in self.stars.values())
    
    def is_bonus_unlocked(self):
        return len(self.stars[3]) + len(self.stars[6]) + len(self.stars[9]) >= 90
    
    def reset_progress(self):
        result = save_system.reset_progress()
        if result: self.unlocked_levels, self.stars = result