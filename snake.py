import random
import pygame
import time


class SnakePart:
    def __init__(self, position):
        self.rect = pygame.Rect(position[0], position[1], 16, 16)


class SnakeHeadOnly(SnakePart):
    def __init__(self, position):
        SnakePart.__init__(self, position)
        self.image = pygame.image.load(r"C:\Users\skyfo\OneDrive - Technion\python\Python Snake\artwork\round_head.png")


class SnakeHead(SnakePart):
    def __init__(self, position):
        SnakePart.__init__(self, position)
        self.image = pygame.image.load(r"C:\Users\skyfo\OneDrive - Technion\python\Python Snake\artwork\head.png")


class SnakeBody(SnakePart):
    def __init__(self, position):
        SnakePart.__init__(self, position)
        self.image = pygame.image.load(r"C:\Users\skyfo\OneDrive - Technion\python\Python Snake\artwork\body.png")


class SnakeBodyRound(SnakePart):
    def __init__(self, position):
        SnakePart.__init__(self, position)
        self.image = pygame.image.load(r"C:\Users\skyfo\OneDrive - Technion\python\Python Snake\artwork\body_round.png")


class SnakeTail(SnakePart):
    def __init__(self, position):
        SnakePart.__init__(self, position)
        self.image = pygame.image.load(r"C:\Users\skyfo\OneDrive - Technion\python\Python Snake\artwork\tail.png")


class Apple:
    def __init__(self):
        self.image = pygame.image.load(r"C:\Users\skyfo\OneDrive - Technion\python\Python Snake\artwork\apple.png")

    def create_food(self, display, coordinates, borders):
        timer = []
        food = (round(random.randint(16, borders[0]-32)/16)*16, round(random.randint(16, borders[1]-32)/16)*16)
        while food in coordinates:
            food = (round(random.randint(16, borders[0]-32)/16)*16, round(random.randint(16, borders[1]-32)/16)*16)
        food_flag = True
        self.rect = pygame.Rect(food[0], food[1], 16, 16)
        display.blit(self.image, self.rect)
        pygame.display.update()
        timer.append(time.time())
        return food, food_flag, timer

    def blink(self, display, food, food_flag, timer):
        timer.append(time.time())
        diff_time = round(timer[-1] - timer[0])
        if food_flag and diff_time >= 3:
            if not diff_time % 2:
                pygame.draw.rect(display, (0, 0, 0), [food[0], food[1], 16, 16])
                self.image.set_alpha(100)
                display.blit(self.image, pygame.Rect([food[0], food[1], 16, 16]))
                pygame.display.update()
            else:
                pygame.draw.rect(display, (0, 0, 0), [food[0], food[1], 16, 16])
                self.image.set_alpha(255)
                display.blit(self.image, pygame.Rect([food[0], food[1], 16, 16]))
                pygame.display.update()
            if not diff_time % 9:
                pygame.draw.rect(display, (0, 0, 0), [food[0], food[1], 16, 16])
                food = ()
                food_flag = False
        return food, food_flag


