# -*- coding: utf-8 -*-
import json

import odoo
from odoo import models, fields, api ,exceptions, _
import odoo.addons.decimal_precision as dp
from odoo import http
from odoo.osv import osv
from odoo.http import request
from odoo import http

# class structure_modeule(models.Model):
#     _name = 'structure_modeule.structure_modeule'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100
class general_info(models.Model):
    _name = 'structure.generalinfo'
    _inherit = 'mail.thread'
    project_id = fields.Many2one('project.project',
                                 string='المشروع ',required=True,track_visibility='onchange')

    @api.onchange('project_id')
    def _onchange_project(self):
        con_count = self.env['structure.generalinfo'].search_count([('project_id', '=',self.project_id.id)])
        if con_count>0:
            return {

                'warning': {'title': 'Error!', 'message': 'Please enter the correct project :where the selected  project have contract in done'},
                'value': {
                    'project_id': None,

                }
            }
            #self.project_id=[]
            #raise odoo.osv.osv.except_osv('title', 'description')
    merfakresomat = fields.Many2one('ir.attachment',string='رسومات المالك',track_visibility='onchange')
   # merfakresomat = fields.Char(string=" مرفق رسومات المالك")
    works = fields.Char(string="أعمال", track_visibility='onchange')
    inDate = fields.Date(string="تاريخ" ,track_visibility='onchange')
    merfak = fields.Char(string="مقايسة الأعمال" ,track_visibility='onchange')
    menband = fields.Char(string="من بند" ,track_visibility='onchange')
    leband = fields.Char(string="الى بند" ,track_visibility='onchange')
    modet = fields.Char(string="مدة تنفيذ المشروع " ,track_visibility='onchange')
    gehatt= fields.Char(string="جهة تنفيذ المشروع " ,track_visibility='onchange')
    tareekhestlaam = fields.Date(string="تاريخ استلام الموقع" ,track_visibility='onchange')
    gomlaatCem = fields.Char(string="قيمة العطاء" ,track_visibility='onchange')
    gomlaatalaam = fields.Char(string="التأمين النهائى" ,track_visibility='onchange')
    mogabrak1 = fields.Char(string="رقم خطاب الضمان(دفعة مقدمة)" ,track_visibility='onchange')
    mogabrak2 = fields.Char(string="رقم خطاب الضمان(ابتدائي)", track_visibility='onchange')
    mogabrak3 = fields.Char(string="رقم خطاب الضمان(نهائي)", track_visibility='onchange')
    bank= fields.Char(string="على بنك" ,track_visibility='onchange')
    faraa  = fields.Char(string="فرع" ,track_visibility='onchange')
    date_mogub1 = fields.Date(string="بتاريخ" ,track_visibility='onchange')
    date_mogub2 = fields.Date(string="وينتهي في", track_visibility='onchange')
    dagha1= fields.Char(string="الدمغات المعدنية" ,track_visibility='onchange')
    damgh2= fields.Char(string="الدمغات العلمية" ,track_visibility='onchange')
    damgh3= fields.Char(string="الدمغات التجريبية" ,track_visibility='onchange')
    damga4= fields.Char(string="الدمغات الحكومية" ,track_visibility='onchange')
    Contract_State = fields.Selection([('draft','التعاقد'),('confirmed','مدير المبيعات'),('done','رئيس مجلس الادارة'),('final','Final')] , default='draft', track_visibility='onchange')
    Lead_State = fields.Selection([('draft','استلام الموقع'),('confirmed','مدير المبيعات'),('done','رئيس مجلس الادارة'),('final','Final')], default='draft')
    recieve_State =fields.Selection([('draft','تسليم الموقع'),('confirmed','مدير المبيعات'),('done','رئيس مجلس الادارة'),('final','Final')], default='draft')
    recipy_State = fields.Selection([('recipy_draft','مقايسة المشروع'),('recipy_confirmed','مدير المكتب الفني'),('recipy_done','رئيس مجلس الادارة'),('recipy_final','Final')], default='recipy_draft')
    def recipy_perform_confirmed(self):
        self.recipy_State = 'recipy_confirmed'
    def recipy_perform_done(self):
        self.recipy_State = 'recipy_done'
    def recipy_perform_final(self):
        self.recipy_State = 'recipy_final'
        product = self.env['product.template']
        record = product.create({
            'name': self.project_id.name,
            'sale_ok': True,
            'purchase_ok': True,
            'type': 'product',

        })
        route = self.env['mrp.routing']
        value = self.env['ir.sequence'].next_by_code('mrp.routing')
        recordroute = route.create({
            'name': self.project_id.name,
            'code': value,
        })
        bom = self.env['mrp.bom']
        recordbom = bom.create({
            'product_tmpl_id': record.id,
            'product_qty': 1,
            'type': 'normal',
            'routing_id': recordroute.id,
        })
        for item in self.mokaysa_works_Project:
            bom_l1 = self.env['mrp.bom.line'].create({
                'bom_id': recordbom.id,
                'product_id': item.product_id.id,
                'product_qty': item.product_qty,
            })
            if item.product_id.type=='service':
                w_c = self.env['mrp.workcenter'].create({
                    'name':item.product_id.name,
                })
                r_w_c =  self.env['mrp.routing.workcenter'].create({
                    'name':item.product_id.name,
                    'workcenter_id':w_c.id,
                    'routing_id': recordroute.id,
                    'time_cycle_manual':item.product_qty * 60  ,
                })
                task_project = self.env['project.task']
                task_project.create({
                    'name': item.task_name,
                    'partner_id': self.elmalek.id,
                    'user_id': self.env.uid,
                    'project_id': self.project_id.id,
                    'stage_id': item.stage_id.id,
                })



    state = fields.Selection([('draft','التعاقد'),('confirmed','مدير المبيعات'),('done','رئيس مجلس الادارة'),('final','Final')],default='draft', track_visibility='onchange')
    def Contract_perform_confirm(self):
        self.state = 'confirmed'
    def Contract_perform_done(self):
        self.state='done'
    def Contract_perform_final(self):
        self.state = 'final'




    def perform_confirm(self):
        self.state='confirmed'
        task_type= self.env['project.task.type']
        record =  task_type.create({
                'name':'التعاقد',
                'project_ids':[self.project_id,]
            })
        task_project = self.env['project.task']
        task_project.create({
            'name': 'التعاقد:',
            'partner_id': self.elmalek.id,
            'user_id': self.env.uid,
            'project_id':self.project_id.id,
            'stage_id':record.id,
        })
    def perform_done(self):
        self.state='done'
        task_type = self.env['project.task.type']
        record = task_type.create({
            'name': 'استلام الموقع',
            'project_ids': [self.project_id, ]

        })
        task_project = self.env['project.task']
        task_project.create({
            'name': 'استلام الموقع',
            'partner_id': self.elmalek.id,
            'user_id': self.env.uid,
            'project_id':self.project_id.id,
            'stage_id': record.id,
        })
    def perform_work(self):
        self.state = 'work'
        task_type = self.env['project.task.type']
        record = task_type.create({
            'name': 'تسليم الموقع',
            'project_ids': [self.project_id, ]

        })
        task_project = self.env['project.task']
        task_project.create({
            'name': 'تسليم الموقع',
            'partner_id': self.elmalek.id,
            'user_id': self.env.uid,
            'project_id': self.project_id.id,
            'stage_id': record.id,
        })
    def perform_final(self):
        self.state = 'final'
        product = self.env['product.template']
        record = product.create({
            'name': self.project_id.name,
            'sale_ok': True,
            'purchase_ok':True,
            'type':'product',


        })
        route = self.env['mrp.routing']
        value = self.env['ir.sequence'].next_by_code('mrp.routing')
        recordroute = route.create({
            'name': self.record.name,
            'code':value,
        })
        bom = self.env['mrp.bom']
        recordbom = bom.create({
            'product_tmpl_id':record.id,
            'routing_id': recordroute.id,
            'product_qty':1,
            'type':'normal',
        })

        for item in self.mokaysa_works_Project:
            bom_l1 = self.env['mrp.bom.line'].create({
                'bom_id': recordbom.id,
                'product_id': item.product_id.id,
                'product_qty': item.product_qty,
            })



    elmalek = fields.Many2one('res.partner',string='المالك ',required=True)
    mokayel = fields.Char(string='المقاول')
    dateGM = fields.Date(string='جلسة فتح المظاريف المالية')
    DateGF = fields.Date(string='جلسة فتح المظاريف الفنية')
    DateTL = fields.Date(string='توصية لجنة البت المنعقدة')
    rakamalataa = fields.Char('رقم العطاء المقبول')
    name = fields.Char(string='Contract Reference', required=True, copy=False, readonly=True, index=True, default=lambda self: _('New'))
    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('structure.generalinfo.sequence') or _('New')
        result = super(general_info, self).create(vals)
        return result


    def name_get(self):
        res = []
        for field in self:
            res.append((field.id, '%s (%s)' % (field.name, field.project_id.name)))
        return res
    elagna_leed_ids = fields.One2many('structure.partners.leed','contract_id', string=" لجنة التسليم" )
    elagna_recieve_ids = fields.One2many('structure.partners.recieve', 'contract_id', string=" لجنة الاستلام")
    NotesOfLead = fields.Text(string="ملاحظات")
    recieve_notes = fields.One2many('structure.recieve.notes','contract_id',string="ملاحظات")


    mokaysa_works = fields.One2many('structure.mokaysa.works', 'contract_id', string="مقايسة الاعمال")
    amount_total = fields.Float(string='Total', store=True, readonly=True, compute='_amount_all',track_visibility='onchange')
    @api.depends('mokaysa_works.price_subtotal')
    def _amount_all(self):
        for order in self:
            total = 0.0
            for line in order.mokaysa_works:
                total += line.price_subtotal
            order.update({
                'amount_total': total,
            })

    mokaysa_works_Project = fields.One2many('structure.mokaysa.works.project', 'contract_id', string="مقايسة الاعمال")
    amount_total_project = fields.Float(string='Total', store=True, readonly=True, compute='_amount_all_project',track_visibility='onchange')

    @api.depends('mokaysa_works_Project.price_subtotal')
    def _amount_all_project(self):
        for order in self:
            total = 0.0
            for line in order.mokaysa_works_Project:
                total += line.price_subtotal
            order.update({
                'amount_total_project': total,
            })

    mostakhlas_elmalek = fields.One2many('structure.mostakhlas.elmalek', 'contract_id', string="مستخلص المالك")


    is_task_contract = fields.Text(string="is task contract ",default='0')


