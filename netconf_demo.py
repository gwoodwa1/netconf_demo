#!/usr/bin/env python3

import os
import sys
import logging
import argparse
from ncclient import manager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)  # Log to stdout
    ]
)
logger = logging.getLogger("NETCONF_Get_Config")

def netconf_get_config(host, username, password, port):
    """Perform a NETCONF get-config operation."""
    try:
        # Connect to the device
        logger.info(f"Connecting to {host} as {username} on port {port}...")
        with manager.connect(
            host=host,
            port=port,
            username=username,
            password=password,
            hostkey_verify=False,  # Disable host key verification for simplicity
            timeout=10
        ) as m:
            # Perform the <get-config> operation
            logger.info("Performing <get-config> operation for running configuration...")
            response = m.get_config(source="running")

            # Log the response
            logger.info("NETCONF response received:")
            logger.info(response.xml)
            return True

    except Exception as e:
        logger.error(f"NETCONF operation failed: {e}")
        return False

def parse_arguments():
    """Parse command-line arguments with environment variable fallbacks."""
    parser = argparse.ArgumentParser(description="Perform a NETCONF get-config operation.")
    parser.add_argument(
        "--host",
        default=os.getenv("NETCONF_HOST", "192.168.1.10"),
        help="Device IP address or hostname (default: NETCONF_HOST env var or 192.168.1.10)"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=os.getenv("NETCONF_PORT", 830),
        help="NETCONF port (default: NETCONF_PORT env var or 830)"
    )
    parser.add_argument(
        "--username",
        default=os.getenv("NETCONF_USERNAME", "admin"),
        help="NETCONF username (default: NETCONF_USERNAME env var or admin)"
    )
    parser.add_argument(
        "--password",
        default=os.getenv("NETCONF_PASSWORD"),
        help="NETCONF password (default: NETCONF_PASSWORD env var)"
    )
    return parser.parse_args()

def main():
    # Parse command-line arguments
    args = parse_arguments()

    # Check if password is provided
    if not args.password:
        logger.error("Password not provided. Use --password or set NETCONF_PASSWORD environment variable.")
        sys.exit(1)

    # Perform the NETCONF get-config operation
    success = netconf_get_config(args.host, args.username, args.password, args.port)
    
    if success:
        logger.info("NETCONF get-config operation completed successfully.")
    else:
        logger.error(f"Failed to perform NETCONF get-config on {args.host}.")
        sys.exit(1)

if __name__ == "__main__":
    main()
