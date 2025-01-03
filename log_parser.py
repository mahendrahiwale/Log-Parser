import argparse
import re
import os

# Define parsers for different log types
def parse_apache_log(line):
    pattern = r'(?P<ip>[\d.]+) - - \[(?P<date>.*?)\] "(?P<request>[A-Z]+ .*?)" (?P<status>\d+) (?P<size>\d+|-)'
    match = re.match(pattern, line)
    return match.groupdict() if match else None

def parse_nginx_log(line):
    pattern = r'(?P<ip>[\d.]+) - (?P<user>.*?) \[(?P<date>.*?)\] "(?P<request>[A-Z]+ .*?)" (?P<status>\d+) (?P<size>\d+|-)'
    match = re.match(pattern, line)
    return match.groupdict() if match else None

def parse_system_log(line):
    pattern = r'(?P<date>[A-Za-z]{3} +\d+ \d+:\d+:\d+) (?P<host>\S+) (?P<process>\S+): (?P<message>.*)'
    match = re.match(pattern, line)
    return match.groupdict() if match else None

# Dispatch table for log types
LOG_PARSERS = {
    "apache": parse_apache_log,
    "nginx": parse_nginx_log,
    "system": parse_system_log,
}

def highlight_matches(line, pattern):
    return re.sub(pattern, lambda m: f"\033[91m{m.group(0)}\033[0m", line)

def parse_log(file_path, log_type, search_pattern=None, first=None, last=None, timestamps=False, ipv4=False, ipv6=False):
    if log_type not in LOG_PARSERS:
        raise ValueError(f"Unsupported log type: {log_type}")

    parser = LOG_PARSERS[log_type]

    with open(file_path, 'r') as log_file:
        lines = log_file.readlines()

    if first:
        lines = lines[:first]
    if last:
        lines = lines[-last:]

    for line in lines:
        if timestamps and not re.search(r'\b\d{2}:\d{2}:\d{2}\b', line):
            continue
        if ipv4 and not re.search(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', line):
            continue
        if ipv6 and not re.search(r'\b([0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}\b', line):
            continue

        parsed_data = parser(line)
        if parsed_data:
            if search_pattern:
                if re.search(search_pattern, line):
                    if ipv4:
                        line = highlight_matches(line, r'\b(?:\d{1,3}\.){3}\d{1,3}\b')
                    if ipv6:
                        line = highlight_matches(line, r'\b([0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}\b')
                    print(line.strip())
            else:
                if ipv4:
                    line = highlight_matches(line, r'\b(?:\d{1,3}\.){3}\d{1,3}\b')
                if ipv6:
                    line = highlight_matches(line, r'\b([0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}\b')
                print(line.strip())

def main():
    parser = argparse.ArgumentParser(description="Parse and analyze log files.")
    parser.add_argument("file", help="Path to the log file")
    parser.add_argument("--type", choices=LOG_PARSERS.keys(), required=True, help="Type of log file (e.g., apache, nginx, system)")
    parser.add_argument("--search", help="Optional search pattern")
    parser.add_argument("-f", "--first", type=int, help="Print first NUM lines")
    parser.add_argument("-l", "--last", type=int, help="Print last NUM lines")
    parser.add_argument("-t", "--timestamps", action="store_true", help="Print lines that contain a timestamp in HH:MM:SS format")
    parser.add_argument("-i", "--ipv4", action="store_true", help="Print lines that contain an IPv4 address, matching IPs are highlighted")
    parser.add_argument("-I", "--ipv6", action="store_true", help="Print lines that contain an IPv6 address (standard notation), matching IPs are highlighted")

    args = parser.parse_args()

    if not os.path.exists(args.file):
        print(f"Error: File '{args.file}' does not exist.")
        return

    try:
        parse_log(
            args.file,
            args.type,
            search_pattern=args.search,
            first=args.first,
            last=args.last,
            timestamps=args.timestamps,
            ipv4=args.ipv4,
            ipv6=args.ipv6
        )
    except ValueError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
