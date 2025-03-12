--- Các tài nguyên, phần mềm cần dùng để chạy chương trình ---


# Visual Studio Code: VS Code là một trong những trình soạn thảo mã nguồn rất phổ biến được các lập trình viên sử dụng. Với các ưu điểm nổi bật là sự nhanh chóng, nhẹ, hỗ trợ đa nền tảng cùng nhiều tính năng và là mã nguồn mở chính. Visual Studio Code ngày càng được ưa chuộng sử dụng, là lựa chọn hàng đầu của các lập trình viên.

!!!Link Tải: https://code.visualstudio.com/ 
Chạy phần mềm và nhấn Finish.
(Version: 1.96.2)


# Python: Python là một ngôn ngữ lập trình bậc cao, mã nguồn mở và đa nền tảng. Python được sử dụng rộng rãi để phát triển các ứng dụng web, phát triển phần mềm, khoa học dữ liệu và máy học (ML).Python được Guido van Rossum giới thiệu vào năm 1991 và đã trải qua 3 giai đoạn phát triển khác nhau tương ứng với các version, mới nhất hiện nay là Python version 3x (3.12.3 vào 9 tháng 4 2024). Python có cú pháp rõ ràng và ngắn gọn, giúp cho việc học và sử dụng ngôn ngữ này trở nên dễ dàng.
 
!!!Link Tải: https://www.python.org/downloads/
Chạy file .exe rồi nhấn "add to PATH" và Finish.
(Version: 3.13.1)


# Numpy(Numeric Python): là một thư viện toán học phổ biến và mạnh mẽ của Python. Cho phép làm việc hiệu quả với ma trận và mảng, đặc biệt là dữ liệu ma trận và mảng lớn với tốc độ xử lý nhanh hơn nhiều lần khi chỉ sử dụng “core Python” đơn thuần.

!!!Sau khi đã cài đặt Ngôn Ngữ Python cho máy, vào Command Prompt (CMD) rồi ghi lệnh " pip install numpy " để tải thư viện. Check version: " pip show numpy "
(Version: 2.2.1)
******* 	Description: bundled in OpenBLAS
 		Availability: https://github.com/OpenMathLib/OpenBLAS/
 		License: BSD-3-Clause-Attribution
   		Copyright (c) 1992-2013 The University of Tennessee and The University
                           of Tennessee Research Foundation.  All rights
                           reserved.
   		Copyright (c) 2000-2013 The University of California Berkeley. All
                           rights reserved.
   		Copyright (c) 2006-2013 The University of Colorado Denver.  All rights
                           reserved.                                            		******


# Mathplolib: Để thực hiện các suy luận thống kê cần thiết, cần phải trực quan hóa dữ liệu của bạn và Matplotlib là một trong những giải pháp như vậy cho người dùng Python. Nó là một thư viện vẽ đồ thị rất mạnh mẽ hữu ích cho những người làm việc với Python và NumPy. Module được sử dụng nhiều nhất của Matplotib là Pyplot cung cấp giao diện như MATLAB nhưng thay vào đó, nó sử dụng Python và nó là nguồn mở.

!!!Để cài đặt Matplotlib, vào CMD rồi gõ lệnh " -m pip install -U pip " và tiếp tục gõ lệnh " m pip install -U matplotlib "

(Version: Version: 3.10.0)
*******		Summary: Python plotting package
		Home-page: https://matplotlib.org
		Author: John D. Hunter, Michael Droettboom
		Author-email: Unknown <matplotlib-users@python.org>
		License: License agreement for matplotlib versions 1.3.0 and later		*******

#FFmpeg: FFmpeg là một dự án phần mềm miễn phí bao gồm một bộ phần mềm khổng lồ gồm các thư viện và chương trình để xử lý video, audio, multimedia files và streams. Cốt lõi của nó là chính chương trình FFmpeg, được thiết kế để xử lý các video và audio dựa trên command line và được sử dụng rộng rãi để chuyển đổi định dạng, chỉnh sửa cơ bản (cắt và ghép), chia tỷ lệ video, hiệu ứng hậu kỳ video. FFmpeg được xuất bản theo Giấy phép GNU Lesser General Public License 2.1+ hay GNU General Public License 2+ (dựa theo option nào được enabled).

