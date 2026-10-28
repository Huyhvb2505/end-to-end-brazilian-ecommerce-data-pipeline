.PHONY: build up down logs restart ps clean

# Build lại toàn bộ Docker image (Airflow, Jupyter)
build:
	docker compose build

# Khởi động tất cả các service ở chế độ nền (detached)
up:
	docker compose up -d

# Dừng và xóa các container
down:
	docker compose down

# Xem nhật ký (logs) của toàn bộ hệ thống
logs:
	docker compose logs -f

# Khởi động lại toàn bộ hệ thống
restart: down up

# Kiểm tra trạng thái các container đang chạy
ps:
	docker compose ps

# Dừng hệ thống và xóa sạch volume dữ liệu (CẨN THẬN: Mất sạch DB và MinIO data)
clean:
	docker compose down -v