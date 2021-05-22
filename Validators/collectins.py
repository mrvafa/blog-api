import re


def min_length_validation(value, length):
    return len(value) >= length


def max_length_validation(value, length):
    return len(value) <= length


def is_digit_validation(value):
    return value.is_digit()


def contains_digit_validation(value):
    pattern = r'\d'
    if re.findall(pattern, value):
        return True


def pattern_validation(value, pattern):
    return re.match(pattern, value) is not None and re.match(pattern, value).string == value
