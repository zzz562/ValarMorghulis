import pandas as pd
import os
import tkinter as tk
from tkinter import scrolledtext, messagebox, font


# 读取标注文件
unlabel_file = 'high_school_biology_test.csv'

progress_file = f"{unlabel_file.split('.')[0]}_progress.csv"
result_file = f"{unlabel_file.split('.')[0]}_labeled.csv"
data = pd.read_csv(unlabel_file)

# 设置每次保存进度的条目数量
batch_size = 10

# 检查是否存在已标注的进度文件
try:
    progress = pd.read_csv(progress_file)
    last_index = progress.iloc[0]['last_index']
    continue_labeling = messagebox.askyesno("继续标注", "检测到上次有未完成的标注任务，是否继续？")

    if continue_labeling:
        start_index = last_index + 1
        messagebox.showinfo("继续标注", f"继续上次未完成的标注任务，当前进度：{start_index}/{len(data)}")
    else:
        start_index = 0
        messagebox.showinfo("开始标注", "开始新的标注任务...")
except FileNotFoundError:
    start_index = 0
    messagebox.showinfo("开始标注", "开始新的标注任务...")

# 创建Tkinter窗口
window = tk.Tk()
window.title("Labeling")
window.geometry("1150x1050+1920+0")

# 创建自定义字体
custom_font = font.Font(size=18)

# 创建列名标签
question_label = tk.Label(window, text="Question:", font=custom_font)
question_label.grid(row=0, column=0, sticky=tk.W)

options_label = tk.Label(window, text="Options:", font=custom_font)
options_label.grid(row=1, column=0, sticky=tk.W)

explanation_gpt4_label = tk.Label(window, text="Explanation (GPT-4):", font=custom_font)
explanation_gpt4_label.grid(row=2, column=0, sticky=tk.W)

answer_gpt4_label = tk.Label(window, text="Answer (GPT-4):", font=custom_font)
answer_gpt4_label.grid(row=3, column=0, sticky=tk.W)

answer_62b_label = tk.Label(window, text="Answer (62B):", font=custom_font)
answer_62b_label.grid(row=4, column=0, sticky=tk.W)

# 创建问题和选项的文本框
question_text = scrolledtext.ScrolledText(window, width=80, height=4, font=custom_font)
question_text.configure(state='disabled')
question_text.grid(row=0, column=1, columnspan=2)

options_text = scrolledtext.ScrolledText(window, width=80, height=4, font=custom_font)
options_text.configure(state='disabled')
options_text.grid(row=1, column=1, columnspan=2)

explanation_gpt4_text = scrolledtext.ScrolledText(window, width=80, height=25, font=custom_font)
explanation_gpt4_text.configure(state='disabled')
explanation_gpt4_text.grid(row=2, column=1, columnspan=2)

answer_gpt4_text = scrolledtext.ScrolledText(window, width=80, height=2, font=custom_font)
answer_gpt4_text.configure(state='disabled')
answer_gpt4_text.grid(row=3, column=1, columnspan=2)

answer_62b_text = scrolledtext.ScrolledText(window, width=80, height=2, font=custom_font)
answer_62b_text.configure(state='disabled')
answer_62b_text.grid(row=4, column=1, columnspan=2)

# 创建标注答案和解析的输入框
answer_label = tk.Label(window, text="标注答案（A/B/C/D）：", font=custom_font)
answer_label.grid(row=5, column=0, sticky=tk.E)
answer_entry = tk.Entry(window, width=60, font=custom_font)
answer_entry.grid(row=5, column=1)

analysis_label = tk.Label(window, text="标注解析：", font=custom_font)
analysis_label.grid(row=6, column=0, sticky=tk.E)
analysis_text = tk.Text(window, height=6, width=60, font=custom_font)
analysis_text.grid(row=6, column=1)

