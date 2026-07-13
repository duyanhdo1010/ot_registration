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
| 3. Views / Menu / Action | ✅ | 2026-06-29 | theo reference: gộp view 1 file, line tree inline; nghiệm thu pass |
| 4. Compute / Onchange / Constrains | ✅ | 2026-07-06 | thử lửa #1 XONG · MS1–MS5 ✅ (compute store ×4 + constrains ×2) · nghiệm thu pass |
| 5. Workflow + Mail | 🔶 | | MS1 (sequence+create) ✅ · MS2 (6 button+action_*) ✅ · **MS3 mail ĐANG LÀM** (scaffold đã đặt, chờ học viên) |
| 6. Wizard + Tracking | ⬜ | | |
| 7. Security & Record Rules | ⬜ | | cần Phụ lục A trước khi test |
| 8. OT Category theo thời gian | ⬜ | | **CHẬM LẠI** — bẫy timezone |
| 9. UI: Decoration + Button list | ⬜ | | |
| 10. Migration + Acceptance | ⬜ | | |
| 11. Automated Testing | ⬜ | | |

**👉 Đang ở:** 🔶 **C5·MS3 — Mail.** MS1 (ir.sequence + override `create`) và MS2 (6 button + `action_*` + luật "submit ≤ 2 ngày") đã pass review. MS3 scaffold đã đặt xong (`data/mail_templates.xml` + 2 stub), **đang chờ học viên viết** `get_record_url()` → `_send_mail()` → nối 4 `action_*` → 3 template TODO.

> ⚠️ **Luật giảng dạy (học viên yêu cầu 2026-07-10):** mở mỗi MS bằng khối **Concept** đầy đủ trước, rồi mới scaffold/code.

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
- [x] **MS0 — Pre-step model**: đổi state → tên reference; thêm field phẳng (`ot_month`,`request_date`; line: `from_date`/`to_date` thay `start/end`, `wfh_bz`,`ot_registration_hours`,`actual_ot_hours`,`reason`,`evidences`) — +fix `name` default='New'
- [x] **MS1 — Form `ot.request`** (reference): header statusbar + oe_title + group 2 cột + notebook
- [x] **MS2 — Line tree INLINE** trong form (theo reference, KHÔNG file riêng) + gỡ `views/ot_request_line_views.xml` khỏi manifest
- [x] **MS3 — Search `ot.request`**: field name/employee/project + 4 filter state (OR) + group by state/project/employee
- [x] **MS4 — Action + Menu** `ot.request` (`menu_ot_root` → `menu_ot_request`)
- ~~MS5 — view `ot.category`~~ → **BỎ** theo reference (category quản lý qua seed data ở C8)
- [x] Nghiệm thu: Create → thêm line inline → Save → filter "Đơn của tôi" + group by ✅ (state vẫn draft là đúng — workflow ở C5)

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

### 🟢 MS3 — Search `ot.request`
**Kiến thức:** Roadmap C3 Concept 3 (căn bản field/filter/group_by) + C9 Concept 5 (search đầy đủ); reference `ot_registration/views/ot_request_views.xml:22-48`. Search view **không** cần khai trong action — Odoo tự nhặt mặc định.

```xml
<record id="view_ot_request_search" model="ir.ui.view">
  <field name="name">ot.request.search</field>
  <field name="model">ot.request</field>
  <field name="arch" type="xml">
    <search string="Tìm đơn OT">
      <field name="name" string="Mã đơn"/>
      <field name="employee_id"/>
      <field name="project_id"/>
      <filter name="my_requests" string="Đơn của tôi" domain="[('employee_id.user_id','=',uid)]"/>
      <separator/>
      <filter name="f_pm" string="Chờ PM" domain="[('state','=','to_approve_pm')]"/>
      <!-- ⭐ TODO: Chờ DL / Đã duyệt / Từ chối -->
      <group expand="0" string="Gom nhóm theo">
        <filter name="gb_state" string="Trạng thái" context="{'group_by':'state'}"/>
        <!-- ⭐ TODO: group by project_id, employee_id -->
      </group>
    </search>
  </field>
</record>
```

**🎯 Your Turn:** điền 3 filter state còn lại + 2 group_by; trả lời (a) `uid` là gì vs `user.id` ở C7? (b) `<separator/>` đổi quan hệ filter (OR/AND)? ⚠️ chỉ dùng field đã có (`name/employee_id/project_id/state`).

