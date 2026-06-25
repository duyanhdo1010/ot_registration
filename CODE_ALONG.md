# 🛠️ CODE-ALONG Dashboard — OT Registration

> File điều phối tiến độ giữa **mentor** và **học viên** theo chế độ **CODE-ALONG** (vừa học vừa pair-programming).
> Roadmap lý thuyết đầy đủ: [Roadmap.md](Roadmap.md). File này CHỈ để tracking + nhịp làm việc.

## Luật chơi (rút gọn)

1. **Cuốn chiếu micro-step:** mentor đưa Concept ngắn + skeleton, chừa "Your Turn" cho học viên hoàn thiện logic cốt lõi.
2. **Mentor không code thay** phần logic nghiệp vụ — chỉ định hướng cấu trúc + viết code nền.
3. **Một micro-step xong** = học viên gửi code → mentor review tại chỗ → tick ✅ → qua bước kế.
4. **Đạp phanh ở C4 & C8** (compute/onchange/constrains + timezone) — đây là 2 chương "thử lửa", học viên cầm bút phần logic.

## Ký hiệu

| Ký hiệu | Nghĩa |
|---|---|
| `[x]` ✅ | Xong, đã review |
| `[~]` 🔶 | Đang làm dở |
| `[ ]` ⬜ | Chưa bắt đầu |
| ⭐ | Bước "Your Turn" — học viên phải tự viết logic |

> 📖 **Mỗi chương có khối "Hướng dẫn mentor"** (concept rút gọn + skeleton + câu hỏi review). Mentor điền dần **đúng lúc pair tới chương đó** — không đổ sẵn cả 11 chương (đó là việc của [Roadmap.md](Roadmap.md)). Khối nào ghi *"(chưa pair tới)"* nghĩa là sẽ viết khi bắt đầu.

---

## 📊 Tổng quan tiến độ

| Chương | Trạng thái | Ngày xong | Ghi chú |
|---|---|---|---|
| 1. Skeleton & Manifest | ✅ | — | manifest chuẩn (depends/version/data) |
| 2. Models (3 model) | ✅ | — | field cơ bản; compute/tracking để dành C4/C6 |
| 3. Views / Menu / Action | 🔶 | | theo reference: gộp view 1 file, line tree inline, bỏ file line riêng + view category |
| 4. Compute / Onchange / Constrains | ⬜ | | **CHẬM LẠI** — chương thử lửa #1 |
| 5. Workflow + Mail | ⬜ | | |
| 6. Wizard + Tracking | ⬜ | | |
| 7. Security & Record Rules | ⬜ | | cần Phụ lục A trước khi test |
| 8. OT Category theo thời gian | ⬜ | | **CHẬM LẠI** — bẫy timezone |
| 9. UI: Decoration + Button list | ⬜ | | |
| 10. Migration + Acceptance | ⬜ | | |
| 11. Automated Testing | ⬜ | | |

**👉 Đang ở:** C3 — MS0 (pre-step model) → MS1/MS2 (form + line tree inline).

---

## 🎯 Bản tham khảo (reference end-state)

> Có một bản project HOÀN CHỈNH ở thư mục lồng [`ot_registration/`](ot_registration/) — coi như "đáp án mẫu" để đối chiếu khi pair. **Không copy mù** (nó có vài bug tiềm ẩn, xem dưới); dùng để học cách tổ chức + xác nhận hướng đi.

**Điểm kiến trúc đáng học từ reference:**
- `pm_id`/`dl_id` là **`hr.employee` compute-store** (reactive), không phải `res.users` + onchange: `dl_id = employee.parent_id` (cấp trên trong hr), `pm_id` ← employee của `project.user_id`.
- **Gộp toàn bộ view vào 1 file** `views/ot_request_views.xml` (tree + search + form + action + menu); **line tree nhúng inline** trong form, **không** tách file riêng; `ot.category` chỉ seed data, không có view.
- Ẩn mail khỏi chatter bằng field `is_hidden_from_chatter` trên `mail.message` (override `models/mail_message.py`) + lọc `message_ids` — tinh vi hơn cách "chỉ dùng `template.send_mail`" của Roadmap.
- Nút random data làm bằng **JS/QWeb widget** (`static/src/js/ot_tree_button.js`), không phải `<tree><header><button>`.
- Thêm khái niệm **`deadline_date` (submit + 3 ngày) + `late_approved`** → decoration-warning trên tree (ngoài README, là bonus).

**⚠️ Đối chiếu Roadmap ↔ Reference (quyết định trước khi code tiếp):**

