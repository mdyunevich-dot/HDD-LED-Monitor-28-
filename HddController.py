import time

class HddLedMonitor:
    """Класс индикатора жесткого диска (HDD LED)"""
    def __init__(self, x, y, radius=45):
        self.x = x
        self.y = y
        self.radius = radius
        self.state = 'idle'  # Состояния: 'idle', 'read', 'write'
        self.last_action_time = time.time()
        self.blink_interval = 0.1  # Скорость мигания (в секундах)

    def trigger_action(self, mode):
        """Активирует режим чтения или записи и сбрасывает таймер"""
        self.state = mode
        self.last_action_time = time.time()

    def update(self):
        """Проверяет таймер бездействия. Спустя 2 секунды переводит в idle"""
        if self.state != 'idle' and time.time() - self.last_action_time > 2.0:
            self.state = 'idle'

    def get_current_color(self, colors):
        """Возвращает цвет светодиода с учетом эффекта мигания"""
        if self.state == 'idle':
            return colors['IDLE']
        
        # Эффект мигания на основе деления системного времени
        is_on = int(time.time() / self.blink_interval) % 2 == 0
        
        if self.state == 'read':
            return colors['READ'] if is_on else colors['IDLE']
        if self.state == 'write':
            return colors['WRITE'] if is_on else colors['IDLE']
            
        return colors['IDLE']
