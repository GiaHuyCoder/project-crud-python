import matplotlib.pyplot as plt
import mysql.connector

class Student():
    def __init__(self,id,name,age,major,gpa):
        self.id = id 
        self.name = name 
        self.age = age 
        self.major = major 
        self.gpa = gpa
        
    def __str__(self):
        return f"Id:{self.id},Name:{self.name},Age:{self.age},Major:{self.major},GPA:{self.gpa}"
    
students = []

menu = (
    ("1","Thêm sinh viên: "),
    ("2","Hiển thị danh sách: "),
    ("3","Xếp loại học sinh có điểm gpa >= 8: "),
    ("4","Tìm kiếm thông tin sinh viên theo ID: "),
    ("5","Sửa thông tin sinh viên: "),
    ("6","Ghi vào file: "),
    ("7","Vẽ biểu đồ GPA: "),
    ("8","Lưu danh sách vào Database: "),
    ("9","Xóa sinh viên theo ID: "),
    ("10","Thoát chương trình: ") 
)

def show_menu():
    print("\n=====Menu=====")
    for item in menu:
        print(item)
        
def add_student():
    try:
        id = input("Nhập ID: ")
        for student in students:
            if student.id == id:
                print("ID này đã có tồn tại trong danh sách!")
                return
        name = input("Nhập tên sinh viên: ")
        age = int(input("Nhập độ tuổi: "))
        major = input("Ngành theo học: ")
        gpa = float(input("GPA: "))
        if gpa >10 or gpa < 0:
            print("GPA phải nằm trong khoảng 0-10")
            return
        student = Student(id,name,age,major,gpa)
        students.append(student)
        print("Thêm sinh viên thành công")
    except Exception as e :
        print(f"Lỗi thêm sinh viên {e}")
        
def show_students():
    if not students:
        print("Không có sinh viên nào để hiển thị!")
        return
    for student in students:
        print(student)
        
def excellent_students():
    found = False
    for student in students:
        if student.gpa >= 8:
            print(student)
            found = True
    if not found:
        print("Không có sinh viên nào gpa lớn hơn và bằng 8")
        
def find_by_id():
    student_id = input("Nhập ID để tìm kiếm thông tin sinh viên: ") 
    found = False
    for student in students:
        if student.id == student_id:
            print(student)
            found = True
    if not found:
        print("Không có sinh viên theo ID")
        
def edit_student():
    student_id = input("Tìm kiếm ID muốn sửa: ")
    found = False
    for student in students:
        if student.id == student_id:
            print("Nhập thay đổi sinh viên ")
            new_id = input(f"ID: ({student.id}) ") or student.id
            new_name = input(f"Name: ({student.name})") or student.name
            age_input = input(f"Age: ({student.age})")
            if age_input.strip():
                new_age = int(age_input)
            else: 
                new_age = student.age
            new_major = input(f"Major: ({student.major}) ") or student.major
            gpa_input = input(f"GPA: ({student.gpa})")
            if gpa_input.strip():
                new_gpa = float(gpa_input)
            else:
                new_gpa = student.gpa
            
            student.id = new_id 
            student.name = new_name
            student.age =  new_age
            student.major = new_major
            student.gpa = new_gpa
            
            print("Cập nhật thành công!")
            found = True
            break
    if not found:
        print("ID nhập không tìm thấy sinmh viên nào!")
        
def save_to_file():
    with open("students.txt","w",encoding="utf-8") as f:
        for student in students:
            f.write(str(student) + "\n")
    print("Đã lưu file thành công!")
    
def draw_chart():
    try:
        if not students:
            print("Không có sinh viên nào để vẽ biểu đồ!")
            return
        names = [student.name for student in students]
        gpas = [student.gpa for student in students]
        
        plt.bar(names,gpas)
        plt.title("Biểu đồ điểm GPA của sinh viên")
        plt.xlabel("Tên sinh viên")
        plt.ylabel("GPA")
        plt.xticks(rotation=45)
        plt.show()
    except Exception as e:
        print(f"Lỗi khi tạo biểu đồ {e}")
        
def save_to_database():
    try:
        conn = mysql.connector.connect(
            host = "localhost",
            user="root",
            password="Password123",
            database="student_db"
        )
        cursor = conn.cursor()
        
        for student in students:
            sql = "INSERT INTO student (id,name,age,major,gpa) VALUES (%s,%s,%s,%s,%s)"
            values = (student.id,student.name,student.age,student.major,student.gpa)
            cursor.execute(sql,values)
            
        conn.commit()
        print("Lưu vào database thành công!")
        
    except mysql.connector.Error as e:
        print(f"Lỗi khi lưu vào database {e}")
        
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
   
def delete_student():
    student_id = input("Nhập ID sinh viên muốn xóa: ")
    found = False
    for student in students:
        if student_id == student.id:
            students.remove(student)
            found = True
            print("Xóa sinh viên thành công!")
            break
    if not found:
        print("Không tìm thấy ính viên với ID đã nhập!")
        
def exit():
    print("Thoát chương trình")
    return

while True:
    show_menu()
    choice = input("Nhập lựa chọn của bạn từ 1-10: ")
    if choice == "1":
        add_student()
    elif choice == "2":
        show_students()
    elif choice == "3":
        excellent_students()
    elif choice == "4":
        find_by_id()
    elif choice == "5":
        edit_student()
    elif choice == "6":
        save_to_file()
    elif choice == "7":
        draw_chart()
    elif choice == "8":
        save_to_database()
    elif choice == "9":
        delete_student()
    elif choice == "10":
        exit()
        break
    else:
        print("Nhập không hợp lệ menu từ 1-10!")