class project_project(models.Model):
    _name = 'project.project'
    _inherit = 'project.project'

    def countOfContract(self):
        contract = self.env['structure.generalinfo']
        for project in self:
            project.Contract_count = contract.search_count([('project_id','=',project.id)])
    Contract_count= fields.Integer(compute="countOfContract")


    def open_contract(self):
        self.ensure_one()
        domain = [
           ('project_id', '=', self.id),
           ]
        return {
            'name': _('Contract'),
            'domain': domain,
            'res_model': 'structure.generalinfo',
            'type': 'ir.actions.act_window',
            'view_id': False,
            'view_mode': 'tree,form',
            'view_type': 'form'
        }



class contract_partneres_leed(models.Model):
    _name = 'structure.partners.leed'
    name= fields.Char()
    contract_id= fields.Many2one('structure.generalinfo',string='contract')
    partner_id= fields.Many2one('res.partner',"member")
    job = fields.Char(related='partner_id.function')

class contract_partneres_recieve(models.Model):
    _name = 'structure.partners.recieve'
    name= fields.Char()
    contract_id= fields.Many2one('structure.generalinfo',string='contract')
    partner_id= fields.Many2one('res.partner',"member")
    job = fields.Char(related='partner_id.function')


class contract_partneres_recieve_Notes(models.Model):
    _name = 'structure.recieve.notes'
    name = fields.Char()
    contract_id = fields.Many2one('structure.generalinfo', string='contract')
    Note = fields.Text(string="الملاحظة")
    Comment = fields.Text(string="المتابعة")


