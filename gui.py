from tkinter import *
from tkinter import messagebox

root: any
email_input: any
password_input: any
submit_button: any
user_information: list
# has_packed_widgets = False


def pack_all_widgets():
    email_input_label = Label(root, text='Login',
                              font='Comfortaa 20',
                              fg="#696464",
                              bg='#fff', )
    global email_input
    email_input = Entry(root, font='Consolas 15',
                        fg="#696464",
                        bg='#fff',
                        relief="groove",  # groove,solid,raised ,ridge ,sunken
                        justify='center')

    password_input_label = Label(root, text='Password',
                                 font='Comfortaa 20',
                                 fg='#696464',
                                 bg='#fff', )
    global password_input
    password_input = Entry(root, font='Consolas 15',
                           fg="#696464",
                           bg='#fff',
                           relief="groove",  # groove,solid,raised ,ridge ,sunken
                           justify='center',
                           show='*')

    remember_login_information = Checkbutton(root, text="Remember login information", variable=IntVar(), onvalue=1,
                                             offvalue=0,
                                             font='Comfortaa 12',
                                             bg='#fff',
                                             fg='#696464',
                                             activebackground='#fff',
                                             activeforeground='#fff',
                                             )
    global submit_button
    submit_button = Button(root,
                           text='SUBMIT',
                           fg='#fff',
                           bg='#696464',
                            activebackground = '#8ac5de',
                            activeforeground = '#fff'
                           )
    email_input_label.place(relx = 0.40,
                      rely = 0.20)

    email_input.place(relx = 0.18,
                      rely = 0.30)

    password_input_label.place(relx = 0.32,
                      rely = 0.40)

    password_input.place(relx = 0.18,
                      rely = 0.50)

    remember_login_information.place(relx = 0.17,
                      rely = 0.60)

    submit_button.place(relx = 0.41,
                        rely = 0.67,)

    # global has_packed_widgets
    # has_packed_widgets = True


def user_login_window():
    # Window settings
    global root
    root = Tk()
    root.resizable( width = False, height= False)
    root.geometry('350x500')
    root.title('Dima and Sander')

    # background image
    bgImage = PhotoImage(file=r"background_main.png")
    Label(root, image=bgImage).place(relwidth=1, relheight=1)

    # background line
    line = Label(root,
                 width = 33,
                 bg = "#fff")
    line.place(relx = 0.15,
               relwidth = 0.70,
               relheight = 1)


    email, password = "", ""

    pack_all_widgets()

    def check_input_fields(event):
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

    submit_button.bind('<Button-1>', check_input_fields)
    root.mainloop()
    global user_information
    user_information = [email, password]


def get_user_information():
    return user_information


def show_compared_results(result_file_name):
    # Window settings
    result_window = Tk()

    result_window.resizable( width = False, height= False)
    result_window.geometry('430x600')
    result_window.title('Dima and Sander')

    result_window['bg'] = '#8ac5de'

    #background img
    bgImage = PhotoImage(file=r"background_result.png")
    Label(result_window, image=bgImage).place(relwidth=1, relheight=1)

    # background line
    line = Label(result_window,
                 width=35,
                 bg="#fff")
    line.place(relx=0.125,
               relwidth=0.75,
               relheight=1)

    heading = Label(result_window, text="Here is your changes:",
                    font='Comfortaa 20',
                    fg="#696464",
                    bg='#fff', )

    def format_data_from_result_file():
        result_file = open(result_file_name, encoding="utf8")
        course_name = result_file.readline().strip().replace("->", "")
        i = 0
        test_data = ""
        formatted_result = ""
        for line in result_file:

            if line[0] == "=" and line.strip().split(";")[1] != "-":
                line = line.strip().replace("=>", "").split(";")
                test_name = line[0]
                test_mark = line[1]
                test_max = line[2]
                test_data += "Test " + str(test_name) + ", hinne " + str(test_mark) + ", vahemik " + str(
                    test_max) + "\n"
                i = 1
            elif line[0] == "-" and i == 1:
                formatted_result += course_name + "\n"
                formatted_result += test_data + "\n"
                test_data = ""

            if line[0] == "-":
                course_name = line.strip().replace("->", "")
                i = 0
        if i == 1:
            formatted_result += course_name + "\n"
            formatted_result += test_data + "\n"

        return formatted_result

    result_label = Text(result_window,
                        width = 35,
                        height = 20,
                        wrap = WORD,
                        font="Conssolas 13",
                        fg="#696464",
                        bg='#fff'
                        )

    result_label.insert(0.0, str(format_data_from_result_file()))

    #Scroll wighet
    scroll = Scrollbar (command = result_label.yview)
    scroll.pack(side = RIGHT, fill = Y)

    result_label.config(yscrollcommand = scroll.set)
    heading.place(relx = 0.19,
                  rely = 0.10)
    result_label.place(relx = 0.13,
                       rely = 0.23)

    result_window.mainloop()

