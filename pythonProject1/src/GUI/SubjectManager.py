from tkinter import *
from tkinter import messagebox

from SQLManagement import SQLManagement
from Subject import Subject
class SubjectManager:

    def __init__(self, parent):
        # list subject_id
        self.list_subject = []
        self.sql_management = SQLManagement()
        self.color_manager = [] # [(class_id, hex color),...]
        self.parent = parent
        self.available_lesson = [[1 for x in range(7)] for x in range(14)] # 1 is free

    def create_list_subject(self, student_id, can_config):
        # search MSV -> list list_data
        # init subject_id
        list_data = self.sql_management.getStudentClasses(student_id)
        for i in list_data:
            print(i)
        for data in list_data:
            self.append(data, can_config)


    def append(self, data, can_config):
        # ('INT2211', 'Cơ sở dữ liệu', 4, 'INT2211 23', 'ThS.Lê Hoàng Quỳnh', 26, 2.0, '3-4', 'PM 307-G2', '2')
        if self.get_total_credit() >= 40:
            messagebox.showinfo("Error", "Số tín chỉ bạn đăng ký trong kỳ này \nđã vượt quá cho phép")
            return
        if len(data) == 11 and self.check_inputdata(data):  # list_data from json
            color = data[10]
            self.color_manager.append([data[3],color])
            new_subject = Subject(self.parent, data[0:10], color, can_config)
            self.list_subject.append(new_subject)
            return

        if self.check_inputdata(data):
            color = self.randomColor()
            # kiem tra xem co mon nay trong color_manager ko
            ck =True
            for i in self.color_manager:
                if i[0] == data[3]:
                    color = i[1]
                    ck = False
                    break
            if ck:
                c = [data[3], color]
                self.color_manager.append(c)
            new_subject = Subject(self.parent, data,color, can_config)
            self.list_subject.append(new_subject)

    def check_inputdata(self, data):
        # kiem tra mon hoc co bi trung thoi gian khong
        lesson = data[7].split("-")
        weekday = int(data[6]) if int(data[6]) != 0 else 8
        for i in range(int(lesson[0]), int(lesson[1]) + 1):
            if self.available_lesson[i - 1][weekday - 2] != 1:
                messagebox.showinfo("Error", "Từ tiết {} đến {} thứ {} đã có môn học được đăng ký".format(lesson[0], lesson[1], weekday if weekday != 0 else "CN"))
                return False
        # kiem tra xem du lieu dua vao co trung voi mon dang co
        for subject in self.list_subject:
            # môn học đã được đăng ký
            if data[3] == subject.class_id and data[9] == subject.type:
                messagebox.showinfo("Error","Lớp học{}-{} đã được đăng ký trước đó".format(data[3], data[1]))
                return False
            if data[3] == subject.class_id and data[9].isdigit() and subject.type.isdigit():
                messagebox.showinfo("Error", "Lớp học{}-{} đã được đăng ký trước đó".format(data[3], data[1]))
                return False
            if data[0] == subject.subject_id and data[3] != subject.class_id:
                messagebox.showinfo("Error", "Bạn đã đăng ký lớp học {}-{} \nnên không thể đăng ký lớp {}".format(subject.class_id, subject.subject_name,data[3]))
                return False

        for i in range(int(lesson[0]), int(lesson[1]) + 1):
            self.available_lesson[i - 1][weekday - 2] = 0
        return True

    def getinfo(self):
        for i in self.list_subject:
            pass

    def randomColor(self):
        import random
        ck = True
        color = None
        while ck:
            ck = False
            r = lambda: random.randint(0, 255)
            color = '#%02X%02X%02X' % (r(), r(), r())
            for c in self.color_manager:
                if c[1] == color:
                    ck =True
        return color

    def delete(self, class_id):
        d=[]
        for subject in self.list_subject:
            if class_id == subject.class_id:
                lesson = subject.time
                weekday = subject.weekday if subject.weekday !=0 else 8
                for i in range(int(lesson[0]), int(lesson[1]) + 1):
                    self.available_lesson[i-1][weekday - 2] = 1
                d.append(subject)
                subject.destroy()
        for i in d:
            self.list_subject.remove(i)
        for i in self.color_manager:
            if i[0] == class_id:
                self.color_manager.remove(i)
                break
        d.clear()

    def delete_all(self):
        for subject in self.list_subject:
            lesson = subject.time
            weekday = subject.weekday if subject.weekday != 0 else 8
            for i in range(int(lesson[0]), int(lesson[1]) + 1):
                self.available_lesson[i-1][weekday - 2] = 1
            subject.destroy()
        self.list_subject.clear()
        self.color_manager.clear()

    def __len__(self):
        return len(self.list_subject)

    def get_total_credit(self):
        total = 0
        a = []
        for subject in self.list_subject:
            if len(a) == 0 or subject.subject_id not in a:
                total += int(subject.credit)
                a.append(subject.subject_id)
        return total

    def get_total_free_time(self):
        """
        Bài toán:
        1100
        0100
        1101
        0101
        0 là có môn học, 1 khong có môn học
        :return số số 1 giữa số 0
        Thuật toán :
        tính tổng số 1
        sau đó duyệt theo chiều dọc từ trên xuống trừ đi 1 nếu gặp số 1,
         nếu gặp 0 mà chưa duyệt hết cột thì duyêt từ dưới lên trừ đi 1 nếu gặp số 1
        """
        cnt = 0
        for weekday in range(7):
            for i in range(14):
                if self.available_lesson[i][weekday] == 1:
                    cnt+=1
        for weekday in range(7):
            temp = 0
            for i in range(14):
                if self.available_lesson[i][weekday] == 1:
                    temp +=1
                else:
                    break
            if temp == 14:
                cnt -= temp
                continue
            for i in range(13,-1,-1):
                if self.available_lesson[i][weekday] == 1:
                    temp +=1
                else:
                    break
            cnt -= temp
        return cnt

    def save_data(self, data):
        for subject in self.list_subject:
            data.append(subject.save_data())

    def get_total_lesson(self):
        cnt = 0
        for weekday in range(7):
            for i in range(14):
                 if self.available_lesson[i][weekday] == 0:
                    cnt += 1
        return cnt


