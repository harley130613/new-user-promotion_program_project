# New Customer Promotion Program - BUTL

Dự án đánh giá hiệu quả chương trình ưu đãi dành cho khách hàng mới, xác định nguyên nhân tỷ lệ giữ chân thấp và đề xuất thiết kế chương trình mới dựa trên **số liệu vận hành thực tế tại BUTL**.

> **Lưu ý về nguồn dữ liệu**
>
> Khác với hai dự án khác trong Portfolio là Paid Ads MMP và BI Dashboard & Demand Forecasting, dự án này không có dữ liệu chi tiết theo từng người dùng hoặc từng Voucher.
>
> Nguồn dữ liệu đầu vào là các KPI tổng hợp từ báo cáo nội bộ **"Phân tích hiệu quả Promotion New User 100K"**. Các Script sử dụng những KPI đã được xác nhận để tính thêm các chỉ số phái sinh như Funnel Drop-off và mức chênh lệch trước - sau.
>
> Toàn bộ công thức được trình bày rõ trong Code. Dự án không giả định hoặc mô phỏng dữ liệu chi tiết khi không có Row-level Data.

## Mục lục

- [Bảo mật dữ liệu](#bảo-mật-dữ-liệu)
- [Bài toán](#bài-toán)
- [Đánh giá chương trình cũ](#đánh-giá-chương-trình-cũ)
- [Thiết kế lại chương trình](#thiết-kế-lại-chương-trình)
- [Kết quả](#kết-quả)
- [BI Dashboard](#bi-dashboard)
- [Công nghệ sử dụng](#công-nghệ-sử-dụng)
- [Cấu trúc thư mục](#cấu-trúc-thư-mục)
- [Cách chạy dự án](#cách-chạy-dự-án)

---

## Bảo mật dữ liệu

Dự án không công khai doanh thu, chi phí hoặc giá trị tài chính tuyệt đối của doanh nghiệp.

Các chỉ số được sử dụng gồm:

- Số lượng người dùng
- Activation Rate
- Retention Rate
- Tỷ lệ quay lại
- Funnel Drop-off
- ROI theo tỷ lệ phần trăm

Vì không chứa số liệu tài chính tuyệt đối nên dự án không cần thực hiện bước ẩn danh hóa dữ liệu như hai dự án còn lại trong Portfolio.

---

## Bài toán

Chương trình **Promotion New User 100K** được triển khai từ tháng 06/2025 đến tháng 12/2025 cho **30.680 khách hàng mới**.

Chương trình sử dụng Voucher để thúc đẩy khách hàng hoàn thành chuyến đầu tiên. Tuy nhiên, hiệu quả giữ chân sau ưu đãi còn thấp.

Dự án tập trung trả lời ba câu hỏi:

1. Khách hàng có quay lại sau chuyến đầu tiên không?
2. Khách hàng rời khỏi hành trình nhiều nhất ở giai đoạn nào?
3. Cơ chế Voucher hiện tại có tạo đủ động lực để khách hàng quay lại sớm không?

Mục tiêu không chỉ là tăng số lượt sử dụng Voucher mà còn chuyển đổi khách hàng mới thành người dùng quay lại.

---

## Đánh giá chương trình cũ

### Bối cảnh khách hàng năm 2025

Phân tích hành vi khách hàng cho thấy:

- **73% khách hàng mới chỉ phát sinh một chuyến mỗi tháng.**
- Retention theo tháng giảm từ khoảng **56% xuống 42%** trong năm.
- Phần lớn khách hàng chưa hình thành thói quen sử dụng dịch vụ sau chuyến đầu tiên.

### Hiệu quả chương trình

| Chỉ số | Kết quả |
| --- | ---: |
| Thời gian triển khai | 06/2025 - 12/2025 |
| Số người dùng | 30.680 |
| Quay lại chuyến thứ hai | 20,45% |
| Tiếp tục đến chuyến thứ ba | 7,43% |
| ROI | 7,14% |

### Funnel khách hàng

```text
Chuyến 1
   -> 20,45% quay lại chuyến 2
   -> 7,43% tiếp tục đến chuyến 3
```

Mức giảm lớn nhất xuất hiện giữa chuyến đầu tiên và chuyến thứ hai:

- Drop-off từ chuyến 1 đến chuyến 2: khoảng **79,55 điểm phần trăm**
- Chênh lệch giữa chuyến 2 và chuyến 3: khoảng **13,02 điểm phần trăm**

Kết quả cho thấy điểm nghẽn chính nằm ở giai đoạn thúc đẩy khách hàng quay lại sau lần sử dụng đầu tiên.

### Nguyên nhân giả định

Cơ chế cũ chỉ cung cấp **một Voucher và không giới hạn thời hạn sử dụng**.

Việc không có thời hạn cụ thể có thể khiến khách hàng:

- Không cảm thấy cần sử dụng Voucher sớm
- Trì hoãn quyết định đặt chuyến
- Quên Voucher sau một thời gian
- Không hình thành hành vi sử dụng lặp lại

Từ kết quả trên, dự án xây dựng giả thuyết:

> Thiếu thời hạn sử dụng và cơ chế nhắc nhở làm giảm động lực quay lại trong giai đoạn đầu của vòng đời khách hàng.

Đây là giả thuyết được hình thành từ dữ liệu và cần được kiểm chứng thông qua quá trình triển khai thực tế.

---

## Thiết kế lại chương trình

### 1. Chuyển từ Voucher đơn sang chuỗi Voucher

Chương trình mới sử dụng chuỗi ưu đãi gắn với năm chuyến đầu tiên của khách hàng.

| Mốc hành trình | Cơ chế |
| --- | --- |
| Chuyến 1 | Ưu đãi cao nhất để thúc đẩy Activation |
| Chuyến 2 | Ưu đãi tiếp nối để giảm Drop-off sau chuyến đầu |
| Chuyến 3 | Duy trì động lực quay lại |
| Chuyến 4 | Giảm dần mức hỗ trợ |
| Chuyến 5 | Hoàn thiện chuỗi hành vi sử dụng ban đầu |

Giá trị Voucher và thời hạn sử dụng được điều chỉnh theo từng mốc nhằm:

- Tạo động lực hoàn thành chuyến đầu tiên
- Khuyến khích khách hàng quay lại sớm
- Giảm phụ thuộc vào ưu đãi theo thời gian
- Hình thành hành vi sử dụng lặp lại

### 2. Bổ sung thời hạn sử dụng

Mỗi Voucher có thời hạn rõ ràng, thay cho cơ chế không giới hạn thời gian của chương trình cũ.

Mục tiêu là tạo cảm giác cấp thiết và hạn chế tình trạng khách hàng nhận Voucher nhưng trì hoãn sử dụng.

### 3. Thiết lập thông báo tự động

Khách hàng được nhắc sử dụng Voucher tại các mốc:

- Ngày thứ 7
- Ngày thứ 14
- Ba ngày trước khi Voucher hết hạn

Thông báo được thiết kế theo hành vi và thời gian còn lại của ưu đãi, thay vì gửi đồng loạt cho toàn bộ khách hàng.

### 4. Triển khai theo hai giai đoạn

#### Giai đoạn 1 - Pilot

- Triển khai trên quy mô giới hạn
- Theo dõi Activation Rate
- Theo dõi Voucher Redemption
- Đánh giá tỷ lệ quay lại
- Xác định điểm rơi chuyển đổi

#### Giai đoạn 2 - Mở rộng

- Mở rộng quy mô sau khi xác nhận hiệu quả
- Tiếp tục theo dõi qua Cohort Dashboard
- Điều chỉnh giá trị Voucher và thời hạn sử dụng
- Kiểm soát chi phí theo từng giai đoạn trong Customer Lifecycle

Cách triển khai này giúp hạn chế rủi ro ngân sách và tạo điều kiện điều chỉnh chương trình trước khi áp dụng trên toàn bộ người dùng mới.

---

## Kết quả

### Kết quả chương trình mới

Chương trình mới được theo dõi trên **35.541 người dùng**, với các kết quả chính:

| Chỉ số | Chương trình cũ | Chương trình mới |
| --- | ---: | ---: |
| Số người dùng | 30.680 | 35.541 |
| Chỉ số giữ chân chính | Quay lại chuyến 2: 20,45% | Retention R30: 15,5% |
| Baseline được sử dụng | ROI: 7,14% | Tăng 8,4 điểm phần trăm so với Baseline |
| Activation Rate | Không có dữ liệu đối chiếu | 24% |

### Diễn giải kết quả

- Chương trình mới ghi nhận **Activation Rate đạt 24%**.
- Retention R30 đạt **15,5%**.
- Kết quả Retention R30 cao hơn Baseline **8,4 điểm phần trăm**.
- Cơ chế Voucher theo chuỗi cho phép theo dõi hành vi khách hàng qua nhiều mốc thay vì chỉ tập trung vào chuyến đầu tiên.

> **Lưu ý khi so sánh**
>
> "Tỷ lệ quay lại chuyến thứ hai" của chương trình cũ và "Retention R30" của chương trình mới là hai KPI có định nghĩa và cửa sổ đo lường khác nhau.
>
> Hai chỉ số được trình bày riêng để phản ánh kết quả của từng giai đoạn, không được sử dụng để kết luận chương trình mới cải thiện bao nhiêu lần so với chương trình cũ.

### Hạn chế của phân tích

Dự án sử dụng dữ liệu tổng hợp cấp chương trình nên chưa thể:

- Phân tích Cohort ở cấp từng khách hàng
- Đánh giá hành vi theo tỉnh hoặc khu vực
- So sánh hiệu quả theo từng loại Voucher
- Kiểm soát khác biệt giữa nhóm Test và Control
- Thực hiện kiểm định Statistical Significance
- Xác định quan hệ nhân quả hoàn toàn giữa cơ chế mới và kết quả Retention

Vì vậy, kết quả được sử dụng để đánh giá xu hướng và hỗ trợ quyết định tối ưu chương trình, không được diễn giải như một kết luận nhân quả tuyệt đối.

---

## BI Dashboard

Dashboard được lưu tại:

```text
output/dashboard.html
```

Dashboard được xây dựng bằng **HTML, CSS, SVG và JavaScript thuần**, không phụ thuộc thư viện biểu đồ bên ngoài và có thể mở trực tiếp trên trình duyệt.

### Nội dung Dashboard

- KPI tổng quan
- Funnel của chương trình cũ
- Drop-off giữa các mốc chuyến
- So sánh thiết kế Voucher trước và sau
- Kết quả Activation và Retention
- Insight chính
- Hạn chế của dữ liệu

---

## Công nghệ sử dụng

| Nhóm | Công nghệ và phương pháp |
| --- | --- |
| Xử lý dữ liệu | Python |
| Dashboard | HTML, CSS, SVG, JavaScript |
| Phương pháp phân tích | Funnel Analysis, Before/After Comparison |
| Thiết kế chương trình | Customer Lifecycle, Voucher Sequencing |
| Triển khai | Pilot, đo lường và mở rộng |
| Đánh giá | Activation Rate, Retention Rate, Funnel Drop-off |

### Quy trình dự án

```text
Business Problem
   -> Đánh giá chương trình cũ
   -> Phân tích Funnel Drop-off
   -> Xây dựng giả thuyết
   -> Thiết kế lại cơ chế Voucher
   -> Triển khai Pilot
   -> Theo dõi KPI
   -> Mở rộng chương trình
```

---

## Cấu trúc thư mục

```text
promotion_program_project/
├── scripts/
│   ├── 01_summary_metrics.py
│   └── 02_build_dashboard.py
├── output/
│   ├── summary.json
│   └── dashboard.html
└── README.md
```

### Mô tả các tệp

| Tệp | Nội dung |
| --- | --- |
| `scripts/01_summary_metrics.py` | Đọc KPI tổng hợp và tính Funnel Drop-off |
| `scripts/02_build_dashboard.py` | Xây dựng Dashboard từ dữ liệu tổng hợp |
| `output/summary.json` | KPI đã xác nhận và các chỉ số phái sinh |
| `output/dashboard.html` | BI Dashboard của dự án |

---

## Cách chạy dự án

### 1. Tính KPI và Funnel Drop-off

```bash
python scripts/01_summary_metrics.py
```

Kết quả:

```text
output/summary.json
```

### 2. Xây dựng Dashboard

```bash
python scripts/02_build_dashboard.py
```

Kết quả:

```text
output/dashboard.html
```

---
