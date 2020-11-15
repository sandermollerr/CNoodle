from login import *
from gui import *
import glob

if __name__ == '__main__':
    open_browser_with_driver()
    while True:
        navigate_to_login_page()
        user_information = get_user_login_info()
        status = get_login_status(user_information[0], user_information[1])

        # Different status codes:
        #   successfully logged in: __utmc
        #   invalid email: buid, MSPRequ
        #   invalid password: esctx

        if status == "__utmc":
            links = get_course_links()
            read_data_from_moodle_into_file(links)
            files_history = glob.glob(".\\history\\*.txt")

            # Checks if history directory contains previous history files
            if len(files_history) >= 2:
                # print(files_history)
                compare_files(files_history[-1], files_history[0])
                show_compared_results("./result/result.txt")
            else:
                print("All grades synced!")

        elif status in ["buid", "MSPRequ"]:
            messagebox.showerror('Error 1x1', 'Invalid email!')
            continue
        elif status == "esctx":
            messagebox.showerror('Error 1x1', 'Invalid password!')
            continue
        else:
            messagebox.showerror('Error 1x1', 'Something went very wrong!')
            print(status)
            exit()
            break
        break