### 🟢 MS4 — Action + Menu
**Kiến thức:** Roadmap C3 Concept 4 (~dòng 513–534) + Concept 5 (external id, thứ tự load); reference `ot_registration/views/ot_request_views.xml:167-174`. Đặt ở CUỐI file (sau các record view): action phải khai TRƯỚC menuitem ref nó; menu cha TRƯỚC menu con.

```xml
<record id="action_ot_request" model="ir.actions.act_window">
  <field name="name">OT Registration</field>
  <field name="res_model">ot.request</field>
  <field name="view_mode">tree,form</field>
</record>
<menuitem id="menu_ot_root" name="OT Registration" sequence="10"/>
<menuitem id="menu_ot_request" name="OT Requests"
          parent="menu_ot_root" action="action_ot_request" sequence="1"/>
```

**🎯 Your Turn:** (a) `view_mode="tree,form"` — vào thấy gì trước? (b) menu_ot_root không có `action` → bấm vào ra gì? (c) đảo menu con lên trước action → lỗi gì? **Nghiệm thu C3:** mở menu → tạo phiếu (name='New') → thêm line inline → save → test filter "Chờ PM" + group by state.

</details>

## CHƯƠNG 4 — Compute / Onchange / Constrains 🔶 ⚠️ CHẬM LẠI (thử lửa #1)

> Theo **reference convention**. Mỗi MS: mentor scaffold (field + `@api.depends` + khung), ⭐ học viên viết thân.

- [x] **MS1** ✅ — `pm_id`/`dl_id` đổi `res.users`→`hr.employee` + **compute store** (nghiệm thu pass: bản ghi mới tự điền PM+DL)
  - [x] `_compute_pm_id` (search hr.employee theo `project_id.user_id.id`, có guard rỗng + `.sudo()`)
  - [x] `_compute_dl_id` (`employee_id.parent_id`)
  - [x] Đưa `pm_id`/`dl_id` lên form (`readonly` + `no_open`)
- [x] **MS2** ✅ — `employee_custom_name` compute store = `Tên <Phòng ban>` (nghiệm thu pass 3 ca: có phòng ban / chưa có phòng ban → `<Chưa có phòng ban>` / form trống → `False`)
  - [x] Thân `_compute_employee_custom_name` (ghép `"tên <dept>"`, bẫy phòng ban rỗng, nhánh else `= False`)
  - [x] Đưa `employee_custom_name` lên form (cột phải, `readonly="1"`)
- [x] **MS3** ✅ — `total_actual_hours` compute store = Σ `line_ids.actual_ot_hours` (nghiệm thu pass 3 ca: tổng đúng / sửa giờ tự đổi / thêm-xóa dòng tự cập nhật)
  - [x] Thân `_compute_total_actual_hours` (`sum(rec.line_ids.mapped('actual_ot_hours'))`)
  - [x] Đưa `total_actual_hours` lên form (cột phải, `readonly="1"`)
- [x] **MS4** ✅ — line `ot_registration_hours` = compute store số giờ (`(to_date-from_date).total_seconds()/3600`); **duration thuần → KHÔNG cần tz** (bẫy tz là của C8); `actual_ot_hours` giữ nhập tay ⭐ *(category để C8)*
- [x] **MS5** ✅ — 2 `@api.constrains` trên line: `_check_date_order` (`to_date > from_date`) + `_check_no_overlap` (chống đè giờ trong CÙNG đơn, formula `<`/`<`) ⭐ → **C4 HOÀN TẤT**
- [ ] Micro-test sớm (tùy chọn): `tests/test_compute.py`

> **2 ngã rẽ chốt sau:** (1) MS4 onchange (reference) vs compute store (Roadmap). (2) Luật "submit ≤ 2 ngày" thuộc `action_submit` (**C5**), KHÔNG phải constrain C4 — bản nháp được giữ ngày cũ, chỉ chặn lúc *gửi*.

<details>
<summary>📖 <b>Hướng dẫn mentor — C4</b></summary>

### 🧠 Mô hình tư duy (chọn đúng công cụ)
- **related** = kéo thẳng field từ bản ghi khác (cứng). **compute store** = server tính + lưu DB → lọc/group/domain/code dùng được, tự cập nhật theo `@api.depends`. **onchange** = chỉ chạy trên form mở, gợi ý trước Save, KHÔNG chạy khi tạo bằng code. **constrains** = gác cổng, raise `ValidationError` chặn Save.
- Quy tắc: cái gì cần đúng **kể cả khi tạo bằng code** ⇒ compute store (hoặc compute + onchange).

