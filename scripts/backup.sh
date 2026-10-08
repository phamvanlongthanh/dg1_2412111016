#!/bin/bash

if [ $# -ne 1 ]; then
    echo "Lỗi: Vui lòng cung cấp đường dẫn thư mục cần sao lưu!"
    echo "Cú pháp: $0 <thư_mục_cần_sao_lưu>"
    exit 1
fi

TARGET_DIR="$1"

if [ ! -d "$TARGET_DIR" ]; then
    echo "Lỗi: Thư mục '$TARGET_DIR' không tồn tại!"
    exit 2
fi

BACKUP_DIR="$HOME/backup"
mkdir -p "$BACKUP_DIR"

DIR_NAME=$(basename "$TARGET_DIR")
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_FILE="${BACKUP_DIR}/${DIR_NAME}_${TIMESTAMP}.tar.gz"

tar -czf "$BACKUP_FILE" -C "$(dirname "$TARGET_DIR")" "$DIR_NAME" 2>/dev/null

if [ $? -eq 0 ]; then
    echo "Sao lưu thành công: $BACKUP_FILE"
    
    SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)
    LOG_FILE="${SCRIPT_DIR}/../logs/backup.log"
    
    LOG_TIME=$(date +"%Y-%m-%d %H:%M:%S")
    echo "[$LOG_TIME] Backup created: $BACKUP_FILE" >> "$LOG_FILE"
else
    echo "Lỗi: Quá trình nén thư mục thất bại!"
    exit 3
fi

exit 0
