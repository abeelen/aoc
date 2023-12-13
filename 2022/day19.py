import re

from dataclasses import dataclass
from collections import namedtuple, deque
from typing import NamedTuple, Iterator, List


RESOURCE = ['ore', 'clay', 'obsidian', 'geode']
# geode is not needed but simpler to have the same length
Recipe = namedtuple('Recipe', RESOURCE, defaults=[0, 0, 0, 0])
RobotRecipies = namedtuple('RobotRecipies', RESOURCE)

@dataclass
class Blueprint:
    id: int
    recipies: RobotRecipies

    @staticmethod
    def from_string(s: str) -> 'Blueprint':
        pattern = "Blueprint (\d+): Each ore robot costs (\d+) ore. Each clay robot costs (\d+) ore. Each obsidian robot costs (\d+) ore and (\d+) clay. Each geode robot costs (\d+) ore and (\d+) obsidian."
        match = re.match(pattern, s)
        if match:
            bp_id, ore_ore, clay_ore, obsidian_ore, obsidian_clay, geode_ore, geode_obsidian = map(int, match.groups())
            ore_robot = Recipe(ore=ore_ore)
            clay_robot = Recipe(ore=clay_ore)
            obsidian_robot = Recipe(ore=obsidian_ore, clay=obsidian_clay)
            geode_robot = Recipe(ore=geode_ore, obsidian=geode_obsidian)
            return Blueprint(bp_id, RobotRecipies(ore_robot, clay_robot, obsidian_robot, geode_robot))
        else:
            raise ValueError('Failed to parse blueprint: %', s)

    def maximum_geodes(self, time: int = 24) -> int:
        start = State(time)
        queue = deque()
        queue.append(([start], start))
        seen = {start}
        max_geodes = 0

        while queue:
            this_chain, this_state = queue.popleft()
            for state in this_state.next_state(self):
                if state in seen or state.max_geodes_full < max_geodes:
                    # Worthless
                    continue
                print(state, max_geodes)
                max_geodes = max(max_geodes, state.max_geodes)
                seen.add(state)
                queue.append((this_chain + [state], state))

        return this_chain + [state], max_geodes

# Number of robots
Robots = namedtuple('Robot', RESOURCE, defaults=[1, 0, 0, 0])
# Number of ressources
Resources = namedtuple('Resource', RESOURCE, defaults=[0, 0, 0, 0])

class State(NamedTuple):
    remaining_time: int = 24
    resources: Resources = Resources() 
    robots: Robots = Robots()

    @property
    def max_geodes(self) -> int:
        return self.resources.geode + self.remaining_time * self.robots.geode

    @property
    def max_geodes_full(self) -> int:
        """if we build a geode robot at each remaining iteration"""
        return self.max_geodes + self.remaining_time * (self.remaining_time - 1) // 2      

    def next_state(self, blueprint: Blueprint) -> Iterator['State']:

        # yield each possible way, but
        # Doing some optimization here...

        # For each robot type
        for robot_type, recipe in zip(RESOURCE, blueprint.recipies):

            # Do we even have the robot to produce the requires resources
            if not all([rob > 0 for rob, res in zip(self.robots, recipe) if res > 0]):
                continue

            # How much time do we need to have ressources for that robot, with the actual robot
            needed_time = 1
            next_resources = Resources(*[res + rob for res, rob in zip(self.resources, self.robots)])
            while any([next < actual for next, actual in zip (next_resources, recipe)]):
                next_resources = Resources(*[res + rob for res, rob in zip(next_resources, self.robots)])
                needed_time += 1

            if needed_time > self.remaining_time:
                continue

            # If we build this robot we need to remove the needed resources
            remaining_time = self.remaining_time - needed_time
            next_resources = Resources(*[res - need for res, need in zip(next_resources, recipe)])
            next_robots = self.robots._replace(**dict([(robot_type, getattr(self.robots, robot_type) + 1)]))
            yield self._replace(remaining_time = remaining_time, resources = next_resources, robots = next_robots)


RAW="""Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 2 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian.
Blueprint 2: Each ore robot costs 2 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 8 clay. Each geode robot costs 3 ore and 12 obsidian."""