!!!Link Tải: https://github.com/BtbN/FFmpeg-Builds/releases rồi tải tải file zip: "ffmpeg-master-latest-win64-gpl.zip". Extract rồi add file Bin và add vào PATH của Environment Variables
(Version: 7.1)

--- Cách sử dụng chương trình ---
#Tệp "fourier_transform.py" lưu giữ hàm để tính toán biến đổi Fourier của <signal> bao gồm <N> điểm dữ liệu và thời gian lấy mẫu trên <T>.


#Tệp "viz_tools.py" có một số hàm trực quan hóa dự định sử dụng với kết quả từ mô hình nước nông 2D swe2D.py
tệp bao gồm: 
	+ eta_animation "Hàm tạo hoạt ảnh của eta."
	+ velocity_animation "Hàm lấy miền x, y (lưới lưới 2D) và danh sách các mảng 2D u_list, v_list và tạo hoạt ảnh rung của trường vận tốc (u, v). Để có tiêu đề cập nhật, người ta cũng cần chỉ định bước thời gian dt giữa mỗi khung hình trong mô phỏng, số bước thời gian giữa mỗi eta trong eta_list và cuối cùng là tên tệp cho video."


#Tệp swe.py bao gồm tập lệnh giải quyết các phương trình nước nông 2D .


*****Chạy chương trình*****
Để chạy được chương trình phải thông qua các bước sau:
+ Bước 1: Kiểm tra môi trường của Python.
	Các thư viện bắt buộc phải có bao gồm:"numpy, matplotlib, ffmpeg" (hướng dẫn tải ở trên). Nếu dùng Visual Studio Code thì có thể cài đặt "Python Extension Pack" trong mục Extensions.

+ Bước 2: Thiết lập tham số mô phỏng:
	Mở tệp swe.py và chỉnh sửa các tham số mô phỏng theo nhu cầu của bài toán bao gồm:
	*Các tham số vật lý và các lực hoặc hiệu ứng ở mục ---Các tham số--- (Lưu ý nếu có sử dụng lực ma sát đáy thì hãy thay đổi giá trị của //kappa// cho phù hợp với bài toán. Trong bài đã có một số trường hợp mẫu của //kappa//).
	*Khởi tạo sóng ban đầu bằng //eta_n// (Ex: eta_n = np.exp(-((X-L_x/2.7)**2/(2*(0.05E+6)**2) + (Y-L_y/4)**2/(2*(0.05E+6)**2))) ).
+ Bước 3: Chạy mô phỏng
	* Chạy tệp swe.py và chờ đợt kết quả.
	* Trong quá trình chạy chương trình sẽ hiển thị thông tin thời gian và khối lượng của bài toán:
	Ex:
		Time:   2.00 hours
		Step:   20 / 5000
		Mass:   12345.678
+ Bước 4: Hiển thị và lưu kết quả:
Sau khi vòng lặp mô phỏng kết thúc, chương trình sẽ tự động tạo các đồ thị và hoạt ảnh. Dưới đây là một số cách hiển thị kết quả:
	a. Hoạt ảnh 2D: Kết quả được tạo bằng hàm eta_animation và lưu vào tệp .mp4.
		Tệp video eta.mp4 sẽ hiển thị sự lan truyền của sóng theo thời gian.
	b. Hoạt ảnh 3D: Kết quả được tạo bằng hàm eta_animation3D để tạo hoạt ảnh bề mặt 3D:
		Tệp video eta_surface.mp4 sẽ hiển thị bề mặt nước 3D.
+ Bước 5: Điều chỉnh tham số nếu cần
Nếu muốn thay đổi thời gian mô phỏng hoặc độ phân giải, sửa các tham số:
	max_time_step = 5000  # Tổng số bước thời gian
	dt = 0.1 * min(dx, dy) / np.sqrt(g * H)  # Bước thời gian.