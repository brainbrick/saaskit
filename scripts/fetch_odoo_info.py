import os
import re

def log_nginx_info(
    config_dir="/etc/nginx/sites-available",
    output_file="/home/odoo_port-info.txt"
):
    """
    Reads all nginx config files and logs Odoo upstream + port info
    into a summary text file.
    """

    try:
        # Clear the output file first
        with open(output_file, 'w'):
            pass

        # Scan config directory
        for config_file in os.listdir(config_dir):
            if config_file.endswith(".conf"):
                config_file_path = os.path.join(config_dir, config_file)

                with open(config_file_path, 'r') as f:
                    content = f.read()

                    # Find upstream & port info
                    upstream_match = re.search(r'upstream\s+odoo[0-9]+\s*{', content)
                    server_match = re.search(r'server\s+127\.0\.0\.1:[0-9]+', content)

                    if upstream_match and server_match:
                        upstream = upstream_match.group(0)
                        server = server_match.group(0)
                        filename = os.path.basename(config_file_path)

                        # Write to output file
                        with open(output_file, 'a') as output:
                            output.write(f"{filename.ljust(35)} - {upstream.ljust(25)} - {server}\n")

        print(f"✅ Odoo upstream & port info logged to {output_file}")

    except Exception as e:
        print(f"❌ Error while logging Nginx info: {e}")
