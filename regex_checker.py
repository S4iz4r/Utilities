import re
import tkinter as tk


def examples():
    regex_entry.delete(0, "end")
    text_entry.delete('1.0', "end")
    regex_entry.insert(
        0, "((https?):((//)|(\\\\))+([a-zA-Z0-9\d:#@%/;$()~_?\+\-=\\\.&](#!)?)*)")
    text_entry.insert(
        '1.0', """This regex above is to check if URL exist in the text.
        
        This is an example text, this text contains emails, phone numbers and other sample designed for
        testing purposes. To use this tool, please type a regular expression in the text-area above.
        
        When designing regex for emails make sure you cover all possible email types like:
        info@breatheco.de, dragon23@gmail.com, dragon_ball@yahoo.com.us and also test for bad email
        formats like ramond=32@skas.com
        
        When texting for urls you have samples like this: https://thedomain.com.ve/dir1/dir2.html, some
        urls don't have extensions like this http://www.thedomain.net/directory1, maybe you will find some
        urls with nested subdomains like http://test.www.thedomain.com.ve/directory1
        
        Credits: Thanks to Florian Dedov for inspiring me to create this simple but entertaining project.
        Sample text extracted from: https://4geeks.com/lesson/regex-tutorial-regular-expression-examples""")
    find_matches('')


def find_matches(event):
    text_entry.tag_delete("match")
    error_label.config(text='')
    regex = regex_entry.get()
    text = text_entry.get(index1='1.0', index2='end-1c')

    if regex and text:
        try:
            matches = re.finditer(regex, text)
            for match in matches:
                start_index = f"1.0 + {match.start()} chars"
                end_index = f"1.0 + {match.end()} chars"
                text_entry.tag_add("match", start_index, end_index)
            if re.match(regex, text):
                text_entry.tag_config("match", foreground='black',
                                      background='orange', font=('Arial', 15, 'bold'))
            else:
                text_entry.tag_config("match", foreground='black',
                                      background='yellow', font=('Arial', 15, 'bold'))
        except Exception as e:
            error_label.config(text=e, fg='brown',
                               font=('Arial', 12, 'bold'))


root = tk.Tk()
root.title('Regex Checker')
menu_bar = tk.Menu()
menu_bar.add_command(label='Example Regex/Text', command=examples)
root.config(bg='grey', menu=menu_bar)


regex_label = tk.Label(root, text='Enter Regex:',
                       font=('Arial', 15, 'bold'), bg='grey', fg='black')
regex_label.grid(row=0, column=0, padx=5, pady=5)

regex_entry = tk.Entry(root, width=80, font=(
    'Arial', 15, 'bold'), bg='lightgrey', justify='center', fg='black')
regex_entry.grid(row=0, column=1, padx=5, pady=5, columnspan=2)
regex_entry.bind('<KeyRelease>', find_matches)

text_label = tk.Label(root, text='Enter Text:',
                      font=('Arial', 15, 'bold'), bg='grey', fg='black')
text_label.grid(row=1, column=0, padx=5, pady=5)

text_entry = tk.Text(root, width=80, height=20,
                     bg='lightgrey', font=('Arial', 15), fg='black')
text_entry.grid(row=1, column=1, padx=5, pady=5, columnspan=2)
text_entry.bind('<KeyRelease>', find_matches)

description = tk.Label(
    root, text='Description:', font=('Arial', 15, 'bold'), bg='grey', fg='black')
description.grid(row=2, column=0, padx=5, pady=5)
matches_description = tk.Label(root, text='Yellow background for all matches', font=(
    'Arial', 12, 'bold'), bg='yellow', fg='black')
matches_description.grid(row=2, column=1, padx=5, pady=5, sticky='e')
match_all_text = tk.Label(root, text='Orange background for whole text match', font=(
    'Arial', 12, 'bold'), bg='orange', fg='black')
match_all_text.grid(row=2, column=2, padx=5, pady=5, sticky='w')


error_label = tk.Label(root, bg='grey', font=('Arial', 12, 'bold'), fg='brown')
error_label.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

root.mainloop()
