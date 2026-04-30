# OT Registration Module Exercise

## Bài toán

Thêm chức năng quản lý đăng ký OT cho một công ty, bao gồm:

- CRUD
- Phân quyền
- Gửi mail
- Luồng duyệt
- Filter
- Group by

## Luồng nghiệp vụ chính

1. Nhân viên khi có nhu cầu cần tạo request đăng ký OT, với thời hạn là **2 ngày** kể từ ngày phát sinh OT.
2. Sau khi nhân viên tạo request và submit, PM của dự án nhận được thông báo qua mail.
3. PM sẽ vào duyệt hoặc từ chối bản ghi của nhân viên.
  - Nếu PM duyệt thì DL nhận được thông báo và vào xác nhận.
  - DL cũng nhận được mail action duyệt và từ chối nếu PM duyệt bản ghi.
4. Nếu PM từ chối thì bản ghi chuyển về trạng thái `reject`.
  - Bản ghi ở `reject`, nhân viên có thể chuyển về `draft` để sửa lại.

## Lưu ý bắt buộc

- Ở mỗi bước của PM và DL, nhân viên đều phải được CC mail.
- Nhân viên chỉ được xem các bản ghi do mình tạo.
- DL có thể xem các bản ghi của department mình:
  - Đang chờ duyệt
  - Đã duyệt
  - Đã từ chối
- PM có thể xem các bản ghi của dự án mình:
  - Đang chờ duyệt
  - Đã duyệt
  - Đã từ chối
- Cần sử dụng đầy đủ các hàm `onchange`, `compute`, `constrains`.
- Tham khảo màn OT từ VMS

## Yêu cầu thêm

- Đổi màu ở list view khi tổng thời gian OT lớn hơn **8 giờ**.
- Làm các OT Category:
  - Thứ 2 - Thứ 6 (18h30 - 22h): Ngày bình thường
  - Thứ 2 - Thứ 6 (22h - 6h): Ngày bình thường - ban đêm
  - Thứ 7 (6h - 22h): Thứ 7
  - Chủ Nhật (6h - 22h): Chủ nhật
  - Thứ 7, Chủ Nhật (22h - 6h): Ngày cuối tuần - ban đêm
- Viết migration để đồng bộ dữ liệu: thêm một field để tính **[Tên + Phòng ban mà user đó làm việc]**.
- Sau khi approve hoặc reject, mail gửi kèm đường dẫn trực tiếp tới bản ghi để người dùng click vào ngay.
- Khi PM hoặc DL từ chối, hiển thị pop-up cho phép nhập **LÝ DO** và kèm lý do đó trong mail.
- Khi có thay đổi trạng thái / giờ OT / PM / DL thì lưu lại lịch sử.
- Không cho phép mail được log ở phần comment.
- Tạo một nút ở list view: bấm vào sẽ tạo ngẫu nhiên bản ghi `ot.request` và `ot.request.line` rỗng.

## Đặc tả triển khai

### 1) Danh sách model

- `ot.request`
  - Thông tin header của phiếu OT.
  - Field gợi ý:
    - `name` (mã phiếu)
    - `employee_id`
    - `department_id` (compute từ employee)
    - `project_id`
    - `pm_id`
    - `dl_id`
    - `state` (`draft`, `pm_waiting`, `dl_waiting`, `approved`, `rejected`)
    - `reject_reason`
    - `total_ot_hours` (compute từ line)
    - `employee_display_name` (migration field: `[Tên + Phòng ban]`)
    - `submitted_at`, `pm_action_at`, `dl_action_at`
    - `line_ids`
- `ot.request.line`
  - Thông tin chi tiết theo từng khung giờ OT.
  - Field gợi ý:
    - `request_id`
    - `ot_date`
    - `start_datetime`
    - `end_datetime`
    - `duration_hours` (compute)
    - `category_id` (compute + onchange)
- `ot.category`
  - Danh mục loại OT theo quy tắc thời gian.
  - Dữ liệu khởi tạo theo 5 category trong đề bài.
- `ot.request.history` (hoặc dùng `mail.tracking.value` nếu đã theo chuẩn tracking)
  - Lưu lịch sử khi thay đổi `state`, `total_ot_hours`, `pm_id`, `dl_id`.

### 2) Workflow trạng thái

