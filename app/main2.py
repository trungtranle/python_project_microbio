from tkinter import *
from tkinter.ttk import *
from tkinter.constants import LEFT, RIGHT, BOTTOM, RAISED, HORIZONTAL, PAGES
import json
from tkinter import messagebox
import sqlite3
import datetime
from functools import partial
import xml.dom.minidom as xml

# log in screen

def login_window():
    global login
    login = Tk()
    login.title('Đăng nhập')
    login.geometry('320x170')
    login.resizable(0, 0)
    login.iconbitmap('data/bug.ico')

    global user_var
    user_var = StringVar()
    global pass_var
    pass_var = StringVar()

    label_user = Label(login, text='Tên đăng nhập:')
    label_user.grid(row=1, column=1, padx=(30, 10), pady=(30, 10))
    entry_user = Entry(login, textvariable=user_var)
    entry_user.grid(row=1, column=2, padx=(30, 10), pady=(30, 10))

    label_pass = Label(login, text='Mật khẩu:')
    label_pass.grid(row=2, column=1, padx=(30, 10), pady=10)
    entry_pass = Entry(login, textvariable=pass_var, show="*")
    entry_pass.grid(row=2, column=2, padx=(30, 10), pady=10)

    login_button = Button(login, text='Đăng nhập', command=login_func)
    login_button.grid(row=3, column=2, padx=10, pady=10)
    login.mainloop()


def login_func():
    global username
    username = user_var.get()
    password = pass_var.get()
    # connect to json
    f = open('data/login.json', 'r', encoding='utf-8')
    data = json.load(f)
    if username in data.keys():
        if password == data[username]:
            messagebox.showinfo('Đăng nhập thành công',
                                'Chào mừng %s vào phần mềm' % username)
            login.destroy()

            main_window()

        else:
            messagebox.showwarning('Sai mật khẩu', 'Mật khẩu không đúng')

    else:
        messagebox.showerror('Sai tên đăng nhập', 'User không tồn tại')

    f.close()


def main_window():
    global main
    main = Tk()
    main.title('Phần mềm quản lý kết quả vi sinh')
    main.geometry('500x500')
    main.resizable(0, 0)
    main.config(menu=menu_bar())
    main.iconbitmap('data/bug.ico')
    main.mainloop()
    return main


def menu_bar():
    menubar = Menu(main)
    funcmenu = Menu(menubar, tearoff=0)

    funcmenu.add_command(label='Nhập bệnh phẩm', command=new_specimen_window)

    funcmenu.add_command(label='Cập nhật kết quả nuôi cấy',
                         command=update_result_window)
    funcmenu.add_command(label='Tìm kiếm thông tin bệnh phẩm')
    funcmenu.add_command(label='Xóa bệnh phẩm')
    funcmenu.add_separator()
    funcmenu.add_command(label = 'Xuất dữ liệu XML')
    funcmenu.add_separator()
    funcmenu.add_command(label='Thoát', command=main.destroy)
    menubar.add_cascade(label='Chức năng', menu=funcmenu)
    return menubar


def connect_to_database():
    conn = sqlite3.connect("data/database.db")
    return conn