### ✅ MS1 — pm_id/dl_id (compute store) — *XONG, nghiệm thu pass*
> 🐞 Bài học debug: "field trống" lần đầu KHÔNG phải bug — bản ghi cũ (tạo trước khi có compute) bị *stale*, compute store không tự backfill cột đã tồn tại. 3 tầng kiểm tra khi field trống: code đúng? → code đã nạp (server mới)? → compute đã chạy (bản ghi mới/depends đổi)? Xác minh field name Odoo 12: `project.project.user_id` (PM), `hr.employee.parent_id` (Manager) — đều đúng.
**Vì sao store=True:** C7 record rule "PM thấy đơn dự án mình" cần lọc theo `pm_id` trong domain → field non-stored không lọc/group được.
**Scaffold đã đặt trong `ot_request.py`:** đổi field sang `hr.employee` + `compute=...,store=True,ondelete='restrict'`; 2 method `_compute_pm_id`/`_compute_dl_id` có `@api.depends` + placeholder `= False` (no-op để server boot).
**⭐ Your Turn:**
- `_compute_pm_id`: PM = hr.employee của `project_id.user_id` (search `user_id`, cân nhắc `.sudo()`, xử lý project chưa có user).
- `_compute_dl_id`: DL = `employee_id.parent_id` (xử lý rỗng).
- Đưa `pm_id` (cột trái, `readonly="1" options="{'no_open':True}"`) + `dl_id` (cột phải) lên form — uncomment chỗ `🔜 C4`.
**Review hỏi:** (a) bỏ `store=True` thì C7 lọc theo pm_id hỏng ở đâu? (b) vì sao cần `.sudo()` trong compute? (c) `_compute_dl_id` nên `@api.depends('employee_id')` hay thêm `'employee_id.parent_id'`? khác nhau khi nào? (d) `ondelete='restrict'` trên field compute store nghĩa là gì khi xóa nhân viên?

### ✅ MS2 — employee_custom_name (compute store) — *XONG, nghiệm thu pass*
**Mục tiêu:** field Char hiển thị `Tên <Phòng ban>` (vd `Mitchell Admin <Management>`). Nguồn: `employee_id.name` + `employee_id.department_id.name`.
**Quyết định thiết kế (⭐ cần hiểu):** *live* (compute store + depends → tự đổi khi NV đổi phòng) vs *snapshot* (đóng băng lúc tạo, set trong `create()`). Reference dùng **live**; thực tế payroll nhiều khi muốn snapshot. Bám reference = live.
**Scaffold:** field `employee_custom_name = Char(compute='_compute_employee_custom_name', store=True)` + method có `@api.depends('employee_id','employee_id.department_id')` + placeholder.
**⭐ Đã làm:** ghép chuỗi `"tên <dept>"`; bẫy NV chưa có phòng ban → `<Chưa có phòng ban>`; nhánh `else` (chưa có employee) → `= False`; đưa field lên form (cột phải, readonly).
> 🐞 Bài học pair khi review thân method: (1) thiếu nhánh `else` khởi tạo `full_name` → biến rò rỉ qua vòng lặp / `NameError` khi record trống — compute store chạy cho **mọi** record kể cả chưa chọn NV. (2) đừng hardcode dữ liệu giả (`"Nguyen Van A"`) ở nhánh trống → dùng `False`. (3) guard nên hỏi `if rec.employee_id:` (đã chọn NV chưa) thay vì `.name`.

### ✅ MS3 — total_actual_hours (compute store, aggregate) — *XONG, nghiệm thu pass*
**Mục tiêu:** field Float = tổng `actual_ot_hours` của mọi dòng `line_ids`. Mẫu *aggregate over one2many* (tổng tiền/tổng giờ).
**Scaffold (mentor thêm Ở session này — trước đó CHƯA có, khác MS1/MS2):** field `total_actual_hours = Float(compute='_compute_total_actual_hours', store=True)` + method `@api.depends('line_ids.actual_ot_hours')` + placeholder `= 0`.
**⭐ Đã làm:** `rec.total_actual_hours = sum(rec.line_ids.mapped('actual_ot_hours'))` + đưa field lên form (cột phải, readonly).
> 🐞 Bài học pair: (1) học viên tự thêm nhánh `if line_ids / else 0` (thói quen tốt từ MS2) — ĐÚNG nhưng THỪA, vì `sum([]) == 0` đã lo ca rỗng. Rút ra: có cần `else` hay không tùy **hàm đã tự xử ca rỗng chưa**, không máy móc thêm mọi lúc (đối chiếu MS2: else ở đó BẮT BUỘC vì biến chưa khởi tạo). (2) Câu hỏi depends — nghiệm thu ca **thêm/xóa dòng PASS** → `@api.depends('line_ids.actual_ot_hours')` **ĐÃ ĐỦ** (đường dẫn qua o2m tự bắt add/remove line), KHÔNG cần thêm `'line_ids'` riêng.

