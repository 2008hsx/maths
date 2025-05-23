import tkinter as tk
from tkinter import ttk
import random

class PlaceholderEntry(ttk.Entry):
    def __init__(self, master=None, placeholder="", **kwargs):
        super().__init__(master, **kwargs)
        self.placeholder = placeholder
        self.default_fg = self["foreground"]
        self.bind("<FocusIn>", self._clear_placeholder)
        self.bind("<FocusOut>", self._set_placeholder)
        self._set_placeholder()

    def _clear_placeholder(self, event=None):
        if self["foreground"] == "#999999":
            self.delete(0, tk.END)
            self["foreground"] = self.default_fg

    def _set_placeholder(self, event=None):
        if not self.get():
            self.insert(0, self.placeholder)
            self["foreground"] = "#999999"

    def get_clean(self):
        content = self.get()
        return "" if content == self.placeholder else content

def generate_all_samples():
    return [(i, j) for i in range(1, 7) for j in range(1, 7)]

def parse_event_description(description):
    if "第一次取出的球的数字是" in description:
        value = int(description.split("是")[-1])
        return lambda s: s[0] == value
    elif "第二次取出的球的数字是" in description:
        value = int(description.split("是")[-1])
        return lambda s: s[1] == value
    elif "两次取出的球的数字之和是" in description:
        value = int(description.split("是")[-1])
        return lambda s: s[0] + s[1] == value
    elif "两次取出的球的数字之积是" in description:
        value = int(description.split("是")[-1])
        return lambda s: s[0] * s[1] == value
    else:
        raise ValueError("不支持的事件格式")

def generate_random_event(is_event_a=True):
    """生成指定类型的事件"""
    if is_event_a:
        types = [
            ("第一次取出的球的数字是", "range", (1, 6)),
            ("两次取出的球的数字之和是", "range", (2, 12)),
            ("两次取出的球的数字之积是", "list", [1,2,3,4,5,6,8,9,10,12,15,16,18,20,24,25,30,36])
        ]
    else:
        types = [
            ("第二次取出的球的数字是", "range", (1, 6)),
            ("两次取出的球的数字之和是", "range", (2, 12)),
            ("两次取出的球的数字之积是", "list", [1,2,3,4,5,6,8,9,10,12,15,16,18,20,24,25,30,36])
        ]
    event_type = random.choice(types)
    value = random.randint(*event_type[2]) if event_type[1] == "range" else random.choice(event_type[2])
    return f"{event_type[0]}{value}"

class IndependenceApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("独立事件分析器")
        self.geometry("1024x725")  # 增加窗口高度
        self.configure(padx=20, pady=20)
        self.mode = tk.IntVar(value=1)
        self.create_widgets()
        self.update_events()

    def create_widgets(self):
        style = ttk.Style()
        style.configure('Big.TButton', font=('微软雅黑', 20), padding=8)
        style.configure('Big.TRadiobutton', font=('微软雅黑', 20))

        # 模式选择
        mode_frame = ttk.Frame(self)
        mode_frame.pack(pady=15)
        ttk.Label(mode_frame, text="选择模式：", font=('微软雅黑', 20)).grid(row=0, column=0, padx=5)
        ttk.Radiobutton(mode_frame, text="自动模式", variable=self.mode, value=1, 
                      command=self.update_events, style='Big.TRadiobutton').grid(row=0, column=1, padx=10)
        ttk.Radiobutton(mode_frame, text="手动模式", variable=self.mode, value=2,
                      command=self.update_events, style='Big.TRadiobutton').grid(row=0, column=2, padx=10)

        # 事件描述区域
        self.event_frame = ttk.LabelFrame(self, text=" 事件描述 ", padding=15)
        self.event_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        # 自动模式组件
        self.auto_frame = ttk.Frame(self.event_frame)
        self.generate_btn = ttk.Button(self.auto_frame, text="开始生成", command=self.generate_events, style='Big.TButton')
        self.lbl_a = ttk.Label(self.auto_frame, font=('微软雅黑', 20), wraplength=550)
        self.lbl_b = ttk.Label(self.auto_frame, font=('微软雅黑', 20), wraplength=550)

        # 手动模式组件
        self.manual_frame = ttk.Frame(self.event_frame)
        # 事件A输入组
        a_group = ttk.Frame(self.manual_frame)
        ttk.Label(a_group, text="事件A", font=('微软雅黑', 14)).pack(anchor=tk.W)
        self.entry_a = PlaceholderEntry(a_group, placeholder="在此输入事件A", 
                                     width=45, font=('微软雅黑', 20))
        self.entry_a.pack(pady=5)
        ttk.Label(a_group, 
                text="格式示例：\n1. 第一次取出的球的数字是1\n2. 两次取出的球的数字之和是7\n3. 两次取出的球的数字之积是12",
                font=('微软雅黑', 12),
                foreground="#666666",
                justify=tk.LEFT).pack(anchor=tk.W)
        a_group.pack(fill=tk.X, pady=10)

        # 事件B输入组
        b_group = ttk.Frame(self.manual_frame)
        ttk.Label(b_group, text="", font=('微软雅黑', 14)).pack(anchor=tk.W)
        self.entry_b = PlaceholderEntry(b_group, placeholder="在此输入事件B",
                                     width=45, font=('微软雅黑', 20))
        self.entry_b.pack(pady=5)
        ttk.Label(b_group,
                text="格式示例：\n1. 第二次取出的球的数字是4\n2. 两次取出的球的数字之和是9\n3. 两次取出的球的数字之积是18",
                font=('微软雅黑', 12),
                foreground="#666666",
                justify=tk.LEFT).pack(anchor=tk.W)
        b_group.pack(fill=tk.X, pady=10)

        # 操作按钮
        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=15)
        self.analyze_btn = ttk.Button(btn_frame, text="分析独立性", command=self.analyze,
                                    style='Big.TButton', state=tk.DISABLED)
        self.analyze_btn.grid(row=0, column=0, padx=10)
        
        # 结果展示
        self.result_label = ttk.Label(self, text="等待操作...", font=('微软雅黑', 20, 'bold'))
        self.result_label.pack(pady=20)

    def update_events(self):
        for widget in self.event_frame.winfo_children():
            widget.pack_forget()
        
        if self.mode.get() == 1:
            self.auto_frame.pack(fill=tk.BOTH, expand=True)
            self.generate_btn.pack(pady=10)
            self.analyze_btn.config(state=tk.DISABLED)
            self.result_label.config(text="请先点击「开始生成」按钮")
        else:
            self.manual_frame.pack(fill=tk.BOTH, expand=True)
            self.analyze_btn.config(state=tk.NORMAL)
            self.result_label.config(text="等待分析...")

    def generate_events(self):
        try:
            self.event_a = generate_random_event(is_event_a=True)
            self.event_b = generate_random_event(is_event_a=False)
            self.lbl_a.config(text=f"事件A：{self.event_a}")
            self.lbl_b.config(text=f"事件B：{self.event_b}")
            self.lbl_a.pack(pady=5)
            self.lbl_b.pack(pady=5)
            self.analyze_btn.config(state=tk.NORMAL)
            self.result_label.config(text="已生成事件，可点击分析")
        except Exception as e:
            self.result_label.config(text=f"生成错误：{str(e)}")

    def analyze(self):
        try:
            if self.mode.get() == 1:
                a_desc, b_desc = self.event_a, self.event_b
            else:
                a_desc = self.entry_a.get_clean()
                b_desc = self.entry_b.get_clean()
                if not a_desc or not b_desc:
                    raise ValueError("请输入有效的事件描述")
                
                # 验证事件描述
                if "第二次" in a_desc:
                    raise ValueError("事件A必须与第一次取出相关")
                if "第一次" in b_desc:
                    raise ValueError("事件B必须与第二次取出相关")

            a_func = parse_event_description(a_desc)
            b_func = parse_event_description(b_desc)
            samples = generate_all_samples()
            count_ab = sum(1 for s in samples if a_func(s) and b_func(s))
            prob_ab = count_ab / 36
            prob_a = sum(1 for s in samples if a_func(s)) / 36
            prob_b = sum(1 for s in samples if b_func(s)) / 36
            
            is_independent = abs(prob_ab - prob_a*prob_b) < 1e-9
            result_text = "结论：事件相互独立 ✅" if is_independent else "结论：事件不独立 ❌"
            color = "#00AA00" if is_independent else "#FF0000"
            self.result_label.config(text=result_text, foreground=color)
            
        except Exception as e:
            self.result_label.config(text=f"分析错误：{str(e)}", foreground="#FF0000")

if __name__ == "__main__":
    app = IndependenceApp()
    app.mainloop()
