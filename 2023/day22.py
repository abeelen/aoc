from dataclasses import dataclass
from typing import List, NamedTuple


class Pos(NamedTuple):
    x: int
    y: int
    z: int

# https://stackoverflow.com/questions/3838329/how-can-i-check-if-two-segments-intersect

def ccw(A,B,C):
    return (C.y-A.y) * (B.x-A.x) > (B.y-A.y) * (C.x-A.x)

# Return true if line segments AB and CD intersect
def intersect(A,B,C,D):
    return ccw(A,C,D) != ccw(B,C,D) and ccw(A,B,C) != ccw(A,B,D)

class Brick(NamedTuple):
    start: Pos
    end: Pos

    def max_x(self):
        return max(self.start.x, self.end.x) 

    def min_x(self):
        return min(self.start.x, self.end.x) 

    def max_y(self):
        return max(self.start.y, self.end.y) 

    def min_y(self):
        return min(self.start.y, self.end.y) 

        
    # def intersect(self, other):
    #     return intersect(self.start, self.end, other.start, other.end)


    def intersect(self, other):
        """Return if self intersects with other"""
        if self.max_x() < other.min_x() or self.min_x() > other.max_x():
            return False        # doesn't intersect in x dimension
        if self.max_y() < other.min_y() or self.min_y() > other.max_y():
            return False        # doesn't intersect in y dimension
        return True

    def to_z(self, z):
        dz = self.end.z - self.start.z 
        start = Pos(self.start.x, self.start.y, z)
        end = Pos(self.end.x, self.end.y, z + dz) 
        return Brick(start, end)

@dataclass
class Bricks:
    bricks: List[Brick]
    
    @classmethod
    def parse_raw(cls, raw: str) -> "Bricks":
        bricks: List[Brick] = []
        for line in raw.split('\n'):
            start, end = line.split('~')
            start = map(int, start.split(','))
            end = map(int, end.split(','))

            bricks.append(Brick(Pos(*start), Pos(*end)))
        
        return cls(bricks)
    
    def fall(self):
        bricks = sorted(self.bricks, key=lambda item: min(item.start.z, item.end.z))
        
        new_positions: List[Bricks] = [bricks[0].to_z(1)]
        for brick in bricks[1:]:
            for other in new_positions[::-1]:
                if brick.intersect(other):
                    new_positions.append(brick.to_z(max(other.start.z, other.end.z) + 1))
                    continue
            new_positions.append(brick.to_z(1))         
    
RAW="""1,0,1~1,2,1
0,0,2~2,0,2
0,2,3~2,2,3
0,0,4~0,2,4
2,0,5~2,2,5
0,1,6~2,1,6
1,1,8~1,1,9"""

BRICKS = Bricks.parse_raw(RAW)
self = BRICKS