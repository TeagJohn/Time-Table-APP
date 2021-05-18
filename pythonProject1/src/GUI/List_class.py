from tkinter.ttk import *
from tkinter import *
from SQLManagement import SQLManagement

class TableSubject(Treeview):
    def __init__(self, parent):
        Treeview.__init__(self, parent)
        self.HEADING = ( "Mã môn học", "Tên Môn học", "Tín",
                       "Mã lớp môn học", "Giảng viên", "Số lượng học sinh",
                       "Buổi", "Thứ", "Tiết", "Địa điểm", "Nhóm")
        self.initUI()
        self.sql_manager = SQLManagement()
        self.suggested_data = None
        #self.read_json_file()
        self.insert_data(self.get_data_from_sql())
    def initUI(self):
        style = Style()
        # configure color
        style.configure("Treeview",
                        backgound="#D3D3D3",
                        foreground="black",
                        rowheight=30,
                        fieldbackground="#D3D3D3"
                        )
        style.map("Treeview",
                  background=[('selected', "#347083")])
        # create scrollbar
        tree_scroll = Scrollbar(self)
        tree_scroll.pack(side=RIGHT, fill=Y)
        self.configure(yscrollcommand=tree_scroll.set, selectmode="extended")
        tree_scroll.configure(command=self.yview)
        self.tag_configure('oddrow', background="white")
        self.tag_configure('evenrow', background="lightblue")
        self['columns'] = self.HEADING
        # formate the columns
        self.column("#0", width=0, stretch=NO)
        for heading in self.HEADING:
            self.column(heading, width=1, anchor=CENTER)

        # create heading
        self.heading("#0", anchor=CENTER, text="")
        for heading in self.HEADING:
            self.heading(heading, text=heading, anchor=CENTER)

    def insert_data(self, data):
        count = 0
        for i in data:
            if count % 2 == 0:
                self.insert(parent='', index='end', iid=count, values=i, tag=('evenrow'))
            else:
                self.insert(parent='', index='end', iid=count, values=i, tag=('oddrow'))
            count += 1

    def find(self, input, findOption, sortOption, is_DESC, is_CLC):
        self.remove_all()
        from App import OPTION
        intFindOption = 0
        intSortOption = 0
        for i in range(11):
            if findOption == OPTION[i]:
                intFindOption = i

                break
        for i in range(11):
            if sortOption == OPTION[i]:
                intSortOption = i
                break
        if intFindOption != 8:
            input = "%" + input + "%"

        list_data = self.sql_manager.find(input, intFindOption, intSortOption,is_DESC, is_CLC)
        self.insert_data(list_data)

    def remove_all(self):
        for record in self.get_children():
            self.delete(record)

    def get_data_from_sql(self):
        return list(self.sql_manager.get_list_class())

    def get_selected_data(self):
        selected = self.selection()
        value = []
        print(1, selected)
        for s in selected:
            d = self.item(s, 'values')
            data = d[0:6]+ d[7:]
            value.append(data)
            print(data)
        return value

    def get_suggested_data(self, course):
        course ="\"" + (course[0:len(course)-1] +"%")+"\""

        self.suggested_data = self.sql_manager.get_suggested_data(course)


    def set_suggestion(self):
        self.insert_data(self.suggested_data)



class StudentTable(Treeview):

    def __init__(self, parent, class_id):
        Treeview.__init__(self, parent)
        self.HEADING = ( "Mã sinh viên", "Họ và tên", "Ngày sinh",
                       "Lớp khóa học")
        self.sql_manager = SQLManagement()
        self.initUI()
        self.insert_data(self.sql_manager.get_list_students(class_id))
    def initUI(self):
        style = Style()
        # configure color
        style.configure("Treeview",
                        backgound="#D3D3D3",
                        foreground="black",
                        rowheight=30,
                        fieldbackground="#D3D3D3"
                        )
        style.map("Treeview",
                  background=[('selected', "#347083")])
        # create scrollbar
        tree_scroll = Scrollbar(self)
        tree_scroll.pack(side=RIGHT, fill=Y)
        self.configure(yscrollcommand=tree_scroll.set, selectmode="extended")
        tree_scroll.configure(command=self.yview)
        self.tag_configure('oddrow', background="white")
        self.tag_configure('evenrow', background="lightblue")
        self['columns'] = self.HEADING
        # formate the columns
        self.column("#0", width=0, stretch=NO)
        for heading in self.HEADING:
            self.column(heading, width=1, anchor=CENTER)

        # create heading
        self.heading("#0", anchor=CENTER, text="")
        for heading in self.HEADING:
            self.heading(heading, text=heading, anchor=CENTER)

    def insert_data(self, data):
        count = 0
        for i in data:
            if count % 2 == 0:
                self.insert(parent='', index='end', iid=count, values=i, tag=('evenrow'))
            else:
                self.insert(parent='', index='end', iid=count, values=i, tag=('oddrow'))
            count += 1

