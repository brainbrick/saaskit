# File: scripts/find_free_port.py
def get_free_port(input_file="/home/upstream_port_info/odoo_port-info.txt", start=9000, end=9999):
    """
    Returns the first available port number between `start` and `end`
    that is not listed in the input file.
    """
    try:
        # Read existing numbers from file
        numbers = set()
        with open(input_file, 'r') as f:
            for line in f:
                numbers.add(line.strip())

        # Find first available port
        for i in range(start, end):
            if str(i) not in numbers:
                return i

    except FileNotFoundError:
        # If file doesn't exist, just return the start of range
        return start

    # If all ports are taken, return None
    return None
