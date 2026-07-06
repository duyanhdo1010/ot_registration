# 🤝 HANDOFF — OT Registration (đọc đầu mỗi session mới)

> **Mục đích:** giúp session Claude kế tiếp (và bạn) bắt nhịp NGAY mà không đọc lại toàn bộ lịch sử chat.
> **Cách dùng:** đầu session mới, mở file này trước → đọc "📸 Snapshot" + "⏭️ Việc tiếp theo" → rồi mở [CODE_ALONG.md](CODE_ALONG.md) để biết tiến độ chi tiết. Cập nhật file này mỗi khi đổi trạng thái lớn.

---

## 📸 Snapshot (cập nhật: 2026-07-06)

- **Project:** module Odoo 12 `ot.registration` — quản lý đăng ký OT. Spec: [README.md](README.md). Giáo trình: [Roadmap.md](Roadmap.md).
- **Chế độ làm việc:** CODE-ALONG (mentor đưa concept + skeleton, học viên hoàn thiện logic; mentor KHÔNG code thay phần nghiệp vụ). Luật + tiến độ đầy đủ ở [CODE_ALONG.md](CODE_ALONG.md).
- **Convention đã chốt:** **theo BẢN THAM KHẢO** `ot_registration/ot_registration/` (state `to_approve_pm/to_approve_dl/reject`, line `from_date/to_date`, gộp view 1 file + line tree inline). Bảng đối chiếu: mục "🎯 Bản tham khảo" trong CODE_ALONG.
- **Đang ở:** 🔶 **C4 — Compute/Onchange/Constrains** (thử lửa #1, đạp phanh). **MS1 ✅ + MS2 ✅ + MS3 ✅** (pm_id/dl_id + employee_custom_name + total_actual_hours, compute store — nghiệm thu pass). Đang **MS4**: giờ OT theo khoảng + localize tz (bắt đầu đụng timezone — đạp phanh #2). Plan MS1→MS5 ở [CODE_ALONG.md](CODE_ALONG.md) §C4.

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

## ⏭️ VIỆC TIẾP THEO — C4 / MS4 (bắt đầu session sau)

**MS1 ✅ ĐÓNG:** `pm_id`/`dl_id` → `hr.employee` compute store. **MS2 ✅ ĐÓNG:** `employee_custom_name` = `Tên <Phòng ban>` compute store (Live). **MS3 ✅ ĐÓNG:** `total_actual_hours` = `sum(line_ids.mapped('actual_ot_hours'))` compute store — đã kiểm `@api.depends('line_ids.actual_ot_hours')` ĐỦ bắt add/xóa line (KHÔNG cần thêm `'line_ids'`). Cả 3 đã lên form (readonly), nghiệm thu pass.

**MS4 — tính giờ OT theo KHOẢNG (`from_date`→`to_date`) trên `ot.request.line`.** ⚠️ Đây là **"đạp phanh #2" — bẫy TIMEZONE**, đi CHẬM. **Chưa có scaffold.**
- 🔀 **QUYẾT ĐỊNH TRƯỚC KHI CODE (ngã rẽ #1):** dùng **onchange** (theo reference) hay **compute store** (theo Roadmap) để điền `ot_registration_hours`/`actual_ot_hours`? Chốt với học viên rồi MỚI dựng skeleton. Nhắc: onchange KHÔNG chạy khi tạo bằng code; compute store chạy mọi lúc (xem "Mô hình tư duy" §C4).
- ⭐ Nội dung: `from_date`/`to_date` lưu **UTC** → **localize về tz người dùng** → suy ra số giờ OT. Bẫy kinh điển: quên localize → lệch giờ.
- ⛔ **KHÔNG làm category** ở MS4 — phân loại OT theo mốc thời gian (ngày/đêm/lễ) để dành **C8**. MS4 chỉ tính số giờ.
- Tham chiếu khi pair: bản reference `ot_registration/ot_registration/` (cách nó tính giờ) + Roadmap (lý thuyết tz). Chi tiết mentor sẽ điền vào [CODE_ALONG.md](CODE_ALONG.md) §C4 lúc bắt đầu.

**Còn lại C4:** MS5 constrains (`to_date > from_date` + chống trùng/đè giờ trong cùng đơn). Chi tiết + 2 ngã rẽ ở [CODE_ALONG.md](CODE_ALONG.md) §C4.

> 🩺 **Lưu ý IDE:** language server hay báo nhầm "Could not find model 'hr.employee'" / "field 'department_id'" — **false positive** (chưa index module `hr`). Đã xác minh tận source Odoo 12: `project.py:193` `user_id`(PM), `hr.py:191` `parent_id`(Manager), `hr.py:190` `department_id`. Đừng đổi code theo cảnh báo này.

---

## ✅ ĐÃ XONG (tóm tắt — chi tiết ở CODE_ALONG)

- **C1** Skeleton + manifest ✅ · **C2** 3 models ✅
- **C3** ✅ ĐÓNG: access csv · MS0 model (rename state + field line, fix `name` default='New') · MS1 form · MS2 line tree inline · MS3 search · MS4 action+menu · nghiệm thu pass
- Đã bỏ file `ot_request_line_views.xml` (inline) + bỏ MS5 (view category — reference không có).

---

## ⚠️ NỢ KỸ THUẬT / GHI CHÚ (đừng quên ở chương sau)

- `name` đang `default='New'` tạm → **C5** thay bằng `ir.sequence` (`OT/2026/00001`) trong `create()`.
- ~~`pm_id`/`dl_id` đang `res.users` → C4 đổi sang `hr.employee` + compute~~ ✅ **XONG ở MS1** (`dl_id=employee.parent_id`, `pm_id` từ `project.user_id`).
- 3 field `submitted_at/pm_action_at/dl_action_at` (kiểu Roadmap) reference không dùng — để đó, đừng đưa lên form.
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
