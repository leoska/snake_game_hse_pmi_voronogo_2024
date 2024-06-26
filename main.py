import asyncio
import pygame
import sys
from random import randrange

RES = 800
SIZE = 50

pygame.init()


class Snake:
    body: list[tuple[int, int]]
    speed: int = 10
    speed_count: int = 0
    pos: list[int]
    len: int = 1

    def __init__(self):
        x = randrange(SIZE, RES - SIZE, SIZE)
        y = randrange(SIZE, RES - SIZE, SIZE)
        self.pos = [x, y]
        self.body = [(self.pos[0], self.pos[1])]
        self.speed = 10
        self.speed_count = 0
        self.len = 1

    def update(self, dx: int, dy: int):
        global apple
        global score

        self.speed_count += 1
        if not self.speed_count % self.speed:
            self.pos[0] += dx * SIZE
            self.pos[1] += dy * SIZE
            self.body.append((self.pos[0], self.pos[1]))
            self.body = self.body[-self.len:]

        # eating food
        if self.body[-1] == apple.pos:
            apple = Apple()
            self.len += 1
            score += 1
            self.speed -= 1
            self.speed = max(self.speed, 4)

    def draw(self, screen):
        [pygame.draw.rect(screen, pygame.Color('green'), (i, j, SIZE - 1, SIZE - 1)) for i, j in self.body]


class Apple:
    def __init__(self):
        self.pos = randrange(SIZE, RES - SIZE, SIZE), randrange(SIZE, RES - SIZE, SIZE)

    def draw(self, screen):
        pygame.draw.rect(screen, pygame.Color('red'), (*self.pos, SIZE, SIZE))


class GUI:
    button_up = ((75, 650), (50, 700), (100, 700))
    button_down = ((75, 800), (50, 750), (100, 750))
    button_left = ((0, 725), (50, 700), (50, 750))
    button_right = ((150, 725), (100, 700), (100, 750))

    def __init__(self):
        self.font_score = pygame.font.SysFont('Arial', 26, bold=True)
        self.font_end = pygame.font.SysFont('Arial', 66, bold=True)

    def update(self, event_pos: tuple[int, int]):
        global touch

        print(event_pos)

        touch['up'] = 50 <= event_pos[0] <= 100 and 650 <= event_pos[1] <= 700
        touch['down'] = 50 <= event_pos[0] <= 100 and 750 <= event_pos[1] <= 800
        touch['left'] = 0 <= event_pos[0] <= 50 and 700 <= event_pos[1] <= 750
        touch['right'] = 100 <= event_pos[0] <= 150 and 700 <= event_pos[1] <= 750

    def draw(self, screen):
        render_score = self.font_score.render(f'SCORE: {score}', 1, pygame.Color('orange'))
        screen.blit(render_score, (5, 5))

        pygame.draw.polygon(screen, pygame.Color('blue'), GUI.button_up)
        pygame.draw.polygon(screen, pygame.Color('blue'), GUI.button_down)
        pygame.draw.polygon(screen, pygame.Color('blue'), GUI.button_left)
        pygame.draw.polygon(screen, pygame.Color('blue'), GUI.button_right)


    def draw_game_over(self, screen):
        render_end = self.font_end.render('GAME OVER', 1, pygame.Color('orange'))
        screen.blit(render_end, (RES // 2 - 200, RES // 3))


def draw_grid(screen):
    for x in range(0, RES, SIZE):
        for y in range(0, RES, SIZE):
            rect = pygame.Rect(x, y, SIZE, SIZE)
            pygame.draw.rect(screen, "#3c3c3b", rect, 1)


def close_game():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()


fps = 60
dirs = {'W': True, 'S': True, 'A': True, 'D': True, }
score = 0
apple = Apple()
snake = Snake()
touch = {}

screen = pygame.display.set_mode([RES, RES])
clock = pygame.time.Clock()


async def main():
    gui = GUI()
    dx, dy = 0, 0

    global dirs
    global snake
    global apple
    global screen
    global clock

    while True:
        # Update

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type in (pygame.MOUSEBUTTONDOWN, pygame.FINGERDOWN, pygame.FINGERMOTION, pygame.FINGERUP):
                gui.update(event.pos)

        # snake movement keyboard
        key = pygame.key.get_pressed()
        if key[pygame.K_w] or touch.get('up'):
            if dirs['W']:
                dx, dy = 0, -1
                dirs = {'W': True, 'S': False, 'A': True, 'D': True, }
        elif key[pygame.K_s] or touch.get('down'):
            if dirs['S']:
                dx, dy = 0, 1
                dirs = {'W': False, 'S': True, 'A': True, 'D': True, }
        elif key[pygame.K_a] or touch.get('left'):
            if dirs['A']:
                dx, dy = -1, 0
                dirs = {'W': True, 'S': True, 'A': True, 'D': False, }
        elif key[pygame.K_d] or touch.get('right'):
            if dirs['D']:
                dx, dy = 1, 0
                dirs = {'W': True, 'S': True, 'A': False, 'D': True, }

        snake.update(dx, dy)

        # Game over
        if snake.pos[0] < 0 or snake.pos[0] > RES - SIZE or snake.pos[1] < 0 or snake.pos[1] > RES - SIZE or len(snake.body) != len(set(snake.body)):
            while True:
                close_game()

                gui.draw_game_over(screen)
                pygame.display.update()
                await asyncio.sleep(0)

        close_game()
        # Draw
        screen.fill((0, 0, 0))
        draw_grid(screen)
        snake.draw(screen)
        apple.draw(screen)
        gui.draw(screen)

        pygame.display.update()
        clock.tick(fps)

        await asyncio.sleep(0)

asyncio.run(main())
