import random

class SudokuGenerator:
    def __init__(self):
        self.used_patterns = {3: [], 6: [], 9: [], 12: []}
        
        # ===== ШАБЛОН ДЛЯ 12x12 (ТОЛЬКО ОДИН) =====
        self.template_12x12 = [
            [1,2,3,4,5,6,7,8,9,10,11,12],
            [4,5,6,7,8,9,10,11,12,1,2,3],
            [7,8,9,10,11,12,1,2,3,4,5,6],
            [10,11,12,1,2,3,4,5,6,7,8,9],
            [2,3,4,5,6,7,8,9,10,11,12,1],
            [5,6,7,8,9,10,11,12,1,2,3,4],
            [8,9,10,11,12,1,2,3,4,5,6,7],
            [11,12,1,2,3,4,5,6,7,8,9,10],
            [3,4,5,6,7,8,9,10,11,12,1,2],
            [6,7,8,9,10,11,12,1,2,3,4,5],
            [9,10,11,12,1,2,3,4,5,6,7,8],
            [12,1,2,3,4,5,6,7,8,9,10,11]
        ]
        
        # ===== ШАБЛОНЫ ДЛЯ 9x9 =====
        self.templates_9x9 = [
            [
                [1,2,3,4,5,6,7,8,9],
                [4,5,6,7,8,9,1,2,3],
                [7,8,9,1,2,3,4,5,6],
                [2,3,1,5,6,4,8,9,7],
                [5,6,4,8,9,7,2,3,1],
                [8,9,7,2,3,1,5,6,4],
                [3,1,2,6,4,5,9,7,8],
                [6,4,5,9,7,8,3,1,2],
                [9,7,8,3,1,2,6,4,5]
            ],
            [
                [9,8,7,6,5,4,3,2,1],
                [6,5,4,3,2,1,9,8,7],
                [3,2,1,9,8,7,6,5,4],
                [8,7,6,5,4,3,2,1,9],
                [5,4,3,2,1,9,8,7,6],
                [2,1,9,8,7,6,5,4,3],
                [7,6,5,4,3,2,1,9,8],
                [4,3,2,1,9,8,7,6,5],
                [1,9,8,7,6,5,4,3,2]
            ]
        ]
        
        # ===== ШАБЛОНЫ ДЛЯ 6x6 =====
        self.templates_6x6 = [
            [
                [1,2,3,4,5,6],
                [4,5,6,1,2,3],
                [2,3,1,5,6,4],
                [5,6,4,2,3,1],
                [3,1,2,6,4,5],
                [6,4,5,3,1,2]
            ],
            [
                [6,5,4,3,2,1],
                [3,2,1,6,5,4],
                [5,4,6,2,1,3],
                [2,1,3,5,4,6],
                [4,6,5,1,3,2],
                [1,3,2,4,6,5]
            ]
        ]
        
        # ===== ШАБЛОНЫ ДЛЯ 3x3 =====
        self.templates_3x3 = [
            [[1,2,3], [4,5,6], [2,3,1]],
            [[2,3,1], [5,6,4], [3,1,2]],
            [[3,1,2], [6,4,5], [1,2,3]],
            [[4,5,6], [1,2,3], [5,6,4]],
            [[5,6,4], [2,3,1], [6,4,5]],
            [[6,4,5], [3,1,2], [4,5,6]]
        ]
    
    # ===== 12x12 - БОНУСНЫЙ УРОВЕНЬ (ТОЛЬКО 1) =====
    def generate_12x12(self):
        """Генерирует супер-легкий бонусный уровень - почти полностью заполненный"""
        
        # Берем готовый шаблон
        puzzle = [row[:] for row in self.template_12x12]
        
        # Делаем пустыми только 8-12 клеток
        all_positions = [(r, c) for r in range(12) for c in range(12)]
        random.shuffle(all_positions)
        
        empty_cells = random.randint(8, 12)
        
        for i in range(empty_cells):
            r, c = all_positions[i]
            puzzle[r][c] = 0
        
        # Проверяем, чтобы в каждой строке было не больше 2 пустых клеток
        for r in range(12):
            empty_in_row = [c for c in range(12) if puzzle[r][c] == 0]
            if len(empty_in_row) > 2:
                for c in empty_in_row[2:]:
                    puzzle[r][c] = self.template_12x12[r][c]
        
        # Проверяем столбцы
        for c in range(12):
            empty_in_col = [r for r in range(12) if puzzle[r][c] == 0]
            if len(empty_in_col) > 2:
                for r in empty_in_col[2:]:
                    puzzle[r][c] = self.template_12x12[r][c]
        
        final_empty = sum(1 for r in range(12) for c in range(12) if puzzle[r][c] == 0)
        print(f"🎁 Бонусный уровень 12x12: {final_empty} пустых клеток")
        
        return puzzle
    
    # ===== 9x9 =====
    def generate_9x9(self, level_num):
        """Генерирует поле 9x9"""
        
        template = random.choice(self.templates_9x9)
        board = [row[:] for row in template]
        
        # Количество подсказок зависит от уровня
        if level_num <= 10:
            clues = random.randint(32, 36)
        elif level_num <= 20:
            clues = random.randint(28, 32)
        else:
            clues = random.randint(24, 28)
        
        puzzle = [[0]*9 for _ in range(9)]
        all_positions = [(r, c) for r in range(9) for c in range(9)]
        random.shuffle(all_positions)
        
        for i in range(clues):
            r, c = all_positions[i]
            puzzle[r][c] = board[r][c]
        
        return puzzle
    
    # ===== 6x6 =====
    def generate_6x6(self, level_num):
        """Генерирует поле 6x6"""
        
        template = random.choice(self.templates_6x6)
        board = [row[:] for row in template]
        
        if level_num <= 10:
            clues = random.randint(16, 20)
        elif level_num <= 20:
            clues = random.randint(12, 16)
        else:
            clues = random.randint(8, 12)
        
        puzzle = [[0]*6 for _ in range(6)]
        all_positions = [(r, c) for r in range(6) for c in range(6)]
        random.shuffle(all_positions)
        
        for i in range(clues):
            r, c = all_positions[i]
            puzzle[r][c] = board[r][c]
        
        return puzzle
    
    # ===== 3x3 =====
    def generate_3x3(self, level_num):
        """Генерирует поле 3x3"""
        
        template = random.choice(self.templates_3x3)
        
        if level_num <= 10:
            clues = 5
        elif level_num <= 20:
            clues = 4
        else:
            clues = 3
        
        puzzle = [[0,0,0], [0,0,0], [0,0,0]]
        all_positions = [(r,c) for r in range(3) for c in range(3)]
        random.shuffle(all_positions)
        
        for i in range(clues):
            r, c = all_positions[i]
            puzzle[r][c] = template[r][c]
        
        return puzzle
    
    # ===== ОСНОВНОЙ МЕТОД =====
    def generate(self, size, level_num):
        """Основной метод генерации"""
        
        if size == 3:
            board = self.generate_3x3(level_num)
        elif size == 6:
            board = self.generate_6x6(level_num)
        elif size == 9:
            board = self.generate_9x9(level_num)
        else:  # size == 12
            board = self.generate_12x12()
        
        # Проверка на дубликаты
        pattern = ''.join(str(cell) for row in board for cell in row)
        if pattern not in self.used_patterns[size]:
            self.used_patterns[size].append(pattern)
            return board
        
        # Если дубликат, пробуем еще раз (до 3 попыток)
        for _ in range(3):
            if size == 3:
                board = self.generate_3x3(level_num)
            elif size == 6:
                board = self.generate_6x6(level_num)
            elif size == 9:
                board = self.generate_9x9(level_num)
            else:
                board = self.generate_12x12()
            
            pattern = ''.join(str(cell) for row in board for cell in row)
            if pattern not in self.used_patterns[size]:
                self.used_patterns[size].append(pattern)
                return board
        
        return board

generator = SudokuGenerator()

def generate_unique_level(size, level_num):
    return generator.generate(size, level_num)