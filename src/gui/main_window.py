"""
离职年假计算器 - 主窗口GUI
完全重写版本，专注于简洁性和可靠性
"""

import sys
import os
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, date
import threading
import queue
import logging
from tkcalendar import DateEntry

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.insert(0, project_root)
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from business.controller import BusinessController


class MainWindow:
    """主窗口类 - 重写版本"""
    
    def __init__(self):
        """初始化主窗口"""
        self.logger = logging.getLogger(__name__)
        self.controller = BusinessController()
        
        # 创建主窗口
        self.root = tk.Tk()
        self.root.title("离职年假计算器")
        self.root.geometry("500x400")
        self.root.resizable(False, False)
        
        # 线程安全的结果队列
        self.result_queue = queue.Queue()
        
        # 创建界面
        self._create_widgets()
        self._setup_layout()
        
        # 启动结果检查器
        self._check_results()
        
        self.logger.info("GUI界面初始化完成")
    
    def _create_widgets(self):
        """创建界面组件"""
        # 主框架
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 标题
        title_label = ttk.Label(main_frame, text="离职年假计算器", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # 员工姓名
        ttk.Label(main_frame, text="员工姓名:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.name_entry = ttk.Entry(main_frame, width=30)
        self.name_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5)
        
        # 离职日期
        ttk.Label(main_frame, text="离职日期:").grid(row=2, column=0, sticky=tk.W, pady=5)
        
        # 创建日期输入框架
        date_frame = ttk.Frame(main_frame)
        date_frame.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=5)
        
        # 使用更兼容的日期输入方案，解决macOS上DateEntry的显示问题
        # 创建日期输入框
        self.date_var = tk.StringVar(value=date.today().strftime('%Y-%m-%d'))
        self.date_entry = ttk.Entry(date_frame, 
                                   textvariable=self.date_var,
                                   width=15,
                                   font=('Arial', 10))
        self.date_entry.pack(side=tk.LEFT, padx=(0, 5))
        
        # 添加日期选择按钮
        self.calendar_button = ttk.Button(date_frame, text="📅", width=3,
                                         command=self._show_calendar)
        self.calendar_button.pack(side=tk.LEFT, padx=(0, 5))
        
        # 添加日期格式提示
        date_hint = ttk.Label(date_frame, text="(YYYY-MM-DD)", 
                             font=('Arial', 8), foreground='gray')
        date_hint.pack(side=tk.LEFT, padx=(5, 0))
        
        # 按钮框架
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, columnspan=2, pady=20)
        
        # 计算按钮
        self.calc_button = ttk.Button(button_frame, text="计算年假", 
                                     command=self._on_calculate)
        self.calc_button.pack(side=tk.LEFT, padx=5)
        
        # 清空按钮
        clear_button = ttk.Button(button_frame, text="清空", 
                                 command=self._on_clear)
        clear_button.pack(side=tk.LEFT, padx=5)
        
        # 结果显示区域
        result_frame = ttk.LabelFrame(main_frame, text="计算结果", padding="10")
        result_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        
        # 结果文本
        self.result_text = tk.Text(result_frame, height=8, width=50, 
                                  state=tk.DISABLED, wrap=tk.WORD)
        scrollbar = ttk.Scrollbar(result_frame, orient=tk.VERTICAL, 
                                 command=self.result_text.yview)
        self.result_text.configure(yscrollcommand=scrollbar.set)
        
        self.result_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # 移除状态栏 - 根据老大要求简化界面
        
        # 配置列权重
        main_frame.columnconfigure(1, weight=1)
        result_frame.columnconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
    
    def _setup_layout(self):
        """设置布局"""
        # 居中窗口
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def _show_calendar(self):
        """显示日历选择器"""
        try:
            # 创建顶层窗口
            calendar_window = tk.Toplevel(self.root)
            calendar_window.title("选择日期")
            calendar_window.geometry("300x250")
            calendar_window.resizable(False, False)
            
            # 居中显示
            calendar_window.transient(self.root)
            calendar_window.grab_set()
            
            # 创建日历组件
            from tkcalendar import Calendar
            
            # 获取当前日期
            try:
                current_date = datetime.strptime(self.date_var.get(), '%Y-%m-%d').date()
            except:
                current_date = date.today()
            
            cal = Calendar(calendar_window,
                          selectmode='day',
                          year=current_date.year,
                          month=current_date.month,
                          day=current_date.day,
                          date_pattern='yyyy-mm-dd',
                          showweeknumbers=False,
                          showothermonthdays=True)
            cal.pack(pady=10)
            
            # 按钮框架
            button_frame = ttk.Frame(calendar_window)
            button_frame.pack(pady=10)
            
            def on_select():
                selected_date = cal.get_date()
                self.date_var.set(selected_date)
                calendar_window.destroy()
            
            def on_cancel():
                calendar_window.destroy()
            
            # 确定和取消按钮
            ttk.Button(button_frame, text="确定", command=on_select).pack(side=tk.LEFT, padx=5)
            ttk.Button(button_frame, text="取消", command=on_cancel).pack(side=tk.LEFT, padx=5)
            
            # 居中窗口
            calendar_window.update_idletasks()
            x = (calendar_window.winfo_screenwidth() // 2) - (calendar_window.winfo_width() // 2)
            y = (calendar_window.winfo_screenheight() // 2) - (calendar_window.winfo_height() // 2)
            calendar_window.geometry(f"+{x}+{y}")
            
        except Exception as e:
            self.logger.error(f"显示日历失败: {e}")
            messagebox.showerror("错误", f"无法显示日历: {e}")
    
    def _on_calculate(self):
        """计算按钮点击事件"""
        # 获取输入
        employee_name = self.name_entry.get().strip()
        
        # 验证日期格式并获取日期
        try:
            leave_date = datetime.strptime(self.date_var.get(), '%Y-%m-%d').date()
        except ValueError:
            messagebox.showerror("错误", "请输入正确的日期格式 (YYYY-MM-DD)")
            return
        
        # 验证输入
        if not employee_name:
            messagebox.showerror("错误", "请输入员工姓名")
            return
        
        # 移除日期限制，允许选择任何日期
        # if leave_date > date.today():
        #     messagebox.showerror("错误", "离职日期不能超过今天")
        #     return
        
        # 禁用按钮，显示计算状态
        self.calc_button.config(state=tk.DISABLED)
        self._update_result_display("正在计算年假，请稍候...", "blue")
        
        # 启动后台计算
        thread = threading.Thread(target=self._calculate_background, 
                                 args=(employee_name, leave_date))
        thread.daemon = True
        thread.start()
        
        self.logger.info(f"开始计算: 员工={employee_name}, 离职日期={leave_date}")
    
    def _calculate_background(self, employee_name, leave_date):
        """后台计算年假"""
        try:
            # 调用业务逻辑
            result = self.controller.process_leave_calculation(
                employee_name, leave_date.strftime('%Y-%m-%d')
            )
            
            # 将结果放入队列
            self.result_queue.put(('success', result))
            
        except Exception as e:
            self.logger.error(f"计算失败: {e}")
            self.result_queue.put(('error', str(e)))
    
    def _check_results(self):
        """检查结果队列并更新UI"""
        try:
            # 非阻塞检查队列
            result_type, result_data = self.result_queue.get_nowait()
            
            if result_type == 'success':
                self._show_success_result(result_data)
            else:
                self._show_error_result(result_data)
                
        except queue.Empty:
            # 队列为空，继续检查
            pass
        
        # 每100ms检查一次
        self.root.after(100, self._check_results)
    
    def _show_success_result(self, result_data):
        """显示成功结果 - 简化界面，去掉标题"""
        # result_data是CalculationResult对象，不是字典
        remaining_days = result_data.remaining_days
        calculation_details = result_data.calculation_details
        
        # 清空并重新配置结果显示区域
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete(1.0, tk.END)
        
        # 配置不同的文本标签样式
        self.result_text.tag_configure("main_result", font=("Arial", 18, "bold"), foreground="#2E8B57", justify="center")
        self.result_text.tag_configure("details_header", font=("Arial", 10, "bold"), foreground="#666666")
        self.result_text.tag_configure("details_content", font=("Arial", 9), foreground="#888888")
        
        # 直接插入主要结果 - 放大强化显示，去掉"计算完成"标题
        main_result = f"🎯 剩余年假: {remaining_days:.1f} 天\n\n"
        self.result_text.insert(tk.END, main_result, "main_result")
        
        # 插入详细信息 - 弱化显示
        if calculation_details:
            self.result_text.insert(tk.END, "📊 详细信息:\n", "details_header")
            
            details_text = ""
            details_text += f"• 理论年假: {calculation_details.get('theoretical_hours', 0):.1f} 小时\n"
            details_text += f"• 已使用: {calculation_details.get('used_hours', 0):.1f} 小时\n"
            details_text += f"• 实际剩余: {calculation_details.get('actual_remaining_hours', 0):.1f} 小时\n"
            details_text += f"• 时间比例: {calculation_details.get('time_ratio', 0):.2%}\n"
            
            self.result_text.insert(tk.END, details_text, "details_content")
        
        # 居中对齐主要结果
        self.result_text.tag_configure("main_result", justify="center")
        
        self.result_text.config(state=tk.DISABLED)
        self.calc_button.config(state=tk.NORMAL)
        
        self.logger.info(f"计算成功: 剩余年假 {remaining_days:.1f} 天")
    
    def _show_error_result(self, error_msg):
        """显示错误结果"""
        result_text = f"计算失败！\n\n错误信息: {error_msg}"
        self._update_result_display(result_text, "red")
        self.status_var.set("计算失败")
        self.calc_button.config(state=tk.NORMAL)
        
        self.logger.error(f"计算失败: {error_msg}")
    
    def _update_result_display(self, text, color="black"):
        """更新结果显示"""
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(1.0, text)
        self.result_text.config(state=tk.DISABLED, fg=color)
    
    def _on_clear(self):
        """处理清空按钮点击事件"""
        # 重置所有输入字段
        self.name_entry.delete(0, tk.END)
        self.date_var.set(date.today().strftime('%Y-%m-%d'))
        self._update_result_display("")
        self.calc_button.config(state=tk.NORMAL)
    
    def run(self):
        """运行主循环"""
        try:
            self.logger.info("启动GUI主循环")
            self.root.mainloop()
        except Exception as e:
            self.logger.error(f"GUI运行错误: {e}")
            raise
        finally:
            self.logger.info("GUI已关闭")


def main():
    """主函数"""
    app = MainWindow()
    app.run()


if __name__ == "__main__":
    main()