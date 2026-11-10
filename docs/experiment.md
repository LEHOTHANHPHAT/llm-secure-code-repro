# Quy ước thực nghiệm

- B0 nhận đề bài và tên hàm. B1 nhận cùng đề bài cộng gợi ý do mô hình tạo trước khi viết code. Nhãn `target_cwe` chỉ phục vụ đánh giá.
- R1 và R2 xuất phát từ cùng một code B0 có cảnh báo. R1 dùng cảnh báo trực tiếp. R2 dùng phần giải thích do một mô hình giải thích cố định tạo từ code và cảnh báo. Mỗi nhánh sửa một lượt.
- Mỗi mẫu có khóa `task_id, model_id, repeat_id, condition`. Dùng cùng ba trường đầu để ghép B0/B1/R1/R2.
- Lưu prompt, phản hồi gốc, code đã trích, trạng thái cú pháp, SARIF, phiên bản công cụ và cấu hình mô hình. Với R1/R2 lưu thêm tham chiếu về B0 và phản hồi đã gửi.
- Ghi riêng trạng thái không có code, lỗi cú pháp, lỗi quét, quét có cảnh báo và quét không có cảnh báo. Ghi số mẫu trong mỗi mẫu số khi báo cáo TarV-R và AllV-R. Các ca chưa phân tích được cần hiện riêng trong bảng độ bao phủ.
- Đối chiếu công thức, dữ liệu và cách xử lý lỗi với repo tác giả trước khi chạy chính. Ghi commit nguồn và mọi thay đổi. Đối chiếu phép so sánh ở Bảng 4, 5 và 11 của bài báo.
- Kiểm thử chức năng là phần đánh giá bổ sung. Chạy code sinh ra trong môi trường cách ly. Khi làm bộ bài mới, lưu riêng manifest và kết quả với tập chính.

## Ghép pipeline đầu tiên

A bàn giao một tệp Python và khóa mẫu cho B. B bàn giao trạng thái quét cùng đường dẫn SARIF. Nếu có cảnh báo, B chuyển cảnh báo cho hai nhánh sửa và gọi lại bộ gọi mô hình của A. Hai bạn kiểm tra rằng cả hai nhánh cùng tham chiếu đúng bản B0.
