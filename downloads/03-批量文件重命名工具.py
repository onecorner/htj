"""
====================================
 批量文件重命名/整理工具
====================================
功能： 按规则批量重命名文件、自动分类整理
用法： 双击运行，选文件夹，配规则
适用： 照片整理、文档归档、下载文件整理

作者： AI编程助手
交付日期： 2024-06-07

客户需求：
  有2000张照片文件名混乱，需要按"日期_序号"统一重命名
====================================
"""

import os
import re
import tkinter as tk
from tkinter import filedialog, messagebox, ttk, scrolledtext
from datetime import datetime

class FileRenamer:
    def __init__(self, root):
        self.root = root
        self.root.title("批量文件重命名工具")
        self.root.geometry("600x500")

        # 文件夹选择
        tk.Label(root, text="目标文件夹:").pack(pady=5)
        self.folder_var = tk.StringVar()
        tk.Entry(root, textvariable=self.folder_var, width=50).pack()
        tk.Button(root, text="浏览...", command=self.select_folder).pack(pady=5)

        # 规则选择
        tk.Label(root, text="命名规则:").pack(pady=5)
        self.rule_var = tk.StringVar(value="序号_原文件名")
        rules = ["序号_原文件名", "日期_序号", "前缀_序号", "自定义(正则)"]
        for r in rules:
            tk.Radiobutton(root, text=r, variable=self.rule_var, value=r).pack()

        # 前缀输入
        tk.Label(root, text="自定义前缀(如: 旅行照片_):").pack()
        self.prefix_var = tk.StringVar()
        tk.Entry(root, textvariable=self.prefix_var, width=30).pack()

        # 预览按钮
        tk.Button(root, text="预览重命名结果", command=self.preview,
                  bg="lightblue").pack(pady=10)

        # 日志
        self.log = scrolledtext.ScrolledText(root, height=12)
        self.log.pack(fill=tk.BOTH, expand=True, padx=10)

        # 执行按钮
        tk.Button(root, text="✅ 执行重命名", command=self.execute,
                  bg="lightgreen", font=("", 12)).pack(pady=10)

        self.files = []

    def select_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.folder_var.set(folder)
            self.scan_files()

    def scan_files(self):
        folder = self.folder_var.get()
        self.files = [f for f in os.listdir(folder)
                     if os.path.isfile(os.path.join(folder, f))]
        self.log.insert(tk.END, f"📁 找到 {len(self.files)} 个文件\n")

    def generate_new_names(self):
        """根据规则生成新文件名"""
        folder = self.folder_var.get()
        prefix = self.prefix_var.get().strip()
        rule = self.rule_var.get()

        renamed = []
        for i, fname in enumerate(self.files, 1):
            ext = os.path.splitext(fname)[1]

            if rule == "序号_原文件名":
                new_name = f"{i:03d}_{fname}"
            elif rule == "日期_序号":
                date_str = datetime.now().strftime("%Y%m%d")
                new_name = f"{date_str}_{i:03d}{ext}"
            elif rule == "前缀_序号":
                new_name = f"{prefix}{i:03d}{ext}"
            else:
                new_name = f"{prefix}{i:03d}{ext}"

            renamed.append((fname, new_name))

        return renamed

    def preview(self):
        self.log.delete(1.0, tk.END)
        renamed = self.generate_new_names()
        self.log.insert(tk.END, "📋 预览重命名结果:\n" + "="*40 + "\n")
        for old, new in renamed[:50]:  # 最多显示50条
            self.log.insert(tk.END, f"  {old}  →  {new}\n")
        if len(renamed) > 50:
            self.log.insert(tk.END, f"  ... 还有 {len(renamed)-50} 个文件\n")
        self.log.insert(tk.END, f"\n共 {len(renamed)} 个文件待重命名\n")

    def execute(self):
        if not messagebox.askyesno("确认", "确定要执行重命名吗？此操作不可撤销！"):
            return

        folder = self.folder_var.get()
        renamed = self.generate_new_names()
        success = 0

        for old_name, new_name in renamed:
            old_path = os.path.join(folder, old_name)
            new_path = os.path.join(folder, new_name)

            # 如果目标文件名已存在，加序号避免覆盖
            if os.path.exists(new_path) and old_name != new_name:
                base, ext = os.path.splitext(new_name)
                n = 1
                while os.path.exists(os.path.join(folder, f"{base}_{n}{ext}")):
                    n += 1
                new_path = os.path.join(folder, f"{base}_{n}{ext}")

            try:
                os.rename(old_path, new_path)
                success += 1
            except Exception as e:
                self.log.insert(tk.END, f"❌ 失败: {old_name} - {e}\n")

        messagebox.showinfo("完成", f"成功重命名 {success}/{len(renamed)} 个文件")

if __name__ == "__main__":
    root = tk.Tk()
    app = FileRenamer(root)
    root.mainloop()
