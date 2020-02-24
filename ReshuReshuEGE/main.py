from tkinter import *
from tkinter import messagebox
from bs4 import BeautifulSoup as bs
import requests
import re

root = Tk()

#window parameters
root.title("ReshuReshuEGE")
#root.iconbitmap("icon.ico")

#window size
root.geometry('400x100')
root.resizable(False, False)

def Answer_root():
    with open("answers.txt") as work_list:
        content = work_list.read()
    root2 = Tk()
    root2.geometry('400x550')
    root2.title("Ответы")
    header2 = Label(root2, text="                       Ответы", font=("Ubuntu", 20))
    header2.grid(column=0, row=0)
    answers = Text(root2, width=30, height=30)
    answers.insert(INSERT, content)
    answers.configure(state='disabled')
    answers.grid(column=0, row=1)


#main func
def parse():
    """
    Parse answers using soup   
    """

    work_list = open("answers.txt", "w")

    url = var_entry.get()
    textlookfor = r"\w+"
    try:
        subject = re.findall(textlookfor, url)[1]
    except IndexError:
        messagebox.showerror("IndexError", "Неправильная ссылка!")
        return
    url_4_pars = requests.get(url)

    soup = bs(url_4_pars.text, 'lxml')
    task_list = soup.find_all("span", {"class":"prob_nums"})
    tasks = []
    for url in task_list:
        tasks.append("https://" + subject + "-ege.sdamgia.ru/problem?id=" + url.a.text)

    
    answers = []

    n = 0
    for i in range(len(tasks)):
        answer_url = requests.get(tasks[i])
        soup = bs(answer_url.text, 'lxml')
        answer = soup.find("div", {"class":"answer"})
        n += 1
        try:
            word = str(answer.span.text)
            line = str(n) + ") " + word[7:] + "\n"
            work_list.write(line)

            
            
        except AttributeError:
            line = str(n) + ") развернутый ответ\n"
            work_list.write(line)
    work_list.close()
    Answer_root()




header = Label(root, text="   Введите ссылку на вариант:", font=("Ubuntu", 20))
header.grid(column=0, row=0)

var_entry = Entry(root, width=40)
var_entry.grid(column=0, row=1)

parse_button = Button(root, text="Parse!", font=("Ubuntu", 10), command=parse)
parse_button.grid(column=0, row=2)



if __name__ == "__main__":
    root.mainloop()
