from odoo import models, fields, api


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
            # ⭐ Your Turn (MS2):
            #   Ghép chuỗi dạng:  "Tên nhân viên <Tên phòng ban>"
            #   - tên NV:        rec.employee_id.name
            #   - tên phòng ban: rec.employee_id.department_id.name
            #   Bẫy: NV chưa có phòng ban → department_id rỗng → .name sẽ là gì?
            #        → cần giá trị thay thế (vd 'Chưa có phòng ban').
            #   Nhánh else: khi rec.employee_id rỗng thì gán gì?
            rec.employee_custom_name = False  # ← placeholder, THAY bằng logic của bạn
