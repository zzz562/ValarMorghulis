import pandas as pd
import os
import threading
import tkinter as tk
from tkinter import scrolledtext, messagebox, font




# 读取标注文件
unlabel_file = 'high_school_chemistry_test.csv'
progress_file = f"{unlabel_file.split('.')[0]}_progress.csv"
result_file = f"{unlabel_file.split('.')[0]}_labeled.csv"

# 设置每次保存进度的条目数量
batch_size = 10

# 检查是否存在已标注的进度文件
try:
    progress = pd.read_csv(progress_file)
    last_index = progress.iloc[-1]['last_index']
    continue_labeling = messagebox.askyesno("继续标注", "检测到上次有未完成的标注任务，是否继续？")

    if continue_labeling:
        # 如果决定继续标注，则加载包含已标注数据的文件
        data = pd.read_csv(result_file)
        start_index = last_index
        messagebox.showinfo("继续标注", f"继续上次未完成的标注任务，当前进度：{start_index}/{len(data)}")
    else:
        # 如果不继续，则重新开始标注任务，读取result 文件 从头开始浏览。
        data = pd.read_csv(result_file)
        start_index = 0
        messagebox.showinfo("开始标注", "开始新的标注任务...")
except FileNotFoundError:
    # 如果没有进度文件，则加载原始未标注数据
    data = pd.read_csv(unlabel_file)
    start_index = 0
    messagebox.showinfo("开始标注", "开始新的标注任务...")


### 在右侧屏幕2上显示：
# 创建Tkinter窗口
window = tk.Tk()
window.title("Labeling")

# 手动设置屏幕2的分辨率
screen2_width = 2560  # 屏幕2的宽度
screen2_height = 1440  # 屏幕2的高度

# 计算窗口的理想大小
window_width = 1100
window_height = 1250

# 计算x和y坐标以使窗口居中在屏幕2
# 假设屏幕2紧跟在屏幕1的右侧
x_coordinate = int(screen2_width*0.75)  # 您可能需要根据实际情况调整这个值
y_coordinate = int((screen2_height/2) - (window_height))

# 设置窗口的尺寸和位置
window.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")

### 在主屏幕上显示
# # 创建Tkinter窗口
# window = tk.Tk()
# window.title("Labeling")
#
# # 获取屏幕宽度和高度
# screen_width = window.winfo_screenwidth()
# screen_height = window.winfo_screenheight()
#
# # 计算窗口的理想大小（例如屏幕大小的75%）
# window_width = 1100
# window_height = 1200
#
# # 计算x和y坐标以使窗口居中
# x_coordinate = int((screen_width/2) - (window_width/2))
# y_coordinate = int((screen_height/2) - (window_height/2))
#
# # 设置窗口的尺寸和位置
# window.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")



# 创建自定义字体
custom_font = font.Font(size=18)

# 创建列名标签和配置函数
def create_label(text, row, column, sticky):
    label = tk.Label(window, text=text, font=custom_font)
    label.grid(row=row, column=column, sticky=sticky)
    return label

question_label = create_label("Question:", 0, 0, tk.W)
options_label = create_label("Options:", 1, 0, tk.W)
explanation_gpt4_label = create_label("Explanation (GPT-4):", 2, 0, tk.W)
answer_gpt4_label = create_label("Answer (GPT-4):", 3, 0, tk.W)
answer_62b_label = create_label("Answer (62B):", 4, 0, tk.W)
answer_label = create_label("标注答案（A/B/C/D）：", 5, 0, tk.W)
analysis_label = create_label("标注解析：", 6, 0, tk.W)

# 创建文本框和配置函数
def create_text_widget(row, height):
    text_widget = scrolledtext.ScrolledText(window, width=80, height=height, font=custom_font)
    text_widget.configure(state='disabled', wrap='word')
    text_widget.grid(row=row, column=1, columnspan=2, sticky='ew')
    window.grid_rowconfigure(row, weight=1)
    return text_widget

question_text = create_text_widget(0, 4)
options_text = create_text_widget(1, 4)
explanation_gpt4_text = create_text_widget(2, 25)
answer_gpt4_text = create_text_widget(3, 2)
answer_62b_text = create_text_widget(4, 2)



# 创建输入框
answer_entry = tk.Entry(window, width=60, font=custom_font)
answer_entry.grid(row=5, column=1)

analysis_text = tk.Text(window, height=4, width=60, font=custom_font)
analysis_text.grid(row=6, column=1)

# 总题目数量
total_questions = len(data)

# 创建一个框架来容纳输入框和标签
jump_frame = tk.Frame(window)
jump_frame.grid(row=5, column=2, sticky=tk.W)

# 创建输入框，供用户输入想要跳转到的题目序号
jump_to_entry = tk.Entry(jump_frame, width=5, font=custom_font)
jump_to_entry.pack(side=tk.LEFT)

# 显示总题数的标签
total_questions_label = tk.Label(jump_frame, text=f"/{total_questions}", font=custom_font)
total_questions_label.pack(side=tk.LEFT)

# 创建跳转按钮的功能
def jump_to():
    global start_index
    try:
        # 减1是因为用户输入的是从1开始的题号，但索引是从0开始的
        jump_index = int(jump_to_entry.get()) - 1
        if 0 <= jump_index < total_questions:
            start_index = jump_index
            update_widgets()
        else:
            messagebox.showerror("错误", "输入的题号超出范围。")
    except ValueError:
        messagebox.showerror("错误", "请输入有效的题号。")

# 创建跳转按钮，并放入框架中
jump_button = tk.Button(jump_frame, text="跳转", command=jump_to, font=custom_font)
jump_button.pack(side=tk.LEFT)