- `draft` -> `pm_waiting`: Nhân viên submit.
- `pm_waiting` -> `dl_waiting`: PM approve.
- `pm_waiting` -> `rejected`: PM reject (bắt buộc nhập lý do).
- `dl_waiting` -> `approved`: DL approve.
- `dl_waiting` -> `rejected`: DL reject (bắt buộc nhập lý do).
- `rejected` -> `draft`: Nhân viên reset về draft để chỉnh sửa và submit lại.

### 3) Phân quyền và phạm vi dữ liệu

- Nhân viên:
  - Tạo/sửa/xóa khi `state = draft` hoặc bản ghi bị reject và đã reset draft.
  - Chỉ thấy bản ghi của chính mình.
- PM:
  - Được action duyệt/từ chối khi `state = pm_waiting`.
  - Chỉ thấy bản ghi thuộc dự án mình quản lý.
- DL:
  - Được action duyệt/từ chối khi `state = dl_waiting`.
  - Chỉ thấy bản ghi thuộc department mình phụ trách.
- Admin HR/OT:
  - Toàn quyền cấu hình category, theo dõi và báo cáo.

### 4) Validation, compute, onchange, constrains

- `@api.constrains`:
  - `end_datetime > start_datetime`.
  - Không cho submit nếu quá 2 ngày kể từ ngày phát sinh OT.
  - Không cho line bị trùng/đè thời gian trong cùng một request.
- `@api.depends`:
  - Tính `duration_hours`.
  - Tính `total_ot_hours`.
  - Tính `department_id`, `employee_display_name`.
- `@api.onchange`:
  - Đổi `pm_id`, `dl_id` khi thay `project_id`/`department_id`.
  - Tự gợi ý `category_id` theo `ot_date`, `start_datetime`, `end_datetime`.

### 5) Mail template và mail action

- Sự kiện gửi mail:
  - Khi submit cho PM.
  - Khi PM approve cho DL.
  - Khi PM/DL reject cho nhân viên (kèm lý do).
  - Khi DL approve cho nhân viên.
- Yêu cầu mail:
  - Nhân viên luôn được CC ở mỗi bước PM/DL xử lý.
  - Nội dung mail phải có link trực tiếp tới bản ghi:
    - Dùng dạng URL `/web#id=<id>&model=ot.request&view_type=form`.
  - Dùng mail template và gửi trực tiếp, không log vào chatter/comment.

### 6) Pop-up nhập lý do từ chối

- Tạo wizard `ot.request.reject.wizard`:
  - Field bắt buộc: `reason`.
  - Nút xác nhận:
    - Cập nhật `state = rejected`.
    - Lưu `reject_reason`.
    - Gửi mail kèm lý do.

### 7) List view, search view, filter, group by

- List view:
  - Trang trí màu khi `total_ot_hours > 8`.
  - Thêm nút tạo dữ liệu ngẫu nhiên `ot.request` + `ot.request.line` rỗng.
- Search view:
  - Filter theo trạng thái: chờ PM, chờ DL, approved, rejected.
  - Filter theo project, department, employee, khoảng ngày OT.
  - Group by: project, department, PM, DL, trạng thái, tháng OT.

### 8) Migration dữ liệu

- Tạo script migration để:
  - Thêm field `employee_display_name`.
  - Backfill dữ liệu cũ theo format: `<Employee Name> - <Department Name>`.
- Đảm bảo migration idempotent (chạy lại không lỗi, không duplicate dữ liệu).

### 9) Logging lịch sử thay đổi

- Theo dõi và lưu lịch sử cho:
  - `state`
  - `total_ot_hours`
  - `pm_id`
  - `dl_id`
- Có thể dùng:
  - `tracking=True` trên field quan trọng, hoặc
  - model lịch sử riêng `ot.request.history` nếu cần audit chi tiết.

### 10) Tiêu chí nghiệm thu (Acceptance Criteria)

- Nhân viên không submit được OT quá hạn 2 ngày.
- PM/DL nhận mail đúng luồng, đúng đối tượng, có CC nhân viên.
- Reject bắt buộc nhập lý do và lý do xuất hiện trong mail.
- Approved/Rejected mail có link mở đúng record.
- List view đổi màu đúng khi OT > 8h.
- Filter/Group by hoạt động theo yêu cầu.
- Lịch sử thay đổi trạng thái/giờ/PM/DL được lưu đầy đủ.
- Mail không xuất hiện ở phần comment/chatter.