# 创建下一题、保存进度和退出按钮
def next_question():
    global start_index  # 修改此处

    # 获取标注结果
    labeled_answer = answer_entry.get()
    labeled_analysis = analysis_text.get()

    # 将标注结果写入数据帧
    data.at[start_index, 'labeled_answer'] = labeled_answer
    data.at[start_index, 'labeled_analysis'] = labeled_analysis

    start_index += 1

    # 清空输入框内容
    answer_entry.delete(0, tk.END)
    analysis_text.delete(0, tk.END)

    # 更新问题和选项
    if start_index < len(data):
        question_text.configure(state='normal')
        question_text.delete('1.0', tk.END)
        question_text.insert(tk.END, data.loc[start_index, 'question'])
        question_text.configure(state='disabled')

        options_text.configure(state='normal')
        options_text.delete('1.0', tk.END)
        options_text.insert(tk.END, '\n'.join([f"{chr(ord('A') + i)}: {option}" for i, option in enumerate(data.loc[start_index, ['A', 'B', 'C', 'D']])]))
        options_text.configure(state='disabled')

        explanation_gpt4_text.configure(state='normal')
        explanation_gpt4_text.delete('1.0', tk.END)
        explanation_gpt4_text.insert(tk.END, data.loc[start_index, 'explanation_gpt4'])
        explanation_gpt4_text.configure(state='disabled')

        answer_gpt4_text.configure(state='normal')
        answer_gpt4_text.delete('1.0', tk.END)
        answer_gpt4_text.insert(tk.END, data.loc[start_index, 'answer_gpt4'])
        answer_gpt4_text.configure(state='disabled')

        answer_62b_text.configure(state='normal')
        answer_62b_text.delete('1.0', tk.END)
        answer_62b_text.insert(tk.END, data.loc[start_index, 'answer_62b'])
        answer_62b_text.configure(state='disabled')

    else:
        messagebox.showinfo("标注完成", "题目已全部标注完成！")
        save_progress()

next_button = tk.Button(window, text="下一题", command=next_question, font=custom_font)
next_button.grid(row=7, column=0, pady=10)

def save_progress():
    # 保存标注结果到文件
    data.to_csv(result_file, index=False)

    # 删除进度文件
    if progress_file in os.listdir():
        os.remove(progress_file)

    messagebox.showinfo("保存进度", "标注进度已保存！")

    window.destroy()

save_button =tk.Button(window, text="保存进度", command=save_progress, font=custom_font)
save_button.grid(row=7, column=1, pady=10)

def close_window():
    exit_confirm = messagebox.askyesno("退出", "是否要退出标注程序？")
    if exit_confirm:
        # 保存标注结果到文件
        data.to_csv(result_file, index=False)

        # 删除进度文件
        if progress_file in os.listdir():
            os.remove(progress_file)

        window.destroy()

exit_button = tk.Button(window, text="退出", command=close_window, font=custom_font)
exit_button.grid(row=7, column=2, pady=10)

# 更新问题和选项
question_text.configure(state='normal')
question_text.delete('1.0', tk.END)
question_text.insert(tk.END, data.loc[start_index, 'question'])
question_text.configure(state='disabled')

options_text.configure(state='normal')
options_text.delete('1.0', tk.END)
options_text.insert(tk.END, '\n'.join([f"{chr(ord('A') + i)}: {option}" for i, option in enumerate(data.loc[start_index, ['A', 'B', 'C', 'D']])]))
options_text.configure(state='disabled')

explanation_gpt4_text.configure(state='normal')
explanation_gpt4_text.delete('1.0', tk.END)
explanation_gpt4_text.insert(tk.END, data.loc[start_index, 'explanation_gpt4'])
explanation_gpt4_text.configure(state='disabled')

answer_gpt4_text.configure(state='normal')
answer_gpt4_text.delete('1.0', tk.END)
answer_gpt4_text.insert(tk.END, data.loc[start_index, 'answer_gpt4'])
answer_gpt4_text.configure(state='disabled')

answer_62b_text.configure(state='normal')
answer_62b_text.delete('1.0', tk.END)
answer_62b_text.insert(tk.END, data.loc[start_index, 'answer_62b'])
answer_62b_text.configure(state='disabled')

# 启动Tkinter主循环
window.mainloop()

# 每标注一定数量的条目后保存进度
if (start_index + 1) % batch_size == 0:
    # 保存标注结果到文件
    data.to_csv(result_file, index=False)

    # 保存进度到文件
    progress = pd.DataFrame({'last_index': start_index})
    progress.to_csv(progress_file, index=False)