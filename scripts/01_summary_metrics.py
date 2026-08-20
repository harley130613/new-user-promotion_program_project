"""
New-Customer Promotion Program — BUTL, phân tích & thiết kế lại (dữ liệu THẬT).

QUAN TRỌNG — nguồn dữ liệu: khác với 2 project "Paid Ads MMP" và "BI Dashboard &
Demand Forecasting" (có file dữ liệu thô .csv/.pkl để build lại pipeline dòng
lệnh/dòng dữ liệu), project này chỉ có **số liệu tổng hợp (KPI cấp chương
trình)** lấy từ báo cáo nội bộ "Phân tích hiệu quả Promotion New User 100K"
tại BUTL — không có bảng dữ liệu từng voucher/từng user để xử lý lại bằng
pandas. Script này KHÔNG "tính lại từ dữ liệu thô" — nó lấy các KPI đã được
xác nhận từ báo cáo (biến `OLD_PROGRAM`, `NEW_PROGRAM` dưới đây) làm input, và
tính các chỉ số SO SÁNH/PHÁI SINH (delta, drop-off funnel) một cách minh bạch,
có công thức rõ ràng — để tránh nhầm giữa "số đo được" và "số tính được".

Không có số VNĐ tuyệt đối nào trong phạm vi này (ROI là tỷ lệ, Activation/
Retention là %) nên không cần bước ẩn danh hóa.
"""
import json

OUT = "/home/claude/promotion_program_project/output"

# ---------- Nguồn: báo cáo "Phân tích hiệu quả Promotion New User 100K" (nội bộ BUTL) ----------
OLD_PROGRAM = {
    "name": "Promotion New User 100K (chương trình cũ)",
    "period": "2025-06-01 to 2025-12-31",
    "users": 30680,
    "return_trip2_rate_pct": 20.45,   # % user quay lại chuyến 2
    "return_trip3_rate_pct": 7.43,    # % user quay lại chuyến 3
    "roi_pct": 7.14,
    "voucher_design": "1 voucher, không giới hạn thời hạn sử dụng",
}

CONTEXT_2025 = {
    "single_trip_month_share_pct": 73.0,   # 73% khách chỉ đi 1 chuyến/tháng
    "retention_mom_start_pct": 56.0,       # đầu kỳ ~56%
    "retention_mom_end_pct": 42.0,         # cuối kỳ 42%
}

NEW_PROGRAM = {
    "name": "Voucher chuỗi 5 chuyến (chương trình thiết kế lại)",
    "period": "2026-07-01 to present",
    "users": 35541,
    "activation_rate_pct": 24.0,
    "retention_r30_pct": 15.5,
    "improvement_vs_baseline_pct_points": 8.4,
    "voucher_design": "chuỗi 5 chuyến, giá trị & hạn dùng giảm dần theo mốc + nhắc tự động (ngày 7, 14, trước hạn 3 ngày)",
    "rollout": "2 giai đoạn: pilot rồi mở rộng dần quy mô, theo dõi qua dashboard cohort",
}

# ---------- Derived: funnel drop-off của chương trình cũ (trip1 -> trip2 -> trip3) ----------
old_funnel = [
    {"step": "Chuyến 1 (mọi user mới)", "rate_pct": 100.0},
    {"step": "Chuyến 2", "rate_pct": OLD_PROGRAM["return_trip2_rate_pct"]},
    {"step": "Chuyến 3", "rate_pct": OLD_PROGRAM["return_trip3_rate_pct"]},
]
drop_1_to_2 = round(100 - OLD_PROGRAM["return_trip2_rate_pct"], 2)
drop_2_to_3 = round(OLD_PROGRAM["return_trip2_rate_pct"] - OLD_PROGRAM["return_trip3_rate_pct"], 2)

print("=" * 70)
print(f"CHƯƠNG TRÌNH CŨ — {OLD_PROGRAM['name']} ({OLD_PROGRAM['period']})")
print(f"  {OLD_PROGRAM['users']:,} user | ROI {OLD_PROGRAM['roi_pct']}%")
print(f"  Funnel: Chuyến 1 (100%) -> Chuyến 2 ({OLD_PROGRAM['return_trip2_rate_pct']}%) "
      f"-> Chuyến 3 ({OLD_PROGRAM['return_trip3_rate_pct']}%)")
print(f"  Drop-off 1->2: {drop_1_to_2}đpt | Drop-off 2->3: {drop_2_to_3}đpt")
print(f"  Thiết kế voucher: {OLD_PROGRAM['voucher_design']}")
print(f"  => Giả thuyết nguyên nhân: không có mốc thời hạn -> thiếu động lực quay lại SỚM "
      f"(user có thể trì hoãn vô thời hạn, dẫn tới drop-off lớn nhất ngay ở bước 1->2)")

print(f"\nBỐI CẢNH 2025: {CONTEXT_2025['single_trip_month_share_pct']}% khách chỉ đi 1 chuyến/tháng; "
      f"retention MoM giảm từ ~{CONTEXT_2025['retention_mom_start_pct']}% xuống "
      f"{CONTEXT_2025['retention_mom_end_pct']}%")

print(f"\nCHƯƠNG TRÌNH MỚI — {NEW_PROGRAM['name']} ({NEW_PROGRAM['period']})")
print(f"  {NEW_PROGRAM['users']:,} user mới | Activation Rate {NEW_PROGRAM['activation_rate_pct']}% | "
      f"Retention R30 {NEW_PROGRAM['retention_r30_pct']}%")
print(f"  Cải thiện: +{NEW_PROGRAM['improvement_vs_baseline_pct_points']}đpt so với baseline")
print(f"  Thiết kế voucher: {NEW_PROGRAM['voucher_design']}")
print(f"  Triển khai: {NEW_PROGRAM['rollout']}")

output = {
    "old_program": OLD_PROGRAM,
    "context_2025": CONTEXT_2025,
    "old_funnel": old_funnel,
    "old_funnel_dropoff": {"trip1_to_trip2_pct_points": drop_1_to_2, "trip2_to_trip3_pct_points": drop_2_to_3},
    "new_program": NEW_PROGRAM,
    "note": "old_program/new_program là KPI tổng hợp lấy từ báo cáo nội bộ BUTL (không phải dữ liệu "
            "dòng lệnh thô); old_funnel_dropoff là chỉ số PHÁI SINH tính từ các KPI đó, công thức nêu "
            "rõ trong script này.",
}
with open(f"{OUT}/summary.json", "w", encoding="utf-8") as f:
    json.dump(output, f, ensure_ascii=False, indent=2)
print("\nSaved output/summary.json")
