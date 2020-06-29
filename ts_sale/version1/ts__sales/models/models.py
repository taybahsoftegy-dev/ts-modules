# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from functools import partial
from itertools import groupby

from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.exceptions import AccessError, UserError, ValidationError
from odoo.tools.misc import formatLang, get_lang
from odoo.osv import expression
from odoo.tools import float_is_zero, float_compare



from werkzeug.urls import url_encode

class product_template_inherit(models.Model):
    _inherit='product.product'
    _name='product.product'

    def name_get(self):
        # TDE: this could be cleaned a bit I think

        def _name_get(d):
            name = ''
            code = self._context.get('display_default_code', True) and d.get('default_code', False) or False
            if code:
                name = '[%s] %s' % (code,name)
            return (d['id'], name)

        partner_id = self._context.get('partner_id')
        if partner_id:
            partner_ids = [partner_id, self.env['res.partner'].browse(partner_id).commercial_partner_id.id]
        else:
            partner_ids = []
        company_id = self.env.context.get('company_id')

        # all user don't have access to seller and partner
        # check access and use superuser
        self.check_access_rights("read")
        self.check_access_rule("read")

        result = []

        # Prefetch the fields used by the `name_get`, so `browse` doesn't fetch other fields
        # Use `load=False` to not call `name_get` for the `product_tmpl_id`
        self.sudo().read(['name', 'default_code', 'product_tmpl_id'], load=False)

        product_template_ids = self.sudo().mapped('product_tmpl_id').ids

        if partner_ids:
            supplier_info = self.env['product.supplierinfo'].sudo().search([
                ('product_tmpl_id', 'in', product_template_ids),
                ('name', 'in', partner_ids),
            ])
            # Prefetch the fields used by the `name_get`, so `browse` doesn't fetch other fields
            # Use `load=False` to not call `name_get` for the `product_tmpl_id` and `product_id`
            supplier_info.sudo().read(['product_tmpl_id', 'product_id', 'product_name', 'product_code'], load=False)
            supplier_info_by_template = {}
            for r in supplier_info:
                supplier_info_by_template.setdefault(r.product_tmpl_id, []).append(r)
        for product in self.sudo():
            variant = product.product_template_attribute_value_ids._get_combination_name()

            name = variant and "%s (%s)" % (product.name, variant) or product.name
            sellers = []
            if partner_ids:
                product_supplier_info = supplier_info_by_template.get(product.product_tmpl_id, [])
                sellers = [x for x in product_supplier_info if x.product_id and x.product_id == product]
                if not sellers:
                    sellers = [x for x in product_supplier_info if not x.product_id]
                # Filter out sellers based on the company. This is done afterwards for a better
                # code readability. At this point, only a few sellers should remain, so it should
                # not be a performance issue.
                if company_id:
                    sellers = [x for x in sellers if x.company_id.id in [company_id, False]]
            if sellers:
                for s in sellers:
                    seller_variant = s.product_name and (
                        variant and "%s (%s)" % (s.product_name, variant) or s.product_name
                        ) or False
                    mydict = {
                              'id': product.id,
                              'name': seller_variant or name,
                              'default_code': s.product_code or product.default_code,
                              }
                    temp = _name_get(mydict)
                    if temp not in result:
                        result.append(temp)
            else:
                mydict = {
                          'id': product.id,
                          'name': name,
                          'default_code': product.default_code,
                          }
                result.append(_name_get(mydict))
        return result

