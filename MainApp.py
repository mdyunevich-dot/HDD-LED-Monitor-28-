import pygame
import sys
# Импортируем наш логический модуль из соседнего файла
from HddController import HddLedMonitor

# Инициализация Pygame
pygame.init()
pygame.font.init()

# Константы графического интерфейса
COLOR_BG = (30, 30, 30)
COLOR_TEXT = (255, 255, 255)
COLOR_TAB_ACTIVE = (60, 60, 60)
COLOR_TAB_INACTIVE = (45, 45, 45)
COLOR_BTN = (70, 130, 180)
COLOR_BTN_HOVER = (100, 149, 237)

# Словарь цветов для индикатора
LED_COLORS = {
    'IDLE': (128, 128, 128),   # Серый
    'READ': (0, 255, 0),       # Зеленый
    'WRITE': (255, 0, 0)       # Красный
}

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 400
FONT_SIZE = 18

class Button:
    """Класс графической кнопки интерфейса"""
    def __init__(self, x, y, width, height, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = pygame.font.SysFont('Arial', FONT_SIZE)

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        color = COLOR_BTN_HOVER if self.rect.collidepoint(mouse_pos) else COLOR_BTN
        pygame.draw.rect(screen, color, self.rect, border_radius=5)
        
        text_surf = self.font.render(self.text, True, COLOR_TEXT)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def is_clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.rect.collidepoint(event.pos)

class TabManager:
    """Класс управления вкладками приложения"""
    def __init__(self):
        self.tabs = ["Вкладка 1", "Вкладка 2"]
        self.active_tab_idx = 0
        self.tab_rects = [
            pygame.Rect(10, 10, 120, 35),
            pygame.Rect(135, 10, 120, 35)
        ]
        self.font = pygame.font.SysFont('Arial', FONT_SIZE)

    def draw(self, screen):
        for i, rect in enumerate(self.tab_rects):
            color = COLOR_TAB_ACTIVE if i == self.active_tab_idx else COLOR_TAB_INACTIVE
            pygame.draw.rect(screen, color, rect, border_top_left_radius=5, border_top_right_radius=5)
            
            text_surf = self.font.render(self.tabs[i], True, COLOR_TEXT)
            text_rect = text_surf.get_rect(center=rect.center)
            screen.blit(text_surf, text_rect)

    def check_click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for i, rect in enumerate(self.tab_rects):
                if rect.collidepoint(event.pos):
                    self.active_tab_idx = i

class App:
    """Главный класс приложения"""
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("HDD LED Monitor — Вариант 28")
        self.clock = pygame.time.Clock()
        self.running = True

        # Инициализация объектов
        self.tab_manager = TabManager()
        self.led_monitor = HddLedMonitor(SCREEN_WIDTH // 2, 280, radius=45)
        
        self.btn_read = Button(150, 100, 200, 40, "Чтение данных")
        self.btn_write = Button(150, 100, 200, 40, "Запись данных")

    def run(self):
        while self.running:
            self.clock.tick(60)
            self.handle_events()
            self.led_monitor.update()
            self.draw()

        pygame.quit()
        sys.exit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            self.tab_manager.check_click(event)

            if self.tab_manager.active_tab_idx == 0:
                if self.btn_read.is_clicked(event):
                    self.led_monitor.trigger_action('read')
            elif self.tab_manager.active_tab_idx == 1:
                if self.btn_write.is_clicked(event):
                    self.led_monitor.trigger_action('write')

    def draw(self):
        self.screen.fill(COLOR_BG)
        self.tab_manager.draw(self.screen)
        pygame.draw.line(self.screen, COLOR_TAB_ACTIVE, (0, 45), (SCREEN_WIDTH, 45), 2)

        if self.tab_manager.active_tab_idx == 0:
            self.btn_read.draw(self.screen)
        elif self.tab_manager.active_tab_idx == 1:
            self.btn_write.draw(self.screen)

        # Получаем динамический цвет из контроллера и рисуем лампочку
        current_color = self.led_monitor.get_current_color(LED_COLORS)
        pygame.draw.circle(self.screen, current_color, (self.led_monitor.x, self.led_monitor.y), self.led_monitor.radius)
        pygame.draw.circle(self.screen, (200, 200, 200), (self.led_monitor.x, self.led_monitor.y), self.led_monitor.radius, 2)
        
        pygame.display.flip()

if __name__ == "__main__":
    app = App()
    app.run()
