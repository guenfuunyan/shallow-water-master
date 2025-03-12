
"""Tập lệnh giải quyết các phương trình nước nông 2D bằng cách sử dụng các phép
tính hữu hạn trong đó các phương trình động lượng được coi là tuyến tính,
nhưng phương trình liên tục được giải quyết ở dạng phi tuyến tính..
Mô hình hỗ trợ bật/tắt các điều kiện khác nhau, nhưng ở dạng hoàn chỉnh nhất,
mô hình giải quyết tập hợp các phương trình sau:

    du/dt - fv = -g*d(eta)/dx + tau_x/(rho_0*H)- kappa*u
    dv/dt + fu = -g*d(eta)/dy + tau_y/(rho_0*H)- kappa*v
    d(eta)/dt + d((eta + H)*u)/dx + d((eta + H)*u)/dy = sigma - w

trong đó f = f_0 + beta*y có thể là tham số coriolis thay đổi theo vĩ độ đầy đủ.
Trong phương trình liên tục, người ta sử dụng một
chênh lệch về phía trước cho đạo hàm thời gian và một sơ đồ ngược gió cho các
điều khoản phi tuyến tính. Mô hình ổn định trong điều kiện CFL của

dt <= min(dx, dy)/sqrt(g*H) và alpha << 1 (nếu sử dụng coriolis)

trong đó dx, dy là khoảng cách lưới theo hướng x và y, g là
gia tốc của trọng lực và H là độ sâu nghỉ của chất lỏng."""

import time
import numpy as np
import matplotlib.pyplot as plt
import viz_tools

# ==================================================================================
# ================================ Các tham số =================================
# ==================================================================================
# --------------- Tham số vật lý ---------------
L_x = 1E+6              # Chiều dài miền theo hướng x
L_y = 1E+6              # Chiều dài miền theo hướng y
g = 9.81                 # Gia tốc trọng trường [m/s^2]
H = 100                # Độ sâu của chất lỏng [m]
f_0 = 1E-4              # Phần cố định của tham số coriolis [1/s]
beta = 2E-11            # Độ dốc của tham số coriolis [1/ms]
rho_0 = 1024.0          # Mật độ chất lỏng [kg/m^3)]
tau_0 = 0.1             # Biên độ ứng suất gió [kg/ms^2]
use_coriolis = True     # True nếu muốn dùng lực coriolis
use_friction = False     # True nếu muốn có ma sát đáy
use_wind = False        # True nếu bạn muốn áp lực gió
use_beta = True         # True nếu muốn có biến thiên coriolis
use_source = False       # True nếu muốn có nguồn khối lượng vào miền
use_sink = False       # True nếu muốn có khối lượng chìm ra khỏi miền
param_string = "\n================================================================"
param_string += "\nuse_coriolis = {}\nuse_beta = {}".format(use_coriolis, use_beta)
param_string += "\nuse_friction = {}\nuse_wind = {}".format(use_friction, use_wind)
param_string += "\nuse_source = {}\nuse_sink = {}".format(use_source, use_sink)
param_string += "\ng = {:g}\nH = {:g}".format(g, H)

# --------------- Tham số tính toán ---------------
N_x = 150                            # Số điểm lưới theo hướng x
N_y = 150                            # Số điểm lưới theo hướng y
dx = L_x/(N_x - 1)                   # Khoảng cách lưới theo hướng x
dy = L_y/(N_y - 1)                   # Khoảng cách lưới theo hướng y
dt = 0.1*min(dx, dy)/np.sqrt(g*H)    # Bước thời gian (được xác định từ điều kiện CFL)
time_step = 1                        # Để đếm các bước vòng lặp thời gian
max_time_step = 5000                 # Tổng số bước thời gian trong mô phỏng
x = np.linspace(-L_x/2, L_x/2, N_x)  # Mảng có điểm x
y = np.linspace(-L_y/2, L_y/2, N_y)  # Mảng có điểm y
X, Y = np.meshgrid(x, y)             # Lưới để vẽ đồ thị
X = np.transpose(X)                  # Để có được các biểu đồ đúng
Y = np.transpose(Y)                  # Để có được các biểu đồ đúng
param_string += "\ndx = {:.2f} km\ndy = {:.2f} km\ndt = {:.2f} s".format(dx, dy, dt)

