import random
import copy

class SudokuGenerator:
    def __init__(self):
        self.used_patterns = {3: [], 6: [], 9: [], 12: []}
        self.max_attempts = 50
    
    def generate(self, size, level_num):
        for _ in range(self.max_attempts):
            if size == 3:
                board = self.generate_3x3(level_num)
            elif size == 6:
                board = self.generate_6x6(level_num)
            elif size == 9:
                board = self.generate_9x9(level_num)
            else:
                board = self.generate_12x12(level_num)
            
            if not self.is_duplicate(board, size):
                pattern = self.board_to_string(board)
                self.used_patterns[size].append(pattern)
                return board
        return self.generate_fallback(size, level_num)
    
    def generate_3x3(self, level_num):
        """Генерирует поле 3x3 с цифрами 1-6"""
        templates = [
            [[1, 2, 3],
             [4, 5, 6],
             [2, 3, 1]],
            
            [[2, 3, 1],
             [5, 6, 4],
             [3, 1, 2]],
            
            [[3, 1, 2],
             [6, 4, 5],
             [1, 2, 3]],
            
            [[4, 5, 6],
             [1, 2, 3],
             [5, 6, 4]],
            
            [[5, 6, 4],
             [2, 3, 1],
             [6, 4, 5]],
            
            [[6, 4, 5],
             [3, 1, 2],
             [4, 5, 6]]
        ]
        
        solution = random.choice(templates)
        
        # Определяем количество цифр
        if level_num <= 10:
            num_clues = 5
        elif level_num <= 20:
            num_clues = 4
        else:
            num_clues = 3
        
        board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        all_positions = [(0,0), (0,1), (0,2), (1,0), (1,1), (1,2), (2,0), (2,1), (2,2)]
        random.shuffle(all_positions)
        clue_positions = all_positions[:num_clues]
        
        for r, c in clue_positions:
            board[r][c] = solution[r][c]
        
        return board
    
    def generate_6x6(self, level_num):
        """Генерирует поле 6x6 с цифрами 1-6 - УСЛОЖНЕННОЕ"""
        # Несколько базовых сложных паттернов для 6x6
        templates = [
            # Паттерн 1 - хаотичный
            [[1, 2, 3, 4, 5, 6],
             [4, 5, 6, 1, 2, 3],
             [2, 3, 1, 5, 6, 4],
             [5, 6, 4, 2, 3, 1],
             [3, 1, 2, 6, 4, 5],
             [6, 4, 5, 3, 1, 2]],
            
            # Паттерн 2 - перетасованный
            [[2, 1, 4, 3, 6, 5],
             [5, 6, 3, 4, 1, 2],
             [1, 3, 2, 5, 4, 6],
             [4, 5, 6, 2, 3, 1],
             [3, 2, 1, 6, 5, 4],
             [6, 4, 5, 1, 2, 3]],
            
            # Паттерн 3 - диагональный
            [[3, 4, 5, 6, 1, 2],
             [6, 1, 2, 3, 4, 5],
             [2, 3, 4, 5, 6, 1],
             [5, 6, 1, 2, 3, 4],
             [1, 2, 3, 4, 5, 6],
             [4, 5, 6, 1, 2, 3]],
            
            # Паттерн 4 - сложный
            [[4, 5, 6, 1, 2, 3],
             [1, 2, 3, 4, 5, 6],
             [6, 1, 2, 3, 4, 5],
             [3, 4, 5, 6, 1, 2],
             [5, 6, 1, 2, 3, 4],
             [2, 3, 4, 5, 6, 1]]
        ]
        
        solution = random.choice(templates)
        
        # Перемешиваем строки в пределах блоков для дополнительной сложности
        for block in range(0, 6, 2):
            rows = list(range(block, block+2))
            random.shuffle(rows)
            temp = [solution[r][:] for r in rows]
            for i, r in enumerate(rows):
                solution[block + i] = temp[i]
        
        # Определяем количество цифр (чем выше уровень, тем меньше подсказок)
        if level_num <= 10:
            num_clues = random.randint(16, 20)  # Легкий: 16-20 цифр
        elif level_num <= 20:
            num_clues = random.randint(12, 16)  # Средний: 12-16 цифр
        else:
            num_clues = random.randint(8, 12)   # Сложный: 8-12 цифр
        
        board = [[0]*6 for _ in range(6)]
        all_positions = [(r, c) for r in range(6) for c in range(6)]
        random.shuffle(all_positions)
        
        # Выбираем позиции так, чтобы они были равномерно распределены
        clue_positions = all_positions[:num_clues]
        
        for r, c in clue_positions:
            board[r][c] = solution[r][c]
        
        print(f"6x6 Уровень {level_num}: {num_clues} подсказок")
        return board
    
    def generate_9x9(self, level_num):
        """Генерирует поле 9x9 с цифрами 1-9 - УСЛОЖНЕННОЕ"""
        # Несколько сложных паттернов для 9x9
        templates = [
            # Паттерн 1 - классический
            [[1, 2, 3, 4, 5, 6, 7, 8, 9],
             [4, 5, 6, 7, 8, 9, 1, 2, 3],
             [7, 8, 9, 1, 2, 3, 4, 5, 6],
             [2, 3, 1, 5, 6, 4, 8, 9, 7],
             [5, 6, 4, 8, 9, 7, 2, 3, 1],
             [8, 9, 7, 2, 3, 1, 5, 6, 4],
             [3, 1, 2, 6, 4, 5, 9, 7, 8],
             [6, 4, 5, 9, 7, 8, 3, 1, 2],
             [9, 7, 8, 3, 1, 2, 6, 4, 5]],
            
            # Паттерн 2 - перетасованный
            [[2, 3, 4, 5, 6, 7, 8, 9, 1],
             [5, 6, 7, 8, 9, 1, 2, 3, 4],
             [8, 9, 1, 2, 3, 4, 5, 6, 7],
             [3, 4, 5, 6, 7, 8, 9, 1, 2],
             [6, 7, 8, 9, 1, 2, 3, 4, 5],
             [9, 1, 2, 3, 4, 5, 6, 7, 8],
             [4, 5, 6, 7, 8, 9, 1, 2, 3],
             [7, 8, 9, 1, 2, 3, 4, 5, 6],
             [1, 2, 3, 4, 5, 6, 7, 8, 9]],
            
            # Паттерн 3 - зигзаг
            [[1, 4, 7, 2, 5, 8, 3, 6, 9],
             [2, 5, 8, 3, 6, 9, 4, 7, 1],
             [3, 6, 9, 4, 7, 1, 5, 8, 2],
             [4, 7, 1, 5, 8, 2, 6, 9, 3],
             [5, 8, 2, 6, 9, 3, 7, 1, 4],
             [6, 9, 3, 7, 1, 4, 8, 2, 5],
             [7, 1, 4, 8, 2, 5, 9, 3, 6],
             [8, 2, 5, 9, 3, 6, 1, 4, 7],
             [9, 3, 6, 1, 4, 7, 2, 5, 8]],
            
            # Паттерн 4 - спиральный
            [[1, 2, 3, 4, 5, 6, 7, 8, 9],
             [6, 7, 8, 9, 1, 2, 3, 4, 5],
             [2, 3, 4, 5, 6, 7, 8, 9, 1],
             [7, 8, 9, 1, 2, 3, 4, 5, 6],
             [3, 4, 5, 6, 7, 8, 9, 1, 2],
             [8, 9, 1, 2, 3, 4, 5, 6, 7],
             [4, 5, 6, 7, 8, 9, 1, 2, 3],
             [9, 1, 2, 3, 4, 5, 6, 7, 8],
             [5, 6, 7, 8, 9, 1, 2, 3, 4]]
        ]
        
        solution = random.choice(templates)
        
        # Перемешиваем строки в пределах блоков для дополнительной сложности
        for block in range(0, 9, 3):
            rows = list(range(block, block+3))
            random.shuffle(rows)
            temp = [solution[r][:] for r in rows]
            for i, r in enumerate(rows):
                solution[block + i] = temp[i]
        
        # Определяем количество цифр (чем выше уровень, тем меньше подсказок)
        if level_num <= 10:
            num_clues = random.randint(30, 35)  # Легкий: 30-35 цифр
        elif level_num <= 20:
            num_clues = random.randint(25, 30)  # Средний: 25-30 цифр
        else:
            num_clues = random.randint(20, 25)  # Сложный: 20-25 цифр
        
        board = [[0]*9 for _ in range(9)]
        all_positions = [(r, c) for r in range(9) for c in range(9)]
        random.shuffle(all_positions)
        
        clue_positions = all_positions[:num_clues]
        
        for r, c in clue_positions:
            board[r][c] = solution[r][c]
        
        print(f"9x9 Уровень {level_num}: {num_clues} подсказок")
        return board
    
    def generate_12x12(self, level_num):
        """Генерирует поле 12x12 (упрощенно для бонуса)"""
        board = [[0]*12 for _ in range(12)]
        
        # Базовая диагональная схема
        for i in range(12):
            for j in range(12):
                board[i][j] = ((i + j) % 12) + 1
        
        # Определяем количество цифр
        if level_num <= 10:
            num_clues = 60
        elif level_num <= 20:
            num_clues = 50
        else:
            num_clues = 40
        
        all_positions = [(r, c) for r in range(12) for c in range(12)]
        random.shuffle(all_positions)
        
        # Создаем копию для удаления
        result = [[0]*12 for _ in range(12)]
        clue_positions = all_positions[:num_clues]
        
        for r, c in clue_positions:
            result[r][c] = board[r][c]
        
        return result
    
    def is_duplicate(self, board, size):
        pattern = self.board_to_string(board)
        return pattern in self.used_patterns[size]
    
    def board_to_string(self, board):
        return ''.join(str(cell) for row in board for cell in row)
    
    def generate_fallback(self, size, level_num):
        """Запасной вариант если все паттерны повторяются"""
        if size == 3:
            return [[1,0,0], [0,2,0], [0,0,3]]
        elif size == 6:
            # Случайная доска с 12 подсказками
            board = [[0]*6 for _ in range(6)]
            positions = [(r,c) for r in range(6) for c in range(6)]
            random.shuffle(positions)
            for i in range(12):
                r, c = positions[i]
                board[r][c] = random.randint(1, 6)
            return board
        elif size == 9:
            # Случайная доска с 25 подсказками
            board = [[0]*9 for _ in range(9)]
            positions = [(r,c) for r in range(9) for c in range(9)]
            random.shuffle(positions)
            for i in range(25):
                r, c = positions[i]
                board[r][c] = random.randint(1, 9)
            return board
        else:
            return [[0]*12 for _ in range(12)]

generator = SudokuGenerator()

def generate_unique_level(size, level_num):
    return generator.generate(size, level_num)