class contract_mokaysa_works(models.Model):
    _name = 'structure.mokaysa.works'

    name = fields.Text(string="البيان")
    contract_id = fields.Many2one('structure.generalinfo', string='contract')
    nband = fields.Integer(string='بند')
    product_qty = fields.Float(string='الكمية', digits=dp.get_precision('Product Unit of Measure'), required=True)
    product_uom = fields.Many2one('uom.uom', string='الوحدة', required=True)
    price_unit = fields.Float(string='الفئة', required=True, digits=dp.get_precision('Product Price'))
    price_subtotal = fields.Float(compute='_compute_amount', string='الاجمالي', store=True)

    @api.depends('product_qty', 'price_unit')
    def _compute_amount(self):
        for line in self:
            line.update({
                'price_subtotal': line['product_qty']* line['price_unit'] ,
            })

class contract_mokaysa_works_project(models.Model):
    _name = 'structure.mokaysa.works.project'

    name = fields.Text(string="البيان")
    contract_id = fields.Many2one('structure.generalinfo', string='contract')
    nband = fields.Integer(string='بند')
   # band_type = fields.Selection([(1,'Service'),(2,'Consumable')],default=1)
    task_name = fields.Char('Task Name')
    stage_id = fields.Many2one('project.task.type', string='Stage')

    product_id = fields.Many2one('product.product',string='Product')
    product_qty = fields.Float(string='الكمية', digits=dp.get_precision('Product Unit of Measure'), required=True)
    product_uom = fields.Many2one('uom.uom', string='الوحدة', required=True)
    price_unit = fields.Float(string='الفئة', required=True, digits=dp.get_precision('Product Price'))
    price_subtotal = fields.Float(compute='_compute_amount', string='الاجمالي', store=True)

    @api.depends('product_qty', 'price_unit')
    def _compute_amount(self):
        for line in self:
            line.update({
                'price_subtotal': line['product_qty']* line['price_unit'] ,
            })