def new_specimen_window():
    main.withdraw()
    new_specimen = Toplevel()
    new_specimen.title('Nhập bệnh phẩm mới')
    new_specimen.geometry('500x500')
    new_specimen.iconbitmap('data/bug.ico')

    conn = connect_to_database()

    label1 = Label(new_specimen, text='NHẬP BỆNH PHẨM MỚI').grid(
        row=0, column=1, padx=(30, 10), pady=(30, 10))
    label_SID = Label(new_specimen, text='Mã số bệnh phẩm (SID):').grid(
        sticky='W', row=1, column=0, padx=10, pady=10)
    sid_var = StringVar()

    entry_SID = Entry(new_specimen, textvariable=sid_var)
    entry_SID.grid(row=1, column=1)
    name_var = StringVar()
    age_var = StringVar()
    sex_var = IntVar()
    ward_var = StringVar()
    address_var = StringVar()
    diagnosis_var = StringVar()
    physician_var = StringVar()
    sample_type_var = StringVar()

    def check_SID(self):
        read_SID = conn.execute('''SELECT SID FROM SAMPLE_INFO''')
        sid_list = []
        for row in read_SID:
            sid_list.append(int(row[0]))
        if len(sid_var.get()) != 0:
            try:
                if int(sid_var.get()) in sid_list:
                    messagebox.showerror(
                        'SID đã tồn tại', 'SID ' + sid_var.get() + ' đã tồn tại')
                    entry_SID.focus_force()
                    sid_var.set("")
            except ValueError:
                messagebox.showerror('Lỗi nhập liệu', 'SID chỉ bao gồm số')
                entry_SID.focus_force()
                sid_var.set("")
        
            
    #entry_SID.bind("<Return>", check_SID)
    
    entry_SID.bind("<FocusOut>", check_SID)

    pid_var = StringVar()
    entry_PID = Entry(new_specimen, textvariable=pid_var)
    label_PID = Label(new_specimen, text='Số bệnh án (PID):').grid(
        sticky='W', row=2, column=0, padx=(10, 0), pady=10)
    entry_PID.grid(row=2, column=1)

    def check_PID(self):

        if len(pid_var.get()) != 0:
            try:
                pid_get = int(pid_var.get())
                read_pid = conn.execute("SELECT PID FROM PATIENT_INFO")
                list_pid = []
                for id_ in read_pid:
                    list_pid.append(id_[0])
                if pid_get in list_pid:

                    data = conn.execute(
                        'SELECT * FROM PATIENT_INFO WHERE PID = ? ', (pid_get,))
                    for row in data:
                        name_var.set(row[2])
                        age_var.set(row[3])
                        sex_var.set(row[4])
                        ward_var.set(row[5])
                        address_var.set(row[6])
                        diagnosis_var.set(row[7])

            except ValueError:
                messagebox.showerror('Lỗi nhập liệu', "PID chỉ bao gồm số")
                entry_PID.focus_force()
                pid_var.set("")
        

    #entry_PID.bind("<Return>", check_PID)
    entry_PID.bind("<FocusOut>", check_PID)

    # name
    entry_name = Entry(new_specimen, textvariable=name_var)
    label_name = Label(new_specimen, text='Họ và tên:').grid(
        sticky='W', row=3, column=0, padx=(10, 0), pady=10)
    entry_name.grid(row=3, column=1)

    # age

    def validate_age(self):
        if len(age_var.get()) != 0:

            try:
                int(age_var.get())
                if len(age_var.get()) != 4:
                    messagebox.showerror('Năm sinh', 'Nhập năm sinh sai')
                    age_var.set("")
                    entry_age.focus_force()
            except ValueError:
                messagebox.showerror('Lỗi nhập liệu', 'Năm sinh phải là số')
                entry_age.focus_force()
                age_var.set("")

    entry_age = Entry(new_specimen, textvariable=age_var, width=5)
    entry_age.bind("<FocusOut>", validate_age)
    label_age = Label(new_specimen, text='Năm sinh').grid(
        sticky='W', row=3, column=2)
    entry_age.grid(row=3, column=3)
    # sex
    label_age = Label(new_specimen, text='Giới tính:').grid(
        sticky='W', row=4, column=0, padx=(10, 0), pady=10)
    sex_radio_button_1 = Radiobutton(
        new_specimen, text='Nam', variable=sex_var, value=1)
    sex_radio_button_1.grid(sticky='W', row=4, column=1)
    sex_radio_button_2 = Radiobutton(
        new_specimen, text='Nữ', variable=sex_var, value=0)
    sex_radio_button_2.grid(row=4, column=1)
    sex_radio_button_3 = Radiobutton(
        new_specimen, text='Khác', variable=sex_var, value=3)
    sex_radio_button_3.grid(sticky='E', row=4, column=1)
    # department
    add = 'data/ward.json'
    file = open(add)
    data = json.load(file)
    list_dep = []
    for key in data.keys():
        list_dep.append(data.get(key))

    label_ward = Label(new_specimen, text='Khoa:').grid(
        sticky='W', row=5, column=0, padx=(10, 0), pady=10)
    ward_var.set(None)
    #ward_var.set(list_dep[0])
    ward_menu = Combobox(new_specimen, textvariable = ward_var, values = list_dep, state  = 'readonly')
    ward_menu['width'] = 10
    ward_menu.grid(row=5, column=0, padx=(50, 10))
    # address
    label_address = Label(new_specimen, text='Địa chỉ:').grid(
        sticky='W', row=5, column=1, padx=(30, 0), pady=10)
    entry_address = Entry(new_specimen, textvariable=address_var)
    scroll_address = Scrollbar(new_specimen, orient=HORIZONTAL)
    entry_address.config(xscrollcommand=scroll_address.set)
    scroll_address.config(command=entry_address.xview)
    scroll_address.grid(sticky=E+W, row=5, column=1,
                        padx=(80, 10), pady=(36.5, 0))
    entry_address.grid(row=5, column=1, padx=(80, 10))
    #scroll_address.pack(side = BOTTOM, fill = 'x')

    # dx
    label_dx = Label(new_specimen, text='Chẩn đoán:').grid(
        sticky='W', row=6, column=0, padx=(10, 0), pady=10)
    entry_dx = Entry(new_specimen, textvariable=diagnosis_var)
    entry_dx.grid(sticky=E+W, row=6, column=1)
    scroll_dx = Scrollbar(new_specimen, orient=HORIZONTAL)
    entry_dx.config(xscrollcommand=scroll_dx)
    scroll_dx.config(command=entry_dx.xview)
    scroll_dx.grid(sticky=E+W, row=6, column=1, padx=(0, 10), pady=(36.5, 0))

    # physician
    label_physician = Label(new_specimen, text='Bác Sĩ chỉ định:').grid(
        sticky='W', row=7, column=0, padx=(10, 0), pady=10)
    entry_physician = Entry(new_specimen, textvariable=physician_var)
    entry_physician.grid(sticky='W', row=7, column=1)
    # date/time
    label_datetime = Label(new_specimen, text='Ngày giờ nhập mẫu:').grid(
        sticky='W', row=8, column=0, padx=(10, 0), pady=10)
    var_datetime = StringVar()
    date = datetime.datetime.now()
    date_string = date.strftime('%Y/%m/%d %H:%M:%S')
    var_datetime.set(date_string)
    entry_datetime = Entry(
        new_specimen, textvariable=var_datetime, state="readonly")
    entry_datetime.grid(sticky='W', row=8, column=1)
    # sample type
    sample_type = json.load(open('data/SAMPLE_TYPE.json'))
    list_sample_type = []
    for key in sample_type.keys():
        list_sample_type.append(sample_type.get(key))

    label_sampletype = Label(new_specimen, text='Loại mẫu:').grid(
        sticky='W', row=9, column=0, padx=(10, 0), pady=10)
    sample_type_var.set(list_sample_type[0])
    sample_type_menu = Combobox(
        new_specimen, textvariable = sample_type_var, values = list_sample_type, state = 'readonly')
    sample_type_menu['width'] = 15
    sample_type_menu.grid(sticky=E+W, row=9, column=1)

    # clear everything function and button
    def clear_everything():
        sid_var.set("")
        pid_var.set("")
        name_var.set("")
        age_var.set("")
        sex_var.set(1)
        ward_var.set(list_dep[0])
        address_var.set("")
        diagnosis_var.set("")
        physician_var.set("")
        sample_type_var.set(list_sample_type[0])

    def reset_everything():
        if messagebox.askokcancel('Xóa tất cả', 'Xóa tất cả và nhập lại?'):
            clear_everything()

    reset_button = Button(new_specimen,  text='Nhập lại',
                          command=reset_everything)
    reset_button.grid(row=10, column=0, padx=(10, 0), pady=10)
    # save button

    def save_button_command():
        if len(sid_var.get()) == 0:
            messagebox.showerror('Chưa nhập SID', 'Chưa nhập SID')
            entry_SID.focus_force() 
        else:    
            sid_get = int(sid_var.get())
        if len(pid_var.get()) == 0:
            messagebox.showerror('Chưa nhập PID', 'Chưa nhập PID')
            entry_PID.focus_force() 
        else:    
            pid_get = int(pid_var.get())
        
        name_get = name_var.get()
        age_get = None
        sex_get = sex_var.get()
        try:
            age_get = int(age_var.get())

        except ValueError:
            pass
        ward_get = ward_var.get()
        address_get = address_var.get()
        dx_get = diagnosis_var.get()
        physician_get = physician_var.get()
        date_get = date_string
        sample_type_get = sample_type_var.get()
        try:
            conn = connect_to_database()
            query_patient = 'INSERT OR REPLACE INTO PATIENT_INFO\
                    (PID, FULL_NAME, AGE, SEX, WARD, ADDRESS, DIAGNOSIS)\
                    VALUES (?, ?, ?, ?, ?, ?, ?)'
            conn.execute(query_patient, (pid_get, name_get, age_get,
                                         sex_get, ward_get, address_get, dx_get))
            query_sample = 'INSERT INTO SAMPLE_INFO\
                            (SID, PID, DATE_TIME, PHYSICIAN, SAMPLE_TYPE)\
                            VALUES (?, ?, ?, ?, ?)'
            conn.execute(query_sample, (sid_get, pid_get,
                                        date_get, physician_get, sample_type_get))
            conn.commit()
        except sqlite3.OperationalError:
            messagebox.showerror(
                'Lỗi CSDL', 'Cơ sở cập nhật hiện đang bị khóa')
        messagebox.showinfo('Thêm mới thành công',
                            'Thêm mới SID ' + str(sid_get) + ' thành công')
        clear_everything()
    save_button = Button(new_specimen, text='Lưu',
                         width=15,  command=save_button_command)
    save_button.grid(row=10, column=1, pady=10)

    #bind Return to move focus
    list_entry = []
    for child in new_specimen.winfo_children():
        if isinstance(child, Entry):
            list_entry.append(child)
       
    def focus_on_next_entry(event, entry_list, this_index):
        next_index = (this_index + 1) % len(list_entry)
        entry_list[next_index].focus_set()

    for idx, entry in enumerate(list_entry):
        entry.bind('<Return>', lambda e, idx = idx: focus_on_next_entry(e, list_entry, idx))            
    # exit button = return to main

    def on_exit():
        if messagebox.askokcancel('Thoát', 'Bạn muốn ngưng nhập mới?'):
            main.deiconify()
            new_specimen.destroy()
            conn.commit()
            conn.close()
    exit_button = Button(new_specimen, text='Quay lại', command=on_exit)
    exit_button.grid(row=10, column=2, pady=10)
    new_specimen.protocol("WM_DELETE_WINDOW", on_exit)

    new_specimen.mainloop()


