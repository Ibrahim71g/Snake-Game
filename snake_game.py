import random
import curses

class Snake:
    def __init__(self, sh, sw):
        self.position = [[sh // 2, sw // 4], [sh // 2, sw // 4 - 1], [sh // 2, sw // 4 - 2]]
        self.length = 3
        self.direction = curses.KEY_RIGHT

    def move(self):
        new_head = [self.position[0][0], self.position[0][1]]
        if self.direction == curses.KEY_DOWN:
            new_head[0] += 1
        if self.direction == curses.KEY_UP:
            new_head[0] -= 1
        if self.direction == curses.KEY_LEFT:
            new_head[1] -= 1
        if self.direction == curses.KEY_RIGHT:
            new_head[1] += 1
        return new_head

    def grow(self):
        self.length += 1

    def check_collision(self, new_head, sh, sw):
        return new_head[0] in [0, sh] or new_head[1] in [0, sw] or new_head in self.position

    def render(self, w):
        for i in range(len(self.position)):
            y, x = self.position[i]
            if i == 0:
                # Head of the snake
                if self.direction in [curses.KEY_LEFT, curses.KEY_RIGHT]:
                    w.addch(int(y), int(x), '■')  # Horizontal head
                else:
                    w.addch(int(y), int(x), '█')  # Vertical head
            else:
                # Body of the snake
                if self.position[i-1][0] == y:  # Same row (horizontal)
                    w.addch(int(y), int(x), '■')
                else:  # Different row (vertical)
                    w.addch(int(y), int(x), '█')

class Food:
    def __init__(self, sh, sw):
        self.position = [sh // 2, sw // 2]

    def spawn(self, sh, sw):
        self.position = [random.randint(1, sh - 1), random.randint(1, sw - 1)]

class Game:
    def __init__(self, sh, sw):
        self.snake = Snake(sh, sw)
        self.food = Food(sh, sw)
        self.score = 0
        self.w = curses.newwin(sh, sw, 0, 0)  # create a new window
        self.w.keypad(1)
        self.w.timeout(100)  # refresh every 100 milliseconds

    def start(self):
        self.w.addch(int(self.food.position[0]), int(self.food.position[1]), '●')  # place food
        while True:
            self.w.clear()  # Clear the window
            self.w.border(0)  # Draw border
            self.w.addch(int(self.food.position[0]), int(self.food.position[1]), '●')  # place food
            next_key = self.w.getch()  # get user input
            print(f"Key pressed: {next_key}")  # Debug output
            if next_key in [curses.KEY_DOWN, curses.KEY_UP, curses.KEY_LEFT, curses.KEY_RIGHT]:
                if (self.snake.direction == curses.KEY_UP and next_key != curses.KEY_DOWN) or \
                   (self.snake.direction == curses.KEY_DOWN and next_key != curses.KEY_UP) or \
                   (self.snake.direction == curses.KEY_LEFT and next_key != curses.KEY_RIGHT) or \
                   (self.snake.direction == curses.KEY_RIGHT and next_key != curses.KEY_LEFT):
                    self.snake.direction = next_key

            new_head = self.snake.move()
            if self.snake.check_collision(new_head, self.w.getmaxyx()[0], self.w.getmaxyx()[1]):
                curses.endwin()  # End the window if collision occurs
                quit()  # Exit the game

            self.snake.position.insert(0, new_head)
            if new_head == self.food.position:
                self.snake.grow()
                self.food.spawn(self.w.getmaxyx()[0], self.w.getmaxyx()[1])
            else:
                self.snake.position.pop()

            self.snake.render(self.w)
            self.w.refresh()  # Refresh the window
            curses.napms(100)  # Ensure consistent speed

# Initialize the window
stdscr = curses.initscr()
curses.curs_set(0)
sh, sw = stdscr.getmaxyx()  # get height and width of window

# Start the game
game = Game(sh, sw)
game.start()
