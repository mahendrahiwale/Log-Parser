# Log Parser and Highlighter

This script is a command-line tool for parsing various types of log files. It supports filtering, highlighting, and extracting useful information from Apache, Nginx, and system logs.

---

## Features
- **Log Type Support:** Apache, Nginx, and system logs.
- **Flexible Filtering:** Filter lines by:
  - Custom search patterns.
  - Presence of timestamps in `HH:MM:SS` format.
  - IPv4 or IPv6 addresses.
- **Highlight Matches:** Highlight matching IPv4 or IPv6 addresses for better readability.
- **Custom Line Ranges:** Limit output to the first or last `N` lines of the log.
- **Dynamic Parsing:** Uses regex to extract and structure log data based on the log type.

### `generate_logs.py`
- Generate synthetic logs for:
  - Apache logs.
  - Nginx logs.
  - System logs.
- Customizable output:
  - Specify the number of log lines to generate.
  - Control log content with placeholders for testing specific cases.

---

## Requirements
- Python 3.x
- No additional libraries are required as it uses built-in modules (`argparse`, `re`, `os`).

---

## Usage

### Command-Line Arguments
Run the script with the following options:

```bash
python log_parser.py <file> --type <log_type> [options]

Examples :

Parse an Apache log file and show lines with IPv4 addresses:
    python log_parser.py /path/to/apache.log --type apache -i

Parse the last 10 lines of a system log file and filter by a search pattern:
    python log_parser.py /path/to/system.log --type system -l 10 --search "error"

Parse an Nginx log file and highlight IPv6 addresses:
    python log_parser.py /path/to/nginx.log --type nginx -I