def update_result_window():
    main.withdraw()
    update_result = Toplevel()
    update_result.title('Cập nhật kết quả nuôi cấy')
    update_result.geometry('550x700')
    update_result.iconbitmap('data/bug.ico')

    conn = connect_to_database()

    top_frame = LabelFrame(update_result, text = 'Thông tin mẫu')
    top_frame.grid(row = 0, column = 0, padx= (10, 10))
    sid_entry_var = StringVar()
    sid_label = Label(top_frame, text='Nhập SID cần cập nhật:')
    sid_label.grid(row=1, column=0, padx=(10, 10), pady=10)
    sid_entry = Entry(top_frame, textvariable=sid_entry_var)

    pid_var = StringVar()
    date_var = StringVar()
    physician_var = StringVar()
    sample_type_var = StringVar()
    name_var = StringVar()
    age_var = StringVar()
    sex_var = IntVar()
    ward_var = StringVar()
    address_var = StringVar()
    diagnosis_var = StringVar()
    result_var = StringVar()
    result_var.set("")
    organism_var =StringVar()
    organism_var.set("")
    
    antibiogram_var = StringVar()
    
    global flag_1
    flag_1 = 0
    def check_sid(self):
        if len(sid_entry_var.get()) != 0:
            try:
                #global sid_get
                global sid_get
                sid_get = int(sid_entry_var.get())
                sql_query = '''SELECT SID FROM SAMPLE_INFO'''
                data = conn.execute(sql_query)
                list_sid = []
                for row in data:
                    list_sid.append(row[0])

                if sid_get in list_sid:
                    sql_query_2 = '''SELECT PID, DATE_TIME, PHYSICIAN, SAMPLE_TYPE, RESULT, ORGANISM, ANTIBIOGRAM FROM SAMPLE_INFO WHERE SID = ?'''
                    data_1 = conn.execute(sql_query_2, (sid_get,))
                    for row in data_1:
                        pid_var.set(row[0])
                        pid = int(pid_var.get())
                        date_var.set(row[1])
                        physician_var.set(row[2])
                        sample_type_var.set(row[3])
                        result_var.set(row[4])
                        organism_var.set(row[5])
                        antibiogram_var.set(row[6])
                    
                    sql_query_3 = '''SELECT FULL_NAME, AGE, SEX, WARD, ADDRESS, DIAGNOSIS FROM PATIENT_INFO WHERE PID = ?'''
                    data_2 = conn.execute(sql_query_3, (pid,))
                    for row in data_2:
                        name_var.set(row[0])
                        age_var.set(row[1])
                        sex_var.set(row[2])
                        ward_var.set(row[3])
                        address_var.set(row[4])
                        diagnosis_var.set(row[5])
                        
                        if sex_var.get() == 1:
                            sex_var_char.set('Nam')
                        elif sex_var.get() == 0:
                            sex_var_char.set('Nữ')
                        else:
                            sex_var_char.set('Khác')
                    
                else:
                    messagebox.showwarning(
                        'Không tìm thấy SID', 'Không tìm thấy SID ' + str(sid_get))

                    sid_entry.focus_force()
                    sid_entry_var.set("")
            except ValueError:
                messagebox.showerror('Lỗi nhập liệu', 'SID chỉ bao gồm số')
                sid_entry.focus_force()
                sid_entry_var.set("")

    
    sid_entry.bind("<Return>", check_sid)
    sid_entry.bind("<FocusOut>", check_sid)
    sid_entry.grid(row=1, column=1, padx=10, pady=10)
    
    entry_PID = Entry(top_frame, textvariable=pid_var, state = 'readonly')
    label_PID = Label(top_frame, text='Số bệnh án (PID):').grid(
        sticky='W', row=2, column=0, padx=(10, 0), pady=10)
    entry_PID.grid(row=2, column=1)

    entry_name = Entry(top_frame, textvariable=name_var, state = 'readonly')
    label_name = Label(top_frame, text='Họ và tên:').grid(
        sticky='W', row=3, column=0, padx=(10, 0), pady=10)
    entry_name.grid(row=3, column=1)

    entry_age = Entry(top_frame, textvariable=age_var, state = 'readonly', width = 5)
    label_age = Label(top_frame, text='Tuổi:').grid(
        sticky='W', row=3, column=2, padx=(10, 0), pady=10)
    entry_age.grid(sticky = 'W', row=3, column=3)
    sex_var_char = StringVar()
    
    if sex_var.get() == 1:
        sex_var_char.set('Nam')
    elif sex_var.get() == 0:
        sex_var_char.set('Nữ')
    else:
        sex_var_char.set('Khác')
    label_sex = Label(top_frame, text = 'Giới tính').grid(
        row = 3, column = 3)
    entry_sex = Entry(top_frame, textvariable = sex_var_char, state = 'readonly', width = 5)
    entry_sex.grid(sticky = 'E', row  = 3, column = 3)    

    entry_address = Entry(top_frame, textvariable=address_var, state = 'readonly')
    scroll_address = Scrollbar(top_frame, orient = HORIZONTAL)
    entry_address.config(xscrollcommand=scroll_address.set)
    scroll_address.config(command=entry_address.xview)
    scroll_address.grid(sticky=E+W, row=4, column=1,
                        padx=(10, 10), pady=(36.5, 0))
    label_address = Label(top_frame, text='Địa chỉ:').grid(
        sticky='W', row=4, column=0, padx=(10, 0), pady=10)
    entry_address.grid(row=4, column=1)
    label_dep = Label(top_frame, text = 'Khoa:').grid(
        sticky='W', row=4, column=2, padx=(10, 0), pady=10)
    entry_dep = Entry(top_frame, textvariable = ward_var, state = 'readonly') 
    entry_dep.grid(row = 4, column= 3)

    label_physician = Label(top_frame, text = 'Bác sĩ chỉ định: ').grid(
        sticky = 'W', row = 5, column = 0, padx = (10, 0), pady = 10)
    entry_physician = Entry(top_frame, textvariable = physician_var, state = 'readonly')
    entry_physician.grid(row = 5, column = 1)

    label_dx = Label(top_frame, text = 'Chẩn đoán:').grid(
        sticky = 'W', row = 5, column = 2, padx = (10, 0), pady = 10)
    entry_dx = Entry(top_frame, textvariable = diagnosis_var, state = 'readonly')
    scroll_dx = Scrollbar(top_frame, orient = HORIZONTAL)
    entry_dx.config(xscrollcommand=scroll_dx.set)
    scroll_dx.config(command=entry_dx.xview)
    scroll_dx.grid(sticky=E+W, row=5, column=3,
                        padx=(10, 10), pady=(36.5, 0))
    entry_dx.grid(row = 5, column = 3)

    label_time = Label(top_frame, text = 'Thời gian nhập mẫu:').grid(
        sticky = 'W', row = 6, column = 0, padx = (10, 0), pady = 10)
    entry_time = Entry(top_frame, textvariable = date_var, state = 'readonly')
    entry_time.grid(row = 6, column = 1)
    label_sample_type = Label(top_frame, text = 'Loại mẫu:').grid(
        sticky = W, row = 6, column = 2, padx = (10, 0), pady = 5)
    entry_sample_type = Entry(top_frame, textvariable = sample_type_var, state = 'readonly')
    entry_sample_type.grid(row = 6, column = 3)
    lable_result = Label(top_frame, text = 'Kết quả:').grid(
        sticky = 'W', row = 7, column = 0, padx = (10, 0), pady = 10)
    list_result=['ÂM TÍNH', 'DƯƠNG TÍNH']

    entry_result = Combobox(top_frame, values = list_result, state = 'readonly', textvariable = result_var)
    
    entry_result.grid(row = 7, column = 1)
    result_frame = LabelFrame(update_result, text = 'Kết quả định danh')
    result_frame.grid(row = 1, column = 0, sticky = W, padx=(10,0), pady = 10)
    
              
    list_bacteria = []
    data_3 = conn.execute('SELECT NAME FROM BACTERIA_ID')            
    for row in data_3:
        list_bacteria.append(row[0])    
    #entry_bacteria = Combobox(result_frame, textvariable = organism_var, values = list_bacteria, state = 'readonly')
    class_var = StringVar()
    ast_frame = LabelFrame(update_result,text = 'Kháng sinh đồ')
    update_result.update_idletasks()
    anti_list = []
    s_list = []
    r_list = []
    list_entry_antibio = []
    list_result_eval = []
    def show_antibiogram(self, *arg):
        def check_ast(radius, s, r, text_var, *arg):
            if len(radius.get()) != 0:
                if int(radius.get()) < 6:
                    radius.set('6')     
                if int(radius.get()) >= s:
                        text_var.set('S')
                elif int(radius.get()) <= r:
                        text_var.set('R')
                elif int(radius.get()) > r and int(radius.get()) < s:
                        text_var.set('I')     
            else:
                text_var.set(" ")
            
        def enter_antibiogram(self, *arg):
            ast_frame.grid(row = 2, column = 0 , sticky = W, padx=(10,0), pady = 10)
            data_4 = conn.execute('SELECT CLASS_ FROM BACTERIA_ID WHERE NAME = ?', (organism_var.get(),))
            for row in data_4:                
                class_var.set(row[0])
            data_5 = conn.execute('SELECT * FROM ANTIBIOTIC WHERE CLASS_ = ?', (class_var.get(),))
            
            anti_list.clear()
            
            s_list.clear()
            
            r_list.clear()
            
            list_entry_antibio.clear()
            
            list_result_eval.clear()
            for row in data_5:
                anti_list.append(row[2])
                s_list.append(row[3])
                r_list.append(row[4])
            for i in range(len(anti_list)):
                row = int(i / 3)
                col = i % 3
                label_row_i = Label(ast_frame, text = anti_list[i], width = 5)
                label_row_i.grid(row = row, column = col, sticky = W, padx = (10, 80), pady = 5)    
                global entry_i_var
                entry_i_var = StringVar()
                result_ast_i = StringVar()
                result_ast_i.set("")
                entry_i = Entry(ast_frame, textvariable = entry_i_var, width = 3)
                list_entry_antibio.append(entry_i_var)
                entry_i.grid(row = row, column = col, padx = (15, 5), pady = 5)
                result_str_i = Label(ast_frame, textvariable = result_ast_i, width = 2)
                result_str_i.grid(row = row, column = col, sticky = E, padx = (0, 10), pady = 5) 
                entry_i.bind('<FocusOut>', partial(check_ast, entry_i_var, s_list[i],  r_list[i], result_ast_i, str(i)))
                list_result_eval.append(result_ast_i)
            data_6 = conn.execute('SELECT ANTIBIOGRAM FROM SAMPLE_INFO WHERE SID = ?', (sid_get,))
            for row in data_6:
                if row[0] != None:
                    dic = eval(row[0])
                    for key in dic.keys():
                        if key in anti_list:
                            index = anti_list.index(key)
                            list_entry_antibio[index].set(dic[key][0])
                            list_result_eval[index].set(dic[key][1])
            #enter to focus on next entry
            list_entry = []
            for child in ast_frame.winfo_children():
                if isinstance(child, Entry):
                    list_entry.append(child)
       
            def focus_on_next_entry(event, entry_list, this_index):
                next_index = (this_index + 1) % len(list_entry)
                entry_list[next_index].focus_set()

            for idx, entry in enumerate(list_entry):
                entry.bind('<Return>', lambda e, idx = idx: focus_on_next_entry(e, list_entry, idx))    
            
            ast_frame.mainloop()

        if result_var.get() == list_result[1]:
            label_bacteria = Label(result_frame, text = 'Vi khuẩn:')
            label_bacteria.grid(sticky = 'W', row = 0, column = 0)
            entry_bacteria = Combobox(result_frame, textvariable = organism_var, values = list_bacteria, state = 'readonly')                             
            entry_bacteria.grid(row = 0, column = 1)        
                      
            entry_bacteria.bind("<<ComboboxSelected>>", enter_antibiogram)
            organism_var.trace('w', enter_antibiogram)
            def re_show(self, *arg):
                if result_var.get == 'DƯƠNG TÍNH':
                    enter_antibiogram(self)
            result_var.trace('w', re_show) 
            label_class = Label(result_frame, text = 'Nhóm kháng sinh:')
            label_class.grid(sticky = 'W', row = 0, column = 2)
            entry_class = Entry(result_frame, textvariable = class_var, state = 'readonly')
            entry_class.grid(row = 0, column = 3)

        else:
            for wid in result_frame.winfo_children():
                wid.destroy()
            for wid in ast_frame.winfo_children():
                wid.destroy()
        #organism_var.trace('w', enter_antibiogram)  
    result_var.trace('w', show_antibiogram)    
    entry_result.bind("<<ComboboxSelected>>", show_antibiogram)
    
   

    #save button
    def clear():
        sid_entry_var.set("")
        pid_var.set("")
        name_var.set("")
        age_var.set("")
        sex_var_char.set("")
        physician_var.set("")
        diagnosis_var.set("")
        address_var.set("")
        ward_var.set("")
        date_var.set("")
        sample_type_var.set("")
        result_var.set("")
    def save():
        if result_var.get() == 'DƯƠNG TÍNH':
            result = result_var.get()
            organism = organism_var.get()
            result_str = "{"
            for item in range(len(anti_list)):
                result_str += "'" + anti_list[item] + "'" + ':['+ list_entry_antibio[item].get() + ',' + "'"+ list_result_eval[item].get() +"'" + '],'
            result_str += "}"
            
        else:
            result = result_var.get()
            organism = None
            result_str = None
        query = '''UPDATE SAMPLE_INFO\
                    SET RESULT = ? ,\
                    ORGANISM = ?,\
                    ANTIBIOGRAM = ?\
                    WHERE SID = ?'''
        if messagebox.askokcancel('Cập nhật dữ liệu', 'Cập nhật kết quả SID ' + str(sid_get) + "?"):        
            conn.execute(query, (result, organism, result_str, sid_get))
            conn.commit()    
            messagebox.showinfo('Cập nhật thành công', 'Cập nhật SID %s thành công'%str(sid_get)) 
            clear()
    
    save_button = Button(update_result, text = 'Lưu kết quả', command = save)
    save_button.grid(row = 4, column = 0,  padx = (50, 10)) 
    #reset button
    def reset_all():
        if messagebox.askokcancel('Nhập lại', 'Xóa tất cả và nhập lại?'):
            clear()
        
    reset_button = Button(update_result, text='Nhập lại', command = reset_all)
    reset_button.grid(row = 4, column = 0, sticky = W, padx= (80, 10))
    
       
    # exit button = return to main

    
    def on_exit():
        if messagebox.askokcancel('Thoát', 'Bạn muốn ngưng thay đổi?'):
            main.deiconify()
            update_result.destroy()
            conn.commit()
            conn.close()
    #exit_button = Button(update_result, text = 'Quay lại', command = on_exit)
    #exit_button.grid(row = 10, column = 2, pady = 10)
    update_result.protocol("WM_DELETE_WINDOW", on_exit)

    update_result.mainloop()


def delete_specimen_window():
    pass


def find_specimen_window():
    pass

def export_to_xml():
    pass

login_window()
