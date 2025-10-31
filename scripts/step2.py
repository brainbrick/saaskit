#!/usr/bin/env python3
import os
import subprocess

def update_files(input_file, output_upstream_file, output_port_file):
    # Ensure the output directory exists
    os.makedirs(os.path.dirname(output_upstream_file), exist_ok=True)
    
    # Read input file and extract data
    with open(input_file, 'r') as f:
        lines = f.readlines()
    
    # Initialize lists to store extracted data
    upstream_numbers = []
    port_numbers = []
    
    # Extract upstream numbers and port numbers
    for line in lines:
        if 'odoo' in line:
            parts = line.split('odoo')
            if len(parts) > 1:
                upstream_numbers.append(parts[1].split()[0].strip())
        
        if '127.0.0.1:' in line:
            parts = line.split(':')
            if len(parts) > 1:
                port_numbers.append(parts[1].strip())
    
    # Sort extracted numbers
    upstream_numbers = sorted(upstream_numbers, key=int)
    port_numbers = sorted(port_numbers, key=int)
    
    # Write sorted numbers to output files
    with open(output_upstream_file, 'w') as f:
        for number in upstream_numbers:
            f.write(number + '\n')
    
    with open(output_port_file, 'w') as f:
        for number in port_numbers:
            f.write(number + '\n')
    
    # Print confirmation message
    print(f"Files updated: {output_upstream_file}, {output_port_file}")

def main():
    # Define file paths
    input_file = "/home/odoo_port-info.txt"
    output_upstream_file = "/home/upstream_port_info/odoo_upstream_info.txt"
    output_port_file = "/home/upstream_port_info/odoo_port-info.txt"
    
    # Update the files
    update_files(input_file, output_upstream_file, output_port_file)

if __name__ == "__main__":
    main()