| Điểm | Roadmap dạy | Reference dùng | Model hiện tại của bạn |
|---|---|---|---|
| Tên state | `pm_waiting, dl_waiting, rejected` | `to_approve_pm, to_approve_dl, reject` | theo Roadmap |
| pm_id/dl_id | `res.users` + onchange | `hr.employee` + compute store | (chưa làm — C4) |
| Field line | `ot_date, start/end_datetime` | `from_date, to_date, wfh_bz, actual_ot_hours...` | theo Roadmap |
| File view | 3 file tách (category/request/line) | 1 file gộp, line inline | đang theo Roadmap (3 file) |
| Group quyền | 4 group (+employee +admin) | 2 group (pm, dl) + `base.group_user` | (chưa làm — C7) |

> **Mentor khuyến nghị:** vì bị ép tiến độ và đã có reference làm đích, **bám convention của reference** (tên state, kiểu employee cho pm/dl) để cuối cùng khớp đáp án — nhưng **hiểu lý do** qua concept Roadmap. Riêng chuyện tách/gộp file view: giữ tách theo Roadmap khi học (dễ thấy ranh giới), gộp lại được ở cuối nếu muốn. **Cần bạn chốt:** đổi state model sang tên reference, hay giữ tên Roadmap? (ảnh hưởng C5 trở đi).

> 🐞 **Bug tiềm ẩn trong reference — đừng chép nguyên:** `ot_request_line.py:74` so `rec.category_id == unknow_cat.id` (recordset == id, luôn sai); `:150` external id sai chính tả `cacot_cat_unknown`. Tốt cho bài tập "tự soi lỗi".

---

## CHƯƠNG 1 — Skeleton & Manifest ✅

- [x] Đổi thư mục `ot-registration` → `ot_registration`
- [x] `__manifest__.py` (name, version `12.0.1.0.0`, depends `base,mail,hr,project`, data, application)
- [x] `__init__.py` root + `models/__init__.py`
- [x] Cấu trúc thư mục con (`models/ views/ security/ data/ wizard/ migrations/`)
- [x] Install sạch, không Traceback

## CHƯƠNG 2 — Models ✅

- [x] `ot.category` (name, code, description, active, +trường thời gian cho C8)
- [x] `ot.request` (header field; state 5 giá trị; `line_ids` One2many)
- [x] `ot.request.line` (request_id, ot_date, start/end_datetime, category_id)
- [x] Khai báo `models/__init__.py`; upgrade ra đủ 3 bảng

## CHƯƠNG 3 — Views / Menu / Action 🔶

- [x] `security/ir.model.access.csv` sơ khai (full CRUD `base.group_user`)
- [x] Tree `ot.request` (đã thêm `model="ir.ui.view"`, bỏ `line_ids`)
- [ ] **MS0 — Pre-step model**: đổi state → tên reference; thêm field phẳng (`ot_month`,`request_date`; line: `from_date`/`to_date` thay `start/end`, `wfh_bz`,`ot_registration_hours`,`actual_ot_hours`,`reason`,`evidences`) ⭐
- [~] **MS1 — Form `ot.request`** (reference): header statusbar + oe_title + group 2 cột + notebook ⭐
- [ ] **MS2 — Line tree INLINE** trong form (theo reference, KHÔNG file riêng) + gỡ `views/ot_request_line_views.xml` khỏi manifest ⭐
- [ ] **MS3 — Search `ot.request`**: field name/employee/project + filter state + group by ⭐
- [ ] **MS4 — Action + Menu** `ot.request` (`menu_ot_root` → `menu_ot_request`)
- ~~MS5 — view `ot.category`~~ → **BỎ** theo reference (category quản lý qua seed data ở C8)
- [ ] Nghiệm thu: user thường CRUD được, không warning "no access rules"

<details>
<summary>📖 <b>Hướng dẫn mentor — C3</b></summary>

### 🔧 Lỗi đã sửa ở tree `ot.request`
- **THIẾU `model="ir.ui.view"`** trong `<record>` → Odoo không biết tạo record vào bảng nào, view không hiện. Mọi view BẮT BUỘC mở bằng `<record id="..." model="ir.ui.view">` (Roadmap C3 Concept 1, dòng 437). → đã thêm. ⚠️ Nhớ áp dụng cho MỌI file view sau.
- `<field name="line_ids"/>` trong tree → One2many trên list chỉ render con số đếm vô nghĩa → đã bỏ.
- *(altitude)* 4 cột `*_at` + `reject_reason` là field audit/chi tiết → thuộc về form, không nên phơi ra list. Cân nhắc lược bớt.

