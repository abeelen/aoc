from collections import namedtuple
from dataclasses import dataclass
from typing import List, Tuple

RAW_INPUT = """##########
#..O..O.O#
#......O.#
#.OO..O.O#
#..O@..O.#
#O#..O...#
#O..O..O.#
#.OO.O.OO#
#....O...#
##########

<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^"""

RAW_INPUT_SMALL = """########
#..O.O.#
##@.O..#
#...O..#
#.#.O..#
#...O..#
#......#
########

<^^>>>vv<v>>v<<"""

WALL = "#"
BOX = "O"
LARGE_BOX = "[]"
ROBOT = "@"
OFFSETS = {"v": (0, 1), "^": (0, -1), "<": (-1, 0), ">": (1, 0)}

Pos = namedtuple("Pos", ["x", "y"])


@dataclass
class Inventory:
    robot: Pos
    boxes: List[Pos]
    walls: List[Pos]
    instructions: List[str]
    size: Tuple[int, int]

    def draw(self):
        output = []
        for j in range(self.size[0]):
            line = []
            for i in range(self.size[1]):
                pos = Pos(i, j)
                if pos == self.robot:
                    line.append(ROBOT)
                elif pos in self.boxes:
                    line.append(BOX)
                elif pos in self.walls:
                    line.append(WALL)
                else:
                    line.append(".")
            output.append("".join(line))
        return "\n".join(output)

    def draw_wide(self):
        output = []
        for j in range(self.size[0]):
            line = []
            for i in range(self.size[1]):
                pos = Pos(i, j)
                if pos == self.robot:
                    line.append(ROBOT + ".")
                elif pos == Pos(round(self.robot.x), self.robot.y):
                    line.append(ROBOT + ".")
                elif pos in self.boxes:
                    line.append(LARGE_BOX)
                elif pos in self.walls:
                    line.append(WALL + WALL)
                else:
                    line.append("..")
            output.append("".join(line))
        return "\n".join(output)

    @classmethod
    def from_raw(cls, raw: str):
        grid, instructions = raw.strip().split("\n\n")
        instructions = list("".join(instructions.strip().split("\n")))
        grid = grid.split("\n")
        size = (len(grid), len(grid[0]))
        robot = None
        boxes = []
        walls = []
        for j, row in enumerate(grid):
            for i, cell in enumerate(row):
                if cell == ROBOT:
                    robot = Pos(i, j)
                elif cell == BOX:
                    boxes.append(Pos(i, j))
                elif cell == WALL:
                    walls.append(Pos(i, j))
        return cls(robot, boxes, walls, instructions, size)

    def move(self, direction: str):
        dx, dy = OFFSETS[direction]
        new_robot = Pos(self.robot.x + dx, self.robot.y + dy)

        # If there is a wall we do not move...
        if new_robot in self.walls:
            return False

        # If there is a box, we move the box and any potential boxes behind it
        if new_robot in self.boxes:
            # There could be more than one box in the same direction
            new_box = Pos(new_robot.x + dx, new_robot.y + dy)
            old_boxes = [new_robot]
            new_boxes = [new_box]

            while new_box in self.boxes:
                old_boxes.append(new_box)
                new_box = Pos(new_box.x + dx, new_box.y + dy)
                new_boxes.append(new_box)

            # At the end of the pile of boxes, we check if there is a wall
            if new_box in self.walls:
                return False
            for box in old_boxes:
                self.boxes.remove(box)
            for box in new_boxes:
                self.boxes.append(box)

        self.robot = new_robot
        return True

    def move_part2(self, direction: str):
        dx, dy = OFFSETS[direction]
        dx = dx / 2
        new_robot = Pos(self.robot.x + dx, self.robot.y + dy)

        # If there is a wall we do not move...
        if Pos(round(new_robot.x), new_robot.y) in self.walls:
            return False

        moved_boxes = []
        if new_robot in self.boxes:
            moved_boxes.append(new_robot)
        elif Pos(round(new_robot.x), new_robot.y) in self.boxes:
            moved_boxes.append(Pos(round(new_robot.x), new_robot.y))
        # If there is one or several boxes, we move them and any potential boxes behind it

        if moved_boxes:
            old_boxes = []
            new_boxes = []
            while moved_boxes:
                old_boxes += moved_boxes
                _new_boxes = [Pos(box.x + 2 * dx, box.y + dy) for box in moved_boxes]
                _moved_boxes = set()
                for box in _new_boxes:
                    if box in self.boxes:
                        _moved_boxes.add(box)
                    if Pos(round(box.x), box.y) in self.boxes:
                        _moved_boxes.add(Pos(round(box.x), box.y))

                # At the end of the pile of boxes, we check if there is a wall
                if any(Pos(round(box.x), box.y) in self.walls for box in _moved_boxes):
                    return False

                new_boxes += list(_new_boxes)
                moved_boxes = _moved_boxes

            for box in old_boxes:
                self.boxes.remove(box)
            for box in new_boxes:
                self.boxes.append(box)

        self.robot = new_robot
        return True

    def run(self):
        for instruction in self.instructions:
            self.move(instruction)
        return self

    def run_part2(self):
        for instruction in self.instructions:
            self.move_part2(instruction)
        return self

    def sum_GPS(self):
        gps = []
        for box in self.boxes:
            gps.append(box.x + box.y * 100)
        return sum(gps)


INVENTORY = Inventory.from_raw(RAW_INPUT_SMALL).run()
assert (
    INVENTORY.draw()
    == """########
#....OO#
##.....#
#.....O#
#.#O@..#
#...O..#
#...O..#
########"""
)

assert INVENTORY.sum_GPS() == 2028
INVENTORY = Inventory.from_raw(RAW_INPUT).run()
assert INVENTORY.sum_GPS() == 10092

# with open("day15.txt", "r") as file:
#     input_raw = file.read()
# inventory = Inventory.from_raw(input_raw).run()
# print(inventory.sum_GPS())

RAW_INPUT_SMALL2 = """#######
#...#.#
#.....#
#..OO@#
#..O..#
#.....#
#######

<vv<<^^<<^^"""
INVENTORY = Inventory.from_raw(RAW_INPUT_SMALL2)
