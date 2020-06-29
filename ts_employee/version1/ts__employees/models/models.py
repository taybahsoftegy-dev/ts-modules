# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Employee_inherit(models.Model):
    _inherit = 'hr.employee'
    _name= 'hr.employee'

    emp_no = fields.Char(string='Employee No')
    emp_name_ar = fields.Char(string='Emp Name Arabic')


# class ts__employees(models.Model):
#     _name = 'ts__employees.ts__employees'
#     _description = 'ts__employees.ts__employees'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100


