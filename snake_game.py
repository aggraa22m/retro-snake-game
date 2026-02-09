"""
Retro Snake Game
A classic snake game with retro aesthetics, demonstrating game loops and memory management.
"""

import pygame
import random
from collections import deque
from enum import Enum

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
GRID_SIZE = 20
GRID_WIDTH = WINDOW_WIDTH // GRID_SIZE
GRID_HEIGHT = WINDOW_HEIGHT // GRID_SIZE

# Colors (Retro palette)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 180, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
GRAY = (50, 50, 50)

# Game settings
FPS = 10
INITIAL_SNAKE_LENGTH = 3


class Direction(Enum):
    """Enumeration for movement directions"""
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)


class Snake:
    """
    Snake class with memory-efficient management using deque.
    Deque provides O(1) append and pop operations from both ends.
    """

    def __init__(self):
        # Use deque for efficient memory management
        # Allows O(1) insertion/deletion at both ends
        self.body = deque()
        self.direction = Direction.RIGHT
        self.grow_pending = False
        self.reset()

    def reset(self):
        """Reset snake to initial state"""
        self.body.clear()
        start_x = GRID_WIDTH // 2
        start_y = GRID_HEIGHT // 2

        # Initialize snake body from tail to head
        # Snake faces RIGHT, so tail is on the left, head is on the right
        for i in range(INITIAL_SNAKE_LENGTH - 1, -1, -1):
            self.body.append((start_x - i, start_y))

        self.direction = Direction.RIGHT
        self.grow_pending = False

    def get_head(self):
        """Get the head position of the snake"""
        return self.body[-1]

    def move(self):
        """
        Move the snake in the current direction.
        Memory efficient: only adds new head and removes tail.
        """
        head_x, head_y = self.get_head()
        dx, dy = self.direction.value
        new_head = (head_x + dx, head_y + dy)

        self.body.append(new_head)

        # Remove tail unless snake is growing
        if not self.grow_pending:
            self.body.popleft()  # O(1) operation with deque
        else:
            self.grow_pending = False

    def grow(self):
        """Mark snake to grow on next move"""
        self.grow_pending = True

    def change_direction(self, new_direction):
        """Change direction if not opposite to current direction"""
        # Prevent 180-degree turns
        opposite_directions = {
            Direction.UP: Direction.DOWN,
            Direction.DOWN: Direction.UP,
            Direction.LEFT: Direction.RIGHT,
            Direction.RIGHT: Direction.LEFT
        }

        if new_direction != opposite_directions.get(self.direction):
            self.direction = new_direction

    def check_collision(self):
        """Check if snake collides with walls or itself"""
        head_x, head_y = self.get_head()

        # Wall collision
        if (head_x < 0 or head_x >= GRID_WIDTH or
            head_y < 0 or head_y >= GRID_HEIGHT):
            return True

        # Self collision (check if head hits body, excluding the head itself)
        body_without_head = list(self.body)[:-1]
        if self.get_head() in body_without_head:
            return True

        return False

    def draw(self, surface):
        """Draw the snake on the surface"""
        for i, segment in enumerate(self.body):
            x, y = segment
            rect = pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)

            # Head is brighter green
            if i == len(self.body) - 1:
                pygame.draw.rect(surface, GREEN, rect)
                pygame.draw.rect(surface, DARK_GREEN, rect, 2)
            else:
                pygame.draw.rect(surface, DARK_GREEN, rect)
                pygame.draw.rect(surface, GREEN, rect, 2)


class Food:
    """Food class for the snake to eat"""

    def __init__(self):
        self.position = (0, 0)
        self.spawn()

    def spawn(self, snake_body=None):
        """
        Spawn food at a random location.
        Avoid spawning on the snake's body for better gameplay.
        """
        while True:
            x = random.randint(0, GRID_WIDTH - 1)
            y = random.randint(0, GRID_HEIGHT - 1)

            # Ensure food doesn't spawn on snake
            if snake_body is None or (x, y) not in snake_body:
                self.position = (x, y)
                break

    def draw(self, surface):
        """Draw the food on the surface"""
        x, y = self.position
        rect = pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
        pygame.draw.rect(surface, RED, rect)
        # Add a small yellow center for retro look
        center_rect = pygame.Rect(
            x * GRID_SIZE + GRID_SIZE // 4,
            y * GRID_SIZE + GRID_SIZE // 4,
            GRID_SIZE // 2,
            GRID_SIZE // 2
        )
        pygame.draw.rect(surface, YELLOW, center_rect)


