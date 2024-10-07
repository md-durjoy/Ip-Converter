import os
import socket
import time
from urllib.parse import urlparse

# Display tool name
print("""

██╗██████╗        ██████╗ ██████╗ ███╗   ██╗██╗   ██╗███████╗██████╗ ████████╗███████╗██████╗ 
██║██╔══██╗      ██╔════╝██╔═══██╗████╗  ██║██║   ██║██╔════╝██╔══██╗╚══██╔══╝██╔════╝██╔══██╗
██║██████╔╝█████╗██║     ██║   ██║██╔██╗ ██║██║   ██║█████╗  ██████╔╝   ██║   █████╗  ██████╔╝
██║██╔═══╝ ╚════╝██║     ██║   ██║██║╚██╗██║╚██╗ ██╔╝██╔══╝  ██╔══██╗   ██║   ██╔══╝  ██╔══██╗
██║██║           ╚██████╗╚██████╔╝██║ ╚████║ ╚████╔╝ ███████╗██║  ██║   ██║   ███████╗██║  ██║
╚═╝╚═╝            ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝  ╚═══╝  ╚══════╝╚═╝  ╚═╝   ╚═╝   ╚══════╝╚═╝  ╚═╝
                                                                                              
TOOL: Domain to IP Converter
""")

# Ask user for input domain file name
domain_file = input("Write your Domain File Name (must be a .txt file): ")

# Check if the file exists and is a .txt file
if not os.path.exists(domain_file) or not domain_file.endswith('.txt'):
    print("Invalid file! Please provide a valid .txt file.")
    exit()

# Ask user for output file name
output_file = input("Enter the output file name where IP addresses will be written (must end with .txt): ")

# Ensure the output file ends with .txt
if not output_file.endswith('.txt'):
    print("Output file must end with .txt!")
    exit()

# List to store IP addresses
ip_addresses = []

# Function to extract domain from URL
def extract_domain(url):
    parsed_url = urlparse(url)
    if not parsed_url.scheme:
        url = 'http://' + url  # Add a default scheme
        parsed_url = urlparse(url)
    return parsed_url.netloc

# Function to validate domain
def is_valid_domain(domain):
    if len(domain) > 255:
        return False
    # Ensure each label is between dots and no label is longer than 63 characters
    labels = domain.split('.')
    if all(0 < len(label) <= 63 for label in labels):
        return True
    return False

# Open the domain file and read URLs
with open(domain_file, 'r') as file:
    urls = file.readlines()
    for url in urls:
        url = url.strip()  # Remove leading/trailing whitespace
        if url:
            # Extract domain from the URL
            domain = extract_domain(url)
            if domain:
                try:
                    # Validate domain before resolving
                    if is_valid_domain(domain):
                        # Display loading animation with skull
                        for i in range(5):  # Adjust the range for more loading steps
                            print("-" * (i + 1) + "💀", end='\r')
                            time.sleep(0.3)  
                        
                        # Resolve domain name to IP address
                        ip = socket.gethostbyname(domain)
                        print(f"Resolved {domain} to {ip}")  # Log resolved IP
                        ip_addresses.append(ip)  # Only store the IP address
                        
                    else:
                        print(f"Invalid domain: {domain}")
                        ip_addresses.append("Invalid domain")
                except socket.gaierror as e:
                    print(f"Unable to resolve {domain}: {e}")
                    ip_addresses.append("Unable to resolve")
                except UnicodeError as ue:
                    print(f"Domain encoding issue with {domain}: {ue}")
                    ip_addresses.append("Encoding error")

# Write only the IP addresses to the output file
with open(output_file, 'w') as file:
    for ip in ip_addresses:
        if ip not in ["Unable to resolve", "Invalid domain", "Encoding error"]:
            file.write(ip + '\n')

# Confirmation message
print(f"IP addresses have been written to {output_file}")