# Xác định mảng ma sát đáy nếu ma sát đáy được bật.
if (use_friction is True):
    kappa_0 = 1/(5*24*3600)
    kappa = np.ones((N_x, N_y))*kappa_0
    #kappa[0, :] = kappa_0
    #kappa[-1, :] = kappa_0
    #kappa[:, 0] = kappa_0
    #kappa[:, -1] = kappa_0
    #kappa[:int(N_x/15), :] = 0
    #kappa[int(14*N_x/15)+1:, :] = 0
    #kappa[:, :int(N_y/15)] = 0
    #kappa[:, int(14*N_y/15)+1:] = 0
    #kappa[int(N_x/15):int(2*N_x/15), int(N_y/15):int(14*N_y/15)+1] = 0
    #kappa[int(N_x/15):int(14*N_x/15)+1, int(N_y/15):int(2*N_y/15)] = 0
    #kappa[int(13*N_x/15)+1:int(14*N_x/15)+1, int(N_y/15):int(14*N_y/15)+1] = 0
    #kappa[int(N_x/15):int(14*N_x/15)+1, int(13*N_y/15)+1:int(14*N_y/15)+1] = 0
    param_string += "\nkappa = {:g}\nkappa/beta = {:g} km".format(kappa_0, kappa_0/(beta*1000))

# Xác định mảng ứng suất gió nếu gió được bật.
if (use_wind is True):
    tau_x = -tau_0*np.cos(np.pi*y/L_y)*0
    tau_y = np.zeros((1, len(x)))
    param_string += "\ntau_0 = {:g}\nrho_0 = {:g} km".format(tau_0, rho_0)

# Xác định mảng Coriolis nếu Coriolis được bật.
if (use_coriolis is True):
    if (use_beta is True):
        f = f_0 + beta*y        # Tham số coriolis thay đổi
        L_R = np.sqrt(g*H)/f_0  # Bán kính biến dạng Rossby
        c_R = beta*g*H/f_0**2   # Tốc độ sóng Rossby dài
    else:
        f = f_0*np.ones(len(y))                 # Tham số Coriolis không đổi

    alpha = dt*f                # Tham số cần thiết cho sơ đồ Coriolis
    beta_c = alpha**2/4         # Tham số cần thiết cho sơ đồ Coriolis

    param_string += "\nf_0 = {:g}".format(f_0)
    param_string += "\nMax alpha = {:g}\n".format(alpha.max())
    param_string += "\nRossby radius: {:.1f} km".format(L_R/1000)
    param_string += "\nRossby number: {:g}".format(np.sqrt(g*H)/(f_0*L_x))
    param_string += "\nLong Rossby wave speed: {:.3f} m/s".format(c_R)
    param_string += "\nLong Rossby transit time: {:.2f} days".format(L_x/(c_R*24*3600))
    param_string += "\n================================================================\n"

# Xác định mảng nguồn nếu nguồn được bật.
if (use_source):
    sigma = np.zeros((N_x, N_y))
    sigma = 0.0001*np.exp(-((X-L_x/2)**2/(2*(1E+5)**2) + (Y-L_y/2)**2/(2*(1E+5)**2)))
    
# Xác định mảng nguồn nếu nguồn được bật.
if (use_sink is True):
    w = np.ones((N_x, N_y))*sigma.sum()/(N_x*N_y)

# Ghi tất cả các tham số vào tệp.
with open("param_output.txt", "w") as output_file:
    output_file.write(param_string)

print(param_string)     # in các tham số ra màn hình
# ============================= Đã hoàn tất việc thêm tham số ===============================

# ==================================================================================
# ==================== Phân bổ mảng và điều kiện ban đầu ====================
# ==================================================================================
u_n = np.zeros((N_x, N_y))      # Giữ u ở bước thời gian hiện tại
u_np1 = np.zeros((N_x, N_y))    # Giữ u ở bước thời gian tiếp theo
v_n = np.zeros((N_x, N_y))      # Giữ v ở bước thời gian hiện tại
v_np1 = np.zeros((N_x, N_y))    # Giữ v ở bước thời gian tiếp theo
eta_n = np.zeros((N_x, N_y))    # Giữ eta tại bước thời gian hiện tại
eta_np1 = np.zeros((N_x, N_y))  # Giữ eta tại bước thời gian tiếp theo

# Biến tạm thời (mỗi bước thời gian) cho sơ đồ ngược gió trong phương trình eta
h_e = np.zeros((N_x, N_y))
h_w = np.zeros((N_x, N_y))
h_n = np.zeros((N_x, N_y))
h_s = np.zeros((N_x, N_y))
uhwe = np.zeros((N_x, N_y))
vhns = np.zeros((N_x, N_y))