class Snake:
    def __init__(self, display, coordinates):
        self.draw_snake(display, coordinates, 'up')
        pygame.display.update()

    def advance(self, display, direction, coordinates, food, food_flag, score):
        prev_coordinates = coordinates.copy()
        if direction == 'up':
            coordinates.insert(0, (coordinates[0][0], coordinates[0][1] - 16))
        elif direction == 'down':
            coordinates.insert(0, (coordinates[0][0], coordinates[0][1] + 16))
        elif direction == 'right':
            coordinates.insert(0, (coordinates[0][0] + 16, coordinates[0][1]))
        elif direction == 'left':
            coordinates.insert(0, (coordinates[0][0] - 16, coordinates[0][1]))
        if coordinates[0] != food:
            drop = coordinates.pop()
            pygame.draw.rect(display, (0, 0, 0), [drop[0], drop[1], 16, 16])
        else:
            food_flag = False
            score += 1
        self.draw_snake(disp, coordinates, direction)
        return coordinates, food_flag, prev_coordinates, score

    def dont_cross(self, coordinates, direction, borders, prev_coordinates):
        # borders
        if coordinates[0][0] == 0 or coordinates[0][0] == borders[0]-16 or coordinates[0][1] == 0 or coordinates[0][1] == borders[1]-16:
            direction = ''
        # self
        if coordinates[0] in prev_coordinates:
            direction = ''
        return direction

    def rotate_image(self, img, direction):
        if direction == 'up':
            rot_image = img.image
        elif direction == 'down':
            rot_image = pygame.transform.rotate(img.image, 180)
        elif direction == 'right':
            rot_image = pygame.transform.rotate(img.image, 270)
        elif direction == 'left':
            rot_image = pygame.transform.rotate(img.image, 90)
        return rot_image

    def draw_head(self, display, head_type, direction):
        head_image = self.rotate_image(head_type, direction)
        display.blit(head_image, head_type.rect)

    def draw_tail(self, display, coordinates, idx, coord_set):
        snake_tail = SnakeTail(coordinates[-1])
        if coordinates[idx - 1][0] == coord_set[0] and coordinates[idx - 1][1] < coord_set[1]:
            # tail facing up
            pygame.draw.rect(display, (0, 0, 0), [coord_set[0], coord_set[1], 16, 16])
            tail_image = self.rotate_image(snake_tail, 'up')
            display.blit(tail_image, snake_tail.rect)
        elif coordinates[idx - 1][0] == coord_set[0] and coordinates[idx - 1][1] > coord_set[1]:
            # tail facing down
            pygame.draw.rect(display, (0, 0, 0), [coord_set[0], coord_set[1], 16, 16])
            tail_image = self.rotate_image(snake_tail, 'down')
            display.blit(tail_image, snake_tail.rect)
        elif coordinates[idx - 1][1] == coord_set[1] and coordinates[idx - 1][0] < coord_set[0]:
            # tail facing left
            pygame.draw.rect(display, (0, 0, 0), [coord_set[0], coord_set[1], 16, 16])
            tail_image = self.rotate_image(snake_tail, 'left')
            display.blit(tail_image, snake_tail.rect)
        elif coordinates[idx - 1][1] == coord_set[1] and coordinates[idx - 1][0] > coord_set[0]:
            # tail facing right
            pygame.draw.rect(display, (0, 0, 0), [coord_set[0], coord_set[1], 16, 16])
            tail_image = self.rotate_image(snake_tail, 'right')
            display.blit(tail_image, snake_tail.rect)

    def draw_body(self, display, coordinates, idx, coord_set):
        snake_body = SnakeBody(coordinates[0])
        snake_body_round = SnakeBodyRound(coordinates[0])
        if coordinates[idx - 1][0] == coord_set[0] == coordinates[idx + 1][0]:
            pygame.draw.rect(display, (0, 0, 0), [coord_set[0], coord_set[1], 16, 16])
            display.blit(snake_body.image, pygame.Rect([coord_set[0], coord_set[1], 16, 16]))
        elif coordinates[idx - 1][1] == coord_set[1] == coordinates[idx + 1][1]:
            pygame.draw.rect(display, (0, 0, 0), [coord_set[0], coord_set[1], 16, 16])
            snake_body_side = pygame.transform.rotate(snake_body.image, 90)
            display.blit(snake_body_side, pygame.Rect([coord_set[0], coord_set[1], 16, 16]))
        elif (coordinates[idx - 1][0] > coord_set[0] and coordinates[idx + 1][1] > coord_set[1]) or (
                coordinates[idx - 1][1] > coord_set[1] and coordinates[idx + 1][0] > coord_set[0]):
            pygame.draw.rect(display, (0, 0, 0), [coord_set[0], coord_set[1], 16, 16])
            body_image = self.rotate_image(snake_body_round, 'up')
            display.blit(body_image, pygame.Rect([coord_set[0], coord_set[1], 16, 16]))
        elif (coordinates[idx - 1][1] < coord_set[1] and coordinates[idx + 1][0] < coord_set[0]) or (
                coordinates[idx - 1][0] < coord_set[0] and coordinates[idx + 1][1] < coord_set[1]):
            pygame.draw.rect(display, (0, 0, 0), [coord_set[0], coord_set[1], 16, 16])
            body_image = self.rotate_image(snake_body_round, 'down')
            display.blit(body_image, pygame.Rect([coord_set[0], coord_set[1], 16, 16]))
        elif (coordinates[idx - 1][0] > coord_set[0] and coordinates[idx + 1][1] < coord_set[1]) or (
                coordinates[idx - 1][1] < coord_set[1] and coordinates[idx + 1][0] > coord_set[0]):
            pygame.draw.rect(display, (0, 0, 0), [coord_set[0], coord_set[1], 16, 16])
            body_image = self.rotate_image(snake_body_round, 'left')
            display.blit(body_image, pygame.Rect([coord_set[0], coord_set[1], 16, 16]))
        else:
            pygame.draw.rect(display, (0, 0, 0), [coord_set[0], coord_set[1], 16, 16])
            body_image = self.rotate_image(snake_body_round, 'right')
            display.blit(body_image, pygame.Rect([coord_set[0], coord_set[1], 16, 16]))

    def draw_snake(self, display, coordinates, direction):
        if len(coordinates) == 1: # only head
            self.draw_head(display, SnakeHeadOnly(coordinates[0]), direction)
        elif len(coordinates) == 2: # head and tail
            for idx, coord_set in enumerate(coordinates):
                if idx == 0:
                    self.draw_head(display, SnakeHead(coordinates[0]), direction)
                else:
                    self.draw_tail(display, coordinates, idx, coord_set)
        else: # head, body and tail
            for idx, coord_set in enumerate(coordinates):
                if idx == 0:
                    self.draw_head(display, SnakeHead(coordinates[0]), direction)
                elif idx == len(coordinates)-1:
                    self.draw_tail(display, coordinates, idx, coord_set)
                else:
                    self.draw_body(display, coordinates, idx, coord_set)
        pygame.display.update()