class SaleOrderLine(models.Model):
    _inherit = 'sale.order'
    _name = 'sale.order'

    discount = fields.Float(string='Discount')
    profit = fields.Float(string='profit')
    rate = fields.Float(string='rate')
    display_price = fields.Boolean(string='Show Cost', default=False)

    @api.onchange('display_price')
    def _onchange_display_price(self):
        for rec in self:
            for line in rec.order_line:
                if rec.display_price:
                    line.price_unit = line.cost * line.Profit * line.discount * line.rate
                else:
                    line.price_unit = line.product_id.lst_price


    def action_confirm(self):
        for rec in self:
            if rec.display_price :
                for line in rec.order_line:
                    line.product_id.standard_price = line.cost


        if self._get_forbidden_state_confirm() & set(self.mapped('state')):
            raise UserError(_(
                'It is not allowed to confirm an order in the following states: %s'
            ) % (', '.join(self._get_forbidden_state_confirm())))

        for order in self.filtered(lambda order: order.partner_id not in order.message_partner_ids):
            order.message_subscribe([order.partner_id.id])
        self.write({
            'state': 'sale',
            'date_order': fields.Datetime.now()
        })
        self._action_confirm()
        if self.env.user.has_group('sale.group_auto_done_setting'):
            self.action_done()
        return True

    def update_discount(self):
        for rec in self:
            for line in rec.order_line:
                if line.check_box:
                    line.discount = rec.discount

    def update_profit(self):
        for rec in self:
            for line in rec.order_line:
                if line.check_box:
                    line.Profit = rec.profit

    def update_rate(self):
        for rec in self:
            for line in rec.order_line:
                if line.check_box:
                    line.rate = rec.rate

    def select_lines(self):
        for rec in self:
            for line in rec.order_line:
                line.check_box = True

    def unselect_lines(self):
        for rec in self:
            for line in rec.order_line:
                line.check_box = False





