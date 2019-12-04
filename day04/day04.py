from collections import Counter

def check_password(password: str) -> bool:

    # It is a six-digit number.
    # if len(password) != 6:
    #     return False
    # Two adjacent digits are the same (like 22 in 122345).
    # We must have at least one duplicate
    if len(set(password)) > 5:
        return False
    # Going from left to right, the digits never decrease; they only ever increase or stay the same (like 111123 or 135679).
    # Would also insure that duplicate values ARE adjacent
    return all([a<= b for a, b in zip(password, password[1:])])

assert check_password("122345") is True
assert check_password("111123") is True
assert check_password("111111") is True
assert check_password("223450") is False
assert check_password("123789") is False

START = 145852
END = 616942

# passwords = [password for password in range(START, END) if check_password(str(password))]
# print(len(passwords))

def check_new_criteria(password: str) -> bool:
    if not check_password(password):
        return False
    # the two adjacent matching digits are not part of a larger group of matching digits.
    return any([count == 2 for count in Counter(password).values()])


assert check_new_criteria("112233") is True
assert check_new_criteria("123444") is False
assert check_new_criteria("111122") is True

passwords = [password for password in range(START, END) if check_new_criteria(str(password))]
print(len(passwords))