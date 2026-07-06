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
    ot_registration_hours = fields.Float(
        string='OT Registration Hours',
        compute='_compute_ot_registration_hours', store=True)
    actual_ot_hours       = fields.Float(string='Actuan OT hours')
    reason     = fields.Char(string='Reason')
    evidences  = fields.Binary(string='Evidences')
    category_id = fields.Many2one('ot.category', string='OT Category')

    # ============================================================
    # C4 · MS4 — ot_registration_hours = số giờ giữa from_date → to_date
    # ============================================================
    @api.depends('from_date', 'to_date')
    def _compute_ot_registration_hours(self):
        for rec in self:
            if rec.from_date and rec.to_date:
                delta = rec.to_date - rec.from_date
                rec.ot_registration_hours = delta.total_seconds() / 3600.0
            else:
                rec.ot_registration_hours = 0.0