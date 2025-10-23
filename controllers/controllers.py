from odoo.addons.auth_signup.controllers.main import AuthSignupHome
from odoo.http import request, route
from ..scripts.creatPostDb import restore_database
from ..scripts.createDirectoryStructure import create_user_dir
import random


class CustomSignupController(AuthSignupHome):

    @route('/web/signup', type='http', auth='public', website=True, sitemap=False)
    def web_auth_signup(self, *args, **kw):
        qcontext = self.get_auth_signup_qcontext()
        print("📥 Signup Data:", kw)

        # Default Odoo signup handling
        response = super(CustomSignupController, self).web_auth_signup(*args, **kw)

        try:
            # Extract extra fields
            mobile = kw.get('mobile_number')
            domain = kw.get('domain1')
            company = kw.get('company_name')

            if mobile and domain and company:
                # Just to generate a random port
                xmlrpc_port = str(random.randint(8070, 9000))

                # -------------------------------------
                # 🧩 Call your scripts here
                # -------------------------------------

                # (1) Restore database from backup
                restore_result = restore_database(
                    master_pwd="admin",  # Odoo master password
                    name=domain,         # new DB name (from signup)
                    endpoint_url="http://localhost:"+xmlrpc_port,  # Odoo endpoint
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

        except Exception as e:
            print("❌ Error during signup automation:", e)

        return response
