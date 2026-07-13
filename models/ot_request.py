from odoo import models, fields, api
from datetime import timedelta
from odoo.exceptions import ValidationError

class OtRequest(models.Model):
    _name = 'ot.request'
    _description = 'OT Request'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    employee_id = fields.Many2one('hr.employee', string='Employee', required=True)
    employee_custom_name = fields.Char(
        string='Employee Info',
        compute='_compute_employee_custom_name', store=True)
    project_id = fields.Many2one('project.project', string='Project', required=True)
    pm_id = fields.Many2one(
        'hr.employee', string='Project Manager',
        compute='_compute_pm_id', store=True, ondelete='restrict')
    dl_id = fields.Many2one(
        'hr.employee', string='Department Leader',
        compute='_compute_dl_id', store=True, ondelete='restrict')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('to_approve_pm', 'To approve'),
        ('to_approve_dl', 'PM approved'),
        ('approved', 'Manager approved'),
        ('reject', 'Reject'),
    ], string='State', default='draft')
    ot_month     = fields.Char(string='OT Month')
    request_date = fields.Datetime(string='Created Date', default=fields.Datetime.now, readonly=True)
    reject_reason = fields.Text(string='Reject Reason')
    submitted_at = fields.Datetime(string='Submitted At', readonly=True)
    pm_action_at = fields.Datetime(string='PM Action At', readonly=True)
    dl_action_at = fields.Datetime(string='DL Action At', readonly=True)
    line_ids = fields.One2many('ot.request.line', 'request_id', string='OT Lines')
    total_actual_hours = fields.Float(
        string='Total Actual OT Hours',
        compute='_compute_total_actual_hours', store=True)

    # ============================================================
    # C5 · MS1 — override create(): sinh name từ ir.sequence
    # ============================================================
    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('ot.request')
        return super(OtRequest, self).create(vals)

    # ============================================================
    # C5 · MS2 — workflow: mỗi nút đổi state + đóng dấu thời gian
    #   (self là record đang mở; dùng self.write({...}))
    # ============================================================
    def action_submit(self):
        # ⭐ draft -> to_approve_pm; đóng dấu submitted_at = fields.Datetime.now()
        #   + Luật "submit ≤ 2 ngày kể từ ngày phát sinh OT":
        #     nếu quá hạn -> raise ValidationError (cần import ở đầu file)
        #     👉 ngã rẽ: "ngày phát sinh OT" lấy từ đâu? (line.from_date sớm nhất?)
        #        -> mình bàn trước khi bạn code phần check này.
        dates = self.line_ids.mapped('from_date')
        if dates:
            oldest = min(dates)
            if fields.Datetime.now() - oldest > timedelta(days=2):
                raise ValidationError("Khong tao duoc OT Request neu qua 2 ngay")
        else:
            raise ValidationError("Khong tao duoc OT Request neu khong co thong tin thoi gian OT")
        self.write({
            'state': 'to_approve_pm',                 # đổi state (mũi tên)
            'submitted_at': fields.Datetime.now(),    # đóng dấu thời gian
        })

    def action_pm_approve(self):
        # ⭐ to_approve_pm -> to_approve_dl; đóng dấu pm_action_at
        self.write({
            'state': 'to_approve_dl',                 # đổi state (mũi tên)
            'pm_action_at': fields.Datetime.now(),    # đóng dấu thời gian
        })

    def action_pm_reject(self):
        # ⭐ to_approve_pm -> reject; đóng dấu pm_action_at
        #   (lý do từ chối: C5 chưa nhập, để wizard C6)
        self.write({
            'state': 'reject',                 # đổi state (mũi tên)
            'pm_action_at': fields.Datetime.now(),    # đóng dấu thời gian
        })

    def action_dl_approve(self):
        # ⭐ to_approve_dl -> approved; đóng dấu dl_action_at
        self.write({
            'state': 'approved',                 # đổi state (mũi tên)
            'dl_action_at': fields.Datetime.now(),    # đóng dấu thời gian
        })

    def action_dl_reject(self):
        self.write({
            'state': 'reject',                 # đổi state (mũi tên)
            'dl_action_at': fields.Datetime.now(),    # đóng dấu thời gian
        })

    def action_reset(self):
        self.write({
            'state': 'draft',                 # đổi state (mũi tên)
            'submitted_at': False,    # đóng dấu thời gian
            'dl_action_at': False,
            'pm_action_at': False
        })

    # Gán pm và dl khi tạo
    @api.depends('project_id')
    def _compute_pm_id(self):
        for rec in self:
            if rec.project_id.user_id:
                pm = self.env['hr.employee'].sudo().search(
                    [('user_id', '=', rec.project_id.user_id.id)], limit=1)
                rec.pm_id = pm
            else:
                rec.pm_id = False

    @api.depends('employee_id')
    def _compute_dl_id(self):
        for rec in self:
            dl = rec.employee_id.parent_id
            rec.dl_id = dl

    # ============================================================
    # C4 · MS2 — employee_custom_name = "Tên <Phòng ban>"
    # ============================================================
    @api.depends('employee_id', 'employee_id.department_id')
    def _compute_employee_custom_name(self):
        for rec in self:
            if rec.employee_id.name:
                full_name = rec.employee_id.name
                if rec.employee_id.department_id.name:
                    full_name += " <" + rec.employee_id.department_id.name + ">"
                else:
                    full_name += " <Chưa có phòng ban>"
            else:
                full_name = False
            rec.employee_custom_name = full_name

    # ============================================================
    # C4 · MS3 — total_actual_hours = Σ line_ids.actual_ot_hours
    # ============================================================
    @api.depends('line_ids.actual_ot_hours')
    def _compute_total_actual_hours(self):
        for rec in self:
            rec.total_actual_hours = sum(rec.line_ids.mapped('actual_ot_hours'))