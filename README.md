
```markdown
# Retro Snake Game

A classic Snake game implemented in Python with Pygame, featuring retro aesthetics and demonstrating proper game loop architecture and memory management techniques.

## Motivation
This project serves as a practical implementation of low-overhead game design within Python. The primary goal was to build a real-time interactive game that strictly adheres to efficient memory structures and optimal CPU utilization. By leveraging O(1) data structures for positional tracking and a deterministic game loop, it demonstrates how fundamental computer science principles apply to game engine architecture, minimizing garbage collection pauses and avoiding unnecessary array allocations.

## Features
* **Game Mechanics:** Classic snake gameplay with smooth movement, growing mechanics, collision detection (walls and self), and a self-correcting food spawning system.
* **Visual Design:** Retro color palette (classic green snake on a black background), two-tone segments with outlined borders, grid overlay, and a semi-transparent Game Over screen.
* **Technical Highlights:** Separation of concerns using distinct, strictly bounded classes for game elements.

## Quick Start

### Prerequisites
* Python 3.7 or higher
* Pip (Python package installer)

### Installation
1. Clone the repository:
   ```bash
   git clone [https://github.com/aggraa22m/retro-snake-game.git](https://github.com/aggraa22m/retro-snake-game.git)
   cd retro-snake-game

```

2. Install the required dependencies:
```bash
pip install -r requirements.txt

```


3. Run the game:
```bash
python snake_game.py

```



## Usage

### Controls

* **Arrow Keys / WASD:** Change direction (Up, Down, Left, Right). Invalid 180-degree turns are programmatically blocked.
* **SPACE / ENTER:** Restart the game (during the Game Over screen).
* **ESC:** Exit the game safely.

### Gameplay Rules

* Guide the snake to eat the red/yellow food pieces.
* Each item consumed increases the score by 10 points and increments the snake's length.
* The game ends immediately if the snake collides with the outer boundary walls or its own body.

### Configuration & Customization

You can tweak the core performance and design parameters directly inside `snake_game.py`:

```python
WINDOW_WIDTH = 800        # Window width in pixels
WINDOW_HEIGHT = 600       # Window height in pixels
GRID_SIZE = 20            # Size of each grid cell
FPS = 10                  # Game speed (frames per second)
INITIAL_SNAKE_LENGTH = 3  # Starting snake length

```

---

## Technical Architecture & Core Concepts

### 1. Game Loop Pattern

The system architecture follows a synchronized, single-threaded game loop processing pattern:

1. **Handle Input Events:** Polls the Pygame event queue to capture asynchronous keyboard interrupts.
2. **Update Game State:** Logic execution for snake tracking, growth calculation, and collision bounds checks.
3. **Render Graphics:** Draws only necessary elements using Pygame's optimized surface rendering pipeline.
4. **Control Frame Rate:** Regulated via `clock.tick(FPS)` to prevent runaway CPU cycles.

### 2. Memory Management Techniques

* **Deque-Based Snake Body:** Utilizing `collections.deque` provides $O(1)$ complexity for head insertion and tail extraction, outperforming dynamic lists ($O(n)$ reallocations).
* **Zero-Copy Movement:** Snake translation updates the existing deque boundary elements inline without copying the underlying positional arrays.
* **Primitive Overhead Reduction:** Food tracking relies on simple tuple pairs rather than redundant object instantiations, keeping heap allocation minimal.

### 3. Code Structure

* `Direction (Enum)`: Strongly typed direction states to prevent invalid or contradictory vector movements.
* `Snake`: Handles body coordination, growth triggers, and self-collision matrices.
* `Food`: Handles pseudo-randomized spawning logic, validating coordinates to prevent overlapping the active snake structure.
* `Game`: The core engine driver managing state flags, clock cycles, and screen blitting.

---

## Contributing

Contributions are welcome. If you intend to introduce new mechanics, please adhere to the existing zero-copy and memory-conscious patterns.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Planned Enhancements

* Introducing fixed and runtime-generated obstacle arrays.
* Persistent binary/file serialization for session high scores.
* Dynamic frame-rate scale changes based on difficulty curves.

## License

Distributed under an open license. Free to use, modify, and distribute for educational purposes.

```
