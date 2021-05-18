import json
import os
import threading
from tkinter import tix, ttk, messagebox
from tkinter.ttk import *
from tkinter import *

from Student import Student
from timetable import Timetable
from List_class import TableSubject
OPTION = ["Mã môn học", "Tên Môn học", "Tín",
                       "Mã lớp môn học", "Giảng viên", "Số lượng học sinh",
                       "Buổi", "Thứ", "Tiết", "Địa điểm", "Nhóm"]
class App(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.student = Student()
        self.is_show_new_timetable = False
        self.is_show_class_list = False
        self.pack(fill=BOTH, expand=True, side=TOP)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=14)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=18)

        Style().configure("", padding=(0, 0, 0, 0), font='Calibri 12')
        self.initUI()
        self.read_save_file()
        threading.Thread(target=self.get_suggested_data).start()


    def initUI(self):
        self.top_frame = LabelFrame(self)
        self.top_frame.grid_rowconfigure(0, weight=1)
        self.top_frame.grid_columnconfigure(0, weight=1)
        self.top_frame.grid_columnconfigure(1, weight=10)
        self.top_frame.grid_columnconfigure(2, weight=1)
        self.top_frame.grid_columnconfigure(3, weight=1)
        self.top_frame.grid(row=0, column=1, rowspan=1, sticky="nsew")

        self.mid_frame = LabelFrame(self)
        self.mid_frame.grid_rowconfigure(0, weight=1)
        self.mid_frame.grid_columnconfigure(0, weight=1)
        self.mid_frame.grid_columnconfigure(1, weight=1)
        self.mid_frame.grid(row=1, column=1, rowspan=1, sticky="nsew")

        # top
        input_label = Label(self.top_frame, text="MSV :")
        input_label.grid(row=0, column=0, rowspan=1, sticky="nsew")
        self.input_bar = Entry(self.top_frame)
        self.input_bar.grid(row=0, column=1, rowspan=1, sticky="nsew")
        self.input_bar.bind("<Return>", self.search_student_id)
        search_button = Button(self.top_frame, text="Tìm", command=self.search_student_id)
        search_button.grid(row=0, column=2, rowspan=1, sticky="nsew")
        mic_button = Button(self.top_frame, text="Lưu", command=self.save_all)
        mic_button.grid(row=0, column=3, rowspan=1, sticky="nsew")
        new_timetable_button = Button(self.top_frame, text="Thời khóa biểu 2", command=self.show_new_timetable)
        new_timetable_button.grid(row=0, column=4, sticky="nsew")
        # mid
        self.timetable1 = Timetable(self.mid_frame, False)
        self.timetable1.grid(row=0, column=0, sticky="nsew")
        self.timetable2 = Timetable(self.mid_frame)

        self.left_frame = LabelFrame(self, width=300)
        self.left_frame.grid_rowconfigure(0, weight=2)
        self.left_frame.grid_rowconfigure(1, weight=1)
        self.left_frame.grid_rowconfigure(2, weight=7)
        self.left_frame.grid_rowconfigure(3, weight=1)
        self.left_frame.grid_columnconfigure(0, weight=1)

        self.left_frame.grid(column=0, row=0, rowspan=2, sticky="nsew")
        self.student_info = StringVar()
        student_info_label = Label(self.left_frame, textvariable=self.student_info)
        student_info_label.grid(row=0, column=0, sticky="nsew")
        self.show_class_list_frame = Frame(self.left_frame)
        # self.show_class_list_frame.grid(row=2, column=0, sticky="nsew")
        self.show_class_list_frame.grid_columnconfigure(0, weight=1)
        self.show_class_list_frame.grid_columnconfigure(1, weight=1)
        self.show_class_list_frame.grid_rowconfigure(0, weight=1)
        self.show_class_list_frame.grid_rowconfigure(1, weight=1)
        self.show_class_list_frame.grid_rowconfigure(2, weight=1)
        self.show_class_list_frame.grid_rowconfigure(3, weight=1)
        self.show_class_list_frame.grid_rowconfigure(4, weight=1)
        self.show_class_list_frame.grid_rowconfigure(5, weight=1)
        self.show_class_list_frame.grid_rowconfigure(6, weight=1)
        self.show_class_list_frame.grid_rowconfigure(7, weight=23)
        self.show_class = StringVar()
        self.show_class.set("Danh sách môn học")
        show_class_list_button = Button(self.left_frame, textvariable=self.show_class, command=self.show_class_list)
        show_class_list_button.grid(row=1, column=0, columnspan=2, sticky="nsew")
        sort_class_list_label = Label(self.show_class_list_frame, text="Sort")
        sort_class_list_label.grid(row=3, column=0, sticky="nsew")
        find_class_list_label = Label(self.show_class_list_frame, text="Find :")
        find_class_list_label.grid(row=0, column=0, sticky="nsew")
        self.find_entry = Entry(self.show_class_list_frame)
        self.find_entry.grid(row=0, column=1, sticky="nsew")
        self.find_entry.bind("<Return>", self.find)

        self.findby = StringVar()
        self.findby.set(OPTION[1])
        self.find_selection = OptionMenu(self.show_class_list_frame, self.findby, *OPTION)
        self.find_selection.grid(row=1, column=1, sticky="ew")
        find_button = Button(self.show_class_list_frame, text="Tìm",command=self.find)
        find_button.grid(row=1, column=0, sticky="ew")
        separator1 = ttk.Separator(self.show_class_list_frame, orient='horizontal')
        separator1.grid(row=2, column=0,columnspan=2, sticky="ew")
        self.sortby = StringVar()
        self.sortby.set(OPTION[7])
        self.sort_selection = OptionMenu(self.show_class_list_frame, self.sortby, *OPTION)  # dropdown(18)
        self.sort_selection.grid(row=3, column=1, sticky="nsew")
        self.subject_table = TableSubject(self)

        self.is_DESC = BooleanVar()
        check_box_sort = Checkbutton(self.show_class_list_frame, text="Giảm dần", variable=self.is_DESC, onvalue=True, offvalue=False)
        check_box_sort.grid(row=4, column=1, sticky="nsew")

        # create popup menu in subject_id table
        self.popup_menu = Menu(self.subject_table, tearoff=False)
        self.popup_menu.add_command(label="Thêm môn học", command=self.insert_data)
        self.subject_table.bind("<Button-3>", self.show_popup_menu)

        setting_button = Button(self.left_frame, text="Help", command=self.open_setting)
        setting_button.grid(row=5, column=0, columnspan=2, sticky="nsew")
        self.subjects_info = StringVar()
        self.set_subjects_info()
        subject_info_label = Label(self.left_frame, textvariable=self.subjects_info)
        subject_info_label.grid(row=4, column=0, columnspan=2, sticky="nsew")
        self.timetable2.bind("<ButtonRelease-1>", self.set_subjects_info)
        self.timetable2.bind("<ButtonRelease-3>", self.set_subjects_info)
        separator1 = ttk.Separator(self.show_class_list_frame, orient='horizontal')
        separator1.grid(row=5, column=0, columnspan=2, sticky="ew")
        self.suggestion_button = Button(self.show_class_list_frame, text="Gợi ý môn học", command=self.show_suggestion_table)
        self.suggestion_button.grid(row=6,column=0, columnspan=2, sticky="nsew")

    def show_suggestion_table(self, event=None):
        self.subject_table.remove_all()
        self.subject_table.set_suggestion()

    def show_class_list(self):
        if self.is_show_class_list:
            self.mid_frame.grid(row=1, column=1, rowspan=1, sticky="nsew")
            self.top_frame.grid(row=0, column=1, rowspan=1, sticky="nsew")
            self.show_class_list_frame.grid_forget()
            self.subject_table.grid_forget()
            self.is_show_class_list = False
            self.show_class.set("Danh sách môn học")
        else:
            self.show_class.set("Thời khóa biểu")
            self.top_frame.grid_forget()
            self.mid_frame.grid_forget()
            self.show_class_list_frame.grid(row=2, column=0, sticky="nsew")
            self.subject_table.grid(column=1, row=0, rowspan=2, sticky="nsew")
            self.is_show_class_list = True

    def show_popup_menu(self, event):
        self.popup_menu.tk_popup(event.x_root, event.y_root)

    def insert_data(self):
        #fix
        self.timetable2.insert_subject(self.subject_table.get_selected_data())
        if self.is_show_new_timetable is not None:
            self.timetable2.grid(row=0, column=1, sticky="nsew")
            self.is_show_new_timetable = True
            self.set_subjects_info()


    def show_new_timetable(self):
        if self.is_show_new_timetable:
            self.timetable2.grid_forget()
            self.is_show_new_timetable = False
        else:
            self.timetable2.grid(row=0, column=1, sticky="nsew")
            self.is_show_new_timetable = True

    def search_student_id(self, event = None):
        from SQLManagement import SQLManagement
        input =self.input_bar.get()
        if len(input) == 8:
            print("search", self.input_bar.get())
            self.timetable1.delete_all_subjects()
            self.timetable2.delete_all_subjects()
            self.timetable1.insert_subject_from_student_id(input)
            self.timetable2.subject_manager.color_manager = self.timetable1.copy_color()
            self.timetable2.insert_subject_from_student_id(input)
            self.set_subjects_info()
            threading.Thread(target=self.get_suggested_data).start()

        else:
            messagebox.showinfo("Error","MSV không hợp lệ \n MSV gồm 8 chữ số" )
            return
        if self.is_show_new_timetable is not None:
            self.timetable2.grid(row=0, column=1, sticky="nsew")
            self.is_show_new_timetable = True
        if len(SQLManagement().get_student(self.input_bar.get())) != 0:
            self.student = Student(SQLManagement().get_student(self.input_bar.get()))
            self.set_student_info()
            self.set_subjects_info()
            self.input_bar.delete(0, END)
        else:
            self.student_info.set("")
            messagebox.showinfo("Error","Không tìm thấy sinh viên" )

    def find(self, event=None):
        #fix
        print(self.find_entry.get())

        self.subject_table.find(self.find_entry.get(), self.findby.get(), self.sortby.get(), self.is_DESC.get(), self.student.is_CLC if self.student is not None else None)


    def open_setting(self):
        import webbrowser
        def open_doc():
            webbrowser.get().open("https://drive.google.com/drive/folders/1716kUv4Pq6Fo-OkcoV40hlahNElg6zM7?usp=sharing")
        def open_drive():
            webbrowser.get().open("https://drive.google.com/drive/folders/17TCXDiTqZ4JZ_KAl1MvKfGjyirzbTVFU?usp=sharing")

        def open_github():
            webbrowser.get().open("https://github.com/BongNT/BTL_CNPM.git")
        def open_register():
            webbrowser.get().open("http://dangkyhoc.vnu.edu.vn/dang-nhap")
        top = Toplevel()
        top.geometry("500x500")
        top.grid_rowconfigure(0, weight=1)
        top.grid_rowconfigure(1, weight=1)
        top.grid_rowconfigure(2, weight=1)
        top.grid_rowconfigure(3, weight=1)
        #top.grid_rowconfigure(4, weight=1)
        top.grid_columnconfigure(0, weight=10)
        top.grid_columnconfigure(1, weight=1)

        label = Label(top, text="Phần mềm quản lý môn học\nPhiên bản : 1.0\n Phát triển bởi Đỗ Minh Hiếu",font='calibri 14')
        doc_button = Button(top,text="Hướng dẫn sử dụng", command=open_doc)
        drive_button = Button(top,text="Lấy dữ liệu", command=open_drive)
        github_button = Button(top,text="Github", command=open_github)
        regist_button = Button(top,text="Đăng ký học", command=open_register)
        doc_button.grid(row=0,column=1, sticky="nsew")
        drive_button.grid(row=1, column=1, sticky="nsew")
        github_button.grid(row=2, column=1, sticky="nsew")
        regist_button.grid(row=3, column=1, sticky="nsew")
        label.grid(row=0,column=0, rowspan=5, sticky="nsew")


    def set_subjects_info(self, event=None):
        s = """Số tín Trường đăng ký : {}
Số tín tự đăng ký: {}
Số tiết 1 tuần trường đăng ký :{}
Số tiết 1 tuần tự đăng ký :{}
Tổng số tiết trống giữa 2 tiết: {}
        """.format(self.timetable1.get_total_credit(), self.timetable2.get_total_credit(), self.timetable1.get_total_lesson(), self.timetable2.get_total_lesson(), self.timetable2.get_total_free_time())
        self.subjects_info.set(s)

    def get_suggested_data(self):
        self.subject_table.get_suggested_data(self.student.course)

    def set_student_info(self):
        if self.student is not None:
            self.student_info.set(self.student.get_info())

    def save_all(self):
        dataPath = self.__get_path_to("save.json")
        data = {}
        data["student"] = []
        data["student"].append(self.student.save_data())
        data["student"].append(self.timetable1.save_data())
        data["student"].append(self.timetable2.save_data())
        with open(dataPath, 'w') as file:
            json.dump(data, file)
        messagebox.showinfo("Lưu thành Công","Lưu thành Công")

    def read_save_file(self):
        dataPath = self.__get_path_to("save.json")
        try:
            with open(dataPath, 'r') as file:
                d = file.read()
                json_data = json.loads(d)
                self.student = Student(self.__extract_data(json_data, 0))
                self.timetable1.insert_subject(self.__extract_data(json_data, 1))
                self.timetable2.insert_subject(self.__extract_data(json_data, 2))
        except :
            print("không có file json")
        self.set_subjects_info()
        self.set_student_info()
    def __extract_data(self, json_data, option):
        """
        option = 0, 1, 2
        0: return student_data
        1: return timetable1 list_data
        2: return timetable2 list_data
        """
        if option ==1:
            timetable1 = json_data["student"][1]["subject"]
            data = []
            for i in timetable1:
                data.append(list(i.values()))
            return data
        elif option == 2:
            timetable1 = json_data["student"][2]["subject"]
            data = []
            for i in timetable1:
                data.append(list(i.values()))
            return data
        elif option ==0:
            student_info = json_data["student"][0]
            data = []
            data.append(list(student_info.values()))
            return data

    def __get_path_to(self, file_name):
        try:
            absFilePath = os.path.abspath(__file__)
            projectPath = absFilePath
            for i in range(3):
                projectPath = os.path.dirname(projectPath)
            dataPath = projectPath + "/res/Data/" + file_name
            return dataPath
        except FileNotFoundError:
            print("không tìm thấy file")

if __name__ == "__main__":
    root = tix.Tk()
    root.geometry()
    root.state('zoomed')
    root.title("Quản lý môn  học")
    app = App(root)
    root.mainloop()
