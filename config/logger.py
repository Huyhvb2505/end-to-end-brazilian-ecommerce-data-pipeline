import logging
import os
import sys

# Tạo thư mục logs nếu chưa tồn tại
LOG_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "logs"
)
os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE = os.path.join(LOG_DIR, "pipeline.log")


"""initializes a logger for the project.
  write logs to both console and file.
  """
def get_logger(name: str) -> logging.Logger:
  
  logger = logging.getLogger(name)

  # Tránh việc logger bị add handler nhiều lần nếu được gọi nhiều nơi
  if logger.handlers:
    return logger

  logger.setLevel(logging.INFO)

  # Định dạng log chuẩn: [Thời gian] - [Level] - [Tên Component] - [Nội dung]
  formatter = logging.Formatter(
      "%(asctime)s - %(levelname)s - [%(name)s] - %(message)s",
      datefmt="%Y-%m-%d %H:%M:%S",
  )

  # 1. Handler ghi ra file (FileHandler)
  file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
  file_handler.setLevel(logging.INFO)
  file_handler.setFormatter(formatter)

  # 2. Handler hiển thị ra màn hình Terminal (StreamHandler)
  console_handler = logging.StreamHandler(sys.stdout)
  console_handler.setLevel(logging.INFO)
  console_handler.setFormatter(formatter)

  # Gắn handlers vào logger
  logger.addHandler(file_handler)
  logger.addHandler(console_handler)

  return logger