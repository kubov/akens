import queue
import operator
import sys
import sdl2
import sdl2.ext
from time import time, sleep

LEFT = (-1, 0)
RIGHT = (1, 0)
UP = (0, -1)
DOWN = (0, 1)

FPS = 30
SPEED = 16
CELL_SIZE = 10
SNAKE_COLOR = sdl2.ext.Color(0, 0, 0)
BG_COLOR = sdl2.ext.Color(255, 255, 255)
START_DIR = RIGHT
START_SIZE = 5


class World(object):
    def __init__(self, w, h):
        self.data = []
        self.w = w
        self.h = h
        for i in xrange(0, h):
            self.data.append([0] * w)

        self.snake = Snake(self)
        self.sdl_init()

    def set_cell(self, x, y, v):
        self.data[x][y] = v

    def sdl_init(self):
        sdl2.ext.init()
        self.window = sdl2.ext.Window('AKENS', size=(self.w*CELL_SIZE,
                                                     self.h*CELL_SIZE))
        self.window.show()

    def flush(self):
        sdl2.ext.fill(self.window.get_surface(), BG_COLOR)
        for i in xrange(self.h):
            for j in xrange(self.w):
                self.set_cell(i, j, 0)

    def render(self, surface):
        self.flush()
        self.snake.render(surface)

    def run(self):
        self.running = True
        frame_count = 0
        while self.running:
            start = time()
            events = sdl2.ext.get_events()
            for event in events:
                if event.type == sdl2.SDL_QUIT:
                    running = False
                    break
                if event.type == sdl2.SDL_KEYDOWN:
                    self.snake.change_direction(event.key.keysym.sym)

            end = time()

            # Adjust framerate and update snake according to speed
            delta = (1.0/FPS) - (end - start)
            sleep(delta)
            frame_count += 1
            if frame_count > FPS/SPEED:
                frame_count = 0
                self.snake.update()

            self.render(self.window.get_surface())
            self.window.refresh()


class Snake(object):
    def __init__(self, world):
        self.q = queue.Queue()
        self.world = world
        self.size = START_SIZE
        self.direction = START_DIR
        self.head = (world.w/2, world.h/2)

    def change_direction(self, event):
        mapping = {
            sdl2.SDLK_RIGHT: RIGHT,
            sdl2.SDLK_DOWN: DOWN,
            sdl2.SDLK_UP: UP,
            sdl2.SDLK_LEFT: LEFT
        }

        opposite = {
            RIGHT: LEFT,
            UP: DOWN,
            LEFT: RIGHT,
            DOWN: UP
        }

        if event in mapping is False:
            return

        direction = mapping[event]
        self.direction = direction if self.direction != opposite[direction] else self.direction

    def update(self):
        self.head = map(operator.add, self.head, self.direction)
        self.q.enqueue(self.head)

        if self.q.size() == self.size:
            self.q.dequeue()

    def render(self, surface):
        l = self.q.to_array()

        for x, y in l:
            sdl2.ext.fill(surface, SNAKE_COLOR, (x * CELL_SIZE,
                                                 y * CELL_SIZE,
                                                 CELL_SIZE,
                                                 CELL_SIZE))


w = World(80, 60)
w.run()
