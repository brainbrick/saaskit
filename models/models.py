from odoo import models, fields

class ResUsers(models.Model):
    _inherit = 'res.users'

    mobile_number = fields.Char(string="Mobile Number")
    domain1 = fields.Char(string="Domain")
    company_name = fields.Char(string="Company Name")