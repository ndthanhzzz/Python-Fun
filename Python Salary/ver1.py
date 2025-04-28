import tkinter as tk
from tkinter import ttk
from datetime import date, timedelta

def tinh_tong_luong():
    try:
        gio_lam = float(gio_lam_entry.get())
        luong_theo_gio = float(luong_theo_gio_entry.get())
        luong_co_ban = float(luong_co_ban_entry.get())
        luong_tro_cap = float(luong_tro_cap_entry.get())

        tong_luong_lam_them = 0
        for frame in tang_ca_frames:
            try:
                gio_tang_ca = float(frame.gio_entry.get())
                ty_le = float(frame.ty_le_entry.get()) / 100
                tong_luong_lam_them += gio_tang_ca * luong_theo_gio * ty_le
            except ValueError:
                pass  # Bỏ qua nếu giá trị nhập không hợp lệ

        tong_tien_luong = (gio_lam * luong_theo_gio) + luong_co_ban + luong_tro_cap + tong_luong_lam_them
        ket_qua_label.config(text=f"Tổng tiền lương: {tong_tien_luong:,.2f} VNĐ")
    except ValueError:
        ket_qua_label.config(text="Vui lòng nhập số hợp lệ cho các trường số.")

def hien_thi_hop_chon_thang():
    def chon_thang():
        thang_chon = thang_var.get()
        nam_chon = nam_var.get()
        hop_chon_thang_window.destroy()
        hien_thi_ky_luong_theo_thang(nam_chon, thang_chon)

    hop_chon_thang_window = tk.Toplevel(root)
    hop_chon_thang_window.title("Chọn tháng và năm")

    # Chọn tháng
    thang_label = ttk.Label(hop_chon_thang_window, text="Chọn tháng:")
    thang_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
    thang_var = tk.StringVar(hop_chon_thang_window)
    thang_combobox = ttk.Combobox(hop_chon_thang_window, textvariable=thang_var,
                               values=list(range(1, 13)), width=5)
    thang_combobox.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
    thang_combobox.set(date.today().month)  # Giá trị mặc định là tháng hiện tại

    # Chọn năm
    nam_label = ttk.Label(hop_chon_thang_window, text="Chọn năm:")
    nam_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
    nam_var = tk.IntVar(hop_chon_thang_window)
    nam_combobox = ttk.Combobox(hop_chon_thang_window, textvariable=nam_var,
                             values=list(range(date.today().year - 5, date.today().year + 6)), width=7)
    nam_combobox.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
    nam_combobox.set(date.today().year)  # Giá trị mặc định là năm hiện tại

    # Nút chọn
    chon_button = ttk.Button(hop_chon_thang_window, text="Xem kỳ lương", command=chon_thang)
    chon_button.grid(row=2, columnspan=2, padx=5, pady=10)

def tinh_so_ngay_cong(ngay_bat_dau, ngay_ket_thuc, so_ngay_thu_bay):
    so_ngay_cong = 0
    current_date = ngay_bat_dau
    while current_date <= ngay_ket_thuc:
        if current_date.weekday() != 6:  # 6 là Chủ Nhật
            so_ngay_cong += 1
        current_date += timedelta(days=1)
    return so_ngay_cong - (so_ngay_cong_thu_bay_mac_dinh(ngay_bat_dau, ngay_ket_thuc) - so_ngay_thu_bay)

def so_ngay_cong_thu_bay_mac_dinh(ngay_bat_dau, ngay_ket_thuc):
    so_ngay_thu_bay = 0
    current_date = ngay_bat_dau
    while current_date <= ngay_ket_thuc:
        if current_date.weekday() == 5:  # 5 là Thứ Bảy
            so_ngay_thu_bay += 1
        current_date += timedelta(days=1)
    return so_ngay_thu_bay

def hien_thi_ky_luong_theo_thang(nam, thang):
    try:
        thang = int(thang)
        nam = int(nam)

        if thang == 1:
            ngay_bat_dau = date(nam - 1, 12, 26)
            ngay_ket_thuc = date(nam, 1, 25)
        else:
            ngay_bat_dau = date(nam, thang - 1, 26)
            ngay_ket_thuc = date(nam, thang, 25)

        thang_bat_dau_str = ngay_bat_dau.strftime("%d/%m/%Y")
        thang_ket_thuc_str = ngay_ket_thuc.strftime("%d/%m/%Y")

        # Tạo cửa sổ nhập số ngày công Thứ Bảy
        def nhap_so_ngay_thu_bay_window(bat_dau, ket_thuc):
            nhap_window = tk.Toplevel(root)
            nhap_window.title("Nhập số ngày Thứ Bảy")

            mac_dinh_label = ttk.Label(nhap_window, text=f"Số Thứ Bảy (mặc định): {so_ngay_cong_thu_bay_mac_dinh(bat_dau, ket_thuc)}")
            mac_dinh_label.pack(padx=10, pady=5)

            so_ngay_label = ttk.Label(nhap_window, text="Số ngày Thứ Bảy làm việc:")
            so_ngay_label.pack(padx=10, pady=5)
            so_ngay_entry = ttk.Entry(nhap_window, width=5)
            so_ngay_entry.pack(padx=10, pady=5)

            def cap_nhat_thong_tin():
                try:
                    so_ngay_thu_bay_nhap = int(so_ngay_entry.get())
                    so_ngay_cong = tinh_so_ngay_cong(bat_dau, ket_thuc, so_ngay_thu_bay_nhap)
                    thong_tin_thang.config(text=f"Kỳ lương: {thang_bat_dau_str} - {thang_ket_thuc_str} ({so_ngay_cong} ngày công)")
                    nhap_window.destroy()
                except ValueError:
                    ttk.Label(nhap_window, text="Vui lòng nhập số nguyên hợp lệ.").pack()

            ok_button = ttk.Button(nhap_window, text="OK", command=cap_nhat_thong_tin)
            ok_button.pack(pady=10)

        nhap_so_ngay_thu_bay_window(ngay_bat_dau, ngay_ket_thuc)

    except ValueError:
        thong_tin_thang.config(text="Lỗi khi xác định kỳ lương.")