class Game:
    """
    Main game class managing the game loop and state.
    Demonstrates proper memory management and game loop implementation.
    """

    def __init__(self):
        # Initialize display
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Retro Snake Game")

        # Clock for controlling frame rate
        self.clock = pygame.time.Clock()

        # Game objects
        self.snake = Snake()
        self.food = Food()

        # Game state
        self.score = 0
        self.high_score = 0
        self.running = True
        self.game_over = False

        # Font for text rendering
        self.font_large = pygame.font.Font(None, 72)
        self.font_medium = pygame.font.Font(None, 36)
        self.font_small = pygame.font.Font(None, 24)

    def handle_events(self):
        """Handle pygame events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.KEYDOWN:
                if self.game_over:
                    # Restart game on any key press when game over
                    if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                        self.reset_game()
                    elif event.key == pygame.K_ESCAPE:
                        self.running = False
                else:
                    # Handle direction changes
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        self.snake.change_direction(Direction.UP)
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        self.snake.change_direction(Direction.DOWN)
                    elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        self.snake.change_direction(Direction.LEFT)
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        self.snake.change_direction(Direction.RIGHT)
                    elif event.key == pygame.K_ESCAPE:
                        self.running = False

    def update(self):
        """Update game state"""
        if self.game_over:
            return

        # Move snake
        self.snake.move()

        # Check collision with walls or self
        if self.snake.check_collision():
            self.game_over = True
            if self.score > self.high_score:
                self.high_score = self.score
            return

        # Check if snake eats food
        if self.snake.get_head() == self.food.position:
            self.snake.grow()
            self.score += 10
            self.food.spawn(self.snake.body)

    def draw_grid(self):
        """Draw a subtle grid for retro aesthetic"""
        for x in range(0, WINDOW_WIDTH, GRID_SIZE):
            pygame.draw.line(self.screen, GRAY, (x, 0), (x, WINDOW_HEIGHT))
        for y in range(0, WINDOW_HEIGHT, GRID_SIZE):
            pygame.draw.line(self.screen, GRAY, (0, y), (WINDOW_WIDTH, y))

    def draw(self):
        """Render everything to the screen"""
        # Clear screen
        self.screen.fill(BLACK)

        # Draw grid
        self.draw_grid()

        # Draw game objects
        self.food.draw(self.screen)
        self.snake.draw(self.screen)

        # Draw score
        score_text = self.font_small.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))

        high_score_text = self.font_small.render(f"High Score: {self.high_score}", True, CYAN)
        self.screen.blit(high_score_text, (10, 35))

        # Draw game over screen
        if self.game_over:
            # Semi-transparent overlay
            overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
            overlay.set_alpha(128)
            overlay.fill(BLACK)
            self.screen.blit(overlay, (0, 0))

            # Game over text
            game_over_text = self.font_large.render("GAME OVER", True, RED)
            text_rect = game_over_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 50))
            self.screen.blit(game_over_text, text_rect)

            # Final score
            final_score_text = self.font_medium.render(f"Final Score: {self.score}", True, YELLOW)
            score_rect = final_score_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 20))
            self.screen.blit(final_score_text, score_rect)

            # Instructions
            restart_text = self.font_small.render("Press SPACE to restart or ESC to quit", True, WHITE)
            restart_rect = restart_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 80))
            self.screen.blit(restart_text, restart_rect)

        # Update display
        pygame.display.flip()

    def reset_game(self):
        """Reset game to initial state"""
        self.snake.reset()
        self.food.spawn(self.snake.body)
        self.score = 0
        self.game_over = False

    def run(self):
        """
        Main game loop.
        Follows the classic game loop pattern:
        1. Handle input
        2. Update game state
        3. Render
        4. Control frame rate
        """
        print("=== Retro Snake Game ===")
        print("Controls:")
        print("  Arrow Keys or WASD - Move snake")
        print("  ESC - Quit game")
        print("  SPACE - Restart (when game over)")
        print("\nStarting game...")

        while self.running:
            # Handle events
            self.handle_events()

            # Update game state
            self.update()

            # Render
            self.draw()

            # Control frame rate (memory efficient - prevents excessive CPU usage)
            self.clock.tick(FPS)

        # Cleanup
        pygame.quit()
        print(f"\nGame ended. Final Score: {self.score}, High Score: {self.high_score}")


def main():
    """Entry point for the game"""
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
