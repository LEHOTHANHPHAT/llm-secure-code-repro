# Guiding AI to Fix Its Own Flaws

Sườn đồ án Lập trình an toàn cho 2 người trong 5 tuần. Nhóm tái hiện các phép so sánh chính trên 40 bài SecCodePLT, 2 mô hình và 1 lượt chạy đầy đủ trước. Bài báo ACM DOI 10.1145/3848030 và [repo tác giả](https://github.com/Ziyu-Yao-NLP-Lab/LLM-Safe-Code-Gen) là nguồn đối chiếu.

## Chạy thử

Mở terminal ở thư mục có README này. Yêu cầu Python 3.10 trở lên. Lệnh lập kế hoạch chỉ dùng thư viện chuẩn.

```powershell
python --version
python -m securecode plan --config configs/smoke.json
```

Trên Linux có thể dùng `python3`. Kết quả smoke phải có `generation_pairs: 4` và `generation_and_hint_calls_planned: 12`. Đây là kế hoạch cho hai bài mẫu do nhóm tự viết, với hai model ID giữ chỗ. Lệnh chỉ kiểm tra cấu hình, đọc dữ liệu và hiển thị prompt mẫu. Tích hợp gọi mô hình, CodeQL và tính kết quả là các đầu việc tiếp theo.

## Cấu trúc repo

| Tệp | Trách nhiệm | Người phụ trách |
|---|---|---|
| `securecode/dataset.py`, `data/` | Đọc manifest, giữ ID nguồn và CWE để chấm | A |
| `securecode/prompts.py`, `generation.py` | B0 sinh thường và B1 sinh từ gợi ý | A |
| `securecode/scanner.py` | Quét CodeQL và đọc kết quả SARIF | B |
| `securecode/repair.py` | R1 cảnh báo trực tiếp và R2 cảnh báo có giải thích | B |
| `securecode/evaluation.py` | Tổng hợp cảnh báo và trạng thái theo mẫu | A và B |
| `configs/` | Cấu hình smoke và mẫu cấu hình 40 bài | A và B |
| `docs/experiment.md` | Quy ước ghép dữ liệu và mốc tích hợp | A và B |

Tên `generation.py` trong bảng nằm trong thư mục `securecode/`. Bốn module generation, scanner, repair và evaluation là vị trí để nhóm triển khai.

## Khởi tạo Git

Giải nén ZIP, mở thư mục dự án rồi chạy:

```powershell
git init -b main
git add .
git commit -m "Initialize secure code reproduction scaffold"
```

Tạo một repo trống trên GitHub, rồi thay URL trong lệnh sau bằng URL repo của nhóm.

```powershell
git remote add origin https://github.com/USERNAME/REPO.git
git push -u origin main
```

Sau commit đầu tiên, A làm trên nhánh `feature/generation`, B làm trên nhánh `feature/codeql`. Cả hai dùng chung manifest và review chéo trước khi gộp. Đặt khóa API trong biến môi trường hoặc tệp `.env` cục bộ. Thư mục `runs/` dùng để lưu kết quả chạy và đã được đưa vào `.gitignore`.

## Mốc đầu tiên

1. A lấy một bài SecCodePLT và lưu ID nguồn, xác minh chạy được một mô hình, lưu prompt, phản hồi gốc và code B0.
2. B đối chiếu CodeQL 2.19.1 và bộ truy vấn Python security-extended với repo tác giả. Thử quét một cặp code có lỗi và đã sửa.
3. Ghép hai phần để đưa code B0 của A vào bộ quét của B. Từ cùng code B0, tạo hai bản sửa rồi quét lại.
4. Chuẩn bị `data/seccodeplt_subset.jsonl` theo cấu trúc smoke và chọn 10 bài mỗi CWE. Đổi model ID trong bản sao của `configs/main.example.json` thành ID thật rồi chạy lại lệnh plan. Nếu kiểm tra độ bao phủ khiến nhóm phải đổi CWE, cập nhật cấu hình và ghi lý do trước khi chạy chính.
