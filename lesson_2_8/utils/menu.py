class Menu:
    @staticmethod
    def show_menu():
        print('''
            1) Add student
            2) Show all students
            3) Add mark
            4) Average grade for courses
            0) Exit
        ''')
        return input('Choose action: ')