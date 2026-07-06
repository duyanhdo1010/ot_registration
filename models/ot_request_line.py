from odoo import models, fields, api
from odoo.exceptions import ValidationError


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

    # ============================================================
    # C4 · MS5 — constrains (GÁC CỔNG: raise ValidationError chặn Save)
    # ============================================================
    @api.constrains('from_date', 'to_date')
    def _check_date_order(self):
        for rec in self:
            if rec.to_date and rec.from_date:
                if rec.to_date <= rec.from_date:
                    raise ValidationError("Thoi gian ket thuc phai sau thoi gian bat dau")
            else:
                raise ValidationError("Hay nhap thoi gian bat dau va ket thuc")

    @api.constrains('from_date', 'to_date')
    def _check_no_overlap(self):
        for rec in self:
            for line in rec.request_id.line_ids:
                if line.id != rec.id:
                    if line.from_date < rec.to_date and rec.from_date < line.to_date:
                        raise ValidationError("Thoi gian OT trung gio nhau")