from collections import namedtuple
from itertools import batched
from typing import List

RAW_INPUT = """2333133121414131402"""

RAW_INPUT_SMALL = "12345"

File = namedtuple("File", ("id", "length", "free"))


def parse_input(raw: str) -> List[File]:
    output = []
    for index, args in enumerate(batched(raw, 2)):
        length = args[0]
        free = args[1] if len(args) > 1 else 0
        output.append(File(index, int(length), int(free)))
    return output


def find_index_free(disk_map: List[File]) -> int:
    for index, file in enumerate(disk_map):
        if file.free > 0:
            return index


def compress_diskmap(disk_map: List[File]) -> List[File]:
    index_free = find_index_free(disk_map)
    while index_free != len(disk_map) - 1:
        file_before = disk_map[index_free]
        file_to_move = disk_map.pop()
        can_move_length = min(file_to_move.length, file_before.free)
        still_free = file_before.free - can_move_length
        still_to_move = file_to_move.length - can_move_length

        disk_map[index_free] = File(file_before.id, file_before.length, 0)
        disk_map.insert(
            index_free + 1, File(file_to_move.id, can_move_length, still_free)
        )

        if still_to_move != 0:
            disk_map.append(
                File(
                    file_to_move.id,
                    still_to_move,
                    file_to_move.free + can_move_length,
                )
            )
        else:
            last_file = disk_map[-1]
            disk_map[-1] = File(
                last_file.id,
                last_file.length,
                last_file.free + file_to_move.length + file_to_move.free,
            )

        index_free = find_index_free(disk_map)

    return disk_map


def find_free_id(disk_map: List[File], length) -> int:
    for index, file in enumerate(disk_map):
        if file.free >= length:
            return index


def find_index_id(disk_map: List[File], _id) -> int:
    for index, file in enumerate(disk_map):
        if file.id == _id:
            return index
    return None


def compress_diskmap_id(disk_map: List[File]) -> List[File]:
    # Where to move
    ids = sorted([file.id for file in disk_map], reverse=True)

    # First id always sorted
    for _id in ids:
        # print(diskmap__repr__(disk_map), _id)
        index_to_move = find_index_id(disk_map, _id)
        index_free = find_free_id(disk_map, disk_map[index_to_move].length)
        if index_free is None or index_free > index_to_move:
            continue

        file_before = disk_map[index_free]
        file_to_move = disk_map[index_to_move]

        # Compute lengths
        can_move_length = min(file_to_move.length, file_before.free)
        still_free = file_before.free - can_move_length
        still_to_move = file_to_move.length - can_move_length

        disk_map[index_free] = File(file_before.id, file_before.length, 0)
        disk_map.insert(
            index_free + 1, File(file_to_move.id, can_move_length, still_free)
        )
        # Beware that with the insert the index has changed
        index_to_move += 1

        if still_to_move != 0:
            disk_map[index_to_move] = File(
                file_to_move.id,
                still_to_move,
                file_to_move.free + can_move_length,
            )
        else:
            file_to_move = disk_map.pop(index_to_move)
            new_before = disk_map[index_to_move - 1]
            disk_map[index_to_move - 1] = File(
                new_before.id,
                new_before.length,
                new_before.free + file_to_move.length + file_to_move.free,
            )

    return disk_map


def diskmap_checksum(disk_map: List[File]) -> int:
    checksum = 0
    pos = 0
    for file in disk_map:
        checksum += sum([file.id * index for index in range(pos, pos + file.length)])
        pos += file.length + file.free
    return checksum


def diskmap__repr__(disk_map: List[File]) -> str:
    return "".join([str(file.id) * file.length + "." * file.free for file in disk_map])


assert (
    diskmap__repr__(compress_diskmap(parse_input(RAW_INPUT_SMALL))) == "022111222......"
)

assert (
    diskmap__repr__(compress_diskmap(parse_input(RAW_INPUT)))
    == "0099811188827773336446555566.............."
)

assert (
    diskmap__repr__(compress_diskmap_id(parse_input(RAW_INPUT)))
    == "00992111777.44.333....5555.6666.....8888.."
)

assert diskmap_checksum(compress_diskmap(parse_input(RAW_INPUT))) == 1928
assert diskmap_checksum(compress_diskmap_id(parse_input(RAW_INPUT))) == 2858

with open("day09.txt", "r") as f:
    raw_input = f.read().strip()

print(diskmap_checksum(compress_diskmap(parse_input(raw_input))))
print(diskmap_checksum(compress_diskmap_id(parse_input(raw_input))))