class Contract_Mostaklas_elmalek(models.Model):
    _name = 'structure.mostakhlas.elmalek'
    name = fields.Char(string='رقم المستخلص')
    contract_id = fields.Many2one('structure.generalinfo', string='contract')
    Mostaklas_item = fields.One2many('structure.mostakhlas.elmalek.item','mostaklas_id')
    band_of_mokaysa = fields.Many2one('structure.mokaysa.works',string='بند المقايسة')
    amount_total_mostakhlas_elmalek = fields.Float(string='Total', store=True, readonly=True,
                                                   compute='_amount_all_mostakhlas_elmalek',
                                                   track_visibility='onchange')
    istektak_or_book_item = fields.One2many('structure.mostakhlas.elmalek.estektak','estektak_item')
    istektak_or_book = fields.Float(string='اجمالي الاستقطاع',compute='_amount_estektak')
    @api.depends('istektak_or_book_item')
    def _amount_estektak(self):
        total= 0.0
        for rec in self:
            for item in rec.istektak_or_book_item:
                total+= item.istektak_or_book
            rec.update({
                'istektak_or_book': total ,
            })

    istektak_or_book2 = fields.Float(related='istektak_or_book')
    total_after_istektak = fields.Float(string='الاجمالي بعد الاستقطاع',compute='_amount_after_istektak')
    @api.depends('amount_total_mostakhlas_elmalek','istektak_or_book')
    def _amount_after_istektak(self):
        for rec in self:
            rec.update({
                'total_after_istektak': rec.amount_total_mostakhlas_elmalek - rec.istektak_or_book,
            })

    invoice_id = fields.Many2one('account.move',string='invoice')
    state = fields.Selection([('draft','Draft'),('done','Done')],default='draft' )
    start_date= fields.Date('start date')
    end_date = fields.Date('end date')


    def name_get(self):
        res = []
        for field in self:
            res.append((field.id, '%s (%s)' % (field.name, field.contract_id.project_id.name)))
        return res
    @api.depends('Mostaklas_item.price_subtotal')
    def _amount_all_mostakhlas_elmalek(self):
        for order in self:
            total = 0.0
            for line in order.Mostaklas_item:
                total += line.price_subtotal
            order.update({
                'amount_total_mostakhlas_elmalek': total,
            })
    @api.onchange('contract_id')
    def _onchange_contract(self):
        for rec in self:
            return  {'domain' : {'band_of_mokaysa':[('contract_id','=',rec.contract_id.id)]} }

    def create_invoice(self):
        for rec in self:
           inv = self.env['account.move'].create({
                'partner_id':rec.contract_id.elmalek.id,
                'is_mostaklas':True,
                'mostaklas_item':rec.id,
            })
           rec.invoice_id= inv.id
           rec.state = 'done'
           for item in rec.Mostaklas_item:
                self.env['account.move.line'].create({
                    'move_id':inv.id,
                    'name':item.name.name,
                    'price_unit':item.price_unit,
                    'quantity':item.inside_work,
                    'account_id':19,
                    'analytic_account_id':rec.contract_id.project_id.analytic_account_id.id

                })


class structure_mostakhlas_elmalek_estektak(models.Model):
    _name = 'structure.mostakhlas.elmalek.estektak'

    estektak_item = fields.Many2one('structure.mostakhlas.elmalek')
    name = fields.Char('البيان')
    istektak_or_book = fields.Float(string='قيمة الاستقطاع')


class Account_invoice(models.Model):
    _name = 'account.move'
    _inherit = 'account.move'


    is_mostaklas = fields.Boolean('is a Mostaklas')
    is_mostaklas_baten = fields.Boolean('is hidden extract')
    mostaklas_item = fields.Many2one('structure.mostakhlas.elmalek', string='mostakas')
    mostaklas_baten = fields.Many2one('structure.mostakhlas.baten', string='mostakas')
    task = fields.Many2one('project.task', string='task')



