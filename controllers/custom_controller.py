from odoo import http
from odoo.http import request
from ..scripts.creatPostDb import restore_database
from ..scripts.createDirectoryStructure import create_user_dir
from ..scripts.fetch_odoo_info import log_nginx_info
from ..scripts.step2 import update_files# 🆕 Added import
from ..scripts.port import get_free_port
from ..scripts.upstream import get_next_available_odoo_number
import random


class CustomPage(http.Controller):

    @http.route('/custom/page', type='http', auth='public', website=True)
    def custom_page(self, **kw):
        """Render custom signup form page"""
        print("📄 Custom form page loaded")
        return request.render('database_handler.menu_saas_reg_template', {})

    @http.route('/custom/form/submit', type='http', auth='public', website=True, csrf=True)
    def custom_form_submit(self, **post):
        """Handle custom form submission and run automation scripts"""
        print("✅ Form Submitted:", post)
        try:
            # Extract form data
            email = post.get('email')
            name = post.get('name')
            mobile = post.get('mobile')
            company = post.get('company')
            domain = post.get('domain')
            password = post.get('password')
            package = post.get('package')  # 🆕 New field: Package name

            # Print all data for debug
            print(f"📦 Selected Package: {package}")

            # Basic validation
            if not (email and name and company and domain and password):
                return request.render('database_handler.menu_saas_reg_template', {
                    'error': "⚠️ Please fill all required fields."
                })



            # -------------------------------------
            # 🧩 Run Nginx info logging first
            # -------------------------------------
            log_nginx_info()
            print("📝 Logged current Nginx upstream/server info.")

            input_file = "/home/odoo_port-info.txt"
            output_upstream_file = "/home/upstream_port_info/odoo_upstream_info.txt"
            output_port_file = "/home/upstream_port_info/odoo_port-info.txt"

            update_files(input_file, output_upstream_file, output_port_file)
            print("✅ Port info files updated successfully!")

            # Random port for new instance
            xmlrpc_port = str(get_free_port())  # 🆕 Use the first available port
            print(f"🚀 New Instance Setup for {company} ({domain}) on port {xmlrpc_port}")

            # (1) Restore database from backup
            restore_result = restore_database(
                master_pwd="C7yB48xPJo3",  # Odoo master password
                name=domain,  # new DB name (from signup)
                endpoint_url="http://localhost:" + xmlrpc_port,  # Odoo endpoint
                backup_file_path="/home/ins/backup/upload/restaurant_2025-10-07_19-03-46.zip",  # your backup template name
                copy=False
            )
            print("✅ Database Restore Result:", restore_result)

            # (2) Create new user directory and nginx config
            odoo_upstream = get_next_available_odoo_number()  # e.g. 'odoo5'

            dir_result = create_user_dir(
                username=company.replace(" ", "_"),
                custom_db_name=domain,
                xmlrpc_port=xmlrpc_port,
                server_name=domain,
                upstream_name=odoo_upstream,  # <-- use the method's return here
                port=xmlrpc_port
            )
            print("✅ Directory Structure Result:", dir_result)
            # -------------------------------------
            print(f"🎉 Signup automation done for {company} / {domain}")

            # -------------------------------------
            # After success → redirect to Thank You page
            # -------------------------------------
            return request.redirect('https://erp-login.brainbrick.info/thank-you')

        except Exception as e:
            print("❌ Error during custom signup automation:", e)
            return request.render('database_handler.menu_saas_reg_template', {
                'error': f"Something went wrong: {e}"
            })
