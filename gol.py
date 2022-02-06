#!/usr/bin/env python
"""The game of life."""
__all__ = ("Universe",)
__version__ = "0.0.1"
__author__ = "Aurélien Chick"

from copy import deepcopy
from random import random, seed
from typing import List, Sequence


class Universe:
    """The universe in which alive and dead cells are contained."""

    def __init__(
        self, width: int, height: int, seed_of_life: int = 1, threshold: float = 0.5
    ) -> None:
        self.width = width
        self.height = height

        nb_cells = width * height
        seed(seed_of_life)
        self.cells = [random() >= threshold for _ in range(nb_cells)]

    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        repr_self = ""
        for row in range(self.height):
            for column in range(self.width):
                index = self._get_index(row, column)
                cell = self.cells[index]
                repr_self += "█" if cell else " "
            repr_self += "\n"
        return repr_self

    def _get_index(self, row: int, column: int) -> int:
        """Get the cells index for the specified row/column combination."""
        return row * self.width + column

    def _live_neighbor_count(self, row: int, column: int) -> int:
        """Return the number of alive neighbors for the given cell."""
        count = 0
        for delta_row in [self.height - 1, 0, 1]:
            for delta_col in [self.width - 1, 0, 1]:
                if delta_row == 0 and delta_col == 0:
                    continue

                neighbor_row = (row + delta_row) % self.height
                neighbor_col = (column + delta_col) % self.width
                index = self._get_index(neighbor_row, neighbor_col)
                count += int(self.cells[index])

        return count

    def tick(self) -> None:
        """Tick over to the next generation.

        Rules of the game:

        * Rule 1: Any live cell with fewer than two live neighbors dies,
        as if caused by underpopulation.
        * Rule 2: Any live cell with two or three live neighbors lives
        on to the next generation.
        * Rule 3: Any live cell with more than three live neighbors dies,
        as if caused by overpopulation.
        * Rule 4: Any dead cell with exactly three live neighbors becomes
        a lie cell, as if by reproduction.
        """
        next_cells = deepcopy(self.cells)

        for row in range(self.height):
            for col in range(self.width):
                index = self._get_index(row, col)
                cell = self.cells[index]
                live_neighbors = self._live_neighbor_count(row, col)

                if cell and live_neighbors < 2:  # Rule 1
                    next_cell = False
                elif cell and live_neighbors in [2, 3]:  # Rule 2
                    next_cell = True
                elif cell and live_neighbors > 3:  # Rule 3
                    next_cell = False
                elif cell is False and live_neighbors == 3:  # Rule 4
                    next_cell = True
                else:
                    next_cell = cell

                next_cells[index] = next_cell

        self.cells = next_cells

    def display(self) -> List[str]:
        """Return a list of strings where each string is a row in
        the universe.
        """
        grid_lines = []
        for row in range(self.height):
            line_str = ""
            for column in range(self.width):
                index = self._get_index(row, column)
                cell = self.cells[index]
                line_str += "█" if cell else " "
            grid_lines.append(line_str)
        return grid_lines


def main(sys_args: Sequence[str] = None) -> None:
    import curses
    import sys

    from argparse import ArgumentParser, RawTextHelpFormatter
    from time import sleep

    parser = ArgumentParser(
        prog="gol",
        formatter_class=RawTextHelpFormatter,
        description=(
            "Conway's game of life.\n"
            "Welcome to the 0 player game in which all you have to do is look.\n"
            "If you do want to play a bit, you can interact with life with the following keys:\n"
            "\t* p : pause life at a given iteration. To resume, enter p again.\n"
            "\t* (1|2|3|4) : toggle the color scheme.\n"
            "\t* q : Exit the program.\n"
        ),
    )
    parser.add_argument(
        "--seed", type=int, default=1, help="The seed to initiate life. Defaults to 1."
    )
    parser.add_argument(
        "--threshold",
        type=float,
        default=0.5,
        help="A float between 0 and 1. Used to determine whether a value will lead to a dead or alive cell.",
    )
    parser.add_argument(
        "--interval",
        type=float,
        default=1,
        help="The refresh interval rate between generations in seconds. Defaults to 1s.",
    )

    args = parser.parse_args(sys_args)
    if args.threshold < 0 or args.threshold > 1:
        print("Threshold must be between 0 and 1 (inclusive).")
        sys.exit(1)

    life_info = {"seed": args.seed, "threshold": args.threshold}

    try:
        stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        stdscr.keypad(True)
        curses.curs_set(0)

        curses.start_color()
        curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_RED)
        curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLUE)
        curses.init_pair(4, curses.COLOR_MAGENTA, curses.COLOR_CYAN)

        used_color_pair = 3
        stdscr.bkgdset(" ", curses.color_pair(used_color_pair))

        stdscr.nodelay(True)

        height, width = curses.LINES - 1, curses.COLS - 1
        universe = Universe(
            width, height, seed_of_life=args.seed, threshold=args.threshold
        )
        life_info["height"] = height
        life_info["width"] = width

        while True:
            stdscr.clear()

            for idx, line in enumerate(universe.display()):
                stdscr.addstr(idx, 0, line)

            stdscr.refresh()

            universe.tick()
            sleep(args.interval)

            # Pause the ticks if this is requested.
            key = stdscr.getch()
            if key == ord("p"):
                while True:
                    key = stdscr.getch()
                    if key and key == ord("p"):
                        break
            elif key == ord("q"):
                raise KeyboardInterrupt()
            elif key in [ord("1"), ord("2"), ord("3"), ord("4")] and key != str(
                int(used_color_pair)
            ):
                if key == ord("1") and used_color_pair != 1:
                    used_color_pair = 1
                elif key == ord("2") and used_color_pair != 2:
                    used_color_pair = 2
                elif key == ord("3") and used_color_pair != 3:
                    used_color_pair = 3
                elif key == ord("4") and used_color_pair != 4:
                    used_color_pair = 4
                stdscr.bkgdset(" ", curses.color_pair(used_color_pair))
    except curses.error:
        key = stdscr.getch()
        if key == curses.KEY_RESIZE:
            life_info["error"] = "The universe cannot change size once it has started."
    except KeyboardInterrupt:
        pass
    finally:
        curses.nocbreak()
        stdscr.keypad(False)
        curses.echo()
        curses.endwin()

        if "error" in life_info:
            print(life_info)
        print(f"The universe's size: {life_info['height']}x{life_info['width']} (HxW)")
        print(f"The seed of life: {args.seed}")
        print(f"The threshold for life: {args.threshold}")


if __name__ == "__main__":
    main()
