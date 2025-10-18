"""
HTML → PDF 변환기 GUI 버전
사용자 친화적인 그래픽 인터페이스
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import threading
from pathlib import Path
from batch_html_to_pdf import batch_html_to_pdf, convert_single_html

class HTMLToPDFConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("HTML → PDF 변환기")
        self.root.geometry("600x500")
        
        # 변수 초기화
        self.input_folder = tk.StringVar()
        self.output_folder = tk.StringVar()
        self.recursive_var = tk.BooleanVar()
        self.overwrite_var = tk.BooleanVar()
        
        self.setup_gui()
        
    def setup_gui(self):
        """GUI 구성"""
        # 메인 프레임
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 제목
        title_label = ttk.Label(main_frame, text="HTML → PDF 변환기", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # 입력 폴더 선택
        ttk.Label(main_frame, text="입력 폴더:").grid(row=1, column=0, sticky=tk.W, pady=5)
        ttk.Entry(main_frame, textvariable=self.input_folder, width=50).grid(row=1, column=1, padx=(5, 5), pady=5)
        ttk.Button(main_frame, text="찾아보기", command=self.select_input_folder).grid(row=1, column=2, pady=5)
        
        # 출력 폴더 선택
        ttk.Label(main_frame, text="출력 폴더:").grid(row=2, column=0, sticky=tk.W, pady=5)
        ttk.Entry(main_frame, textvariable=self.output_folder, width=50).grid(row=2, column=1, padx=(5, 5), pady=5)
        ttk.Button(main_frame, text="찾아보기", command=self.select_output_folder).grid(row=2, column=2, pady=5)
        
        # 옵션 프레임
        options_frame = ttk.LabelFrame(main_frame, text="옵션", padding="10")
        options_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        
        ttk.Checkbutton(options_frame, text="하위 폴더까지 재귀 검색", 
                       variable=self.recursive_var).grid(row=0, column=0, sticky=tk.W)
        ttk.Checkbutton(options_frame, text="기존 PDF 파일 덮어쓰기", 
                       variable=self.overwrite_var).grid(row=0, column=1, sticky=tk.W, padx=(20, 0))
        
        # 단일 파일 변환 프레임
        single_frame = ttk.LabelFrame(main_frame, text="단일 파일 변환", padding="10")
        single_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        
        self.single_file_var = tk.StringVar()
        ttk.Label(single_frame, text="HTML 파일:").grid(row=0, column=0, sticky=tk.W, pady=5)
        ttk.Entry(single_frame, textvariable=self.single_file_var, width=40).grid(row=0, column=1, padx=(5, 5), pady=5)
        ttk.Button(single_frame, text="파일 선택", command=self.select_single_file).grid(row=0, column=2, pady=5)
        ttk.Button(single_frame, text="변환", command=self.convert_single_file).grid(row=0, column=3, padx=(10, 0), pady=5)
        
        # 변환 버튼
        convert_button = ttk.Button(main_frame, text="배치 변환 시작", 
                                   command=self.start_batch_conversion)
        convert_button.grid(row=5, column=0, columnspan=3, pady=20)
        
        # 진행 상황 프레임
        progress_frame = ttk.LabelFrame(main_frame, text="진행 상황", padding="10")
        progress_frame.grid(row=6, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        
        self.progress_var = tk.StringVar(value="대기 중...")
        ttk.Label(progress_frame, textvariable=self.progress_var).grid(row=0, column=0, sticky=tk.W)
        
        self.progress_bar = ttk.Progressbar(progress_frame, mode='indeterminate')
        self.progress_bar.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(5, 0))
        
        # 결과 텍스트
        result_frame = ttk.LabelFrame(main_frame, text="결과", padding="10")
        result_frame.grid(row=7, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        
        self.result_text = tk.Text(result_frame, height=8, wrap=tk.WORD)
        scrollbar = ttk.Scrollbar(result_frame, orient=tk.VERTICAL, command=self.result_text.yview)
        self.result_text.configure(yscrollcommand=scrollbar.set)
        
        self.result_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # 그리드 가중치 설정
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(7, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)
        result_frame.grid_rowconfigure(0, weight=1)
        result_frame.grid_columnconfigure(0, weight=1)
        
    def select_input_folder(self):
        """입력 폴더 선택"""
        folder = filedialog.askdirectory(title="HTML 파일이 있는 폴더 선택")
        if folder:
            self.input_folder.set(folder)
            # 출력 폴더 자동 설정
            if not self.output_folder.get():
                self.output_folder.set(folder)
    
    def select_output_folder(self):
        """출력 폴더 선택"""
        folder = filedialog.askdirectory(title="PDF 파일을 저장할 폴더 선택")
        if folder:
            self.output_folder.set(folder)
    
    def select_single_file(self):
        """단일 HTML 파일 선택"""
        file = filedialog.askopenfilename(
            title="HTML 파일 선택",
            filetypes=[("HTML files", "*.html"), ("All files", "*.*")]
        )
        if file:
            self.single_file_var.set(file)
    
    def log_result(self, message):
        """결과 로그 출력"""
        self.result_text.insert(tk.END, message + "\n")
        self.result_text.see(tk.END)
        self.root.update()
    
    def convert_single_file(self):
        """단일 파일 변환"""
        html_file = self.single_file_var.get()
        if not html_file:
            messagebox.showerror("오류", "HTML 파일을 선택해주세요.")
            return
        
        if not os.path.exists(html_file):
            messagebox.showerror("오류", "선택한 HTML 파일을 찾을 수 없습니다.")
            return
        
        self.progress_var.set("단일 파일 변환 중...")
        self.progress_bar.start()
        self.result_text.delete(1.0, tk.END)
        
        def convert_thread():
            try:
                self.log_result(f"HTML 파일: {html_file}")
                
                # 출력 파일명 자동 생성
                base_name = os.path.splitext(os.path.basename(html_file))[0]
                output_dir = os.path.dirname(html_file)
                output_pdf = os.path.join(output_dir, f"{base_name}.pdf")
                
                self.log_result(f"PDF 파일: {output_pdf}")
                self.log_result("-" * 30)
                
                # PDF 변환
                success = convert_single_html(html_file, output_pdf)
                
                if success:
                    file_size = os.path.getsize(output_pdf)
                    self.log_result("변환 완료!")
                    self.log_result(f"파일 크기: {file_size:,} bytes")
                    self.log_result(f"저장 위치: {os.path.abspath(output_pdf)}")
                    messagebox.showinfo("완료", "PDF 변환이 완료되었습니다!")
                else:
                    self.log_result("변환 실패")
                    messagebox.showerror("오류", "PDF 변환에 실패했습니다.")
                
            except Exception as e:
                self.log_result(f"오류 발생: {str(e)}")
                messagebox.showerror("오류", f"변환 중 오류가 발생했습니다:\n{str(e)}")
            finally:
                self.progress_bar.stop()
                self.progress_var.set("완료")
        
        # 별도 스레드에서 변환 실행
        thread = threading.Thread(target=convert_thread)
        thread.daemon = True
        thread.start()
    
    def start_batch_conversion(self):
        """배치 변환 시작"""
        input_folder = self.input_folder.get()
        if not input_folder:
            messagebox.showerror("오류", "입력 폴더를 선택해주세요.")
            return
        
        if not os.path.exists(input_folder):
            messagebox.showerror("오류", "선택한 입력 폴더를 찾을 수 없습니다.")
            return
        
        output_folder = self.output_folder.get() or input_folder
        
        self.progress_var.set("배치 변환 중...")
        self.progress_bar.start()
        self.result_text.delete(1.0, tk.END)
        
        def batch_thread():
            try:
                self.log_result(f"입력 폴더: {input_folder}")
                self.log_result(f"출력 폴더: {output_folder}")
                self.log_result(f"재귀 검색: {'예' if self.recursive_var.get() else '아니오'}")
                self.log_result(f"덮어쓰기: {'예' if self.overwrite_var.get() else '아니오'}")
                self.log_result("-" * 50)
                
                # 배치 변환 실행
                success = batch_html_to_pdf(
                    input_folder, 
                    output_folder, 
                    self.recursive_var.get(), 
                    self.overwrite_var.get()
                )
                
                if success:
                    self.log_result("\n배치 변환이 완료되었습니다!")
                    messagebox.showinfo("완료", "배치 변환이 완료되었습니다!")
                else:
                    self.log_result("\n일부 파일 변환에 실패했습니다.")
                    messagebox.showwarning("경고", "일부 파일 변환에 실패했습니다.")
                
            except Exception as e:
                self.log_result(f"오류 발생: {str(e)}")
                messagebox.showerror("오류", f"변환 중 오류가 발생했습니다:\n{str(e)}")
            finally:
                self.progress_bar.stop()
                self.progress_var.set("완료")
        
        # 별도 스레드에서 변환 실행
        thread = threading.Thread(target=batch_thread)
        thread.daemon = True
        thread.start()

def main():
    """메인 함수"""
    root = tk.Tk()
    app = HTMLToPDFConverter(root)
    root.mainloop()

if __name__ == "__main__":
    main()