def score_display(display, borders, score=0):
    score_font = pygame.font.SysFont("silkscreennormal", 25)
    value = score_font.render("Score: " + str(score), True, (0, 0, 0))
    pygame.draw.lines(surface=display, color=(50, 153, 213), closed=True, points=[(0, 0), (0, borders[1]), borders, (borders[0], 0)], width=31)
    display.blit(value, [0, 0])
    pygame.display.update()


def initialize_screen():
    pygame.init()
    borders = (30*16, 30*16)
    disp = pygame.display.set_mode(borders)
    pygame.draw.lines(surface=disp, color=(50, 153, 213), closed=True, points=[(0, 0), (0, borders[1]), borders, (borders[0], 0)], width=31)
    pygame.display.set_caption('Snake by LitalB')
    programIcon = pygame.image.load(r"C:\Users\skyfo\OneDrive - Technion\python\Python Snake\artwork\round_head.png")
    pygame.display.set_icon(programIcon)
    quit_flag = False
    game_over_flag = False
    food_flag = False
    food = ()
    coordinates = [(borders[0] / 2, borders[1] / 2)]
    direction = ''
    snake = Snake(disp, coordinates)
    score = 0
    return borders, disp, quit_flag, game_over_flag, food_flag, food, coordinates, direction, snake, score


def game_over(display, borders, food, coordinates, direction, snake, quit_flag, game_over_flag, food_flag, score):
    image = pygame.image.load(r"C:\Users\skyfo\OneDrive - Technion\python\Python Snake\artwork\game_over.png")
    display.blit(image, [borders[0]/2-150, borders[1]/2-81.5])
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit_flag = True
            game_over_flag = True
            food_flag = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                quit_flag = True
                game_over_flag = True
                food_flag = True
            elif event.key == pygame.K_r:
                borders, display, quit_flag, game_over_flag, food_flag, food, coordinates, direction, snake, score = initialize_screen()
    return borders, display, quit_flag, game_over_flag, food_flag, food, coordinates, direction, snake, score


def play_game(borders, disp, quit_flag, game_over_flag, food_flag, food, coordinates, direction, snake, score):
    image = pygame.image.load(r"C:\Users\skyfo\OneDrive - Technion\python\Python Snake\artwork\arrows.png")
    disp.blit(image, [borders[0]/2-150, borders[1]/2-81.5])
    pygame.display.update()
    clock = pygame.time.Clock()
    clock.tick(0.3)
    disp.fill((0, 0, 0))
    snake.draw_snake(disp, coordinates, 'up')
    timer = []
    while not quit_flag:
        while not game_over_flag:
            score_display(disp, borders, score)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit_flag = True
                    return quit_flag
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        direction = 'up'
                    elif event.key == pygame.K_DOWN:
                        direction = 'down'
                    elif event.key == pygame.K_RIGHT:
                        direction = 'right'
                    elif event.key == pygame.K_LEFT:
                        direction = 'left'
            if direction:
                coordinates, food_flag, prev_coordinates, score = snake.advance(disp, direction, coordinates, food, food_flag, score)
                direction = snake.dont_cross(coordinates, direction, borders, prev_coordinates)
                clock.tick(10)
                if not direction:
                    game_over_flag = True
                if not food_flag:
                    apple = Apple()
                    food, food_flag, timer = apple.create_food(disp, coordinates, borders)
                try:
                    food, food_flag = apple.blink(disp, food, food_flag, timer)
                except:
                    pass
        if game_over_flag:
            borders, disp, quit_flag, game_over_flag, food_flag, food, coordinates, direction, snake, score = game_over(disp, borders, food, coordinates, direction, snake, quit_flag, game_over_flag, food_flag, score)
    pygame.quit()
    quit()


borders, disp, quit_flag, game_over_flag, food_flag, food, coordinates, direction, snake, score = initialize_screen()
play_game(borders, disp, quit_flag, game_over_flag, food_flag, food, coordinates, direction, snake, score)
