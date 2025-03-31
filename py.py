import pandas as pd  # Thư viện để xử lý dữ liệu bảng
import matplotlib.pyplot as plt  # Thư viện để vẽ biểu đồ

# 1. Đọc dữ liệu
file_path = "/mnt/data/sample.csv"  # Đường dẫn tới file dữ liệu
df = pd.read_csv(file_path)  # Đọc file CSV vào DataFrame

# 2. Hiển thị thông tin tổng quan
df_info = df.info()  # Hiển thị thông tin về kiểu dữ liệu và giá trị null
df_head = df.head(10)  # Hiển thị 10 dòng đầu tiên
df_describe = df.describe(include="all")  # Thống kê dữ liệu (cả số và chữ)
print(df_info)  # In thông tin của DataFrame
print(df_head)  # In 10 dòng đầu
print(df_describe)  # In mô tả thống kê của DataFrame

# 3. Xử lý dữ liệu bị thiếu
df.loc[:, 'dispatching_base_num'] = df['dispatching_base_num'].fillna(df['dispatching_base_num'].mode()[0])  # Điền giá trị thiếu bằng giá trị phổ biến nhất

# 4. Chuyển đổi cột thời gian
df['pickup_datetime'] = pd.to_datetime(df['pickup_datetime'], format='%m/%d/%Y %I:%M:%S %p')  # Chuyển đổi cột thời gian nhận khách sang dạng datetime
df['dropoff_datetime'] = pd.to_datetime(df['dropoff_datetime'], format='%m/%d/%Y %I:%M:%S %p')  # Chuyển đổi cột thời gian trả khách

# 5. Tính thời gian chuyến đi (phút)
df['duration_min'] = (df['dropoff_datetime'] - df['pickup_datetime']).dt.total_seconds() / 60  # Tính thời gian chuyến đi theo phút

# 6. Lọc dữ liệu bất thường
df = df[(df['duration_min'] >= 2) & (df['duration_min'] <= 1440)]  # Chỉ giữ lại các chuyến đi hợp lý (2 phút - 1 ngày)

# 7. Trích xuất thông tin thời gian
df['hour'] = df['pickup_datetime'].dt.hour  # Trích xuất giờ trong ngày
df['day_of_week'] = df['pickup_datetime'].dt.day_name()  # Trích xuất tên ngày trong tuần
df['month'] = df['pickup_datetime'].dt.month  # Trích xuất tháng

# 8. Tính thời gian trung bình theo tháng
avg_duration_per_month = df.groupby('month')['duration_min'].mean()  # Tính thời gian trung bình của chuyến đi theo tháng
print(avg_duration_per_month)  # In kết quả thời gian trung bình theo tháng

# 9. Vẽ biểu đồ số chuyến đi theo tháng
trip_count_per_month = df['month'].value_counts().sort_index()  # Đếm số chuyến đi theo tháng
plt.figure(figsize=(8, 5))  # Thiết lập kích thước biểu đồ
plt.bar(trip_count_per_month.index, trip_count_per_month.values, color='skyblue')  # Vẽ biểu đồ cột
plt.xlabel("Tháng")  # Nhãn trục x
plt.ylabel("Số chuyến đi")  # Nhãn trục y
plt.title("Số chuyến đi theo tháng")  # Tiêu đề biểu đồ
plt.xticks(trip_count_per_month.index)  # Đặt nhãn cho các cột theo tháng
plt.show()  # Hiển thị biểu đồ