### ✅ MS4 — ot_registration_hours (compute store, duration) — *XONG, nghiệm thu pass*
**Mục tiêu:** field Float trên `ot.request.line` = số giờ giữa `from_date`→`to_date` (thập phân, vd 19:00→21:30 = 2.5).
**🔀 Ngã rẽ #1 đã chốt:** **compute store** (không phải onchange) — đồng bộ MS1–MS3 + để C9 "tạo ngẫu nhiên bằng code" ra số giờ đúng (onchange KHÔNG chạy khi tạo bằng code).
**⭐ Quyết định ngữ nghĩa 2 field:** `ot_registration_hours` = giờ **đăng ký** (auto từ range, compute) vs `actual_ot_hours` = giờ **thực làm** (giữ **nhập tay** → chính là cái MS3 `total_actual_hours` cộng dồn). Không auto cả hai (sẽ luôn bằng nhau → thừa field).
**Scaffold (mentor):** đổi `ot_registration_hours` sang `compute='_compute_ot_registration_hours', store=True` + `@api.depends('from_date','to_date')` + placeholder `= 0.0`.
**⭐ Đã làm (học viên):** `delta = to_date - from_date` (timedelta, **không import** gì); `= delta.total_seconds() / 3600.0`; guard `if from_date and to_date … else 0.0`.
> 🐞 Bài học pair (3 lỗi review): (1) gọi `timedelta.total_seconds(x)` → `timedelta` chưa import + nhánh else truyền float vào → `NameError/TypeError`. Sửa: gọi method thẳng trên object hiệu `(...).total_seconds()`, KHÔNG cần import class. (2) đặt phép đổi NGOÀI `if` → nhánh else vỡ; phải đưa conversion vào trong `if`, else gán thẳng `0.0`. (3) `total_seconds()` ra **GIÂY** → thiếu `/3600`. Rút ra: hiệu 2 Datetime cho sẵn timedelta, cứ `.total_seconds()/3600`.
> 🧠 Chốt Q&A: (a) duration bất biến với tz (hiệu 2 mốc UTC = hiệu 2 mốc local) → MS4 **không** localize; C8 mới cần vì lấy `.hour/.weekday()`. (b) `@api.depends('from_date','to_date')` đủ (field nguồn nằm ngay trên record, khác MS3 phải đi qua o2m). (c) guard rỗng che ca form đang gõ dở (NewId), dù field `required+default=now`. (d) **negative hours KHÔNG xử ở compute** — để **MS5 constrain** `raise ValidationError` gác cổng (compute tính thật, constrain chặn Save).

