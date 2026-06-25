from odoo import models, fields, api


class OtRequestLine(models.Model):
    _name = 'ot.request.line'
    _description = 'OT Request Line'

    request_id = fields.Many2one(
        'ot.request', string='OT Request',
        required=True, ondelete='cascade')
    from_date  = fields.Datetime(string='Giờ Bắt đầu', required=True, default=fields.Datetime.now)
    to_date    = fields.Datetime(string='Kết thúc', required=True, default=fields.Datetime.now)
    wfh_bz     = fields.Selection([('wfh','WFH'),('bz','BZ')], string='WFH/BZ', required=True)
    ot_registration_hours = fields.Float(string='Giờ OT đăng ký')
    actual_ot_hours       = fields.Float(string='Giờ OT thực tế')
    reason     = fields.Char(string='Lý do OT', default='N/A')
    evidences  = fields.Binary(string='Minh chứng')
    category_id = fields.Many2one('ot.category', string='OT Category')