def them_khung_tang_ca():
    new_tang_ca_frame = ttk.Frame(tang_ca_frame)
    new_tang_ca_frame.pack(pady=5, fill="x")

    gio_label = ttk.Label(new_tang_ca_frame, text="Giờ:")
    gio_label.pack(side="left", padx=5)
    gio_entry = ttk.Entry(new_tang_ca_frame, width=7)
    gio_entry.pack(side="left", padx=5)
    new_tang_ca_frame.gio_entry = gio_entry

    ty_le_label = ttk.Label(new_tang_ca_frame, text="Tỷ lệ (%):")
    ty_le_label.pack(side="left", padx=5)
    ty_le_entry = ttk.Entry(new_tang_ca_frame, width=5)
    ty_le_entry.pack(side="left", padx=5)
    new_tang_ca_frame.ty_le_entry = ty_le_entry

    tang_ca_frames.append(new_tang_ca_frame)

# Tạo cửa sổ chính
root = tk.Tk()
root.title("Ứng dụng tính tiền lương")

# Khung chọn tháng
chon_thang_frame = ttk.LabelFrame(root, text="Chọn tháng tính lương")
chon_thang_frame.pack(padx=10, pady=10, fill="x")

chon_thang_button = ttk.Button(chon_thang_frame, text="Chọn tháng", command=hien_thi_hop_chon_thang)
chon_thang_button.pack(pady=5)

# Khung thông tin kỳ lương
thong_tin_frame = ttk.LabelFrame(root, text="Thông tin kỳ lương")
thong_tin_frame.pack(padx=10, pady=10, fill="x")

thong_tin_thang = ttk.Label(thong_tin_frame, text="Vui lòng chọn tháng.")
thong_tin_thang.pack(padx=5, pady=5)

# Khung nhập liệu
nhap_lieu_frame = ttk.LabelFrame(root, text="Nhập thông tin làm việc")
nhap_lieu_frame.pack(padx=10, pady=10, fill="x")

# Nhãn và ô nhập cho giờ làm
gio_lam_label = ttk.Label(nhap_lieu_frame, text="Tổng số giờ làm trong kỳ:")
gio_lam_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
gio_lam_entry = ttk.Entry(nhap_lieu_frame)
gio_lam_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

# Nhãn và ô nhập cho lương theo giờ
luong_theo_gio_label = ttk.Label(nhap_lieu_frame, text="Mức lương theo giờ:")
luong_theo_gio_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
luong_theo_gio_entry = ttk.Entry(nhap_lieu_frame)
luong_theo_gio_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

# Nhãn và ô nhập cho lương cơ bản
luong_co_ban_label = ttk.Label(nhap_lieu_frame, text="Lương cơ bản:")
luong_co_ban_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")
luong_co_ban_entry = ttk.Entry(nhap_lieu_frame)
luong_co_ban_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

# Nhãn và ô nhập cho lương trợ cấp
luong_tro_cap_label = ttk.Label(nhap_lieu_frame, text="Lương trợ cấp:")
luong_tro_cap_label.grid(row=3, column=0, padx=5, pady=5, sticky="w")
luong_tro_cap_entry = ttk.Entry(nhap_lieu_frame)
luong_tro_cap_entry.grid(row=3, column=1, padx=5, pady=5, sticky="ew")

# Khung nhập tăng ca
tang_ca_frame = ttk.LabelFrame(root, text="Thông tin tăng ca")
tang_ca_frame.pack(padx=10, pady=10, fill="x")

tang_ca_frames = []
them_khung_tang_ca() # Thêm một khung tăng ca ban đầu

them_button = ttk.Button(tang_ca_frame, text="+ Thêm giờ tăng ca", command=them_khung_tang_ca)
them_button.pack(pady=5)

# Nút tính lương
tinh_button = ttk.Button(root, text="Tính tổng lương", command=tinh_tong_luong)
tinh_button.pack(pady=10)

# Nhãn hiển thị kết quả
ket_qua_label = ttk.Label(root, text="")
ket_qua_label.pack(pady=10)

# Cấu hình cột để resize tốt hơn
nhap_lieu_frame.columnconfigure(1, weight=1)

root.mainloop()