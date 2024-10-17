#!/usr/bin/env python3

import os
import re
import argparse

def replace_ip_port(directory, new_ip, new_port=None):
    # Define regex patterns for valid IP address and port
    ip_pattern = re.compile(r'(?<!\d)(\d{1,3}\.){3}\d{1,3}(?!\d)')
    port_pattern = re.compile(r'\b(?!0)\d{1,5}\b')  # Port cannot be 0 and must be up to 65535

    for root, dirs, files in os.walk(directory):
        for filename in files:
            file_path = os.path.join(root, filename)
            try:
                # Open the file and read its content
                with open(file_path, 'r') as file:
                    content = file.read()

                # Replace valid IP addresses
                updated_content = ip_pattern.sub(new_ip, content)

                # Replace valid ports only if new_port is provided
                if new_port is not None:
                    updated_content = port_pattern.sub(new_port, updated_content)

                # Write the changes back to the file if there were any replacements
                if updated_content != content:
                    with open(file_path, 'w') as file:
                        file.write(updated_content)
                    print(f"Updated: {file_path}")

            except Exception as e:
                print(f"Failed to process {file_path}: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Replace IP addresses and ports in files.")
    parser.add_argument("-d", "--directory", default=os.getcwd(), help="Directory to search for files (default: current directory).")
    parser.add_argument("-i", "--ip", required=True, help="New IP address to replace with.")
    parser.add_argument("-p", "--port", help="New port to replace with (optional).")  # Made optional
    args = parser.parse_args()

    replace_ip_port(args.directory, args.ip, args.port)

