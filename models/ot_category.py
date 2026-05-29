from odoo import models, fields, api


class OtCategory(models.Model):
    _name = 'ot.category'
    _description = 'OT Category'
    _order = 'sequence, id'

    name = fields.Char(string='Name', required=True)
    code = fields.Char(string='Code')
    description = fields.Text(string='Description')
    active = fields.Boolean(string='Active', default=True)
    sequence = fields.Integer(string='Sequence', default=10)

    start_hour = fields.Float(string='Start Hour')
    end_hour = fields.Float(string='End Hour')

    weekday_type = fields.Selection([
        ('weekday', 'Thu 2 - Thu 6'),
        ('saturday', 'Thu 7'),
        ('sunday', 'Chu nhat'),
        ('weekend', 'Thu 7 & Chu nhat'),
    ], string='Weekday Type', required=True, default='weekday')
