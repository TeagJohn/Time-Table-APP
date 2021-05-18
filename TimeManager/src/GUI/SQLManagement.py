import json
import os

import mysql.connector
from mysql.connector import Error

class SQLManagement:

    def __init__(self):
        data = self.get_config()
        self.conn = mysql.connector.connect(host=data["host"], user=data["user"], port=data["port"], database=data["database"])
        self.connectDB()

    def connectDB(self):
        self.cur = self.conn.cursor()

    def getStudentClasses(self,student_id):
        print("sql")
        query ='''SELECT subject.subject_id, subject.subject_name, subject.credit,
            class.class_id, class.teacher_name, class.number_of_students
            ,class.weekday, class.lesson, class.place, class.`type`
            FROM students JOIN listsubject ON students.`student_id` = listsubject.`student_id`
            JOIN subject ON subject.`subject_id` = listsubject.`subject_id`
            JOIN class ON class.class_id = listsubject.class_id 
            WHERE students.student_id = {} AND listsubject.type = class.type'''.format(student_id)
        self.cur.execute(query)
        s = self.cur.fetchall()
        return s

    def find(self, input, findOption, sortOption, is_DESC, is_CLC):
        option = ["class.subject_id", "subject.subject_name", "subject.credit", "class.class_id",
                  "class.teacher_name", "class.number_of_students", "class.time", "class.weekday",
                  "lesson", "place", "note"]
        query = '''SELECT class.subject_id, subject.subject_name, subject.credit, 
                    class.class_id,class.teacher_name, class.number_of_students, 
                    class.time, class.weekday, class.lesson, class.place, class.type
                    FROM `class`  JOIN subject ON class.subject_id = subject.subject_id
                    '''
        if findOption == 8:
            start = 1
            end = 14
            if "-" in input:
                time = input.split("-")
                start = time[0]
                end = time[1]
            elif len(input) > 0:
                start = input
            query+=""" WHERE LEFT(`lesson`,LOCATE('-',`lesson`)-1) >= {} 
	AND RIGHT(`lesson`,LENGTH(`lesson`)-LOCATE('-',`lesson`)) <={} 
            """.format(start, end)

        else:
            if len(input) >2 :
                query += " WHERE {} LIKE '{}' ".format(option[findOption], input)

        if is_CLC:
            query += " AND (subject.`subject_id` LIKE '%PES%' OR class.weekday = 0 OR RIGHT(class.`class_id`,2) >= 20) "
        else:
            query += "AND (subject.`subject_id` LIKE '%PES%' OR class.weekday = 0 OR RIGHT(class.`class_id`,2) < 20) "
        query += " ORDER BY {} ".format(option[sortOption])
        if is_DESC:
            query += "DESC"


        print(query)
        self.cur.execute(query)
        s = self.cur.fetchall()
        return s

    def get_list_students(self, class_id):
        query = '''SELECT students.student_id, students.student_name, students.DOB, students.student_class 
FROM students  JOIN listsubject  on students.`student_id` = listsubject.`student_id`
WHERE listsubject.class_id = "{}"
GROUP BY students.student_id ORDER BY students.student_id'''.format(class_id)
        self.cur.execute(query)
        s = self.cur.fetchall()
        return s

    def get_list_class(self):
        query = '''SELECT class.subject_id, subject.subject_name, subject.credit, 
            class.class_id,class.teacher_name, class.number_of_students, 
            class.time, class.weekday, class.lesson, class.place, class.type
            FROM `class`  JOIN subject ON class.subject_id = subject.subject_id
            ORDER BY `weekday` DESC,`lesson`DESC'''
        self.cur.execute(query)
        s = self.cur.fetchall()
        return s

    def get_student(self, student_id):
        query = '''SELECT * FROM `students` WHERE student_id = {}'''.format(student_id)
        self.cur.execute(query)
        s = self.cur.fetchall()
        return s

    def get_suggested_data(self, course):
        query = '''SELECT class.subject_id, subject.subject_name, subject.credit, 
            class.class_id,class.teacher_name, class.number_of_students, 
            class.time, class.weekday, class.lesson, class.place, class.type
	        FROM students JOIN listsubject on students.`student_id` = listsubject.`student_id`
	        JOIN subject ON subject.`subject_id` = listsubject.`subject_id`
	        JOIN class ON class.class_id = listsubject.class_id
	        WHERE students.student_class LIKE {}
	        GROUP BY class.class_id
    	    ORDER BY subject.subject_name,class.`weekday`, class.`lesson`'''.format(course)
        self.cur.execute(query)
        s = self.cur.fetchall()
        return s

    def close(self):
        self.conn.close()
        self.cur.close()

    def get_config(self):
        dataPath = None
        try:
            absFilePath = os.path.abspath(__file__)
            projectPath = absFilePath
            for i in range(3):
                projectPath = os.path.dirname(projectPath)
            dataPath = projectPath + "/res/Data/config.json"

        except FileNotFoundError:
            print("không tìm thấy file config.json")
        with open(dataPath, 'r') as file:
            d = file.read()
            data = json.loads(d)
        return data


