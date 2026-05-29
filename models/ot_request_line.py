from odoo import models, fields, api


class OtRequestLine(models.Model):
    _name = 'ot.request.line'
    _description = 'OT Request Line'

    request_id = fields.Many2one(
        'ot.request', string='OT Request',
        required=True, ondelete='cascade')
    ot_date = fields.Date(string='OT Date', required=True)
    start_datetime = fields.Datetime(string='Start')
    end_datetime = fields.Datetime(string='End')
    category_id = fields.Many2one('ot.category', string='OT Category')
