import os
import argparse
import subprocess
import time

def create_user_dir(username, custom_db_name, xmlrpc_port, server_name, upstream_name, port, base_dir="/odoo_dir"):
    """
    Creates a directory structure for a new Odoo user, including configuration files,
    systemd service files, and Nginx configuration, and then restarts the relevant services.

    Args:
        username: The username for the new Odoo user.
        custom_db_name: The custom database name for Odoo.
        xmlrpc_port: The XML-RPC port for Odoo.
        server_name: The server name for the Nginx configuration.
        upstream_name: The upstream name for the Odoo instance.
        port: The port for the Odoo instance.
        base_dir: The base directory to create the user directory under (default: /odoo_dir).

    Returns:
        str: A summary of the operations performed.
    """

    # Create user directory in /home
    user_dir = os.path.join(base_dir, username)
    subdirs = ["conf", "log", "custom"]

    # Create user directory
    os.makedirs(user_dir, exist_ok=True)

    # Create subdirectories
    for subdir in subdirs:
        os.makedirs(os.path.join(user_dir, subdir), exist_ok=True)

    # Create Odoo configuration file
    conf_file_path = os.path.join(user_dir, "conf", f"{username}.conf")
    with open(conf_file_path, "w") as f:
        f.write("[options]\n")
        f.write("admin_passwd = C7yB48xPJo3\n")
        f.write("db_host = 127.0.0.1\n")
        f.write("db_port = 5432\n")
        f.write("db_user = umair\n")
        f.write("db_password = w9M5wFlVINLC7y\n")
        f.write("pg_path = /usr/lib/postgresql/16/bin\n")
        f.write("addons_path = /odoo/general/odoo/addons,/odoo/general_custom_addons/addons\n")
        f.write("default_productivity_apps = True\n")
        f.write(";admin_passwd = $pbkdf2-sha512$600000$Q4gxBmDMuXfO2Tvn3DunVA$uK1v5Sya7BmiH8P2kzyEJ9qbGc/EsB0B0WTif1pJUS//dG7sdbTJ7aaiPb/QIaR48d4u7gyzUabKiW48Ut>\n")
        f.write(f"xmlrpc_port = {xmlrpc_port}\n")  # Use custom XML-RPC port
        f.write(f"db_name = {custom_db_name}\n")  # Use custom database name

    # Create log directory and log files
    log_dir = os.path.join(user_dir, "log")
    os.makedirs(log_dir, exist_ok=True)
    open(os.path.join(log_dir, f"odoo-{username}.log"), "a").close()  # Create odoo log file
    open(os.path.join(log_dir, f"odoo-{username}-error.log"), "a").close()  # Create error log file

    # Create nginx configuration file
    nginx_conf_dir = "/etc/nginx/sites-available"
    os.makedirs(nginx_conf_dir, exist_ok=True)
    nginx_conf_path = os.path.join(nginx_conf_dir, f"{username}mawriderp.conf")
    nginx_conf_content = """upstream {upstream_name} {{
    server 127.0.0.1:{port};
}}

server {{
    listen 80;
    server_name {server_name}.brainbrick.info;

    # Redirect HTTP to HTTPS
    return 301 https://$host$request_uri;
}}

server {{
    listen 443 ssl;
    server_name {server_name}.brainbrick.info;

    ssl_certificate /etc/letsencrypt/live/brainbrick.info/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/brainbrick.info/privkey.pem;

    # Add any additional SSL configurations as needed

    # Add Content-Security-Policy header
    add_header Content-Security-Policy upgrade-insecure-requests;

    location / {{
        proxy_pass http://{upstream_name};
        proxy_redirect off;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }}
}}"""
    with open(nginx_conf_path, "w") as f:
        f.write(nginx_conf_content.format(upstream_name=upstream_name, port=port, server_name=server_name))

    # Create systemd service unit file
    systemd_dir = "/etc/systemd/system"
    os.makedirs(systemd_dir, exist_ok=True)
    service_path = os.path.join(systemd_dir, f"odoo-{username}.service")
    systemd_content = """[Unit]
Description=Odoo Service for {username}
Requires=postgresql.service
After=network.target postgresql.service

[Service]
User=root
Group=root
Environment="VIRTUAL_ENV=/odoo/general_odoo_env"
Environment="PATH=/odoo/general_odoo_env/bin:$PATH"
Environment=PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/usr/bin/wkhtmltopdf
ExecStart=/bin/bash -c 'source /odoo/general_odoo_env/bin/activate && /odoo/general/odoo/odoo-bin -c /odoo_dir/{username}/conf/{username}.conf'
Environment="PG_PATH=/usr/lib/postgresql/16/bin"
WorkingDirectory=/odoo/
StandardOutput=file:/odoo_dir/{username}/log/odoo-{username}.log
StandardError=file:/odoo_dir/{username}/log/odoo-{username}-error.log
Restart=always

[Install]
WantedBy=multi-user.target"""
    with open(service_path, "w") as f:
        f.write(systemd_content.format(username=username))

    # Restart services and show output
    restart_commands = [
        "sudo systemctl daemon-reload",
        "sudo systemctl restart nginx.service",
        f"sudo systemctl enable odoo-{username}.service",
        f"sudo systemctl start odoo-{username}.service"
    ]

    for command in restart_commands:
        output, error = execute_command(command)
        if error:
            print(f"Error executing '{command}': {error}")
        else:
            print(f"Output of '{command}': {output}")

            restart_again_commands = [
                f"sudo systemctl restart odoo-{username}.service"
            ]
            time.sleep(30)
            execute_command(restart_again_commands)

    value = f"Directory structure created for user: {username}, Configuration file created: {conf_file_path}, Log directory created: {log_dir}, Nginx configuration file generated: {nginx_conf_path}, Systemd service unit file generated: {service_path}"
    return value

def execute_command(command):
    """
    Execute a system command and return the output and error, if any.

    Args:
        command (str): The command to execute.

    Returns:
        output (str): The command's standard output.
        error (str): The command's standard error.
    """
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()
    return output.decode('utf-8'), error.decode('utf-8')

# Main code
if __name__ == "__main__":

    # Create the parser
    parser = argparse.ArgumentParser(description='Create directory structure for a new Odoo user.')

    # Add the arguments
    parser.add_argument('username', type=str, help='The username for the new Odoo user')
    parser.add_argument('server_name', type=str, help='The server name for the Nginx configuration')
    parser.add_argument('upstream_name', type=str, help='The upstream name for the Odoo instance')
    parser.add_argument('port', type=str, help='The port')
    parser.add_argument('custom_db_name', type=str, help='The custom database name')
    parser.add_argument('xmlrpc_port', type=str, help='The XML-RPC port')

    # Parse the arguments
    args = parser.parse_args()

    # Now you can use the arguments in your script
    username = args.username
    server_name = args.server_name
    upstream_name = args.upstream_name
    port = args.port
    custom_db_name = args.custom_db_name
    xmlrpc_port = args.xmlrpc_port

    return_value = create_user_dir(username, custom_db_name, xmlrpc_port, server_name, upstream_name, port)
    
    print(return_value)
