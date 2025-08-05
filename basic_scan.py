import socket
import sys
from datetime import datetime

# --- Configuration ---
# ANSI color codes for output
GREEN = '\033[0;32m'
RED = '\033[0;31m'
YELLOW = '\033[0;33m'
BLUE = '\033[0;34m'
NC = '\033[0m' # No Color

# --- Main Function ---
def run_port_scanner():
    """
    Main function to get user input and run the port scanner.
    """
    print(f"{BLUE}========================================={NC}")
    print(f"{BLUE}  Simple Python Port Scanner             {NC}")
    print(f"{BLUE}========================================={NC}")

    # Get target host from user
    target = input(f"{YELLOW}Enter target IP address or hostname (e.g., 127.0.0.1 or example.com): {NC}")

    # Resolve hostname to IP address
    try:
        target_ip = socket.gethostbyname(target)
        print(f"{BLUE}Scanning target: {target_ip}{NC}")
    except socket.gaierror:
        print(f"{RED}Error: Hostname could not be resolved. Exiting.{NC}")
        sys.exit()

    # Get port range from user
    port_range_str = input(f"{YELLOW}Enter port range (e.g., 1-1024 or 80,443,8080): {NC}")

    ports_to_scan = []
    if '-' in port_range_str:
        try:
            start_port, end_port = map(int, port_range_str.split('-'))
            ports_to_scan = range(start_port, end_port + 1)
        except ValueError:
            print(f"{RED}Error: Invalid port range format. Please use 'start-end'. Exiting.{NC}")
            sys.exit()
    elif ',' in port_range_str:
        try:
            ports_to_scan = [int(p.strip()) for p in port_range_str.split(',')]
        except ValueError:
            print(f"{RED}Error: Invalid port list format. Please use 'port1,port2'. Exiting.{NC}")
            sys.exit()
    else:
        try:
            single_port = int(port_range_str)
            ports_to_scan = [single_port]
        except ValueError:
            print(f"{RED}Error: Invalid port number. Exiting.{NC}")
            sys.exit()

    # Record the start time
    t1 = datetime.now()

    print(f"{BLUE}Scanning ports...{NC}")

    open_ports = []

    # Iterate over the specified ports
    for port in ports_to_scan:
        if not (0 <= port <= 65535):
            print(f"{YELLOW}Skipping invalid port: {port}{NC}")
            continue

        # Create a socket object
        # AF_INET specifies the address family (IPv4)
        # SOCK_STREAM specifies the socket type (TCP)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Set a timeout for the connection attempt
        sock.settimeout(1) # 1 second timeout

        # Attempt to connect to the target IP and port
        result = sock.connect_ex((target_ip, port)) # connect_ex returns an error indicator

        if result == 0:
            # If result is 0, the connection was successful (port is open)
            print(f"  Port {port}: {GREEN}Open{NC}")
            open_ports.append(port)
        else:
            # print(f"  Port {port}: Closed") # Uncomment for verbose output
            pass # Keep output clean for closed ports

        # Close the socket
        sock.close()

    # Record the end time
    t2 = datetime.now()
    # Calculate the total time taken
    total_time = t2 - t1

    print(f"{BLUE}========================================={NC}")
    if open_ports:
        print(f"{BLUE}Scan complete. Open ports found:{NC}")
        for p in open_ports:
            print(f"  - {GREEN}{p}{NC}")
    else:
        print(f"{YELLOW}Scan complete. No open ports found in the specified range.{NC}")

    print(f"{BLUE}Scanning finished in: {total_time}{NC}")
    print(f"{BLUE}========================================={NC}")

# Ensure the script runs when executed directly
if __name__ == "__main__":
    run_port_scanner()
