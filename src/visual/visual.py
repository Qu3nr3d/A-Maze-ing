from collections.abc import Callable
from pathlib import Path
import re
import subprocess
from mlx import Mlx


class MazeRenderer:
    """Draw a maze with automatic fitting, zoom and keyboard navigation."""

    LEFT = 24
    RIGHT = 24
    TOP = 72
    BOTTOM = 24

    MAX_CELL = 60
    MIN_CELL = 2
    MIN_READABLE_CELL = 4
    DEFAULT_ZOOM_CELL = 6

    WALL_COLORS = [
        0xFFFFFFFF,  # White
        0xFF00C8FF,  # Cyan
        0xFFFFAA00,  # Orange
        0xFFFF55AA,  # Pink
    ]

    def __init__(
        self,
        grid: list[list[int]],
        entry: tuple[int, int],
        exit: tuple[int, int],
        solution: str,
        regenerate: Callable[[], tuple[list[list[int]], str]] | None = None,
    ) -> None:
        """Store maze data, select initial scale and create an MLX window."""
        self._validate_grid(grid)
        self.grid = grid
        self.entry = entry
        self.exit = exit
        self.solution = solution
        self.regenerate = regenerate
        self.rows = len(grid)
        self.cols = len(grid[0])
        self._validate_endpoints()

        self.show_path = False
        self.color_index = 0
        self.window_width, self.window_height = self._window_size()

        self.CELL = self.MIN_READABLE_CELL
        self.offset_x = 0
        self.offset_y = 0
        self.fit_view()

        self.m = Mlx()
        self.mlx_ptr = self.m.mlx_init()
        if self.mlx_ptr is None:
            raise RuntimeError("mlx_init failed")

        self.win_ptr = self.m.mlx_new_window(
            self.mlx_ptr, self.window_width, self.window_height, "A-Maze-ing"
        )
        if self.win_ptr is None:
            self.m.mlx_release(self.mlx_ptr)
            raise RuntimeError("Window creation failed")

        self.m.mlx_hook(self.win_ptr, 2, 1, self.on_key, None)
        self.m.mlx_hook(self.win_ptr, 33, 0, self.on_close, None)

    @staticmethod
    def _validate_grid(grid: list[list[int]]) -> None:
        """Ensure that the maze contains a non-empty rectangular grid."""
        if not grid or not grid[0]:
            raise ValueError("Maze must not be empty")
        if any(len(row) != len(grid[0]) for row in grid):
            raise ValueError("Maze must be rectangular")

    def _validate_endpoints(self) -> None:
        """Ensure that the entry and exit fit inside the current grid."""
        for name, (x, y) in (("Entry", self.entry), ("Exit", self.exit)):
            if not (0 <= x < self.cols and 0 <= y < self.rows):
                raise ValueError(f"{name} is outside the maze")

    @staticmethod
    def _window_size() -> tuple[int, int]:
        """Use the WSL/X11 screen dimensions when available,
        or a safe default."""
        try:
            result = subprocess.run(
                ["xrandr", "--current"],
                capture_output=True,
                text=True,
                check=False,
                timeout=2,
            )
            match = re.search(r"\bcurrent (\d+) x (\d+)", result.stdout)
            if match:
                screen_w, screen_h = map(int, match.groups())
                return (
                    max(320, min(1400, screen_w - 100)),
                    max(240, min(850, screen_h - 130)),
                )
        except (OSError, subprocess.TimeoutExpired):
            pass
        return 1100, 700

    @property
    def view_width(self) -> int:
        """Width of the region reserved for the maze."""
        return self.window_width - self.LEFT - self.RIGHT

    @property
    def view_height(self) -> int:
        """Height of the region reserved for the maze."""
        return self.window_height - self.TOP - self.BOTTOM

    def _clamp_view(self) -> None:
        """Keep the maze centered when small,
        or prevent scrolling beyond it."""
        maze_w = self.cols * self.CELL
        maze_h = self.rows * self.CELL

        if maze_w <= self.view_width:
            self.offset_x = self.LEFT + (self.view_width - maze_w) // 2
        else:
            self.offset_x = max(
                self.LEFT + self.view_width - maze_w,
                min(self.LEFT, self.offset_x),
            )

        if maze_h <= self.view_height:
            self.offset_y = self.TOP + (self.view_height - maze_h) // 2
        else:
            self.offset_y = max(
                self.TOP + self.view_height - maze_h,
                min(self.TOP, self.offset_y),
            )

    def fit_view(self) -> None:
        """Fit a normal maze on screen; show a navigable crop if too large."""
        cell_w = self.view_width // self.cols
        cell_h = self.view_height // self.rows  # Height uses ROWS.
        fit_cell = min(self.MAX_CELL, cell_w, cell_h)

        if fit_cell >= self.MIN_READABLE_CELL:
            self.CELL = fit_cell
            self.offset_x = self.LEFT
            self.offset_y = self.TOP
        else:
            # A readable rendering is physically impossible at overview size.
            # Start at the entrance, with scrolling and zoom enabled.
            self.CELL = self.DEFAULT_ZOOM_CELL
            ex, ey = self.entry
            self.offset_x = (
                self.LEFT + self.view_width // 2
                - (ex * self.CELL + self.CELL // 2)
            )
            self.offset_y = (
                self.TOP + self.view_height // 2
                - (ey * self.CELL + self.CELL // 2)
            )

        self._clamp_view()

    def zoom(self, zoom_in: bool) -> None:
        """Zoom around the center of the visible area."""
        old_cell = self.CELL
        if zoom_in:
            new_cell = min(
                self.MAX_CELL * 2,
                max(old_cell + 1,
                    round(old_cell * 1.25)))
        else:
            new_cell = max(self.MIN_CELL,
                           min(old_cell - 1,
                               round(old_cell / 1.25)))
        if new_cell == old_cell:
            return

        center_x = self.LEFT + self.view_width / 2
        center_y = self.TOP + self.view_height / 2
        world_x = (center_x - self.offset_x) / old_cell
        world_y = (center_y - self.offset_y) / old_cell
        self.CELL = new_cell
        self.offset_x = round(center_x - world_x * new_cell)
        self.offset_y = round(center_y - world_y * new_cell)
        self._clamp_view()
        self.draw()

    def pan(self, dx: int, dy: int) -> None:
        """Move the visible area without
        allowing blank space beyond the maze."""
        self.offset_x += dx
        self.offset_y += dy
        self._clamp_view()
        self.draw()

    def _pixel(self, x: int, y: int, color: int) -> None:
        """Draw one pixel only inside the maze viewport."""
        if (self.LEFT <= x < self.window_width - self.RIGHT
                and self.TOP <= y < self.window_height - self.BOTTOM):
            self.m.mlx_pixel_put(self.mlx_ptr, self.win_ptr, x, y, color)

    def horizontal(self, x: int, y: int, color: int) -> None:
        """Draw one cell-wide horizontal wall, clipped to the viewport."""
        if not self.TOP <= y < self.window_height - self.BOTTOM:
            return
        start = max(x, self.LEFT)
        end = min(x + self.CELL, self.window_width - self.RIGHT - 1)
        for px in range(start, end + 1):
            self.m.mlx_pixel_put(self.mlx_ptr, self.win_ptr, px, y, color)

    def vertical(self, x: int, y: int, color: int) -> None:
        """Draw one cell-high vertical wall, clipped to the viewport."""
        if not self.LEFT <= x < self.window_width - self.RIGHT:
            return
        start = max(y, self.TOP)
        end = min(y + self.CELL, self.window_height - self.BOTTOM - 1)
        for py in range(start, end + 1):
            self.m.mlx_pixel_put(self.mlx_ptr, self.win_ptr, x, py, color)

    def fill_cell(self, px: int, py: int, color: int) -> None:
        """Fill one fully enclosed cell, e.g., part of the '42' symbol."""
        left = max(self.LEFT, px)
        right = min(self.window_width - self.RIGHT, px + self.CELL)
        top = max(self.TOP, py)
        bottom = min(self.window_height - self.BOTTOM, py + self.CELL)
        for y in range(top, bottom):
            for x in range(left, right):
                self.m.mlx_pixel_put(self.mlx_ptr, self.win_ptr, x, y, color)

    def marker(self, x: int, y: int, color: int) -> None:
        """Draw an entry/exit marker scaled to the size of the cell."""
        cx = self.offset_x + x * self.CELL + self.CELL // 2
        cy = self.offset_y + y * self.CELL + self.CELL // 2
        radius = min(4, (self.CELL - 1) // 2)
        for dy in range(-radius, radius + 1):
            for dx in range(-radius, radius + 1):
                self._pixel(cx + dx, cy + dy, color)

    def draw_solution(self) -> None:
        """Draw a continuous path of thickness adjusted to the zoom level."""
        x, y = self.entry
        moves = {"N": (0, -1), "E": (1, 0), "S": (0, 1), "W": (-1, 0)}
        color = 0xFF00FF66
        thickness = max(1, min(5, self.CELL // 3))
        before = (thickness - 1) // 2
        after = thickness // 2

        for direction in self.solution:
            dx, dy = moves[direction]
            px = self.offset_x + x * self.CELL + self.CELL // 2
            py = self.offset_y + y * self.CELL + self.CELL // 2
            nx = px + dx * self.CELL
            ny = py + dy * self.CELL

            # Avoid drawing path segments that are fully outside the view.
            if dx:
                if (self.TOP - after
                    <= py < self.window_height - self.BOTTOM + before
                        and max(px, nx) >= self.LEFT
                        and min(px, nx) < self.window_width - self.RIGHT):
                    for offset in range(-before, after + 1):
                        self.horizontal(min(px, nx), py + offset, color)
            elif (
                self.LEFT - after <=
                px < self.window_width - self.RIGHT + before
                and max(py, ny) >= self.TOP
                and min(py, ny) < self.window_height - self.BOTTOM
            ):
                for offset in range(-before, after + 1):
                    self.vertical(px + offset, min(py, ny), color)

            x += dx
            y += dy

    def draw(self) -> None:
        """Redraw the menu and only the visible portion of the maze."""
        self.m.mlx_clear_window(self.mlx_ptr, self.win_ptr)
        self.m.mlx_string_put(
            self.mlx_ptr, self.win_ptr, 12, 18, 0xFFFFFFFF,
            "R:new  S:path  C:color  +/-:zoom  arrows:move  F:fit  ESC:exit",
        )
        self.m.mlx_string_put(
            self.mlx_ptr, self.win_ptr, 12, 38, 0xFFFFFFFF,
            f"Maze: {self.cols}x{self.rows}   Cell: {self.CELL}px",
        )

        color = self.WALL_COLORS[self.color_index]
        first_col = max(0, (self.LEFT - self.offset_x) // self.CELL - 1)
        last_col = min(
            self.cols,
            (self.window_width - self.RIGHT - self.offset_x) // self.CELL + 2,
        )
        first_row = max(0, (self.TOP - self.offset_y) // self.CELL - 1)
        last_row = min(
            self.rows,
            (self.window_height - self.BOTTOM - self.offset_y)
            // self.CELL + 2,
        )

        for y in range(first_row, last_row):
            for x in range(first_col, last_col):
                cell = self.grid[y][x]
                px = self.offset_x + x * self.CELL
                py = self.offset_y + y * self.CELL
                if cell == 0xF:
                    self.fill_cell(px, py, color)
                    continue
                if cell & 1:
                    self.horizontal(px, py, color)
                if cell & 8:
                    self.vertical(px, py, color)
                if y == self.rows - 1 and cell & 4:
                    self.horizontal(px, py + self.CELL, color)
                if x == self.cols - 1 and cell & 2:
                    self.vertical(px + self.CELL, py, color)

        if self.show_path:
            self.draw_solution()
        self.marker(*self.entry, 0xFF0088FF)
        self.marker(*self.exit, 0xFFFF4444)

    def on_key(self, keycode: int, param: object) -> None:
        """Handle colors, path, regeneration, fit, zoom and navigation."""
        if keycode == 65307:  # ESC
            self.m.mlx_loop_exit(self.mlx_ptr)
        elif keycode in (115, 83):  # S / Shift+S
            self.show_path = not self.show_path
            self.draw()
        elif keycode in (99, 67):  # C / Shift+C
            self.color_index = (self.color_index + 1) % len(self.WALL_COLORS)
            self.draw()
        elif keycode in (102, 70):  # F / Shift+F
            self.fit_view()
            self.draw()
        elif keycode in (43, 61, 65451):  # + / = / keypad +
            self.zoom(True)
        elif keycode in (45, 95, 65453):  # - / _ / keypad -
            self.zoom(False)
        elif keycode == 65361:  # Left
            self.pan(self.view_width // 5, 0)
        elif keycode == 65363:  # Right
            self.pan(-self.view_width // 5, 0)
        elif keycode == 65362:  # Up
            self.pan(0, self.view_height // 5)
        elif keycode == 65364:  # Down
            self.pan(0, -self.view_height // 5)
        elif keycode in (114, 82):  # R / Shift+R
            if self.regenerate is None:
                print("Generator not connected yet")
                return
            try:
                new_grid, new_solution = self.regenerate()
                self._validate_grid(new_grid)
                new_rows = len(new_grid)
                new_cols = len(new_grid[0])
                for name, (x, y) in (("Entry", self.entry),
                                     ("Exit", self.exit)):
                    if not (0 <= x < new_cols and 0 <= y < new_rows):
                        raise ValueError(f"{name} is outside regenerated maze")
                self.grid = new_grid
                self.solution = new_solution
                self.rows = new_rows
                self.cols = new_cols
                self.fit_view()
                self.draw()
            except Exception as exc:
                print(f"Regeneration failed: {exc}")

    def on_close(self, param: object) -> None:
        """Exit the MLX event loop when the window is closed."""
        self.m.mlx_loop_exit(self.mlx_ptr)

    def run(self) -> None:
        """Start event processing and release MLX resources when done."""
        try:
            self.draw()
            self.m.mlx_loop(self.mlx_ptr)
        finally:
            self.m.mlx_destroy_window(self.mlx_ptr, self.win_ptr)
            self.m.mlx_release(self.mlx_ptr)


def load_maze(
    path: Path,
) -> tuple[list[list[int]], tuple[int, int], tuple[int, int], str]:
    """Load hexadecimal wall data, entry,
    exit and solution from a text file."""
    lines = path.read_text(encoding="utf-8").splitlines()
    try:
        separator = next(i for i, line in enumerate(lines) if not line.strip())
    except StopIteration as exc:
        raise ValueError("Missing separator in maze file") from exc

    maze_lines = lines[:separator]
    info = lines[separator + 1:]
    grid = [[int(char, 16) for char in line.strip()] for line in maze_lines]
    MazeRenderer._validate_grid(grid)
    if len(info) != 3:
        raise ValueError("Invalid maze metadata")

    entry_x, entry_y = map(int, info[0].split(","))
    exit_x, exit_y = map(int, info[1].split(","))
    solution = info[2].strip()
    if any(move not in "NESW" for move in solution):
        raise ValueError("Invalid solution path")
    return grid, (entry_x, entry_y), (exit_x, exit_y), solution