# 创建按钮和它们的功能
def save_progress():
    # 保存标注结果到文件
    data.to_csv(result_file, index=False)
    # 保存进度到文件
    progress = pd.DataFrame({'last_index': [start_index]})
    progress.to_csv(progress_file, index=False)
    messagebox.showinfo("保存进度", "标注进度已保存！")

def close_window():
    if messagebox.askyesno("退出", "是否要退出标注程序？"):
        save_progress()
        window.destroy()


# 创建一个框架来容纳“上一题”和“下一题”按钮
navigation_frame = tk.Frame(window)
navigation_frame.grid(row=7, column=1, pady=10, sticky=tk.EW)  # 使用sticky=tk.EW使得框架扩展到整个列宽

# “上一题”按钮
prev_button = tk.Button(navigation_frame, text="上一题", command=lambda: prev_question(), font=custom_font)
prev_button.pack(side=tk.LEFT, expand=True)

# “下一题”按钮
next_button = tk.Button(navigation_frame, text="下一题", command=lambda: next_question(), font=custom_font)
next_button.pack(side=tk.RIGHT, expand=True)

# “保存进度”按钮
save_button = tk.Button(window, text="保存进度", command=lambda: save_progress(), font=custom_font)
save_button.grid(row=7, column=0, pady=10)

# “退出”按钮
exit_button = tk.Button(window, text="退出", command=lambda: close_window(), font=custom_font)
exit_button.grid(row=7, column=2, pady=10)

# 创建复制问题和选项的按钮
copy_button = tk.Button(window, text="复制问题和选项", command=lambda: copy_question_options(), font=custom_font)
copy_button.grid(row=6, column=2, pady=10)


def update_ui_elements(question_text_content, options_text_content,
                       explanation_gpt4_text_content, answer_gpt4_text_content,
                       answer_62b_text_content):

    # 一次性更新文本框，减少状态切换
    for text_widget, content in [(question_text, question_text_content),
                                 (options_text, options_text_content),
                                 (explanation_gpt4_text, explanation_gpt4_text_content),
                                 (answer_gpt4_text, answer_gpt4_text_content),
                                 (answer_62b_text, answer_62b_text_content)]:
        text_widget.configure(state='normal')
        text_widget.delete('1.0', tk.END)
        text_widget.insert(tk.END, content)
        text_widget.configure(state='disabled')

    # 清空并更新标注答案和标注解析的输入框
    answer_entry.delete(0, tk.END)
    labeled_answer = data.loc[start_index, 'labeled_answer']
    if not pd.isna(labeled_answer):
        answer_entry.insert(0, labeled_answer)

    analysis_text.delete('1.0', tk.END)
    labeled_analysis = data.loc[start_index, 'labeled_analysis']
    if not pd.isna(labeled_analysis):
        analysis_text.insert(tk.END, labeled_analysis)

    jump_to_entry.delete(0, tk.END)
    jump_to_entry.insert(0, start_index + 1)

    # 强制更新UI
    window.update()      # 或者可以使用 window.update_idletasks()

def update_data():
    # 获取当前题目的数据
    current_question_data = data.loc[start_index]

    # 构建需要插入的文本
    question_text_content = current_question_data['question']
    options_text_content = '\n'.join([f"{chr(ord('A') + i)}: {option}" for i, option in enumerate(current_question_data[['A', 'B', 'C', 'D']])])
    explanation_gpt4_text_content = current_question_data['explanation_gpt4']
    answer_gpt4_text_content = current_question_data['answer_gpt4']
    answer_62b_text_content = current_question_data['answer_62b']

    # 更新UI元素（注意：所有对UI的操作都应该在主线程中执行）
    window.after(0, lambda: update_ui_elements(
        question_text_content,
        options_text_content,
        explanation_gpt4_text_content,
        answer_gpt4_text_content,
        answer_62b_text_content
    ))


# 功能：更新文本框内容和保存进度
def update_widgets():

    # 启动后台线程来更新数据
    threading.Thread(target=update_data).start()

    # 获取当前题目的数据
    current_question_data = data.loc[start_index]


# 功能：前往上一问题：
def prev_question():
    global start_index
    if start_index > 0:
        start_index -= 1
        update_widgets()
    else:
        messagebox.showinfo("信息", "已经是第一题了。")

# 功能：前往下一问题
def next_question(save=True):
    global start_index
    if save:
        # 获取标注结果并更新数据帧
        labeled_answer = answer_entry.get()
        if not labeled_answer:
            messagebox.showerror("错误", "标注答案不能为空。")
            return
        labeled_analysis = analysis_text.get("1.0", tk.END)
        data.at[start_index, 'labeled_answer'] = labeled_answer
        data.at[start_index, 'labeled_analysis'] = labeled_analysis

        # 清空输入框
        answer_entry.delete(0, tk.END)
        analysis_text.delete('1.0', tk.END)

    # 增加索引并检查是否完成
    start_index += 1
    if start_index < len(data):
        update_widgets()
    else:
        messagebox.showinfo("标注完成", "题目已全部标注完成！")
        save_progress()

    # 检查是否需要保存进度
    if start_index % batch_size == 0 and save:
        save_progress()

# 复制问题和选项到剪贴板的函数
def copy_question_options():
    # 获取问题文本
    question = question_text.get("1.0", tk.END).strip()
    # 获取选项文本
    options = options_text.get("1.0", tk.END).strip()
    # 格式化文本
    text_to_copy = f"{question}\n\n{options}"
    # 复制到剪贴板
    window.clipboard_clear()  # 清除剪贴板内容
    window.clipboard_append(text_to_copy)  # 添加新内容到剪贴板
    window.update()  # 现在更新剪贴板的内容
    messagebox.showinfo("复制成功", "问题和选项已复制到剪贴板。")



# 启动程序和更新初始文本框内容
update_widgets()
window.mainloop()