### ✅ MS5 — constrains (gác cổng) — *XONG, nghiệm thu pass → ĐÓNG C4*
**Mục tiêu:** `@api.constrains` chặn Save khi (1) `to_date <= from_date`; (2) 2 dòng OT trong **cùng đơn** trùng/đè khoảng giờ. `raise ValidationError`.
**🔀 Thiết kế đã chốt:** **tách 2 method** (`_check_date_order` + `_check_no_overlap`), mỗi luật một hàm → thông báo lỗi rõ, một-hàm-một-việc. Cả hai `@api.constrains('from_date','to_date')`.
**Scaffold (mentor):** thêm `from odoo.exceptions import ValidationError` + 2 method skeleton (guard + hint overlap, thân `pass`).
**⭐ Đã làm (học viên):** L1 guard 2 mốc → `if rec.to_date <= rec.from_date: raise`. L2 duyệt `rec.request_id.line_ids`, loại self, overlap `line.from_date < rec.to_date and rec.from_date < line.to_date` → raise. Nghiệm thu pass 3 ca (to<from chặn / đè chặn / nối đuôi qua).
> 🐞 Bài học pair: (1) `if to_date <= from_date` quên `rec.` → **NameError** (biến không có trong scope; compute/constrain luôn đi qua `rec`). (2) `pass` thừa sau block đã có lệnh → dọn. (3) `else: raise "hãy nhập..."` được nhưng thừa vì `required=True` đã chặn rỗng.
> 🧠 Chốt Q&A: (a) `ValidationError` = sai **dữ liệu/ràng buộc**; `UserError` = **hành động** không được phép. (b) overlap dùng `<` (không `<=`) để chạm biên 21:00–21:00 KHÔNG tính đè → OT nối đuôi hợp lệ. (c) **ĐÍNH CHÍNH quan trọng:** `@api.constrains` chạy **SAU khi ghi DB** → record đều có **id thật** → `line.id != rec.id` KHÔNG lỗi ở đây; **NewId (id ảo) là chuyện của `@api.onchange`**, không phải constrain. (`line != rec` gọn hơn nhưng chỉ là style.) (d) chỉ chống đè **trong cùng đơn**; nhiều người khác đơn trùng giờ là bình thường → không chặn cross-đơn.
> 📐 Ghi chú: công thức overlap **đối xứng** → dù constrain kích hoạt trên dòng mới hay dòng bị sửa cho đè, đều bắt được, không sót chiều.

</details>

## CHƯƠNG 5 — Workflow + Mail 🔶 ĐANG LÀM

> ⚠️ **Luật mới từ 2026-07-10 (học viên yêu cầu):** mỗi MS phải mở bằng khối **Concept** đầy đủ (API là gì, chạy thế nào bên dưới, vì sao chọn nó thay cái khác) **TRƯỚC** khi đưa scaffold. Xong concept mới tới code. Vẫn giữ luật gốc: mentor KHÔNG code thay phần nghiệp vụ.

- [x] **MS1** ✅ — `ir.sequence` (`data/ot_sequence.xml`, bọc `<data noupdate="1">`) + override `create()` → `name = OT/2026/00001`
- [x] **MS2** ✅ — Form: 6 button workflow (`states="..."`) + 6 method `action_*` (đổi state + đóng dấu thời gian) + luật "submit ≤ 2 ngày" trong `action_submit`
- [ ] **MS3** 🔶 **ĐANG LÀM** — Mail: `get_record_url()` + `_send_mail()` + 4 `mail.template`, gửi KHÔNG log chatter
  - [x] Scaffold mentor: `data/mail_templates.xml` (template Submit viết đầy đủ làm mẫu + 3 TODO), 2 stub trong `ot_request.py`, khai manifest
  - [ ] ⭐ Học viên: thân `get_record_url()` (dùng `ir.config_parameter` key `web.base.url`, nhớ `.sudo()`)
  - [ ] ⭐ Học viên: thân `_send_mail(xml_id)` (`self.env.ref(...)` → `template.send_mail(id, force_send=True)`); **ngã rẽ:** loop hay `ensure_one()`?
  - [ ] ⭐ Học viên: nối mail vào 4 `action_*` — gọi **SAU** `self.write(...)` (template đọc `object.state`)
  - [ ] ⭐ Học viên: điền 3 template TODO (PM approve → DL + CC nhân viên; DL approve → nhân viên; Reject → nhân viên + lý do)
  - [ ] **Ngã rẽ chưa chốt:** 2 nút reject dùng CHUNG 1 template hay tách 2? (khác nhau ở "ai từ chối" — lấy từ field nào?)
- [ ] Nghiệm thu luồng thật (Phụ lục A)

<details>
<summary>📖 <b>Hướng dẫn mentor — C5</b></summary>

### ✅ MS1 — ir.sequence + override create() — *XONG*
**Scaffold mentor:** không có (học viên tự làm cả). **Học viên viết:** `data/ot_sequence.xml` + `create()` với pattern `vals.get('name','New') == 'New'`.
> 🐞 Review bắt: `<record>` trần **không** có `noupdate="1"` → mỗi lần `-u ot_registration` Odoo ghi đè record, kéo `number_next` về 1 → mã đơn trùng **âm thầm** (`name` không có unique constraint). Fix: bọc `<data noupdate="1">`.
> 🧠 `copy=False` trên `name` đã có sẵn từ C3 → duplicate đơn không kéo theo mã cũ.