class contract_mostakhlas_works(models.Model):
    _name = 'structure.mostakhlas.elmalek.item'

    name = fields.Many2one('structure.mokaysa.works')
    mostaklas_id = fields.Many2one('structure.mostakhlas.elmalek', string='contract')

    @api.onchange('contract_id')
    def _onchange_contract(self):
        print(self.contract_id)
        for rec in self:
            return {'domain': {'name': [('contract_id', '=', rec.contract_id.id)]}}

    nband = fields.Integer(string='بند')
    product_qty = fields.Float(related="name.product_qty", string='كمية العقد', digits=dp.get_precision('Product Unit of Measure'), required=True)
    product_uom = fields.Many2one('uom.uom', string='الوحدة', required=True)


    @api.onchange('name')
    def _onchange_name(self):
        for line in self:
            items = self.env['structure.mostakhlas.elmalek.item'].search([('name', '=', line.name.id)])
            total= 0.0
            for item in items:
                total= total+item.inside_work

            line.update({
                'product_uom': line['name'].product_uom,
                'previous_work':total,
            })
    price_unit = fields.Float(related="name.price_unit", string='الفئة', required=True, digits=dp.get_precision('Product Price'))
    previous_work = fields.Float(string='مقدار العمل السابق اجراؤه', digits=dp.get_precision('Product Unit of Measure'), required=True)
    inside_work = fields.Float(string='مقدار الاعمال المنفذة في خلال هذه المدة', digits=dp.get_precision('Product Unit of Measure'),required=True)
    total_work = fields.Float(string='جملة مقدار الاعمال التي تمت في خلال هذه المدة', digits=dp.get_precision('Product Unit of Measure'),
                               required=True, compute="_compute_total_work")

    @api.depends('previous_work', 'inside_work')
    def _compute_total_work(self):
        for line in self:
            line.update({
                'total_work': line['previous_work'] + line['inside_work'],
            })


    isgary = fields.Boolean(string ='جاري')
    stektak = fields.Float(string='استقطاع او ححز', digits=dp.get_precision('Product Unit of Measure'))
    reminder = fields.Float(string='الباقي بعد الاستقطاع', digits=dp.get_precision('Product Unit of Measure'))
    note = fields.Text(string='ملاحظات')

    price_subtotal = fields.Float(compute='_compute_amount', string='اجمالي قيمة الاعمال المنفذة', store=True)

    @api.depends('total_work', 'price_unit')
    def _compute_amount(self):
        for line in self:
            line.update({
                'price_subtotal': line['total_work']* line['price_unit'] ,
            })

class Contract_Mostaklas_baten(models.Model):
    _name = 'structure.mostakhlas.baten'
    name = fields.Char(string='رقم المستخلص')
    contract_id = fields.Many2one('structure.generalinfo', string='contract')
    Mostaklas_item = fields.One2many('structure.mostakhlas.baten.item','mostaklas_id')
    sub_contract = fields.Many2one('res.partner',string='المقاول')
    band_of_mokaysa = fields.Many2one('structure.mokaysa.works',string='بند المقايسة')
    amount_total_mostakhlas_elmalek = fields.Float(string='Total', store=True, readonly=True,
                                                   compute='_amount_all_mostakhlas_elmalek',
                                                   track_visibility='onchange')
    istektak_or_book_item = fields.One2many('structure.mostakhlas.baten.estektak', 'estektak_item')
    istektak_or_book = fields.Float(string='اجمالي الاستقطاع', compute='_amount_estektak')

    @api.depends('istektak_or_book_item')
    def _amount_estektak(self):
        total = 0.0
        for rec in self:
            for item in rec.istektak_or_book_item:
                total += item.istektak_or_book
            rec.update({
                'istektak_or_book': total,
            })

    istektak_or_book2 = fields.Float(related='istektak_or_book')
    total_after_istektak = fields.Float(string='الاجمالي بعد الاستقطاع',compute='_amount_after_istektak')
    @api.depends('amount_total_mostakhlas_elmalek','istektak_or_book')
    def _amount_after_istektak(self):
        for rec in self:
            rec.update({
                'total_after_istektak': rec.amount_total_mostakhlas_elmalek - rec.istektak_or_book,
            })

    invoice_id = fields.Many2one('account.move',string='invoice')
    state = fields.Selection([('draft','Draft'),('done','Done')],default='draft' )
    start_date= fields.Date('start date')
    end_date = fields.Date('end date')


    def name_get(self):
        res = []
        for field in self:
            res.append((field.id, '%s (%s)' % (field.name, field.contract_id.project_id.name)))
        return res
    @api.depends('Mostaklas_item.price_subtotal')
    def _amount_all_mostakhlas_elmalek(self):
        for order in self:
            total = 0.0
            for line in order.Mostaklas_item:
                total += line.price_subtotal
            order.update({
                'amount_total_mostakhlas_elmalek': total,
            })
    @api.onchange('contract_id')
    def _onchange_contract(self):
        for rec in self:
            return  {'domain' : {'band_of_mokaysa':[('contract_id','=',rec.contract_id.id)]} }

    def create_invoice(self):
        for rec in self:
           inv = self.env['account.move'].create({
                'partner_id':rec.sub_contract.id,
                'is_mostaklas_baten':True,
                'mostaklas_baten':rec.id,
            })
           rec.invoice_id= inv.id
           rec.state = 'done'
           for item in rec.Mostaklas_item:
                self.env['account.move.line'].create({
                    'move_id':inv.id,
                    'name':item.name.name,
                    'price_unit':item.price_unit,
                    'quantity':item.inside_work,
                    'account_id':24,
                    'analytic_account_id':rec.contract_id.project_id.analytic_account_id.id

                })
