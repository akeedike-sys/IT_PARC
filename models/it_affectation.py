from odoo import models, fields, api
from datetime import datetime


class ITAffectation(models.Model):
    _name = 'it.affectation'
    _description = 'Affectation d\'équipement'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'assignment_date desc'

    equipment_id = fields.Many2one('it.equipment', 'Équipement', required=True, ondelete='cascade', tracking=True)
    employee_id = fields.Many2one('hr.employee', 'Employé', required=True, tracking=True)
    department_id = fields.Many2one('hr.department', 'Département', tracking=True)
    assignment_date = fields.Date('Date d\'affectation', default=fields.Date.today, required=True, tracking=True)
    return_date = fields.Date('Date de retour', tracking=True)
    reason = fields.Text('Motif de l\'affectation', tracking=True)

    is_current = fields.Boolean('Affectation actuelle?', compute='_compute_is_current')

    @api.depends('return_date')
    def _compute_is_current(self):
        for record in self:
            record.is_current = not record.return_date

    def action_return_equipment(self):
        self.return_date = fields.Date.today()
        self.equipment_id.employee_id = False
        self.equipment_id.department_id = False
