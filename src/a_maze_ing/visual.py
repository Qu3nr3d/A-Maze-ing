from collections.abc import Callable
from mlx import Mlx
from pathlib import Path

class MazeRenderer:
    CELL = 60
    MARGIN = 40
    TOP = 60
    WALL_COLORS = [
        0xFFFFFFFF,  # White
        0xFF00C8FF,  # Cyan
        0xFFFFAA00,  # Orange
        0xFFFF55AA,  # Pink
    ]

    def __init__(self, grid: list[list[int]], entry: tuple[int, int],
                 exit: tuple[int, int],
                 solution: str,
                 regenerate: Callable[[], tuple[list[list[int]], str]] | None = None) -> None:
        self.grid = grid
        self.entry = entry
        self.exit = exit
        self.solution = solution
        self.regenerate = regenerate
        self.rows = len(grid)
        self.cols = len(grid[0])
        self.show_path = False
        self.color_index = 0
        width = self.cols * self.CELL + 2 * self.MARGIN
        height = self.rows * self.CELL + self.TOP + self.MARGIN
        self.m = Mlx()
        self.mlx_ptr = self.m.mlx_init()

        if self.mlx_ptr is None:
            raise RuntimeError("mlx_init failed")
        self.win_ptr = self.m.mlx_new_window(
            self.mlx_ptr, width, height, "A-Maze-ing"
        )

        if self.win_ptr is None:
            self.m.mlx_release(self.mlx_ptr)
            raise RuntimeError("Window creation failed")
        self.m.mlx_hook(
            self.win_ptr, 2, 1, self.on_key, None
        )
        self.m.mlx_hook(
            self.win_ptr, 33, 0, self.on_close, None
        )

    def horizontal(self, x: int, y: int, color: int) -> None:
        for dx in range(self.CELL + 1):
            self.m.mlx_pixel_put(self.mlx_ptr, self.win_ptr, x + dx, y, color)

    def vertical(self, x: int, y: int, color: int) -> None:
        for dy in range(self.CELL + 1):
            self.m.mlx_pixel_put(
                self.mlx_ptr, self.win_ptr,
                x, y + dy, color
            )

    def marker(self, x: int, y: int, color: int) -> None:
        cx = self.MARGIN + x * self.CELL + self.CELL // 2
        cy = self.TOP + y * self.CELL + self.CELL // 2

        for dy in range(-4, 5):
            for dx in range(-4, 5):
                self.m.mlx_pixel_put(
                    self.mlx_ptr, self.win_ptr,
                    cx + dx, cy + dy, color
                )

    def draw_solution(self) -> None:
        x, y = self.entry
        moves = {
            "N": (0, -1),
            "E": (1, 0),
            "S": (0, 1),
            "W": (-1, 0),
        }
        color = 0xFF00FF66
        thickness = 5

        for direction in self.solution:
            dx, dy = moves[direction]
            x1 = self.MARGIN + x * self.CELL + self.CELL // 2
            y1 = self.TOP + y * self.CELL + self.CELL // 2
            x2 = x1 + dx * self.CELL
            y2 = y1 + dy * self.CELL
            if dx != 0:
                for px in range(min(x1, x2), max(x1, x2) + 1):
                    for offset in range(-thickness // 2 + 1,
                                        thickness // 2 + 1):
                        self.m.mlx_pixel_put(
                            self.mlx_ptr, self.win_ptr,
                            px, y1 + offset, color
                        )
            else:
                for py in range(min(y1, y2), max(y1, y2) + 1):
                    for offset in range(-thickness // 2 + 1,
                                        thickness // 2 + 1):
                        self.m.mlx_pixel_put(
                            self.mlx_ptr, self.win_ptr,
                            x1 + offset, py, color
                        )
            x += dx
            y += dy

    def draw(self) -> None:
        self.m.mlx_clear_window(
            self.mlx_ptr, self.win_ptr
        )

        self.m.mlx_string_put(
            self.mlx_ptr, self.win_ptr,
            12, 18, 0xFFFFFFFF,
            "R:new  S:path  C:color"
        )
        self.m.mlx_string_put(
            self.mlx_ptr, self.win_ptr,
            12, 35, 0xFFFFFFFF, "ESC:exit"
        )
        color = self.WALL_COLORS[self.color_index]

        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                px = self.MARGIN + x * self.CELL
                py = self.TOP + y * self.CELL

                if cell == 0xF:
                    self.fill_cell(px, py, color)
                    continue
                if cell & 1:  # North
                    self.horizontal(px, py, color)
                if cell & 8:  # West
                    self.vertical(px, py, color)
                if y == self.rows - 1 and cell & 4:
                    self.horizontal(
                        px, py + self.CELL, color
                    )
                if x == self.cols - 1 and cell & 2:
                    self.vertical(
                        px + self.CELL, py, color
                    )
        if self.show_path:
            self.draw_solution()
        self.marker(*self.entry, 0xFF0088FF)
        self.marker(*self.exit, 0xFFFF4444)

    def on_key(self, keycode: int, param: object) -> None:
        if keycode == 65307:  # ESC
            self.m.mlx_loop_exit(self.mlx_ptr)
        elif keycode == 115:  # S
            self.show_path = not self.show_path
            self.draw()
        elif keycode == 99:  # C
            self.color_index = (
                self.color_index + 1
            ) % len(self.WALL_COLORS)
            self.draw()
        elif keycode == 114:  # R
            if self.regenerate is None:
                print("Generator not connected yet")
                return
            try:
                grid, solution = self.regenerate()
                if len(grid) != self.rows or any(
                    len(row) != self.cols for row in grid
                ):
                    raise ValueError("Maze size changed")
                self.grid = grid
                self.solution = solution
                self.draw()
            except Exception as exc:
                print(f"Regeneration failed: {exc}")

    def on_close(self, param: object) -> None:
        self.m.mlx_loop_exit(self.mlx_ptr)

    def run(self) -> None:
        try:
            self.draw()
            self.m.mlx_loop(self.mlx_ptr)
        finally:
            self.m.mlx_destroy_window(
                self.mlx_ptr, self.win_ptr
            )
            self.m.mlx_release(self.mlx_ptr)

    def fill_cell(
            self, px: int, py: int, color: int
    ) -> None:
        for dy in range(self.CELL + 1):
            for dx in range(self.CELL + 1):
                self.m.mlx_pixel_put(
                    self.mlx_ptr,
                    self.win_ptr,
                    px + dx,
                    py + dy,
                    color
                )


def load_maze(path: Path,) -> tuple[list[list[int]],tuple[int, int],tuple[int, int],str,]:
    lines = path.read_text(encoding="utf-8").splitlines()

    separator = next(i for i, line in enumerate(lines) if not line.strip())
    maze_lines = lines[:separator]
    info = lines[separator + 1:]
    grid = [[int(char, 16) for char in line.strip()] for line in maze_lines]

    if not grid or any(len(row) != len(grid[0]) for row in grid):
        raise ValueError("Invalid maze dimensions")
    if len(info) != 3:
        raise ValueError("Invalid maze metadata")

    entry_x, entry_y = map(int, info[0].split(","))
    exit_x, exit_y = map(int, info[1].split(","))
    entry = (entry_x, entry_y)
    exit_pos = (exit_x, exit_y)
    solution = info[2].strip()

    if any(move not in "NESW" for move in solution):
        raise ValueError("Invalid solution path")
    return grid, entry, exit_pos, solution


if __name__ == "__main__":
    project_dir = Path(__file__).resolve().parents[2]
    maze_path = project_dir / "maze.txt"
    try:
        grid, entry, exit_pos, solution = load_maze(maze_path)
        app = MazeRenderer(
            grid=grid,
            entry=entry,
            exit=exit_pos,
            solution=solution,
        )
        app.run()
    except (OSError, ValueError, StopIteration) as error:
        print(f"Error loading maze: {error}")