class structure_mostakhlas_baten_estektak(models.Model):
    _name = 'structure.mostakhlas.baten.estektak'

    estektak_item = fields.Many2one('structure.mostakhlas.baten')
    name = fields.Char('البيان')
    istektak_or_book = fields.Float(string='قيمة الاستقطاع')


class contract_mostakhlas_baten_item(models.Model):
    _name = 'structure.mostakhlas.baten.item'

    name = fields.Many2one('structure.mokaysa.works.project')
    mostaklas_id = fields.Many2one('structure.mostakhlas.baten', string='contract')

    @api.onchange('contract_id')
    def _onchange_contract(self):
        print(self.contract_id)
        for rec in self:
            return {'domain': {'name': [('contract_id', '=', rec.contract_id.id)]}}

    nband = fields.Integer(string='بند')
    product_qty = fields.Float(related="name.product_qty", string='كمية العقد', digits=dp.get_precision('Product Unit of Measure'), required=True)
    product_uom = fields.Many2one('uom.uom', string='الوحدة', required=True)


    @api.onchange('name')
    def _onchange_name(self):
        for line in self:
            items = self.env['structure.mostakhlas.baten.item'].search([('name', '=', line.name.id)])
            total= 0.0
            for item in items:
                total= total+item.inside_work

            line.update({
                'product_uom': line['name'].product_uom,
                'previous_work':total,
            })
    price_unit = fields.Float(related="name.price_unit", string='الفئة', required=True, digits=dp.get_precision('Product Price'))
    previous_work = fields.Float(string='مقدار العمل السابق اجراؤه', digits=dp.get_precision('Product Unit of Measure'), required=True)
    inside_work = fields.Float(string='مقدار الاعمال المنفذة في خلال هذه المدة', digits=dp.get_precision('Product Unit of Measure'),required=True)
    total_work = fields.Float(string='جملة مقدار الاعمال التي تمت في خلال هذه المدة', digits=dp.get_precision('Product Unit of Measure'),
                               required=True, compute="_compute_total_work")

    @api.depends('previous_work', 'inside_work')
    def _compute_total_work(self):
        for line in self:
            line.update({
                'total_work': line['previous_work'] + line['inside_work'],
            })



    note = fields.Text(string='ملاحظات')

    price_subtotal = fields.Float(compute='_compute_amount', string='اجمالي قيمة الاعمال المنفذة', store=True)

    @api.depends('total_work', 'price_unit')
    def _compute_amount(self):
        for line in self:
            line.update({
                'price_subtotal': line['total_work']* line['price_unit'] ,
            })