### 🟡 MS0 — Pre-step model (làm TRƯỚC, để view trỏ đúng field reference)
- **`ot_request.py`:** đổi Selection state → `draft / to_approve_pm / to_approve_dl / approved / reject`; thêm `ot_month = Char(required=True)`, `request_date = Datetime(default=now, readonly=True)`. *(pm_id/dl_id/total_actual_hours/employee_custom_name = compute → để dành C4.)*
- **`ot_request_line.py`:** `start_datetime`→`from_date`, `end_datetime`→`to_date`, bỏ `ot_date`; thêm `wfh_bz = Selection([wfh,bz], required=True)`, `ot_registration_hours = Float`, `actual_ot_hours = Float`, `reason = Char(default='N/A')`, `evidences = Binary`. *(is_unknown_category + auto-gán giờ/category → C4/C8.)*
- ⚠️ Đổi tên state ảnh hưởng record cũ mang giá trị `pm_waiting`… → xử lý ở bước nghiệm thu.

### 🟢 MS1 — Form `ot.request` (reference-shaped)
**Concept:** 4 vùng — `<header>` (statusbar + nút workflow để dành C5), `oe_title`, `<group>` lồng `<group>`, `<notebook>/<page>`. Field compute (pm_id/dl_id/total_actual_hours…) đánh dấu `🔜 C4/C5`, chưa đưa vào.

```xml
<record id="view_ot_request_form" model="ir.ui.view">
  <field name="name">ot.request.form</field>
  <field name="model">ot.request</field>
  <field name="arch" type="xml">
    <form string="OT Registration">
      <header>
        <!-- 🔜 C5: 5 nút workflow -->
        <field name="state" widget="statusbar"
               statusbar_visible="draft,to_approve_pm,to_approve_dl,approved,reject"/>
      </header>
      <sheet>
        <div class="oe_title"><h1><field name="name" readonly="1"/></h1></div>
        <group>
          <group>                                  <!-- TRÁI -->
            <field name="project_id"/>
            <field name="ot_month"/>
            <!-- 🔜 C4: pm_id (readonly, options no_open) -->
          </group>
          <group>                                  <!-- PHẢI ⭐ -->
            <field name="employee_id"/>
            <field name="request_date"/>
            <!-- 🔜 C4: employee_custom_name, dl_id, total_actual_hours -->
            <!-- 🔜 C5: deadline_date, late_approved (+ alert) -->
          </group>
        </group>
        <notebook>
          <page string="OT Request Lines">
            <field name="line_ids">
              <!-- 👇 MS2: tree INLINE ngay đây -->
            </field>
          </page>
        </notebook>
      </sheet>
      <!-- 🔜 C6: <div class="oe_chatter"> -->
    </form>
  </field>
</record>
```

### 🟢 MS2 — Line tree INLINE (theo reference, KHÔNG file riêng)
**Concept:** reference nhúng `<tree>` thẳng vào `<field name="line_ids">` của form — không có file `ot_request_line_views.xml`. Điền vào chỗ `👇` của MS1:

```xml
<field name="line_ids" attrs="{'readonly':[('state','not in',['draft','reject'])]}">
  <tree editable="bottom">
    <field name="from_date"/>
    <field name="to_date"/>
    <field name="category_id"/>
    <field name="wfh_bz"/>
    <field name="ot_registration_hours"/>
    <field name="actual_ot_hours"/>
    <field name="reason"/>
    <field name="evidences"/>
    <!-- 🔜 C8: is_unknown_category invisible + decoration-danger -->
    <!-- 🔜 C5: late_approved -->
  </tree>
</field>
```

**→ Dọn dẹp bắt buộc:** gỡ `views/ot_request_line_views.xml` khỏi `__manifest__.py['data']` (file 0 byte → **ParseError** khi load) và xóa file.

**🎯 Your Turn (review):**
- (a) `attrs readonly` theo state: vì sao line chỉ sửa được khi `draft/reject`?
- (b) `category_id`/`actual_ot_hours` ở reference có `force_save="1"` — đoán vì sao? (gợi ý: C4 chúng thành readonly/compute)
- (c) Đã gỡ file line khỏi manifest + xóa file chưa? Upgrade còn ParseError không?

### 🔎 Quyết định đã chốt (theo reference)
- **Gộp view 1 file** + **line tree inline** → bỏ file `ot_request_line_views.xml` (cả manifest lẫn file).
- **Bỏ MS5** (view `ot.category`): reference không có; category seed data ở C8.
- Tên state + tên field line theo reference (MS0). Bảng đối chiếu đầy đủ ở mục "🎯 Bản tham khảo" đầu file.

### ⬜ MS3 (Search) / MS4 (Action + Menu) — (chưa pair tới)

</details>

## CHƯƠNG 4 — Compute / Onchange / Constrains ⬜ ⚠️ CHẬM LẠI

- [ ] `ot.request.line.duration_hours` compute `store=True` (từ start/end) ⭐
- [ ] `ot.request.total_ot_hours` compute `store=True` (từ `line_ids.duration_hours`) ⭐
- [ ] `department_id` related từ `employee_id.department_id`, `store=True`
- [ ] `employee_display_name` compute `store=True` — quyết định live vs snapshot ⭐
- [ ] Onchange `project_id` → fill `pm_id`; onchange `employee_id`/`department_id` → fill `dl_id` ⭐
- [ ] Constrains: `end > start`; submit ≤ 2 ngày; line không trùng/đè giờ ⭐
- [ ] Micro-test sớm: `tests/test_compute.py` (duration_hours + end>start)