class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    _name = 'sale.order.line'

    cost = fields.Float(string='Cost')
    Profit = fields.Float(string='Profit',default=1.0)
    discount = fields.Float(string='Discount',default=1.0)
    rate = fields.Float(string='Rate',default=1.0)
    check_box = fields.Boolean(string='check box')
    price_unit = fields.Float(string='Unit Price',default=0.0,compute='_compute_unit_price',readonly=True)
    price_subtotal = fields.Float(string='Subtotal',compute='_compute_subtotal',readonly=True)

    @api.onchange( 'discount')
    def _onchange_line_discount(self):
        for rec in self :
            if rec.order_id.display_price:
                rec.price_unit = rec.cost * rec.Profit * rec.discount * rec.rate

    @api.onchange('cost')
    def _onchange_line_cost(self):
        for rec in self:
            if rec.order_id.display_price:
                rec.price_unit = rec.cost * rec.Profit * rec.discount * rec.rate

    @api.onchange('Profit')
    def _onchange_line_profit(self):
        for rec in self:
            if rec.order_id.display_price:
                rec.price_unit = rec.cost * rec.Profit * rec.discount * rec.rate

    @api.onchange('rate')
    def _onchange_line_rate(self):
        for rec in self:
            if rec.order_id.display_price:
                rec.price_unit = rec.cost * rec.Profit * rec.discount * rec.rate

    # @api.onchange('price_unit')
    # def _onchange_line_price_unit(self):
    #     for rec in self:
    #         rec.price_subtotal = rec.price_unit * rec.product_uom_qty
    #
    # @api.onchange('product_uom_qty')
    # def _onchange_line_product_uom_qty(self):
    #     for rec in self:
    #         rec.price_subtotal = rec.price_unit * rec.product_uom_qty

    @api.depends('cost', 'discount', 'rate', 'Profit')
    def _compute_amount_unit_price(self):
        for rec in self:
            if rec.order_id.display_price:
                rec.price_unit = rec.cost * rec.Profit * rec.discount * rec.rate

    # @api.depends('product_uom_qty', 'discount', 'price_unit', 'tax_id')
    # def _compute_amount(self):
    #     """
    #     Compute the amounts of the SO line.
    #     """
    #     for line in self:
    #         price = line.cost * line.Profit * line.discount * line.rate
    #         taxes = line.tax_id.compute_all(price, line.order_id.currency_id, line.product_uom_qty,
    #                                         product=line.product_id, partner=line.order_id.partner_shipping_id)
    #         line.update({
    #             'price_tax': sum(t.get('amount', 0.0) for t in taxes.get('taxes', [])),
    #             'price_total': taxes['total_included'],
    #             'price_subtotal': taxes['total_excluded'],
    #         })

    def _compute_subtotal(self):
        for rec in self:
            if rec.order_id.display_price:
                rec.price_subtotal = rec.price_unit * rec.product_uom_qty
    def _compute_unit_price(self):
        for rec in self :
            if rec.order_id.display_price:
                rec.price_unit = rec.cost * rec.Profit * rec.discount * rec.rate
            else:
                rec.price_unit = rec.product_id.lst_price


    @api.onchange('product_id')
    def product_id_change(self):
        if not self.product_id:
            return
        valid_values = self.product_id.product_tmpl_id.valid_product_template_attribute_line_ids.product_template_value_ids
        # remove the is_custom values that don't belong to this template
        for pacv in self.product_custom_attribute_value_ids:
            if pacv.custom_product_template_attribute_value_id not in valid_values:
                self.product_custom_attribute_value_ids -= pacv

        # remove the no_variant attributes that don't belong to this template
        for ptav in self.product_no_variant_attribute_value_ids:
            if ptav._origin not in valid_values:
                self.product_no_variant_attribute_value_ids -= ptav

        vals = {}
        if not self.product_uom or (self.product_id.uom_id.id != self.product_uom.id):
            vals['product_uom'] = self.product_id.uom_id
            vals['product_uom_qty'] = self.product_uom_qty or 1.0

        product = self.product_id.with_context(
            lang=get_lang(self.env, self.order_id.partner_id.lang).code,
            partner=self.order_id.partner_id,
            quantity=vals.get('product_uom_qty') or self.product_uom_qty,
            date=self.order_id.date_order,
            pricelist=self.order_id.pricelist_id.id,
            uom=self.product_uom.id
        )

        vals.update(name=self.product_id.name)
        vals.update(cost=self.product_id.standard_price)


        self._compute_tax_id()

        if self.order_id.pricelist_id and self.order_id.partner_id:
            vals['price_unit'] = self.env['account.tax']._fix_tax_included_price_company(
                self._get_display_price(product), product.taxes_id, self.tax_id, self.company_id)
        # vals.update(cost=self.product_id.standard_price)
        self.update(vals)

        title = False
        message = False
        result = {}
        warning = {}
        if product.sale_line_warn != 'no-message':
            title = _("Warning for %s") % product.name
            message = product.sale_line_warn_msg
            warning['title'] = title
            warning['message'] = message
            result = {'warning': warning}
            if product.sale_line_warn == 'block':
                self.product_id = False
        for rec in self:
            rec.price_unit = rec.cost * rec.Profit * rec.discount * rec.rate
            rec.price_subtotal = rec.price_unit * rec.product_uom_qty

        return result

    @api.depends('cost', 'discount', 'rate', 'Profit')
    def _compute_amount_unit_price(self):
        for rec in self:
            if rec.order_id.display_price:
                rec.price_unit = rec.cost * rec.Profit * rec.discount * rec.rate

    @api.onchange('product_uom_qty')
    def _onchange_line_product_uom_qty(self):
        for rec in self:
            if rec.order_id.display_price:
                rec.price_unit = rec.cost * rec.Profit * rec.discount * rec.rate
            rec.price_subtotal = rec.price_unit * rec.product_uom_qty

    @api.depends('product_uom_qty')
    def _compute_subtotal(self):
        for rec in self:
            if rec.order_id.display_price:
                rec.price_unit = rec.cost * rec.Profit * rec.discount * rec.rate
            rec.price_subtotal = rec.price_unit * rec.product_uom_qty

class SMultiProduct(models.TransientModel):
    _name = 's.multi.product'

    product_ids = fields.Many2many('product.product', string="Product")

    def add_product(self):
        for line in self.product_ids:
            self.env['sale.order.line'].create({
                'product_id': line.id,
                'order_id': self._context.get('active_id')
            })
        return


# class ts__sales(models.Model):
#     _name = 'ts__sales.ts__sales'
#     _description = 'ts__sales.ts__sales'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