class project_tasks(models.Model):
    _name = 'project.task'
    _inherit = 'project.task'

    url = fields.Char(string="URL:")
    expectedMatC =  fields.Float(string='expected cost', required=True, digits=dp.get_precision('Product Price'))
    ActualMatC = fields.Float(string='Actual cost', required=True, digits=dp.get_precision('Product Price'))
    VarianceMatC = fields.Float(string='Variance cost', required=True, digits=dp.get_precision('Product Price'),compute='_compute_VMatC')
    @api.depends('expectedMatC', 'ActualMatC')
    def _compute_VMatC(self):
        for line in self:
            line.update({
                'VarianceMatC': line['expectedMatC'] - line['ActualMatC'],
            })


    expectedLabC = fields.Float(string='expected cost', required=True, digits=dp.get_precision('Product Price'))
    ActualLabC = fields.Float(string='Actual cost', required=True, digits=dp.get_precision('Product Price'))
    VarianceLabC = fields.Float(string='Variance cost', required=True, digits=dp.get_precision('Product Price'),compute='_compute_VLabC')
    @api.depends('expectedLabC', 'ActualLabC')
    def _compute_VLabC(self):
        for line in self:
            line.update({
                'VarianceLabC': line['expectedLabC'] - line['ActualLabC'],
            })

    expectedMachC = fields.Float(string='expected cost', required=True, digits=dp.get_precision('Product Price'))
    ActualMachC = fields.Float(string='Actual cost', required=True, digits=dp.get_precision('Product Price'))
    VarianceMachC = fields.Float(string='Variance cost', required=True, digits=dp.get_precision('Product Price'),compute='_compute_VMachC')
    @api.depends('expectedMachC', 'ActualMachC')
    def _compute_VMachC(self):
        for line in self:
            line.update({
                'VarianceMachC': line['expectedMachC'] - line['ActualMachC'],
            })

    expectedToolC = fields.Float(string='expected cost', required=True, digits=dp.get_precision('Product Price'))
    ActualToolC = fields.Float(string='Actual cost', required=True, digits=dp.get_precision('Product Price'))
    VarianceToolC = fields.Float(string='Variance cost', required=True, digits=dp.get_precision('Product Price'),compute='_compute_VToolC')
    @api.depends('expectedToolC', 'ActualToolC')
    def _compute_VToolC(self):
        for line in self:
            line.update({
                'VarianceToolC': line['expectedToolC'] - line['ActualToolC'],
            })

    TotalexpectedC = fields.Float(string='expected cost', required=True, digits=dp.get_precision('Product Price'),compute='_compute_ExpecC')
    TotalActualC = fields.Float(string='Actual cost', required=True, digits=dp.get_precision('Product Price'),compute='_compute_ActualC')
    TotalVarianceC = fields.Float(string='Variance cost', required=True, digits=dp.get_precision('Product Price'),compute='_compute_VarianC')
    InitPC = fields.Float(related='TotalexpectedC',string='expected cost', required=True, digits=dp.get_precision('Product Price'),compute='_compute_ExpecC')
    InitAC = fields.Float(related='TotalActualC',string='expected cost', required=True, digits=dp.get_precision('Product Price'),compute='_compute_ExpecC')

    progressOfCost = fields.Float(compute='_costs_get', store=True,  string='Working Cost Recorded', group_operator="avg")


    @api.depends('expectedMatC', 'expectedLabC','expectedMachC','expectedToolC')
    def _compute_ExpecC(self):
        for line in self:
            line.update({
                'TotalexpectedC': line['expectedMatC'] + line['expectedLabC'] + line['expectedMachC'] + line['expectedToolC'] ,
            })

    @api.depends('ActualMatC', 'ActualLabC', 'ActualMachC', 'ActualToolC')
    def _compute_ActualC(self):
        for line in self:
            line.update({
                'TotalActualC': line['ActualMatC'] + line['ActualLabC'] + line['ActualMachC'] + line['ActualToolC'],
            })

    @api.depends('VarianceMatC', 'VarianceLabC', 'VarianceMachC', 'VarianceToolC')
    def _compute_VarianC(self):
        for line in self:
            line.update({
                'TotalVarianceC': line['VarianceMatC'] + line['VarianceLabC'] + line['VarianceMachC'] + line['VarianceToolC'],
            })

    @api.depends('TotalActualC', 'TotalexpectedC')
    def _costs_get(self):
        for line in self:
            if ( line['InitAC'] > 0.0):
                line.update({
                    'progressOfCost': line['InitPC'] / line['InitAC'] * 100,
                })
            else:
                line.update({
                    'progressOfCost': 0,
                })
    tasks_next = fields.One2many('project.task.nexts','task_id',string='Next Tasks')
    Slak_Hours = fields.Integer(string="Slak (Hours)")
    start_date = fields.Date(string='start Date')
    end_Date =   fields.Date(string='End Date')
    EVs = fields.One2many('project.task.value','task_id',string='EV')
    EV = fields.Float(string='EV',store=True,  digits=dp.get_precision('Product Price'),compute='_compute_EV')
    PV = fields.Float(string='PV', store=True, digits=dp.get_precision('Product Price'),compute='_compute_PV')
    AV = fields.Float(string='AV',store=True , digits=dp.get_precision('Product Price'),compute='_compute_AV')
    SPI = fields.Float(string='SPI',store=True,  digits=dp.get_precision('Product Price'),compute='_compute_SPI')
    CPI = fields.Float(string='CPI',store=True,  digits=dp.get_precision('Product Price'),compute='_compute_CPI')

    @api.depends('EVs')
    def _compute_EV(self):
        for line in self:
            for record in line.EVs:
                line.update({
                    'EV': record['EV'],
                })

    @api.depends('EVs')
    def _compute_PV(self):
        for line in self:
            for record in line.EVs:
                line.update({
                    'PV': record['PV'],
                })

    @api.depends('EVs')
    def _compute_AV(self):
        for line in self:
            for record in line.EVs:
                line.update({
                    'AV': record['AV'],
                })

    @api.depends('EVs')
    def _compute_SPI(self):
        for line in self:
            for record in line.EVs:
                line.update({
                    'SPI': record['SPI'],
                })

    @api.depends('EVs')
    def _compute_CPI(self):
        for line in self:
            for record in line.EVs:
                line.update({
                    'CPI': record['CPI'],
                })

    @api.model
    def search_student(self):
        item = self.env['project.task.value'].search([('task_id', '=', 27)])
        list = []
        for record in item:
            list.append({'EV': record.EV, 'PV': record.PV, 'AV': record.AV, 'date': record.date})
        task = self.env['project.task'].search([('id', '=', 27)])
        for rec in task:
            list.append({'start': rec.start_date,'PV': rec.InitPC, 'date': rec.end_Date})

        return json.dumps(list)









