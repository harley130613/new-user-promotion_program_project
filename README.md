# New-Customer Promotion Program — BUTL

Đánh giá hiệu quả chương trình khuyến mãi khách hàng mới đang chạy, xác định nguyên nhân giữ chân
khách kém, và thiết kế lại chương trình — dựa trên **số liệu thật** tại BUTL.

> **Về nguồn dữ liệu:** khác với 2 project khác trong portfolio (Paid Ads MMP, BI Dashboard & Demand
> Forecasting) vốn có file dữ liệu thô (`.csv`/`.pkl`) để build lại pipeline dòng dữ liệu, project này
> chỉ có **số liệu tổng hợp cấp chương trình** (KPI) lấy từ báo cáo nội bộ "Phân tích hiệu quả
> Promotion New User 100K" tại BUTL — không có bảng dữ liệu từng voucher/từng user để xử lý lại. Các
> script trong repo lấy KPI đã xác nhận từ báo cáo làm input, và tính các chỉ số **phái sinh** (funnel
> drop-off, so sánh trước/sau) một cách minh bạch — công thức được ghi rõ trong code, không có bước
> nào "tính lại từ dữ liệu thô" giả vờ như có row-level data.

## Bảo mật dữ liệu

Không có số VNĐ tuyệt đối nào trong phạm vi project này — mọi chỉ số đều là **tỷ lệ %** (ROI,
Activation Rate, Retention Rate) hoặc **số lượng user**, không làm lộ doanh thu/chi phí tuyệt đối của
doanh nghiệp, nên không cần bước ẩn danh hóa như 2 project kia.

## Bài toán

Chương trình *Promotion New User 100K* chạy 06/2025–12/2025 (30.680 user) nhằm thu hút khách hàng
mới, nhưng đặt câu hỏi: chương trình có đang **giữ chân** được khách sau lần dùng voucher đầu tiên
không, hay chỉ là một khuyến mãi one-off?

## Đánh giá chương trình cũ

- **Bối cảnh 2025:** 73% khách chỉ đi 1 chuyến/tháng; retention MoM giảm từ ~56% xuống 42% trong năm.
- **Chương trình cũ (30.680 user, 06–12/2025):** chỉ **20,45%** quay lại chuyến 2, **7,43%** đến
  chuyến 3, **ROI 7,14%**.
- **Funnel drop-off:** ~79,6 điểm phần trăm "rơi rụng" ngay giữa chuyến 1 và chuyến 2 — lớn hơn nhiều
  so với drop-off chuyến 2→3 (~13 điểm phần trăm). Voucher cũ là **1 voucher, không giới hạn thời hạn
  sử dụng** — giả thuyết nguyên nhân: không có mốc thời gian nên khách không có động lực quay lại
  *sớm*, dễ trì hoãn vô thời hạn rồi quên luôn.

## Thiết kế lại chương trình

- **Voucher chuỗi 5 chuyến**, giá trị & hạn dùng **giảm dần theo mốc** (tạo áp lực thời gian tăng dần
  qua từng chuyến) kết hợp **nhắc tự động** ở ngày 7, ngày 14, và trước hạn 3 ngày.
- **Triển khai theo 2 giai đoạn:** chạy thử nghiệm (pilot) trước, sau đó mở rộng dần quy mô — theo dõi
  liên tục qua dashboard cohort để điều chỉnh kịp thời trong quá trình mở rộng.

## Kết quả (tính đến hiện tại)

| Chỉ số | Chương trình cũ | Chương trình mới |
|---|---:|---:|
| User | 30.680 | 35.541 |
| Chỉ số giữ chân chính | Quay lại chuyến 2: 20,45% | Retention R30: 15,5% |
| Baseline so sánh | ROI 7,14% | +8,4 điểm % so với baseline |
| Activation Rate | — | 24% |

> Lưu ý: "Quay lại chuyến 2" (chương trình cũ) và "Retention R30" (chương trình mới) là 2 định nghĩa
> KPI khác nhau giữa 2 giai đoạn báo cáo — không phải cùng 1 công thức đo, nên được trình bày tách
> biệt thay vì gộp chung thành "cải thiện X lần" gây hiểu lầm.

## BI Dashboard

`output/dashboard.html` — dashboard HTML + SVG thuần (không phụ thuộc thư viện ngoài): KPI tổng quan,
funnel chương trình cũ, so sánh thiết kế voucher trước/sau, và insight chính.

## Công nghệ sử dụng

Python cho tổng hợp & tính chỉ số phái sinh (funnel drop-off) · HTML/CSS/SVG/JavaScript thuần cho BI
Dashboard · Phương pháp: funnel analysis, so sánh chương trình trước/sau (before/after), thiết kế lại
sản phẩm khuyến mãi dựa trên causal hypothesis từ dữ liệu (thiếu mốc thời hạn → thiếu động lực quay
lại sớm), triển khai theo mô hình pilot-rồi-mở-rộng có đo lường liên tục.

## Cấu trúc thư mục

```
promotion_program_project/
├── scripts/
│   ├── 01_summary_metrics.py   # KPI tổng hợp từ báo cáo nội bộ + tính funnel drop-off
│   └── 02_build_dashboard.py   # dựng output/dashboard.html
├── output/
│   ├── summary.json            # KPI + chỉ số phái sinh
│   └── dashboard.html          # BI Dashboard
└── README.md
```

## Cách chạy lại

```bash
python scripts/01_summary_metrics.py   # in KPI + ghi output/summary.json
python scripts/02_build_dashboard.py   # dựng output/dashboard.html
```

---
*Trần Thị Cẩm Loan — Marketing Data Analyst*