# Điều kiện ban đầu cho u và v.
u_n[:, :] = 0.0             # Điều kiện ban đầu cho u.
v_n[:, :] = 0.0             # Điều kiện ban đầu cho v.
u_n[-1, :] = 0.0            # Đảm bảo u ban đầu thỏa mãn BC
v_n[:, -1] = 0.0            # Đảm bảo v ban đầu thỏa mãn BC

# Điều kiện ban đầu cho eta.
#eta_n[:, :] = np.sin(4*np.pi*X/L_y) + np.sin(4*np.pi*Y/L_y)
#eta_n = np.exp(-((X-0)**2/(2*(L_R)**2) + (Y-0)**2/(2*(L_R)**2)))
eta_n = np.exp(-((X-L_x/2.7)**2/(2*(0.05E+6)**2) + (Y-L_y/4)**2/(2*(0.05E+6)**2)))
eta_n += np.exp(-((X+L_x/2.7)**2/(2*(0.05E+6)**2) + (Y+L_y/4)**2/(2*(0.05E+6)**2)))
#eta_n[int(3*N_x/8):int(5*N_x/8),int(3*N_y/8):int(5*N_y/8)] = 1.0
#eta_n[int(6*N_x/8):int(7*N_x/8),int(6*N_y/8):int(7*N_y/8)] = 1.0
#eta_n[int(3*N_x/8):int(5*N_x/8), int(13*N_y/14):] = 1.0
#eta_n[:, :] = 0.0

#viz_tools.surface_plot3D(X, Y, eta_n, (X.min(), X.max()), (Y.min(), Y.max()), (eta_n.min(), eta_n.max()))

# Biến mẫu.
eta_list = list(); u_list = list(); v_list = list()         # Danh sách chứa eta và u,v cho video
hm_sample = list(); ts_sample = list(); t_sample = list()   # Danh sách cho Hovmuller và chuỗi thời gian
hm_sample.append(eta_n[:, int(N_y/2)])                      # Mẫu eta ban đầu ở giữa miền
ts_sample.append(eta_n[int(N_x/2), int(N_y/2)])             # Mẫu eta ban đầu ở trung tâm của miền
t_sample.append(0.0)                                        # Thêm thời gian ban đầu vào mẫu t-samples
anim_interval = 20                                         # Tần suất lấy mẫu cho chuỗi thời gian
sample_interval = 1000                                      # Tần suất lấy mẫu cho chuỗi thời gian
# =============== Hoàn tất việc thiết lập mảng và điều kiện ban đầu ===============

t_0 = time.perf_counter()  # Tính thời gian cho vòng lặp tính toán

