# Generate 100 entries for each log type
import random

def generate_apache_log(num_entries=100):
    lines = []
    for _ in range(num_entries):
        ip = ".".join(map(str, (random.randint(0, 255) for _ in range(4))))
        date = f"01/Jan/2025:00:{random.randint(0, 59):02}:{random.randint(0, 59):02} +0000"
        method = random.choice(["GET", "POST", "PUT", "DELETE"])
        resource = random.choice(["/index.html", "/api/v1/resource", "/contact.html", "/about.html"])
        status = random.choice(["200", "404", "500", "302"])
        size = random.choice(["1234", "567", "0", "345"])
        lines.append(f"{ip} - - [{date}] \"{method} {resource} HTTP/1.1\" {status} {size}\n")
    return lines

def generate_nginx_log(num_entries=100):
    lines = []
    for _ in range(num_entries):
        ip = ".".join(map(str, (random.randint(0, 255) for _ in range(4))))
        user = f"user{random.randint(1, 100)}"
        date = f"01/Jan/2025:00:{random.randint(0, 59):02}:{random.randint(0, 59):02} +0000"
        method = random.choice(["GET", "POST", "PATCH", "PUT"])
        resource = random.choice(["/home", "/login", "/profile", "/settings"])
        status = random.choice(["200", "403", "201", "204"])
        size = random.choice(["512", "1024", "256", "0"])
        lines.append(f"{ip} - {user} [{date}] \"{method} {resource} HTTP/1.1\" {status} {size}\n")
    return lines

def generate_system_log(num_entries=100):
    lines = []
    for _ in range(num_entries):
        date = f"Jan  1 00:{random.randint(0, 59):02}:{random.randint(0, 59):02}"
        host = f"server{random.randint(1, 10)}"
        process = random.choice(["systemd", "kernel", "sshd", "CRON", "sudo"])
        message = random.choice([
            "Started session 1 of user root.",
            "[   1.234567] CPU: 4 PID: 1 Comm: init",
            "Accepted publickey for user1 from 192.168.1.100 port 22 ssh2",
            "(user2) CMD (/usr/bin/some_task)",
            "user3 : TTY=pts/1 ; PWD=/home/user3 ; USER=root ; COMMAND=/bin/ls"
        ])
        lines.append(f"{date} {host} {process}: {message}\n")
    return lines

# Write to files
with open("apache.log", "w") as f:
    f.writelines(generate_apache_log())

with open("nginx.log", "w") as f:
    f.writelines(generate_nginx_log())

with open("system.log", "w") as f:
    f.writelines(generate_system_log())

"Sample log files created successfully."
