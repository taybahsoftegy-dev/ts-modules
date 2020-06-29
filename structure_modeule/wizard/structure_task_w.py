# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo import http

class structuretaskw(models.TransientModel):
    _name = 'structure.task.w'
    _description = 'create task from wizard by button'

    name = fields.Char('Task Name')
    url = fields.Char('url')
    stage_id = fields.Many2one('project.task.type', string='Stage')


    def action_create_task_apply(self):
        contract = self.env['structure.generalinfo'].browse(self.env.context.get('active_ids'))
        contract.write({'is_task_contract':'1'})
        task_project = self.env['project.task']
        task_project.create({
            'name': self.name,
            'partner_id': contract.elmalek.id,
            'user_id': self.env.uid,
            'project_id': contract.project_id.id,
            'stage_id': self.stage_id.id,
            'url':self.url
        })
        return contract
