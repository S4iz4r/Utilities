import re
import tkinter as tk


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
root.config(bg='grey')


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

text_entry = tk.Text(root, width=80, height=15,
                     bg='lightgrey', font=('Arial', 15), fg='black')
text_entry.grid(row=1, column=1, padx=5, pady=5, columnspan=2)
text_entry.bind('<KeyRelease>', find_matches)

description = tk.Label(
    root, text='Description:', font=('Arial', 15, 'bold'), bg='grey', fg='black')
description.grid(row=2, column=0, padx=5, pady=5)
matches_description = tk.Label(root, text='Yellow background for all matches', font=(
    'Arial', 12, 'bold'), bg='yellow', fg='black')
matches_description.grid(row=2, column=1, padx=5, pady=5, sticky='e')
match_all_text = tk.Label(root, text='Orange background for specific match', font=(
    'Arial', 12, 'bold'), bg='orange', fg='black')
match_all_text.grid(row=2, column=2, padx=5, pady=5, sticky='w')


error_label = tk.Label(root, bg='grey', font=('Arial', 12, 'bold'), fg='brown')
error_label.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

root.mainloop()
