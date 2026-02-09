# Retro Snake Game

A classic Snake game implemented in Python with pygame, featuring retro aesthetics and demonstrating proper game loop architecture and memory management techniques.

## Features

### Game Mechanics
- Classic snake gameplay with smooth movement
- Score tracking with high score persistence during session
- Collision detection (walls and self)
- Food spawning system that avoids the snake's body
- Growing snake mechanic

### Technical Highlights

#### Memory Management
- **Deque-based Snake Body**: Uses `collections.deque` for O(1) append/pop operations at both ends
- **Efficient Movement**: Only adds new head and removes tail each frame (no array copying)
- **Frame Rate Control**: Clock-based FPS limiting prevents excessive CPU usage
- **Event-driven Architecture**: Pygame event queue for efficient input handling

#### Game Loop
- Follows the classic game loop pattern:
  1. Handle input events
  2. Update game state
  3. Render graphics
  4. Control frame rate
- Separation of concerns with distinct classes for Snake, Food, and Game

### Visual Design
- Retro color palette (classic green snake on black background)
- Grid overlay for authentic retro feel
- Two-tone snake segments with outlined borders
- Red and yellow food sprite
- Game over overlay with semi-transparency
- Real-time score display

## Installation

1. Ensure Python 3.7+ is installed
2. Install dependencies:
```bash
pip install -r requirements.txt
```

## How to Play

### Starting the Game
```bash
python snake_game.py
```

### Controls
- **Arrow Keys** or **WASD** - Move the snake (Up, Down, Left, Right)
- **ESC** - Quit game
- **SPACE** or **ENTER** - Restart game (when game over)

### Gameplay
- Guide the snake to eat the red food
- Each food eaten increases your score by 10 points
- The snake grows longer with each food consumed
- Avoid hitting the walls or your own body
- Try to beat your high score!

## Code Structure

### Classes

#### `Direction` (Enum)
- Enumeration for movement directions with vector values
- Prevents invalid direction states

#### `Snake`
- Manages snake body using `deque` for memory efficiency
- Handles movement, growth, and collision detection
- Prevents 180-degree turns

#### `Food`
- Manages food spawning and rendering
- Ensures food doesn't spawn on snake's body

#### `Game`
- Main game controller
- Manages game loop, state, and rendering
- Handles events and user input

## Memory Management Techniques

1. **Deque Data Structure**
   - O(1) complexity for adding head and removing tail
   - More efficient than list operations for this use case

2. **No Unnecessary Copies**
   - Snake movement modifies existing deque, doesn't create new arrays
   - Food position is a simple tuple, not an object with overhead

3. **Frame Rate Limiting**
   - `clock.tick(FPS)` prevents runaway loops
   - Saves CPU cycles and battery life

4. **Efficient Rendering**
   - Only redraws what's necessary each frame
   - Uses pygame's optimized rendering pipeline

## Customization

You can easily modify these constants in the code:

```python
WINDOW_WIDTH = 800      # Window width in pixels
WINDOW_HEIGHT = 600     # Window height in pixels
GRID_SIZE = 20          # Size of each grid cell
FPS = 10                # Game speed (frames per second)
INITIAL_SNAKE_LENGTH = 3  # Starting snake length
```

## Future Enhancements

Potential additions for learning purposes:
- Difficulty levels (speed adjustment)
- Obstacles on the playing field
- Power-ups (speed boost, invincibility, etc.)
- Persistent high score storage (file or database)
- Sound effects and background music
- Multiplayer mode
- Different game modes (infinite, timed, etc.)

## Learning Objectives

This implementation demonstrates:
- Event-driven programming
- Game loop architecture
- Object-oriented design in Python
- Memory-efficient data structures
- Frame rate management
- Collision detection algorithms
- State management in games

## License

Free to use for educational purposes.