# ==================================================================================
# ========================= Vòng lặp thời gian chính cho mô phỏng ==================
# ==================================================================================
while (time_step < max_time_step):
    # ------------ Tính toán giá trị cho u và v tại bước thời gian tiếp theo --------------
    u_np1[:-1, :] = u_n[:-1, :] - g*dt/dx*(eta_n[1:, :] - eta_n[:-1, :])
    v_np1[:, :-1] = v_n[:, :-1] - g*dt/dy*(eta_n[:, 1:] - eta_n[:, :-1])

    # Thêm ma sát nếu được bật.
    if (use_friction is True):
        u_np1[:-1, :] -= dt*kappa[:-1, :]*u_n[:-1, :]
        v_np1[:-1, :] -= dt*kappa[:-1, :]*v_n[:-1, :]

    # Thêm áp lực gió nếu được bật.
    if (use_wind is True):
        u_np1[:-1, :] += dt*tau_x[:]/(rho_0*H)
        v_np1[:-1, :] += dt*tau_y[:]/(rho_0*H)

    # Sử dụng phương pháp hiệu chỉnh để thêm Coriolis nếu phương pháp này được bật.
    if (use_coriolis is True):
        u_np1[:, :] = (u_np1[:, :] - beta_c*u_n[:, :] + alpha*v_n[:, :])/(1 + beta_c)
        v_np1[:, :] = (v_np1[:, :] - beta_c*v_n[:, :] - alpha*u_n[:, :])/(1 + beta_c)
    
    v_np1[:, -1] = 0.0      # Điều kiện ranh giới phía bắc
    u_np1[-1, :] = 0.0      # Điều kiện ranh giới phía nam
    # -------------------------- xử lý xong u và v -----------------------------

    # --- Tính toán các mảng cần thiết cho sơ đồ ngược gió trong phương trình eta.----
    h_e[:-1, :] = np.where(u_np1[:-1, :] > 0, eta_n[:-1, :] + H, eta_n[1:, :] + H)
    h_e[-1, :] = eta_n[-1, :] + H

    h_w[0, :] = eta_n[0, :] + H
    h_w[1:, :] = np.where(u_np1[:-1, :] > 0, eta_n[:-1, :] + H, eta_n[1:, :] + H)

    h_n[:, :-1] = np.where(v_np1[:, :-1] > 0, eta_n[:, :-1] + H, eta_n[:, 1:] + H)
    h_n[:, -1] = eta_n[:, -1] + H

    h_s[:, 0] = eta_n[:, 0] + H
    h_s[:, 1:] = np.where(v_np1[:, :-1] > 0, eta_n[:, :-1] + H, eta_n[:, 1:] + H)

    uhwe[0, :] = u_np1[0, :]*h_e[0, :]
    uhwe[1:, :] = u_np1[1:, :]*h_e[1:, :] - u_np1[:-1, :]*h_w[1:, :]

    vhns[:, 0] = v_np1[:, 0]*h_n[:, 0]
    vhns[:, 1:] = v_np1[:, 1:]*h_n[:, 1:] - v_np1[:, :-1]*h_s[:, 1:]
    # ------------------------- tính toán xong sơ đồ ngược gió -------------------------

    # ----------------- Tính toán giá trị eta tại bước thời gian tiếp theo -------------------
    eta_np1[:, :] = eta_n[:, :] - dt*(uhwe[:, :]/dx + vhns[:, :]/dy)   

    if (use_source is True):
        eta_np1[:, :] += dt*sigma

    if (use_sink is True):
        eta_np1[:, :] -= dt*w
    # ----------------------------- tính toán xong etaeta --------------------------------

    u_n = np.copy(u_np1)        # cập nhật u cho lần xử lý tiếp theo
    v_n = np.copy(v_np1)        # cập nhật v cho lần xử lý tiếp theo
    eta_n = np.copy(eta_np1)    # cập nhật etaeta cho lần xử lý tiếp theo

    time_step += 1

    # Các mẫu cho sơ đồ Hovmuller và quang phổ ở mỗi bước thời gian sample_interval.
    if (time_step % sample_interval == 0):
        hm_sample.append(eta_n[:, int(N_y/2)])              # Sample middle of domain for Hovmuller
        ts_sample.append(eta_n[int(N_x/2), int(N_y/2)])     # Sample center point for spectrum
        t_sample.append(time_step*dt)                       # Keep track of sample times.

    # Lưu trữ eta và (u, v) sau mỗi bước thời gian anin_interval cho hoạt ảnh.
    if (time_step % anim_interval == 0):
        print("Time: \t{:.2f} hours".format(time_step*dt/3600))
        print("Step: \t{} / {}".format(time_step, max_time_step))
        print("Mass: \t{}\n".format(np.sum(eta_n)))
        u_list.append(u_n)
        v_list.append(v_n)
        eta_list.append(eta_n)

# ============================= hoàn thành vòng lặp chínhchính ================================
print("Main computation loop done!\nExecution time: {:.2f} s".format(time.perf_counter() - t_0))
print("\nVisualizing results...")

# ==================================================================================
# ================== Hiển thị kết quả bằng cách gọi đến tệp bên ngoài ==================
# ==================================================================================
#viz_tools.pmesh_plot(X, Y, eta_n, "Final state of surface elevation $\eta$")
#viz_tools.quiver_plot(X, Y, u_n, v_n, "Final state of velocity field $\mathbf{u}(x,y)$")
#viz_tools.hovmuller_plot(x, t_sample, hm_sample)
#viz_tools.plot_time_series_and_ft(t_sample, ts_sample)
eta_anim = viz_tools.eta_animation(X, Y, eta_list, anim_interval*dt, "eta")
eta_surf_anim = viz_tools.eta_animation3D(X, Y, eta_list, anim_interval*dt, "eta_surface")
quiv_anim = viz_tools.velocity_animation(X, Y, u_list, v_list, anim_interval*dt, "velocity")
# ============================ Hoàn tất hiển thị kết quả =============================

print("\nVisualization done!")
plt.show()
