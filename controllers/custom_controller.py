from odoo import http
from odoo.http import request
from ..scripts.creatPostDb import restore_database
from ..scripts.createDirectoryStructure import create_user_dir
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
            mobile = post.get('mobile_number')
            company = post.get('company_name')
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

            # Random port for new instance
            xmlrpc_port = str(random.randint(8070, 9000))
            print(f"🚀 New Instance Setup for {company} ({domain}) on port {xmlrpc_port}")

            # -------------------------------------
            # 🧩 Call your scripts here
            # -------------------------------------

            # (1) Restore database from backup
            restore_result = restore_database(
                master_pwd="admin",  # Odoo master password
                name=domain,  # new DB name (from signup)
                endpoint_url="http://localhost:" + xmlrpc_port,  # Odoo endpoint
                backup_file_path="test_main.zip",  # your backup template name
                copy=False
            )
            print("✅ Database Restore Result:", restore_result)

            # (2) Create new user directory and nginx config
            dir_result = create_user_dir(
                username=company.replace(" ", "_"),
                custom_db_name=domain,
                xmlrpc_port=xmlrpc_port,
                server_name=domain,
                upstream_name=f"{domain}_upstream",
                port="8069"
            )
            print("✅ Directory Structure Result:", dir_result)

            # -------------------------------------
            print(f"🎉 Signup automation done for {company} / {domain}")

            # -------------------------------------
            # After success → redirect to Thank You page
            # -------------------------------------
            return request.redirect('/thank-you')

        except Exception as e:
            print("❌ Error during custom signup automation:", e)
            return request.render('database_handler.menu_saas_reg_template', {
                'error': f"Something went wrong: {e}"
            })