### ✅ MS2 — 6 button workflow — *XONG*
**Học viên viết:** 6 `action_*` dùng `self.write({...})` + 6 `<button states="...">` trong `<header>`.
> 🐞 Review bắt 3 lỗi: (1) `if dates > 0:` với `dates = mapped('from_date')` → **TypeError** (`list > int` không hợp lệ trong Python 3; Odoo 12 trả `datetime` object, không phải string). Đúng là `if dates:`. (2) `action_reset` chỉ xoá `submitted_at`, để sót `pm_action_at`/`dl_action_at` → dữ liệu nói dối. (3) `<record>` sequence thiếu `noupdate` (xem MS1).
> 🧠 Chốt Q&A: (a) luật "≤ 2 ngày" ở `action_submit` chứ KHÔNG phải `@api.constrains` — bản nháp giữ được ngày cũ, chỉ chặn lúc *gửi*. (b) "Ngày phát sinh OT" = `min(line_ids.mapped('from_date'))` (dòng sớm nhất) + `timedelta(days=2)` = đúng 48h. Đơn có 1 dòng quá hạn → chặn **cả đơn**. Học viên đã chọn có ý thức. (c) Học viên tự yêu cầu chặn luôn **đơn không có dòng nào** → thêm nhánh raise.
> 📌 **Nợ style (đã nói, học viên chưa sửa — không ép):** `if dates: ... else: raise` nên đảo thành guard `if not self.line_ids: raise` ở đầu hàm (bớt 1 cấp thụt lề); message `"Khong tao duoc OT Request..."` sai ngữ cảnh (đơn đã tạo rồi, nút tên là Submit); `action_submit` chưa `ensure_one()` → nếu sau này bấm hàng loạt từ list view, `self.line_ids` gộp dòng của mọi đơn → `min()` sai.

### 🔶 MS3 — Mail (ĐANG LÀM)

**🧠 Concept đã giảng (2026-07-10) — session sau đừng giảng lại, chỉ nhắc:**
1. `mail.template` là **bản ghi dữ liệu** trong bảng `mail_template`, không phải cấu hình. Sửa được trên UI (Settings → Technical → Email → Templates). Không đặt `noupdate` để lúc học `-u` còn cập nhật được.
2. `ref="model_ot_request"` — Odoo tự sinh external id cho mọi model theo công thức `model_` + `_name` thay `.` bằng `_`. `model_id` trỏ tới `ir.model` (bảng metadata Odoo tự mô tả chính nó).
3. `${...}` là **Jinja2**, không phải f-string: Odoo dựng `SandboxedEnvironment` rồi đổi delimiter sang `${ }` (`mail/models/mail_template.py:85-88`). Sandbox chặn `import` + attribute `_`; gọi method công khai thì được → `${object.get_record_url()}` chạy.
4. Biến có sẵn khi render (`mail_template.py:325-330`): **chỉ** `object` (record), `user` (`env.user`), `ctx`, `format_date`/`format_tz`/`format_amount`. KHÔNG có `env`, KHÔNG có `self`.
5. Hai quirk: render ra chuỗi `"False"` → Odoo tự thay bằng chuỗi rỗng (`:341`) nên `email_to` rỗng sẽ gửi **im lặng**; render **nổ** → `UserError("Failed to render template...")` hiện ngay trên UI.
6. `send_mail(res_id, force_send)` (`:502`): `ensure_one()` áp lên **template**, `res_id` là **một** int → đó là lý do `_send_mail` phải quyết loop hay `ensure_one()`. `force_send=False` → mail nằm chờ cron "Mail: Email Queue Manager", dev tưởng code hỏng.
7. **Vì sao không log chatter:** `mail.mail` có `_inherits = {'mail.message': 'mail_message_id'}` (`mail_mail.py:27`) nên vẫn đẻ ra `mail.message`. NHƯNG chatter là **widget** đọc `message_ids` do `mail.thread` cấp; `ot.request` không kế thừa `mail.thread` + form không có chatter widget → message tồn tại trong DB mà không có đường hiển thị. Thoả README:52. **Đối chiếu:** `message_post_with_template()` sẽ vừa gửi vừa hiện chatter — đúng thứ đề bài cấm.
8. `email_to`/`email_cc` là `Char` (chuỗi email, ngăn bằng dấu phẩy), khác hẳn `partner_ids` (M2m `res.partner`, đường đi của notification chuẩn và **có** đụng chatter). Nhân viên là `hr.employee` → địa chỉ lấy từ `work_email` (xác minh `hr/models/hr.py:186`).
9. `web.base.url` nằm trong `ir.config_parameter` — bảng có tham số nhạy cảm nên nhân viên thường **không có quyền đọc**. Thiếu `.sudo()` → admin bấm thì chạy, nhân viên bấm thì `AccessError`. Cùng nguyên lý `.sudo()` đã dùng ở `_compute_pm_id` (C4·MS1).
10. ⚠️ `auto_delete` mặc định **True** → gửi **thành công** thì Odoo **xoá** `mail.mail`, chỉ giữ lại khi `state='exception'` (`mail_mail.py:285`). Ngược trực giác lúc debug. Scaffold đã đặt `eval="False"` cho cả 4 template để soi được ở Technical → Emails.

