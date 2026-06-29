from odoo import models, fields, api


class OtRequestLine(models.Model):
    _name = 'ot.request.line'
    _description = 'OT Request Line'

    request_id = fields.Many2one(
        'ot.request', string='OT Request',
        required=True, ondelete='cascade')
    from_date  = fields.Datetime(string='From', required=True, default=fields.Datetime.now)
    to_date    = fields.Datetime(string='To', required=True, default=fields.Datetime.now)
    wfh_bz     = fields.Selection([('wfh','WFH'),('bz','BZ')], string='WFH/BZ', required=True)
    ot_registration_hours = fields.Float(string='OT Registration Hours')
    actual_ot_hours       = fields.Float(string='Actuan OT hours')
    reason     = fields.Char(string='Reason')
    evidences  = fields.Binary(string='Evidences')
    category_id = fields.Many2one('ot.category', string='OT Category')
