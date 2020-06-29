# -*- coding: utf-8 -*-

from odoo import models, fields, api,_

class inventory_product(models.Model):
    _inherit ='product.template'
    _name = 'product.template'

    brand_id = fields.Many2one('product.brand',string='Brand ID')
    part2_no = fields.Char(string='Part2 Num')

class product_brand(models.Model):
    _name = 'product.brand'

    name = fields.Char(string='Name')


# class ts__inventory(models.Model):
#     _name = 'ts__inventory.ts__inventory'
#     _description = 'ts__inventory.ts__inventory'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