**Scaffold mentor (ĐÃ đặt):** `data/mail_templates.xml` (4 record; **Submit viết đầy đủ làm mẫu**, 3 cái còn lại `TODO`) · 2 stub `get_record_url()` + `_send_mail(xml_id)` trong `ot_request.py` (thân `TODO`/`pass`) · khai `data/mail_templates.xml` vào manifest.

**⭐ Your Turn (thứ tự bắt buộc):** `get_record_url()` **trước** (template Submit đã gọi nó rồi) → `_send_mail()` → nối vào 4 `action_*` (sau `write`) → cuối cùng mới điền 3 template TODO.

**Review sẽ hỏi:** (a) `_send_mail` chọn loop hay `ensure_one()`, và nó có nhất quán với `action_submit` không? (b) gọi mail trước `write` thì `${object.state}` in ra gì? (c) 2 nút reject: chung template hay tách? field nào cho biết "ai từ chối"? (d) `email_to` render rỗng thì chuyện gì xảy ra — có ai báo lỗi không?

**Nghiệm thu MS3:** bấm Submit → Settings → Technical → Email → Emails phải thấy 1 mail mới, `To` = email PM, thân mail có link bấm được. Nếu KHÔNG thấy mail nào → lỗi ở `_send_mail`, không phải ở template.

