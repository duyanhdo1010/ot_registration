# 🤝 HANDOFF — OT Registration (đọc đầu mỗi session mới)

> **Mục đích:** giúp session Claude kế tiếp (và bạn) bắt nhịp NGAY mà không đọc lại toàn bộ lịch sử chat.
> **Cách dùng:** đầu session mới, mở file này trước → đọc "📸 Snapshot" + "⏭️ Việc tiếp theo" → rồi mở [CODE_ALONG.md](CODE_ALONG.md) để biết tiến độ chi tiết. Cập nhật file này mỗi khi đổi trạng thái lớn.

---

## 📸 Snapshot (cập nhật: 2026-07-10)

- **Project:** module Odoo 12 `ot.registration` — quản lý đăng ký OT. Spec: [README.md](README.md). Giáo trình: [Roadmap.md](Roadmap.md).
- **Chế độ làm việc:** CODE-ALONG (mentor đưa concept + skeleton, học viên hoàn thiện logic; mentor KHÔNG code thay phần nghiệp vụ). Luật + tiến độ đầy đủ ở [CODE_ALONG.md](CODE_ALONG.md).
- **⚠️ LUẬT MỚI (học viên yêu cầu 2026-07-10):** mỗi milestone phải **giảng khối Concept đầy đủ TRƯỚC** khi đưa scaffold hoặc để học viên code — nói rõ *API là gì, chạy thế nào bên dưới, vì sao chọn nó thay cái khác*, không chỉ liệt kê "làm gì".
- **Convention đã chốt:** **theo BẢN THAM KHẢO** `ot_registration/ot_registration/` (state `to_approve_pm/to_approve_dl/reject`, line `from_date/to_date`, gộp view 1 file + line tree inline). Bảng đối chiếu: mục "🎯 Bản tham khảo" trong CODE_ALONG.
- **Đang ở:** 🔶 **C5·MS3 — Mail** (xem "⏭️ Việc tiếp theo"). C4 ✅ đóng trọn (compute store ×4 + 2 constrains). C5·MS1 (ir.sequence + override `create`) ✅ và C5·MS2 (6 button + `action_*` + luật "submit ≤ 2 ngày") ✅ đã pass review.
- **📌 Bài học chốt MS4 (đừng quên ở C8):** tính **duration** (số giờ giữa 2 mốc) **KHÔNG cần timezone** — hiệu 2 mốc UTC = hiệu 2 mốc local. Bẫy tz THẬT nằm ở **C8** khi lấy `.hour/.weekday()` để phân loại category. MS4 đã bỏ hẳn pytz.

---

## ✅ BLOCKER (đã gỡ 2026-06-29) — chạy NHIỀU server Odoo song song

**Hiện tượng đã gặp:** sửa `.py` (label EN, bỏ `required` ot_month, `default='New'` name) nhưng UI vẫn bản cũ → save lỗi `Reference invalid`, ot_month vẫn required, label vẫn tiếng Việt.

**Nguyên nhân THẬT (đã xác định bằng diag):** có **3+ tiến trình `odoo-bin` chạy song song**. Cái CŨ nhất (khởi động buổi sáng) vẫn **ôm cổng 8069** → trình duyệt luôn trúng code cũ. Mỗi lần "restart", học viên Ctrl+C terminal MỚI nhưng tiến trình cũ không chết → vô hiệu. → **KHÔNG phải pycache.** (`--dev=xml` không reload `.py` chỉ là yếu tố phụ.)

**Đã xử (mentor):** kill hết python odoo-bin → xác nhận **0 server + cổng 8069 FREE**. Còn lại: học viên start DUY NHẤT 1 server.

### ▶️ Khởi động lại (chạy trong terminal CỦA BẠN, KHÔNG qua Claude)

```powershell
& "C:\Program Files (x86)\Odoo 12\python\python.exe" "C:\Program Files (x86)\Odoo 12\server\odoo-bin" -c "C:\Program Files (x86)\Odoo 12\server\odoo.conf" -u ot_registration --dev=reload,xml
```
- `--dev=reload` = tự restart khi `.py` đổi (cần package `watchdog`).

### 🩺 Khi nghi "dính cache" lần sau — check NGAY 2 lệnh này

```powershell
# 1) Còn server python odoo nào đang chạy? (LỌC python.exe, đừng match 'odoo-bin' chung — sẽ dính chính lệnh của bạn)
Get-CimInstance Win32_Process | Where-Object { $_.Name -eq 'python.exe' -and $_.CommandLine -match 'odoo-bin' } | Select ProcessId, CreationDate
# 2) Ai ôm cổng 8069?
Get-NetTCPConnection -LocalPort 8069 -State Listen | Select OwningProcess
```
> Quy tắc vàng: **chỉ được CÓ ĐÚNG 1** python odoo-bin ôm 8069. Nhiều hơn = cái cũ phục vụ code cũ → kill hết rồi start lại 1 cái.

**Kiểm chứng sau khi lên:** Create → name='New', ot_month không required, statusbar EN (Draft/To approve/PM approved/Manager approved/Reject).

---

## ⏭️ VIỆC TIẾP THEO — C5·MS3 Mail (học viên đang viết)

**Đã xong:** C4 trọn vẹn · C5·MS1 `ir.sequence` + override `create()` (đã fix `<data noupdate="1">`) · C5·MS2 6 button workflow + 6 `action_*` + luật "submit ≤ 2 ngày" + chặn đơn rỗng.

**Mentor ĐÃ dựng scaffold MS3, học viên CHƯA viết:**
- `data/mail_templates.xml` — 4 record `mail.template`; **Submit viết đầy đủ làm mẫu**, 3 cái còn lại để `TODO`. Đã khai vào manifest. Đặt `auto_delete="False"` cho dễ debug.
- `models/ot_request.py` — 2 stub: `get_record_url()` (thân `return ''`) và `_send_mail(xml_id)` (thân `pass`).

