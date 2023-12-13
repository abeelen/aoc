def find_marker(raw:str) -> int:
    i = 4
    while len(set(raw[i-4:i])) < 4:
        i += 1
    return i

def find_start_of_message(raw:str) -> int:
    i = 14
    while len(set(raw[i-14:i])) < 14:
        i += 1
    return i

assert find_marker("mjqjpqmgbljsphdztnvjfqwrcgsmlb") == 7

assert find_marker("bvwbjplbgvbhsrlpgdmjqwftvncz") ==  5
assert find_marker("nppdvjthqldpwncqszvftbrmjlhg") == 6
assert find_marker("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg") == 10
assert find_marker("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw") == 11

with open('day06.txt') as f:
    raw = f.read().strip()

print(find_marker(raw))


assert find_start_of_message("mjqjpqmgbljsphdztnvjfqwrcgsmlb") == 19
assert find_start_of_message("bvwbjplbgvbhsrlpgdmjqwftvncz") ==  23
assert find_start_of_message("nppdvjthqldpwncqszvftbrmjlhg") == 23
assert find_start_of_message("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg") == 29
assert find_start_of_message("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw") == 26

print(find_start_of_message(raw))
