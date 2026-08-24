"""
IPv4 Validator
Checks whether a string is a valid IPv4 address.
Practices: the FLAG PATTERN (assume valid, flip on any failure, decide once),
.split(), .isdigit(), range checks, functions returning bool.
"""


def is_valid_ipv4(ip):
    parts = ip.split(".")
    if len(parts) != 4:
        return False
    for part in parts:
        if not part.isdigit():          # reject non-numeric (and empty)
            return False
        if int(part) < 0 or int(part) > 255:   # reject out of range
            return False
    return True


# tests
print(is_valid_ipv4("192.168.2.1"))     # True
print(is_valid_ipv4("192.168.2.999"))   # False (octet > 255)
print(is_valid_ipv4("192.168.2"))       # False (only 3 parts)
print(is_valid_ipv4("192.168.a.1"))     # False (non-numeric)
