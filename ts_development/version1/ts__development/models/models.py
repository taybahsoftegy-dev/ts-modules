# -*- coding: utf-8 -*-
from odoo import models, fields, api,_
import time

class Development_Tracking(models.Model):
    _name = 'development.tracking'
    _inherit = ['portal.mixin', 'mail.thread.cc', 'mail.activity.mixin', 'rating.mixin']
    _mail_post_access = 'read'
    _check_company_auto = True
    # _mail_post_access = 'read'

    serial = fields.Integer(string='Serial',tracking=True)
    Date = fields.Date(default=lambda *a: time.strftime('%Y-%m-%d'),tracking=True)
    module = fields.Char(string='Module',tracking=True)
    form = fields.Char(string = 'Form',tracking=True)
    report = fields.Char(string='Report',tracking=True)
    new = fields.Char(string='New',tracking=True)
    description = fields.Text(string= 'Description',tracking=True)
    status = fields.Selection([
        ('open', 'Open'),
        ('closed', 'Closed'),
        ('rejected', 'Rejected')], default='open', tracking=True)
    time_consumed = fields.Char('Time Consumed',tracking=True)
    user_id = fields.Many2one('res.users',
                              default=lambda self: self.env.uid,
                              index=True, tracking=True)
    user_email = fields.Char(related='user_id.email', string='User Email', readonly=True, related_sudo=False)
    partner_id = fields.Many2one('res.partner',
                                 string='Customer',
                                 default=lambda self: self.env.uid,)
    user_email = fields.Char(related='user_id.email', string='User Email', readonly=True, related_sudo=False)

# class Development_Tracking(models.Model):
#     _name = 'Development.Tracking'
#     _description = 'For Tracking Development for TaybahSoft'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
