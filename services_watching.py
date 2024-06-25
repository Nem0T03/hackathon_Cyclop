#file chay code kiem tra cac dich vu moi 
import time
import psutil

# Tạo một tập hợp lưu trữ các dịch vụ đã phát hiện
detected_services = {}
import subprocess

def verify_signature(file_path):
    # Sử dụng subprocess để chạy lệnh signtool
    process = subprocess.Popen(['signtool', 'verify', '/pa', '/v', file_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()  # Nhận kết quả đầu ra và lỗi (nếu có)

    # Kiểm tra kết quả
    if not error:  # Kiểm tra nếu không có lỗi
        return file_path, "Safe" , output.decode('utf-8')
    else:
        return file_path, "Malware", " "

# Tạo danh sách để lưu tên các tệp tin an toàn và malware
safe_files = []
malware_files = []



##################################################################################################

while True:
    # Lấy danh sách các dịch vụ đang chạy
    running_services = {}
    for proc in psutil.process_iter(['name', 'exe']):
        try:
            name = proc.name()
            exe = proc.exe()
            running_services[name] = exe
        except (psutil.AccessDenied, psutil.NoSuchProcess):
            pass

    # Tìm các dịch vụ mới
    new_services = {name: exe for name, exe in running_services.items() if name not in detected_services}

    # Hiển thị thông tin đầy đủ về các dịch vụ mới
    if new_services:
        print("Các dịch vụ mới:")
        for name, exe in new_services.items():
            print("Tên dịch vụ:", name)
            print("Đường dẫn:", exe)
            result = verify_signature(exe)
            print("Cer:" + result[2])
            if result[1] == "Safe":
                safe_files.append((result[0] , result[2]))
            else:
                malware_files.append(result[0])
            #print()
        # Lưu tên các tệp tin vào các tệp văn bản
        with open("safe_files.txt", "w") as f:
            for file_name, file_path, certi in safe_files:
                f.write(file_name + "\n" + certi)

        with open("malware_files.txt", "w") as f:
            for file_name in malware_files:
                f.write(file_name + "\n")
        # Cập nhật tập hợp các dịch vụ đã phát hiện
        detected_services.update(new_services)

    # Chờ 5 phút trước khi tiếp tục quét
    #time.sleep(50)  # 300 giây = 5 phút



