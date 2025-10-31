#!/usr/bin/env python3
import os

def get_next_available_odoo_number():
    """
    Reads /home/upstream_port_info/odoo_upstream_info.txt
    and returns the first available 'odoo' number as a string, e.g. 'odoo5'.
    """
    input_file = "/home/upstream_port_info/odoo_upstream_info.txt"

    if not os.path.exists(input_file):
        raise FileNotFoundError(f"{input_file} not found")

    numbers = set()
    with open(input_file, 'r') as f:
        for line in f:
            number = line.split()[0]  # First column
            if number.startswith("odoo"):
                number = number[4:]  # Remove 'odoo' prefix
            numbers.add(number)

    i = 1
    while True:
        if str(i) not in numbers:
            return f"odoo{i}"
        i += 1