</details>

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
| 2026-07-10 | C5·MS3 | ▶️ **MỞ MS3 (mail).** Học viên yêu cầu **giảng concept đầy đủ trước khi code** → thành luật cho mọi MS về sau (ghi ở đầu C5 + memory). Mentor giảng 10 điểm (mail.template là data; external id `model_ot_request`; Jinja2 `${ }` sandboxed; chỉ có `object`/`user`/`ctx`; quirk `"False"`→rỗng & UserError khi render nổ; `send_mail` ensure_one trên *template*, res_id là 1 int; không log chatter vì `ot.request` thiếu `mail.thread` dù `mail.mail` `_inherits` `mail.message`; `email_to` là Char ≠ `partner_ids`; `.sudo()` đọc `web.base.url`; `auto_delete=True` xoá mail sau khi gửi **thành công**). Mentor dựng scaffold: `data/mail_templates.xml` (Submit đầy đủ + 3 TODO, `auto_delete=False` để debug) + stub `get_record_url()`/`_send_mail()` + khai manifest. **Chờ học viên viết.** |
| 2026-07-10 | C5·MS2 | ✅ **ĐÓNG MS2.** Học viên viết 6 `action_*` (`self.write` đổi state + đóng dấu `submitted_at`/`pm_action_at`/`dl_action_at`) + 6 `<button states="...">`. Review bắt lỗi chặn: `if dates > 0:` → **TypeError** (`mapped('from_date')` trả list `datetime`, Odoo 12 không còn string) → sửa `if dates:`. Bắt thêm: `action_reset` sót `pm_action_at`/`dl_action_at`. Học viên **tự yêu cầu** chặn luôn đơn không có dòng nào → thêm nhánh raise. Nợ style chưa sửa (guard đảo, message sai ngữ cảnh, thiếu `ensure_one`). Sang **MS3** (mail). |
| 2026-07-10 | C5·MS1 | ✅ **ĐÓNG MS1.** Học viên viết `data/ot_sequence.xml` + override `create()` (`vals.get('name','New') == 'New'` → `next_by_code`). Review bắt: `<record>` thiếu `<data noupdate="1">` → mỗi lần `-u` reset `number_next` về 1 → **mã đơn trùng âm thầm** (`name` không unique). Đã fix. |
| 2026-07-06 | C4 | ✅ **ĐÓNG C4 (MS5 + nghiệm thu).** Mentor dựng scaffold 2 `@api.constrains` + import `ValidationError`. Học viên viết `_check_date_order` (`rec.to_date <= rec.from_date`) + `_check_no_overlap` (duyệt `request_id.line_ids`, loại self, overlap `<`/`<`). Review bắt: quên `rec.` → NameError, `pass` thừa. Đính chính (c): constrain chạy sau ghi DB nên id thật → `.id` không lỗi; NewId là của onchange. Nghiệm thu pass 3 ca. **C4 hoàn tất → sang C5 (workflow+mail).** |
| 2026-07-06 | C4·MS4 | ✅ **ĐÓNG MS4.** Chốt ngã rẽ #1 = **compute store** (không onchange). Mentor dựng scaffold (`ot_registration_hours` compute store + `@api.depends('from_date','to_date')`). Học viên viết `(to_date-from_date).total_seconds()/3600.0` + guard. Review bắt 3 lỗi: `timedelta` chưa import, phép đổi ngoài `if` làm else vỡ, thiếu `/3600` (giây≠giờ). Chốt: **duration KHÔNG cần tz** (bẫy tz để C8); negative hours để **MS5 constrain**, không xử ở compute. `actual_ot_hours` giữ nhập tay. Nghiệm thu `19:00→21:30 = 2.50` pass. Sang **MS5** (constrains). |
| 2026-07-06 | C4·MS3 | ✅ **ĐÓNG MS3.** Mentor dựng scaffold (`total_actual_hours` Float compute store + `@api.depends('line_ids.actual_ot_hours')` + placeholder — trước đó CHƯA có). Học viên viết thân `sum(rec.line_ids.mapped('actual_ot_hours'))` + đưa lên form (readonly). Nghiệm thu pass 3 ca. Bài học: nhánh `if/else 0` THỪA (`sum([])==0`); ca thêm/xóa dòng pass → depends `line_ids.actual_ot_hours` ĐÃ ĐỦ. Sang **MS4** (giờ OT theo khoảng — timezone). |
| 2026-07-06 | C4·MS2 | ✅ **ĐÓNG MS2.** Học viên viết thân `_compute_employee_custom_name` (ghép `"tên <dept>"`, bẫy phòng ban rỗng → `<Chưa có phòng ban>`, else `= False`) + đưa field lên form (cột phải, readonly). Nghiệm thu pass 3 ca. Review bắt 3 lỗi: else thiếu init biến, hardcode tên giả, format thiếu `< >`. Sang **MS3** (`total_actual_hours` — CHƯA có scaffold). |
| 2026-06-29 | C4·MS2 | ▶️ Mở **MS2** (`employee_custom_name` = `Tên <Phòng ban>`). |
| 2026-06-29 | C4·MS1 | ✅ **MS1 pass.** Học viên điền `_compute_pm_id` (guard rỗng + `.id` + `.sudo()`) + `_compute_dl_id` (`employee_id.parent_id`) + đưa field lên form. Bug "field trống" = bản ghi cũ stale (compute store không backfill cột cũ), KHÔNG sửa code. Field name Odoo 12 đã xác minh. |
| 2026-06-29 | C3 | ✅ **ĐÓNG C3** — MS4 action+menu + nghiệm thu pass. Blocker "cache" = 3 server odoo song song (đã kill). Sang C4. |
| 2026-06-29 | C3 | ✅ MS3 search (4 filter state OR + group by). Sang MS4 (action+menu) → nghiệm thu C3. |
| 2026-06-29 | C3 | ✅ MS0/MS1/MS2 (model + form + line tree inline; fix name default='New'). Sang MS3 (search). |
| 2026-06-29 | C3 | Chốt theo reference: thêm MS0 (rename state + field line), MS1/MS2 reference-shaped, line tree inline, bỏ MS5; thêm callout vào Roadmap |
| 2026-06-29 | — | Thêm mục "Bản tham khảo" + bảng đối chiếu Roadmap↔Reference; ghi chú reference cho C3 |
| 2026-06-29 | C3 | Backfill khối "Hướng dẫn mentor" (fix tree + MS1 Form + MS2 line tree) vào dashboard |
| 2026-06-29 | — | Chuyển sang chế độ CODE-ALONG; dựng dashboard; xác nhận C1-C2 ✅, C3 đang dở |