class project_task_next (models.Model):
    _name = 'project.task.nexts'
    task_id= fields.Many2one('project.task',string='next task')
    relation= fields.Selection([('0','Flag'),('1','Lead')],default='0')
    span_hours = fields.Float(string='span (Hours)')
    realtion_type= fields.Selection([('0','FF'),('1','FS'),('2','SF'),('3','SS')],default='0')

class project_task_Value (models.Model):
    _name = 'project.task.value'
    name= fields.Char(string="البيان")
    task_id= fields.Many2one('project.task',string='next task')
    EV = fields.Float(string='EV',  digits=dp.get_precision('Product Price'))
    PV = fields.Float(string='PV', digits=dp.get_precision('Product Price'))
    AV = fields.Float(string='AV',  digits=dp.get_precision('Product Price'))
    SPI = fields.Float(string='SPI',  digits=dp.get_precision('Product Price'),
                                compute='_compute_SPI')
    CPI = fields.Float(string='CPI',  digits=dp.get_precision('Product Price'),
                                compute='_compute_CPI')
    date = fields.Date('Date')
    product_qty = fields.Float(string='كمية', digits=dp.get_precision('Product Unit of Measure'), required=True)
    product_uom = fields.Many2one('uom.uom', string='الوحدة', required=True)
    price_unit = fields.Float(string='الفئة', required=True, digits=dp.get_precision('Product Price'))
    price_subtotal = fields.Float(compute='_compute_amount', string='الاجمالي', store=True)
    work_accurate = fields.Float(compute='_compute_work_accurate', string='اعتماد الاعمال', store=True)
    volume_work_accurate = fields.Float(compute='_compute_volume_work_accurate', string='حجم الاعمال المعتمدة', store=True)
    invoice_id = fields.Many2one('account.move', string='invoice')

    def create_invoice(self):
        for rec in self:
            inv = self.env['account.move'].create({
                'partner_id': rec.task_id.user_id.id,
                'is_mostaklas_baten': True,
                'task': rec.task_id.id,
            })
            rec.invoice_id = inv.id
            #rec.invoice_id = inv.id
            #rec.state = 'done'
            self.env['account.move.line'].create({
                'move_id': inv.id,
                'name': rec.name,
                'price_unit': rec.price_unit,
                'quantity': rec.product_qty,
                'account_id': 17,
                'analytic_account_id': rec.task_id.project_id.analytic_account_id.id

            })




    @api.depends('product_qty', 'price_unit')
    def _compute_amount(self):
        for line in self:
            line.update({
                'price_subtotal': line['product_qty'] * line['price_unit'],
            })

    @api.depends('AV', 'PV')
    def _compute_work_accurate(self):
        for line in self:
            if(line['PV']>0.0):
                line.update({
                    'work_accurate': line['AV'] / line['PV'] * 100,
                })
            else:
                line.update({
                    'work_accurate': 0,
                })

    @api.depends('work_accurate', 'price_subtotal')
    def _compute_volume_work_accurate(self):
        for line in self:
                line.update({
                    'volume_work_accurate': line['work_accurate'] / 100 * line['price_subtotal'] ,
                })

    @api.depends('PV', 'EV')
    def _compute_SPI(self):
        for line in self:
            if ( line['EV'] > 0.0):
                line.update({
                    'SPI': line['PV'] / line['EV'] ,
                })
            else:
                line.update({
                    'SPI': 0,
                })

    @api.depends('AV', 'EV')
    def _compute_CPI(self):
        for line in self:
            if ( line['EV'] > 0.0):
                line.update({
                    'CPI': line['AV'] / line['EV'] ,
                })
            else:
                line.update({
                    'CPI': 0,
                })


class tructure_mrp_quality(models.Model):
    _name = 'mrp.routing.workcenter'
    _inherit = 'mrp.routing.workcenter'

    quality_ids = fields.One2many('structure.quality','mrp_id',string='quality')


class structure_mrp_quality_item(models.Model):
    _name = 'structure.quality'
    _rec_name = 'name'
    _description = ''

    name = fields.Char()
    mrp_id = fields.Many2one('mrp.routing.workcenter')
    bnd = fields.Integer(string='بند')
    description = fields.Char('الوصف')
    status = fields.Boolean('الحالة')
    notes = fields.Text('ملاحظات')


