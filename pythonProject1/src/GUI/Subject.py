
from tkinter.ttk import *

from tkinter import *
from tkinter import colorchooser
from tkinter.tix import *

from List_class import StudentTable


class Subject(Label):
    def __init__(self, parent, data, color="yellow", can_config=True):
        # 1 subject_id co thể có tiết thực hành, bài tập, hoặc chỉ có thực hành
        Label.__init__(self, parent)
        self.can_config = can_config
        self.parent = parent
        self.color = color
        self.get_data(data)
        self.initUI(color)

    def initUI(self, color):

        self.color = color
        self.configure(text="{}\n{}".format(self.partition(self.subject_name), self.place), background=color, relief=GROOVE,
                       font='calibri 8')
        self.popup_menu = Menu(self, tearoff=False)
        if self.can_config:
            self.popup_menu.add_command(label="Xóa", command=self.delete_subject)
        self.popup_menu.add_command(label="Đổi màu", command=self.change_color)
        self.popup_menu.add_command(label="Danh sách lớp", command=self.show_list_student)
        self.bind("<Button-3>", self.show_popup_menu)

    # list_data of one subject_id
    def get_data(self, data):
        self.subject_id = data[0]
        self.subject_name = data[1]
        self.credit = data[2]
        self.class_id = data[3]
        self.teacher_name = data[4]
        self.number_of_student = data[5]
        self.weekday = int(data[6])
        self.time = data[7].split("-")
        self.place = data[8]
        self.type = data[9]

        self.grid(column=self.weekday -1 if self.weekday !=0 else 7, row=self.time[0], rowspan=int(self.time[1]) - int(self.time[0]) + 1,
                  sticky="nsew")
        info = Balloon(self,bg="red")
        info.bind_widget(self, balloonmsg=self.get_info())
        info.message.config(bg="white")

    def get_info(self):
        return "Tên môn : {}\nMã môn học : {}\nGiảng viên : {}\nSố lượng sinh viên :{}\nTín chỉ : {}\nNhóm : {}".format(
            self.subject_name, self.class_id, self.teacher_name
            , self.number_of_student, self.credit, self.type)



    def show_popup_menu(self, event):
        self.popup_menu.tk_popup(event.x_root, event.y_root)

    def delete_subject(self):
        self.parent.subject_manager.delete(self.class_id)

    def set_color(self, color):
        self.configure(background=color)

    def show_list_student(self):
        top = Toplevel()
        top.grid_rowconfigure(0, weight=5)
        top.grid_rowconfigure(1, weight=95)
        top.grid_columnconfigure(0, weight=1)
        label = Label(top, text = self.get_info() + "\nTiết : {}-{}\n Thứ:{}".format(self.time[0],self.time[1],self.weekday))
        label.grid(row=0,column=0, sticky="nsew")
        student_table = StudentTable(top ,self.class_id).grid(row=1,column=0, sticky="nsew")
        top.geometry("1000x500")
    def change_color(self):
        subject_manager = self.parent.subject_manager
        color_manager = subject_manager.color_manager
        color_picker = colorchooser.askcolor()[1]
        print(color_picker)
        # kiem tra xem co mau nao trung voi mau da chon
        for class_id, color  in color_manager:
            if color == color_picker:
                print("error, Mau nay da duoc dung")
                break

        for i in range(len(color_manager)):
            if self.class_id == color_manager[i][0]:
                color_manager[i][1] = color_picker
                self.color = color_picker
        for subject in subject_manager.list_subject:
            if self.class_id == subject.class_id:
                subject.set_color(color_picker)
                subject.color = color_picker

    def save_data(self):
        data = {
            "subject_id" : str(self.subject_id),
            "subject_name" : str(self.subject_name),
            "credit" : str(self.credit),
            "class_id" : str(self.class_id),
            "teacher_name" : str(self.teacher_name),
            "number_of_student" : str(self.number_of_student),
            "weekday" : str(self.weekday),
            "time" : (str(self.time[0])+"-"+str(self.time[1])),
            "place" : str(self.place),
            "type" : str(self.type),
            "color" : str(self.color)
        }
        return data

    def partition(self, s):
        if len(s) <= 40:
            pos = s.find(" ", 20)
            if pos != -1:
                return s[0:pos] + "\n" + s[pos:]
            return s
        else:
            pos = s.find(" ", 20)
            if pos != -1:
                next_pos = s.find(" ", pos +20)
                return s[0:pos] + "\n" + s[pos: next_pos] + "\n" + s[next_pos:]
            return s
