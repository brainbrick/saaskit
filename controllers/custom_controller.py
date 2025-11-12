from odoo import http
from odoo.http import request
from ..scripts.creatPostDb import restore_database
from ..scripts.createDirectoryStructure import create_user_dir
from ..scripts.fetch_odoo_info import log_nginx_info
from ..scripts.step2 import update_files
from ..scripts.port import get_free_port
from ..scripts.upstream import get_next_available_odoo_number
import random
import time


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
            package = post.get('package')  # New field: Package name

            # Print all data for debug
            print(f"📦 Selected Package: {package}")


            # Basic validation
            # if not (email and name and company and domain and password):
            #     return request.render('database_handler.menu_saas_reg_template', {
            #         'error': "⚠️ Please fill all required fields."
            #     })
            #
            # # -------------------------------------
            # # Run Nginx info logging
            # # -------------------------------------
            # log_nginx_info()
            # print("📝 Logged current Nginx upstream/server info.")
            #
            # input_file = "/home/odoo_port-info.txt"
            # output_upstream_file = "/home/upstream_port_info/odoo_upstream_info.txt"
            # output_port_file = "/home/upstream_port_info/odoo_port-info.txt"
            #
            # update_files(input_file, output_upstream_file, output_port_file)
            # print("✅ Port info files updated successfully!")
            #
            # # Random port for new instance
            # xmlrpc_port = str(get_free_port())
            # print(f"🚀 New Instance Setup for {company} ({domain}) on port {xmlrpc_port}")
            #
            # # (1) Restore database from backup
            # restore_result = restore_database(
            #     master_pwd="C7yB48xPJo3",
            #     name=domain,
            #     endpoint_url="http://localhost:9029",
            #     backup_file_path="restaurant_2025-10-07_19-03-46.zip",
            #     copy=False
            # )
            # print("✅ Database Restore Result:", restore_result)
            #
            # # (2) Create new user directory and nginx config
            # odoo_upstream = get_next_available_odoo_number()  # e.g. 'odoo5'
            #
            # dir_result = create_user_dir(
            #     username=company.replace(" ", "_"),
            #     custom_db_name=domain,
            #     xmlrpc_port=xmlrpc_port,
            #     server_name=domain,
            #     upstream_name=odoo_upstream,
            #     port=xmlrpc_port
            # )
            # print("✅ Directory Structure Result:", dir_result)

            # -------------------------------------
            # 🆕 Create SaaS database record
            # -------------------------------------
            saas_record = request.env['saas.databases'].sudo().create({
                'domain_name': domain,
                'company_name': company,
                'state': 'active',
                # 'db_url': f"http://localhost:{xmlrpc_port}",
            })

            # 🆕 Create the user record linked to the SaaS DB
            user_record = request.env['database.user'].sudo().create({
                'user_name': name,
                'login': email,
                'user_password': password,
                'state': 'active',
                'saas_id': saas_record.id,  # yahi link karta hai one2many ko
            })

            print(f"🎉 SaaS module record created for {company} / {domain} / {email} / {password}")
            print(saas_record.user_ides)  # ye me list of database.user records show karega

            # -------------------------------------
            # After success → redirect to Thank You page
            # -------------------------------------
            return request.redirect('/thank-you')

        except Exception as e:
            print("❌ Error during custom signup automation:", e)
            return request.render('database_handler.menu_saas_reg_template', {
                'error': f"Something went wrong: {e}"
            })
