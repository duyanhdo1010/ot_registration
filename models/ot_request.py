from odoo import models, fields, api


class OtRequest(models.Model):
    _name = 'ot.request'
    _description = 'OT Request'

    name = fields.Char(string='Reference', required=True)
    employee_id = fields.Many2one('hr.employee', string='Employee', required=True)
    project_id = fields.Many2one('project.project', string='Project', required=True)
    pm_id = fields.Many2one('res.users', string='Project Manager')
    dl_id = fields.Many2one('res.users', string='Department Leader')
    state = fields.Selection([
        ('draft', 'Nháp'),
        ('to_approve_pm', 'Chờ PM duyệt'),
        ('to_approve_dl', 'PM đã duyệt'),
        ('approved', 'Đã duyệt'),
        ('reject', 'Từ chối'),
    ], string='Trạng thái', default='draft')
    ot_month     = fields.Char(string='Tháng OT', required=True)
    request_date = fields.Datetime(string='Ngày tạo đơn', default=fields.Datetime.now, readonly=True)
    reject_reason = fields.Text(string='Reject Reason')
    submitted_at = fields.Datetime(string='Submitted At', readonly=True)
    pm_action_at = fields.Datetime(string='PM Action At', readonly=True)
    dl_action_at = fields.Datetime(string='DL Action At', readonly=True)
    line_ids = fields.One2many('ot.request.line', 'request_id', string='OT Lines')
