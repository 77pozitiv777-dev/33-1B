from database.db_manager import DataBaseManager
from utils.menu import Menu

def main():
    db = DataBaseManager

    while True:
        choice = Menu.show_menu()

        if choice == '1':
            f = str(input('Name: '))
            l = str(input('Last name: '))
            a = int(input('Age: '))
            sid = int(input('Student ID: '))
            db.add_student(f, l, a, sid)

        elif choice == '2':
            for s in db.list_student():
                print(s)

        elif choice == '3':
            sid = int(input('Student ID: '))
            cid = int(input('Course ID: '))
            g = float(input('Grade:'))
            db.add_grade(sid, cid, g)

        elif choice == '4':
            for row in db.get_average_by_Course():
                print(f'{row[0]} - {row[1]:2f}')

        elif choice == '0':
            print('EXIT')
            break

        else:
            print('Error')
main()