## CHƯƠNG 5 — Workflow + Mail ⬜

- [ ] Sequence `ot.request` (`data/ot_sequence.xml`) + override `create`; `copy=False` các field
- [ ] Form: statusbar + 5 button (Submit/PM Approve/PM Reject/DL Approve/DL Reject/Reset)
- [ ] Methods `action_*` (đổi state + đóng dấu thời gian + gửi mail) ⭐
- [ ] 4 `mail.template` (`data/mail_templates.xml`) có link record
- [ ] Helper `get_record_url()`
- [ ] Gửi mail KHÔNG log chatter (`template.send_mail`)
- [ ] Nghiệm thu luồng thật (Phụ lục A)

## CHƯƠNG 6 — Wizard + Tracking ⬜

- [ ] `wizard/ot_request_reject_wizard.py` (request_id, reason required) + `action_confirm` ⭐
- [ ] `wizard/..._views.xml` form có `<footer>` 2 nút
- [ ] Button Reject trên form → mở wizard
- [ ] `_inherit=['mail.thread']` + `tracking=True` cho state/total_ot_hours/pm_id/dl_id
- [ ] `<div class="oe_chatter">` cuối form; KHÔNG thêm `mail.activity.mixin`

## CHƯƠNG 7 — Security & Record Rules ⬜

- [ ] `security/ot_security.xml`: category + 4 groups (`implied_ids` hợp lý)
- [ ] `ir.rule`: Employee own / PM project / DL department (+ điều kiện state) ⭐
- [ ] Tinh chỉnh `ir.model.access.csv` theo group (PM/DL `create=0,unlink=0`)
- [ ] Thêm `groups="...group_ot_pm"` cho button PM Approve
- [ ] Nghiệm thu: 3 user thấy 3 list khác nhau

## CHƯƠNG 8 — OT Category theo thời gian ⬜ ⚠️ CHẬM LẠI (bẫy timezone)

- [ ] `data/ot_category_data.xml` seed 5 category, bọc `<data noupdate="1">`
- [ ] Helper `_detect_category` — **localize UTC→user.tz TRƯỚC** khi lấy `.hour/.weekday()` ⭐
- [ ] `category_id`: onchange (gợi ý form) + compute `store=True` (cho code C9) ⭐
- [ ] Quyết định + document xử lý OT qua đêm (docstring) ⭐
- [ ] Nghiệm thu 5 case + 1 case qua đêm

## CHƯƠNG 9 — UI: Decoration + Button list ⬜

- [ ] Tree `decoration-danger="total_ot_hours > 8"`
- [ ] Header button "Tạo ngẫu nhiên" + `action_create_random` (`@api.model`) ⭐
- [ ] Search view đầy đủ: filter trạng thái/project/dept/ngày + group by (mục 7 README)
- [ ] Nghiệm thu: random tạo record, tree đỏ khi >8h

## CHƯƠNG 10 — Migration + Acceptance ⬜

- [ ] Bump version `12.0.1.1.0`
- [ ] `migrations/12.0.1.1.0/post-backfill_employee_display_name.py` — idempotent ⭐
- [ ] Test: backfill 3 record cũ; upgrade lần 2 không đổi
- [ ] Acceptance Checklist (11 mục — xem Roadmap §10.4)
- [ ] Viết section "Cài đặt & test" vào README

## CHƯƠNG 11 — Automated Testing ⬜

- [ ] `tests/__init__.py` + `tests/test_ot_request.py`
- [ ] Test: happy path / reject+reset / end>start / 2 ngày / trùng giờ / total_ot_hours / category theo giờ ⭐
- [ ] Chạy `--test-enable` ra `X passed, 0 failed`
- [ ] Mentor code review tổng thể

---

## 📝 Nhật ký phiên (mới nhất ở trên)

| Ngày | Chương/MS | Nội dung |
|---|---|---|
| 2026-06-24 | C3 | Chốt theo reference: thêm MS0 (rename state + field line), MS1/MS2 reference-shaped, line tree inline, bỏ MS5; thêm callout vào Roadmap |
| 2026-06-24 | — | Thêm mục "Bản tham khảo" + bảng đối chiếu Roadmap↔Reference; ghi chú reference cho C3 |
| 2026-06-24 | C3 | Backfill khối "Hướng dẫn mentor" (fix tree + MS1 Form + MS2 line tree) vào dashboard |
| 2026-06-24 | — | Chuyển sang chế độ CODE-ALONG; dựng dashboard; xác nhận C1-C2 ✅, C3 đang dở |
