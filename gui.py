from tkinter import *
from tkinter import messagebox

root: any
email_input: any
password_input: any
submit_button: any
has_packed_widgets = False


def pack_all_widgets():
    email_input_label = Label(root, text='Login',
                              font='Comfortaa 20',
                              fg="#fff",
                              bg='#8ac5de', )
    global email_input
    email_input = Entry(root, font='Consolas 15',
                        fg="#8ac5de",
                        bg='#fff',
                        relief="groove",  # groove,solid,raised ,ridge ,sunken
                        justify='center')

    password_input_label = Label(root, text='Password',
                                 font='Comfortaa 20',
                                 fg='#fff',
                                 bg='#8ac5de', )
    global password_input
    password_input = Entry(root, font='Consolas 15',
                           fg="#8ac5de",
                           bg='#fff',
                           relief="groove",  # groove,solid,raised ,ridge ,sunken
                           justify='center',
                           show='*')

    remember_login_information = Checkbutton(root, text="Remember login information", variable=IntVar(), onvalue=1,
                                             offvalue=0,
                                             font='Comfortaa 12',
                                             bg='#8ac5de',
                                             fg='#c7eeff',
                                             activebackground='#8ac5de',
                                             activeforeground='#fff',
                                             )
    global submit_button
    submit_button = Button(root, text='Submit',
                           font='Consolas 13',
                           fg='#fff',
                           bg='#8ac5de',
                           # relief="solid",
                           activebackground='#8ac5de',
                           activeforeground='#fff',
                           )
    email_input_label.pack()
    email_input.pack()

    password_input_label.pack()
    password_input.pack()

    remember_login_information.pack()

    submit_button.pack()
    global has_packed_widgets
    has_packed_widgets = True


def get_user_login_info():
    # Window settings
    global root
    root = Tk()
    # root.resizable( width = False, height= False)
    root.geometry('500x500')
    root.title('Dima and Sander')
    root.wm_attributes('-alpha', 0.9)
    root['bg'] = '#8ac5de'

    email, password = "", ""

    pack_all_widgets()

    def check(event):
        user_email = email_input.get()
        user_password = password_input.get()

        if user_email and user_password:
            nonlocal email, password
            email = user_email
            password = user_password
            root.destroy()
            root.quit()
            return event
        if not user_email and user_password:
            messagebox.showerror('Error 0x1', 'Sisestage login!')
        elif not user_password and user_email:
            messagebox.showerror('Error 0x2', 'Sisestage salasõna', )

        if not user_email and not user_password:
            messagebox.showerror('Error 1x1', 'Sisestage login ja salasõna')

    submit_button.bind('<Button-1>', check)
    root.mainloop()
    return [email, password]


def destroy_root():
    root.destroy()


def lugemine(comparison_result):
    f = open(comparison_result, encoding="utf8")
    course_name = f.readline().strip().replace("->", "")
    i = 0
    test = ""
    vastus = ""
    for line in f:

        if line[0] == "=":
            line = line.strip().replace("=>", "").split(";")
            test_name = line[0]
            test_mark = line[1]
            test_max = line[2]
            test += "Test " + str(test_name) + ", hinne " + str(test_mark) + ", vehemik " + str(test_max) + "\n"
            i = 1
        elif line[0] == "-" and i == 1:
            vastus += course_name + "\n"
            vastus += test + "\n"
            test = ""

        if line[0] == "-":
            course_name = line.strip().replace("->", "")
            i = 0

    return vastus


def tulemused(comparison_result):
    # Window settings
    result_window = Tk()

    # root.resizable( width = False, height= False)
    # root.geometry('250x400')
    result_window.title('Dima and Sander')
    result_window.wm_attributes('-alpha', 0.9)
    result_window['bg'] = '#8ac5de'

    # Event
    hello = Label(result_window, text="Hello",
                  font='Comfortaa 20',
                  fg="#fff",
                  bg='#8ac5de', )

    d = lugemine(comparison_result)
    tekst = Label(result_window, text=d,
                  font="Conssolas 10",
                  fg="#fff",
                  bg='#8ac5de'
                  )

    # Packer
    hello.pack()
    tekst.pack()

    result_window.mainloop()
