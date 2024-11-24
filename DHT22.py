import smbus2
import time

# Địa chỉ I2C của BME280 (thường là 0x76 hoặc 0x77)
BME280_ADDRESS = 0x76

# Đăng ký cần thiết cho BME280
REG_ID = 0xD0
REG_CTRL_HUM = 0xF2
REG_CTRL_MEAS = 0xF4
REG_CONFIG = 0xF5
REG_PRESS_MSB = 0xF7

# Hàm đọc dữ liệu từ cảm biến
def read_bme280_data(bus):
    # Kiểm tra ID cảm biến (nên trả về 0x60 nếu là BME280)
    chip_id = bus.read_byte_data(BME280_ADDRESS, REG_ID)
    if chip_id != 0x60:
        raise Exception("Không tìm thấy cảm biến BME280!")

    # Cấu hình cảm biến
    # Đặt oversampling cho độ ẩm
    bus.write_byte_data(BME280_ADDRESS, REG_CTRL_HUM, 0x01)
    # Đặt oversampling cho nhiệt độ và áp suất, chế độ Normal Mode
    bus.write_byte_data(BME280_ADDRESS, REG_CTRL_MEAS, 0x27)
    # Cấu hình chế độ chờ và bộ lọc
    bus.write_byte_data(BME280_ADDRESS, REG_CONFIG, 0xA0)

    time.sleep(0.5)  # Chờ cảm biến ổn định

    # Đọc dữ liệu thô từ cảm biến
    data = bus.read_i2c_block_data(BME280_ADDRESS, REG_PRESS_MSB, 8)

    # Tính toán áp suất, nhiệt độ và độ ẩm
    raw_pressure = (data[0] << 12) | (data[1] << 4) | (data[2] >> 4)
    raw_temperature = (data[3] << 12) | (data[4] << 4) | (data[5] >> 4)
    raw_humidity = (data[6] << 8) | data[7]

    # Chuyển đổi dữ liệu thô thành giá trị thực tế
    # Lưu ý: BME280 cần hiệu chỉnh dữ liệu thô bằng cách sử dụng các hằng số hiệu chỉnh
    # Đoạn mã dưới đây chỉ là ví dụ đơn giản (nếu cần chính xác, cần dùng thêm hiệu chỉnh).

    temperature = raw_temperature / 100.0  # Chuyển đổi nhiệt độ
    pressure = raw_pressure / 100.0        # Chuyển đổi áp suất
    humidity = raw_humidity / 1024.0       # Chuyển đổi độ ẩm

    return temperature, pressure, humidity

def main():
    try:
        # Kết nối với I2C
        bus = smbus2.SMBus(1)
        print("Đang đọc dữ liệu từ BME280...")

        while True:
            temperature, pressure, humidity = read_bme280_data(bus)
            print(f"Nhiệt độ: {temperature:.2f} °C")
            print(f"Áp suất: {pressure:.2f} hPa")
            print(f"Độ ẩm: {humidity:.2f} %")
            time.sleep(2)

    except Exception as e:
        print(f"Lỗi: {e}")
    finally:
        bus.close()

if __name__ == "__main__":
    main()
