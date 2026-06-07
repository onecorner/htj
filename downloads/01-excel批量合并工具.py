"""
====================================
 Excel 批量合并工具
====================================
功能： 把多个Excel文件自动合并成一个
用法： 把脚本放在Excel文件夹里，双击运行
适用： 月报汇总、数据整合、部门报表合并

作者： AI编程助手
交付日期： 2024-06-07

客户需求：
  有50个分店的销售Excel，需要合并成一个总表
====================================
"""

import pandas as pd
import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import glob

def merge_excel_files():
    """选择文件夹，合并里面所有Excel"""
    # 创建窗口让用户选文件夹
    root = tk.Tk()
    root.withdraw()  # 隐藏主窗口

    folder = filedialog.askdirectory(title="选择存放Excel文件的文件夹")
    if not folder:
        return

    # 找所有Excel文件
    excel_files = glob.glob(os.path.join(folder, "*.xlsx")) + \
                  glob.glob(os.path.join(folder, "*.xls"))

    if not excel_files:
        messagebox.showwarning("提示", "该文件夹下没有找到Excel文件！")
        return

    all_data = []
    for f in excel_files:
        try:
            df = pd.read_excel(f)
            # 添加一列标记数据来源（文件名）
            df['来源文件'] = os.path.basename(f)
            all_data.append(df)
            print(f"  ✅ 已读取: {os.path.basename(f)} ({len(df)}行)")
        except Exception as e:
            print(f"  ❌ 读取失败: {os.path.basename(f)} - {e}")

    if not all_data:
        messagebox.showerror("错误", "所有文件读取失败，请检查格式")
        return

    # 合并
    result = pd.concat(all_data, ignore_index=True)

    # 保存
    output_path = os.path.join(folder, "合并结果.xlsx")
    result.to_excel(output_path, index=False)

    messagebox.showinfo(
        "完成",
        f"合并完成！\n"
        f"共处理: {len(excel_files)} 个文件\n"
        f"总数据: {len(result)} 行\n"
        f"保存至: {output_path}"
    )

if __name__ == "__main__":
    merge_excel_files()