**⭐ Thứ tự học viên phải làm (đã dặn):**
1. `get_record_url()` **trước tiên** — template Submit đã gọi nó rồi. Dùng `ir.config_parameter` key `web.base.url`, **nhớ `.sudo()`**.
2. `_send_mail(xml_id)` — `self.env.ref('ot_registration.<id>')` → `template.send_mail(<res_id>, force_send=True)`. **Ngã rẽ chưa chốt:** loop hay `ensure_one()`?
3. Nối vào 4 `action_*` — gọi mail **SAU** `self.write(...)` (template đọc `object.state`).
4. Điền 3 template TODO. **Ngã rẽ chưa chốt:** 2 nút reject dùng chung 1 template hay tách 2? (khác ở "ai từ chối" — lấy từ field nào?)

**🧠 Concept MS3 ĐÃ giảng đủ 10 điểm** (mail.template là data · external id `model_ot_request` · Jinja2 `${ }` sandboxed · chỉ có `object`/`user`/`ctx` · quirk `"False"`→rỗng & `UserError` khi render nổ · `send_mail` `ensure_one()` áp lên *template* và `res_id` là 1 int · **không log chatter vì `ot.request` thiếu `mail.thread`**, dù `mail.mail` `_inherits` `mail.message` · `email_to` là `Char` ≠ `partner_ids` · `.sudo()` để đọc `web.base.url` · `auto_delete=True` xoá mail sau khi gửi **thành công**). Chi tiết + số dòng source: [CODE_ALONG.md](CODE_ALONG.md) §C5·MS3. **Session sau đừng giảng lại, chỉ nhắc.**

**Nghiệm thu MS3:** bấm Submit → Settings → Technical → Email → Emails thấy mail mới, `To` = email PM, thân có link bấm được. Không thấy mail nào ⇒ lỗi ở `_send_mail`, không phải template.

**📌 Nợ style C5·MS2 (đã nói, học viên chưa sửa — KHÔNG ép):** `if dates: ... else: raise` nên đảo thành guard `if not self.line_ids: raise` đầu hàm · message `"Khong tao duoc OT Request..."` sai ngữ cảnh (đơn đã tạo, nút tên Submit) · `action_submit` thiếu `ensure_one()` → bấm hàng loạt từ list view sẽ gộp `line_ids` mọi đơn, `min()` sai.

> 🩺 **Lưu ý IDE:** language server hay báo nhầm "Could not find model 'hr.employee'" / "field 'department_id'" — **false positive** (chưa index module `hr`). Đã xác minh tận source Odoo 12: `project.py:193` `user_id`(PM), `hr.py:191` `parent_id`(Manager), `hr.py:190` `department_id`. Đừng đổi code theo cảnh báo này.

---

## ✅ ĐÃ XONG (tóm tắt — chi tiết ở CODE_ALONG)

- **C1** Skeleton + manifest ✅ · **C2** 3 models ✅
- **C3** ✅ ĐÓNG: access csv · MS0 model (rename state + field line, fix `name` default='New') · MS1 form · MS2 line tree inline · MS3 search · MS4 action+menu · nghiệm thu pass
- Đã bỏ file `ot_request_line_views.xml` (inline) + bỏ MS5 (view category — reference không có).

---

## ⚠️ NỢ KỸ THUẬT / GHI CHÚ (đừng quên ở chương sau)

- ~~`name` đang `default='New'` tạm → C5 thay bằng `ir.sequence`~~ ✅ **XONG ở C5·MS1** (`create()` gọi `next_by_code('ot.request')`; `copy=False` đã có sẵn).
- ⚠️ **Mọi `<record>` data không được ghi đè khi `-u` phải bọc `<data noupdate="1">`** — bài học từ `ir.sequence` (không có nó, `number_next` reset về 1 mỗi lần update → mã đơn trùng âm thầm vì `name` không unique). Áp dụng lại ở **C8** khi seed `ot_category_data.xml`. Ngược lại, `mail.template` thì CỐ Ý không đặt `noupdate` để lúc học `-u` còn cập nhật được.
- ~~`pm_id`/`dl_id` đang `res.users` → C4 đổi sang `hr.employee` + compute~~ ✅ **XONG ở MS1** (`dl_id=employee.parent_id`, `pm_id` từ `project.user_id`).
- ~~3 field `submitted_at/pm_action_at/dl_action_at` reference không dùng~~ ✅ **C5·MS2 đã dùng** (mỗi `action_*` đóng dấu 1 field; `action_reset` xoá cả 3). Vẫn KHÔNG đưa lên form.
- `ot_category_views.xml` còn là vỏ rỗng trong manifest — cân nhắc gỡ (MS5 đã bỏ).
- Bug trong reference (đừng chép mù): `ot_request_line.py:74` so recordset==id; `:150` external id sai chính tả `cacot_cat_unknown`.

---

## 🗺️ Bản đồ file

| File | Vai trò |
|---|---|
| [CODE_ALONG.md](CODE_ALONG.md) | **Nguồn sự thật** về tiến độ + hướng dẫn mentor từng chương (tick dần) |
| [Roadmap.md](Roadmap.md) | Giáo trình lý thuyết 11 chương (concept, ví dụ) |
| [README.md](README.md) | Spec nghiệp vụ gốc |
| `HANDOFF.md` (file này) | Trạng thái sống giữa các session |
| `ot_registration/` (nested) | Bản tham khảo hoàn chỉnh = đáp án để đối chiếu |
