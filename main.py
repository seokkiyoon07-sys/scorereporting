import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import os
from data_processor import DataProcessor
from pdf_generator import PDFGenerator
from html_pdf_generator import HTMLPDFGenerator

class ScoringSystemGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("성적 관리 시스템")
        self.root.geometry("800x600")
        
        # 데이터 저장용 변수
        self.subject_files = {}
        self.grade_cutoff_file = None
        self.processed_data = None
        
        # 등급컷 및 표점 데이터 저장 변수 초기화
        self.saved_grade_cutoff_data = None
        self.saved_standard_scores = None
        self.saved_grade_standard_scores = None
        
        # GUI 구성
        self.setup_gui()
        
    def setup_gui(self):
        # 메인 프레임 (스크롤 가능)
        canvas = tk.Canvas(self.root)
        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # 메인 프레임
        main_frame = ttk.Frame(scrollable_frame, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 제목
        title_label = ttk.Label(main_frame, text="성적 관리 시스템", font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=4, pady=(0, 20))
        
        # PDF 제목 입력 필드
        pdf_title_frame = ttk.Frame(main_frame)
        pdf_title_frame.grid(row=1, column=0, columnspan=4, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(pdf_title_frame, text="PDF 성적표 제목:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        self.pdf_title_entry = ttk.Entry(pdf_title_frame, width=50)
        self.pdf_title_entry.insert(0, "학생 성적표")
        self.pdf_title_entry.grid(row=0, column=1, sticky=(tk.W, tk.E))
        
        # HTML 파일 저장 옵션
        self.save_html_var = tk.BooleanVar()
        html_checkbox = ttk.Checkbutton(pdf_title_frame, text="HTML 파일도 함께 저장", 
                                       variable=self.save_html_var)
        html_checkbox.grid(row=1, column=0, columnspan=2, sticky=tk.W, pady=(5, 0))
        
        pdf_title_frame.grid_columnconfigure(1, weight=1)
        
        # 과목별 파일 업로드 섹션
        self.setup_subject_upload(main_frame)
        
        # 등급컷 파일 업로드 섹션
        self.setup_grade_cutoff_upload(main_frame)
        
        # 처리 버튼
        self.setup_process_buttons(main_frame)
        
        # 진행상황 표시
        self.setup_progress_section(main_frame)
        
        # 결과 표시
        self.setup_result_section(main_frame)
        
        # 스크롤바와 캔버스 배치
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # 마우스 휠 이벤트 바인딩
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        # 그리드 가중치 설정
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)
        
    def setup_subject_upload(self, parent):
        # 과목별 파일 업로드 프레임
        subject_frame = ttk.LabelFrame(parent, text="과목별 성적 파일 업로드", padding="10")
        subject_frame.grid(row=2, column=0, columnspan=4, sticky=(tk.W, tk.E), pady=(0, 10))
        
        subjects = ["국어", "수학", "영어", "한국사", "탐구1", "탐구2"]
        self.subject_buttons = {}
        self.subject_labels = {}
        self.subject_delete_buttons = {}
        
        # 2열로 배치하여 간격 조정 (컬럼 수 증가)
        for i, subject in enumerate(subjects):
            row = i // 2
            col = (i % 2) * 5  # 5칸씩 띄어서 배치 (더 넓은 간격)
            
            # 과목명 라벨
            ttk.Label(subject_frame, text=f"{subject}:", width=8).grid(row=row, column=col, sticky=tk.W, padx=(0, 5))
            
            # 파일 선택 버튼
            btn = ttk.Button(subject_frame, text="파일 선택", 
                           command=lambda s=subject: self.select_subject_file(s))
            btn.grid(row=row, column=col+1, padx=(0, 5))
            self.subject_buttons[subject] = btn
            
            # 선택된 파일명 표시
            label = ttk.Label(subject_frame, text="파일이 선택되지 않음", foreground="gray", width=20)
            label.grid(row=row, column=col+2, sticky=tk.W, padx=(0, 5))
            self.subject_labels[subject] = label
            
            # 파일 삭제 버튼
            delete_btn = ttk.Button(subject_frame, text="삭제", 
                                  command=lambda s=subject: self.delete_subject_file(s),
                                  state="disabled")
            delete_btn.grid(row=row, column=col+3, padx=(0, 5))
            self.subject_delete_buttons[subject] = delete_btn
            
            # 간격을 위한 빈 프레임
            if i % 2 == 0:  # 첫 번째 열일 때만
                ttk.Frame(subject_frame, width=30).grid(row=row, column=col+4)
        
        # 그리드 가중치 설정
        subject_frame.grid_columnconfigure(2, weight=1)
        subject_frame.grid_columnconfigure(7, weight=1)
            
    def setup_grade_cutoff_upload(self, parent):
        # 등급컷 및 표점 직접 입력 프레임
        grade_frame = ttk.LabelFrame(parent, text="등급컷 및 표점 데이터 입력", padding="10")
        grade_frame.grid(row=3, column=0, columnspan=4, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # 탭 컨트롤 생성
        notebook = ttk.Notebook(grade_frame)
        notebook.grid(row=0, column=0, columnspan=10, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        
        # 과목별 탭 생성
        self.grade_cutoff_entries = {}
        self.standard_score_entries = {}
        self.grade_standard_scores = {}  # 등급별 표점 저장
        
        # 모든 과목코드별 탭 생성 (선택과목만)
        subject_categories = {
            "국어": ["언어와 매체", "화법과 작문"],
            "수학": ["확률과 통계", "미적분", "기하"],
            "영어": ["영어"],
            "한국사": ["한국사"],
            "사회탐구": ["생활과 윤리", "윤리와 사상", "한국지리", "세계지리", "동아시아사", "세계사", "경제", "정치와 법", "사회·문화"],
            "과학탐구": ["물리학 I", "화학 I", "생명과학 I", "지구과학 I", "물리학 II", "화학 II", "생명과학 II", "지구과학 II"]
        }
        
        for category, subjects in subject_categories.items():
            # 각 카테고리별 탭 생성
            tab_frame = ttk.Frame(notebook)
            notebook.add(tab_frame, text=category)
            
            # 헤더 (등급컷)
            ttk.Label(tab_frame, text="과목", font=("Arial", 10, "bold")).grid(row=0, column=0, padx=5, pady=5)
            for grade in range(1, 10):
                ttk.Label(tab_frame, text=f"{grade}등급컷", font=("Arial", 10, "bold")).grid(row=0, column=grade, padx=5, pady=5)
            ttk.Label(tab_frame, text="만점 표점", font=("Arial", 10, "bold")).grid(row=0, column=9, padx=5, pady=5)
            
            # 각 과목별 입력 필드
            for i, subject in enumerate(subjects):
                row = i + 1
                
                # 과목명
                ttk.Label(tab_frame, text=subject).grid(row=row, column=0, padx=5, pady=2)
                
                # 등급컷 입력 필드들 (1-9등급)
                grade_cutoffs = {}
                for grade in range(1, 10):
                    entry = ttk.Entry(tab_frame, width=6)
                    entry.grid(row=row, column=grade, padx=2, pady=2)
                    grade_cutoffs[grade] = entry
                self.grade_cutoff_entries[subject] = grade_cutoffs
                
                # 만점 표점 입력 필드
                std_score_entry = ttk.Entry(tab_frame, width=8)
                std_score_entry.grid(row=row, column=9, padx=5, pady=2)
                self.standard_score_entries[subject] = std_score_entry
            
            # 등급별 표점 입력 섹션 추가
            separator = ttk.Separator(tab_frame, orient='horizontal')
            separator.grid(row=len(subjects)+2, column=0, columnspan=10, sticky=(tk.W, tk.E), pady=10)
            
            # 등급별 표점 헤더
            ttk.Label(tab_frame, text="등급별 표점 입력", font=("Arial", 12, "bold")).grid(row=len(subjects)+3, column=0, columnspan=10, pady=5)
            
            # 등급별 표점 입력 필드
            for i, subject in enumerate(subjects):
                row = len(subjects) + 4 + i
                
                # 과목명
                ttk.Label(tab_frame, text=subject).grid(row=row, column=0, padx=5, pady=2)
                
                # 등급별 표점 입력 필드들 (1-9등급)
                grade_standard_scores = {}
                for grade in range(1, 10):
                    entry = ttk.Entry(tab_frame, width=6)
                    entry.grid(row=row, column=grade, padx=2, pady=2)
                    grade_standard_scores[grade] = entry
                self.grade_standard_scores[subject] = grade_standard_scores
        
        # 기본값 설정
        self.set_default_values()
        
        # 저장 버튼 추가
        save_button = ttk.Button(grade_frame, text="등급컷 및 표점 저장", 
                                command=self.save_grade_cutoff_data)
        save_button.grid(row=1, column=0, columnspan=10, pady=10)
        
        grade_frame.grid_columnconfigure(0, weight=1)
        
    def save_grade_cutoff_data(self):
        """등급컷 및 표점 데이터 저장"""
        try:
            # 등급컷 데이터 수집
            grade_cutoff_data = {}
            standard_scores = {}
            grade_standard_scores = {}
            
            for subject in self.grade_cutoff_entries:
                # 등급컷 데이터
                grade_cutoffs = {}
                for grade in range(1, 10):
                    value = self.grade_cutoff_entries[subject][grade].get().strip()
                    if value:
                        try:
                            grade_cutoffs[grade] = float(value)
                        except ValueError:
                            self.log_result(f"⚠️ {subject} {grade}등급컷 값이 올바르지 않습니다: {value}")
                            continue
                    else:
                        self.log_result(f"⚠️ {subject} {grade}등급컷이 비어있습니다")
                        continue
                
                if len(grade_cutoffs) == 9:  # 1-9등급 모두 입력되었는지 확인
                    grade_cutoff_data[subject] = grade_cutoffs
                
                # 만점 표점
                max_std_score = self.standard_score_entries[subject].get().strip()
                if max_std_score:
                    try:
                        standard_scores[subject] = float(max_std_score)
                    except ValueError:
                        self.log_result(f"⚠️ {subject} 만점 표점 값이 올바르지 않습니다: {max_std_score}")
                        standard_scores[subject] = 100  # 기본값
                else:
                    standard_scores[subject] = 100  # 기본값
                
                # 등급별 표점
                grade_std_scores = {}
                for grade in range(1, 10):
                    value = self.grade_standard_scores[subject][grade].get().strip()
                    if value:
                        try:
                            grade_std_scores[grade] = float(value)
                        except ValueError:
                            self.log_result(f"⚠️ {subject} {grade}등급 표점 값이 올바르지 않습니다: {value}")
                            grade_std_scores[grade] = 100 - (grade-1)*10  # 기본값
                    else:
                        grade_std_scores[grade] = 100 - (grade-1)*10  # 기본값
                
                grade_standard_scores[subject] = grade_std_scores
            
            # 데이터 저장
            self.saved_grade_cutoff_data = grade_cutoff_data
            self.saved_standard_scores = standard_scores
            self.saved_grade_standard_scores = grade_standard_scores
            
            self.log_result(f"✅ 등급컷 및 표점 데이터 저장 완료: {len(grade_cutoff_data)}개 과목")
            messagebox.showinfo("저장 완료", f"등급컷 및 표점 데이터가 저장되었습니다.\n({len(grade_cutoff_data)}개 과목)")
            
        except Exception as e:
            error_msg = f"등급컷 데이터 저장 중 오류: {str(e)}"
            self.log_result(f"❌ {error_msg}")
            messagebox.showerror("저장 오류", error_msg)
            import traceback
            traceback.print_exc()

    def set_default_values(self):
        """기본값 설정"""
        # 모든 과목에 대해 기본값 설정 (선택과목만)
        all_subjects = [
            "언어와 매체", "화법과 작문",
            "확률과 통계", "미적분", "기하",
            "영어", "한국사",
            "생활과 윤리", "윤리와 사상", "한국지리", "세계지리", "동아시아사", "세계사", "경제", "정치와 법", "사회·문화",
            "물리학 I", "화학 I", "생명과학 I", "지구과학 I", "물리학 II", "화학 II", "생명과학 II", "지구과학 II"
        ]
        
        for subject in all_subjects:
            if subject in self.grade_cutoff_entries:
                # 영어 등급컷 기본값 (고정)
                if subject == "영어":
                    grade_cutoffs = [90, 80, 70, 60, 50, 40, 30, 20, 0]  # 영어 등급컷
                    for grade in range(1, 10):
                        if grade <= len(grade_cutoffs):
                            self.grade_cutoff_entries[subject][grade].insert(0, str(grade_cutoffs[grade-1]))
                    
                    # 영어는 표점과 백분위 없음
                    self.standard_score_entries[subject].insert(0, "0")
                    if subject in self.grade_standard_scores:
                        for grade in range(1, 10):
                            self.grade_standard_scores[subject][grade].insert(0, "0")
                
                # 한국사 등급컷 기본값 (고정)
                elif subject == "한국사":
                    grade_cutoffs = [40, 35, 30, 25, 20, 15, 10, 5, 0]  # 한국사 등급컷
                    for grade in range(1, 10):
                        if grade <= len(grade_cutoffs):
                            self.grade_cutoff_entries[subject][grade].insert(0, str(grade_cutoffs[grade-1]))
                    
                    # 한국사는 표점과 백분위 없음
                    self.standard_score_entries[subject].insert(0, "0")
                    if subject in self.grade_standard_scores:
                        for grade in range(1, 10):
                            self.grade_standard_scores[subject][grade].insert(0, "0")
                
                # 다른 과목들
                else:
                    # 사탐과 과탐은 50점 만점
                    if subject in ["생활과 윤리", "윤리와 사상", "한국지리", "세계지리", "동아시아사", "세계사", "경제", "정치와 법", "사회·문화", 
                                 "물리학 I", "화학 I", "생명과학 I", "지구과학 I", "물리학 II", "화학 II", "생명과학 II", "지구과학 II"]:
                        # 사탐/과탐 등급컷 (50점 만점 기준)
                        grade_cutoffs = [47, 43, 39, 35, 31, 27, 23, 19, 15]  # 1등급부터 9등급까지
                        for grade in range(1, 10):
                            if grade <= len(grade_cutoffs):
                                self.grade_cutoff_entries[subject][grade].insert(0, str(grade_cutoffs[grade-1]))
                        
                        # 사탐/과탐 표점 (100점 만점)
                        max_score = 100
                        self.standard_score_entries[subject].insert(0, str(max_score))
                        
                        # 등급별 표점 기본값 (1-9등급)
                        if subject in self.grade_standard_scores:
                            grade_standard_scores = [
                                max_score,           # 1등급
                                max_score * 0.9,     # 2등급
                                max_score * 0.8,     # 3등급
                                max_score * 0.7,     # 4등급
                                max_score * 0.6,     # 5등급
                                max_score * 0.5,     # 6등급
                                max_score * 0.4,     # 7등급
                                max_score * 0.3,     # 8등급
                                max_score * 0.2      # 9등급
                            ]
                            for grade in range(1, 10):
                                if grade <= len(grade_standard_scores):
                                    self.grade_standard_scores[subject][grade].insert(0, str(int(grade_standard_scores[grade-1])))
                    
                    # 국어, 수학, 언어와 매체, 화법과 작문, 확률과 통계, 미적분, 기하
                    else:
                        # 등급컷 기본값 (1-9등급)
                        grade_cutoffs = [95, 90, 85, 80, 75, 70, 65, 60, 55]  # 1등급부터 9등급까지
                        for grade in range(1, 10):
                            if grade <= len(grade_cutoffs):
                                self.grade_cutoff_entries[subject][grade].insert(0, str(grade_cutoffs[grade-1]))
                        
                        # 만점 표점 기본값
                        if subject in ["국어", "수학"]:
                            max_score = 150
                            self.standard_score_entries[subject].insert(0, str(max_score))
                        else:
                            max_score = 100
                            self.standard_score_entries[subject].insert(0, str(max_score))
                        
                        # 등급별 표점 기본값 (1-9등급)
                        if subject in self.grade_standard_scores:
                            grade_standard_scores = [
                                max_score,           # 1등급
                                max_score * 0.9,     # 2등급
                                max_score * 0.8,     # 3등급
                                max_score * 0.7,     # 4등급
                                max_score * 0.6,     # 5등급
                                max_score * 0.5,     # 6등급
                                max_score * 0.4,     # 7등급
                                max_score * 0.3,     # 8등급
                                max_score * 0.2      # 9등급
                            ]
                            for grade in range(1, 10):
                                if grade <= len(grade_standard_scores):
                                    self.grade_standard_scores[subject][grade].insert(0, str(int(grade_standard_scores[grade-1])))
        
    def setup_process_buttons(self, parent):
        # 처리 버튼 프레임
        button_frame = ttk.Frame(parent)
        button_frame.grid(row=4, column=0, columnspan=4, pady=10)
        
        self.process_button = ttk.Button(button_frame, text="데이터 처리", 
                                       command=self.process_data, state="disabled")
        self.process_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.upload_grade_cutoff_button = ttk.Button(button_frame, text="등급컷 CSV 업로드", 
                                                   command=self.upload_grade_cutoff_csv)
        self.upload_grade_cutoff_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.upload_standard_scores_button = ttk.Button(button_frame, text="표점 CSV 업로드", 
                                                      command=self.upload_standard_scores_csv)
        self.upload_standard_scores_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.pdf_button = ttk.Button(button_frame, text="PDF 생성", 
                                   command=self.generate_pdfs, state="disabled")
        self.pdf_button.pack(side=tk.LEFT)
        
    def setup_progress_section(self, parent):
        # 진행상황 표시 프레임
        progress_frame = ttk.LabelFrame(parent, text="진행상황", padding="10")
        progress_frame.grid(row=5, column=0, columnspan=4, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.progress_var = tk.StringVar(value="대기 중...")
        ttk.Label(progress_frame, textvariable=self.progress_var).pack(anchor=tk.W)
        
        self.progress_bar = ttk.Progressbar(progress_frame, mode='indeterminate')
        self.progress_bar.pack(fill=tk.X, pady=(5, 0))
        
    def setup_result_section(self, parent):
        # 결과 표시 프레임
        result_frame = ttk.LabelFrame(parent, text="결과", padding="10")
        result_frame.grid(row=6, column=0, columnspan=4, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # 결과 텍스트 위젯
        self.result_text = tk.Text(result_frame, height=10, wrap=tk.WORD)
        scrollbar = ttk.Scrollbar(result_frame, orient=tk.VERTICAL, command=self.result_text.yview)
        self.result_text.configure(yscrollcommand=scrollbar.set)
        
        self.result_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # 그리드 가중치 설정
        parent.grid_rowconfigure(5, weight=1)
        parent.grid_columnconfigure(0, weight=1)
        result_frame.grid_rowconfigure(0, weight=1)
        result_frame.grid_columnconfigure(0, weight=1)
        
    def select_subject_file(self, subject):
        """과목별 파일 선택"""
        file_path = filedialog.askopenfilename(
            title=f"{subject} 파일 선택",
            filetypes=[("CSV files", "*.csv"), ("Excel files", "*.xlsx"), ("All files", "*.*")]
        )
        
        if file_path:
            self.subject_files[subject] = file_path
            filename = os.path.basename(file_path)
            self.subject_labels[subject].config(text=filename, foreground="black")
            self.subject_delete_buttons[subject].config(state="normal")
            self.log_result(f"{subject} 파일 선택됨: {filename}")
            self.check_files_ready()
    
    def delete_subject_file(self, subject):
        """과목별 파일 삭제"""
        if subject in self.subject_files:
            del self.subject_files[subject]
            self.subject_labels[subject].config(text="파일이 선택되지 않음", foreground="gray")
            self.subject_delete_buttons[subject].config(state="disabled")
            self.log_result(f"{subject} 파일 삭제됨")
            self.check_files_ready()
            
    def select_grade_cutoff_file(self):
        """등급컷 파일 선택"""
        file_path = filedialog.askopenfilename(
            title="등급컷/표점 파일 선택",
            filetypes=[("CSV files", "*.csv"), ("Excel files", "*.xlsx"), ("All files", "*.*")]
        )
        
        if file_path:
            self.grade_cutoff_file = file_path
            filename = os.path.basename(file_path)
            self.grade_label.config(text=filename, foreground="black")
            self.check_files_ready()
            
    def check_files_ready(self):
        """최소 1개 과목 파일이 선택되었는지 확인"""
        if len(self.subject_files) >= 1:
            self.process_button.config(state="normal")
        else:
            self.process_button.config(state="disabled")
            
    def process_data(self):
        """데이터 처리"""
        try:
            self.progress_var.set("데이터 처리 중...")
            self.progress_bar.start()
            self.process_button.config(state="disabled")
            
            self.log_result("[시작] 데이터 처리 시작...")
            
            # 데이터 처리기 초기화
            processor = DataProcessor()
            
            # 과목별 데이터 로드
            self.log_result(f"[파일] 총 {len(self.subject_files)}개 과목 파일 처리 시작...")
            for subject, file_path in self.subject_files.items():
                try:
                    self.log_result(f"[로드] {subject} 데이터 로딩 중: {file_path}")
                    processor.load_subject_data(subject, file_path)
                    self.log_result(f"[완료] {subject} 로드 완료")
                except Exception as e:
                    self.log_result(f"[오류] {subject} 로드 실패: {str(e)}")
                    raise Exception(f"{subject} 파일 처리 중 오류가 발생했습니다:\n{str(e)}")
            
            # 저장된 등급컷과 표점 데이터 사용
            self.log_result("등급컷 및 표점 데이터 설정 중...")
            
            # 저장된 데이터가 있으면 사용, 없으면 기본값 사용
            if hasattr(self, 'saved_grade_cutoff_data') and self.saved_grade_cutoff_data:
                grade_cutoff_data = self.saved_grade_cutoff_data
                standard_scores = self.saved_standard_scores
                grade_standard_scores = self.saved_grade_standard_scores
                self.log_result(f"✅ 저장된 등급컷 데이터 사용: {len(grade_cutoff_data)}개 과목")
            else:
                self.log_result("⚠️ 저장된 등급컷 데이터가 없습니다. 기본값을 사용합니다.")
                # 기본값 설정
                grade_cutoff_data = {}
                standard_scores = {}
                grade_standard_scores = {}
                
                # 과목코드 기반으로 처리 (선택과목만)
                all_subjects = [
                    "언어와 매체", "화법과 작문",
                    "확률과 통계", "미적분", "기하",
                    "영어", "한국사",
                    "생활과 윤리", "윤리와 사상", "한국지리", "세계지리", "동아시아사", "세계사", "경제", "정치와 법", "사회·문화",
                    "물리학 I", "화학 I", "생명과학 I", "지구과학 I", "물리학 II", "화학 II", "생명과학 II", "지구과학 II"
                ]
                
                for subject in all_subjects:
                    # 등급컷 데이터 (1-9등급)
                    grade_cutoffs = {}
                    for grade in range(1, 10):
                        try:
                            value = float(self.grade_cutoff_entries[subject][grade].get())
                            grade_cutoffs[grade] = value
                        except ValueError:
                            grade_cutoffs[grade] = 0
                    
                    # 만점 표점
                    try:
                        max_score = float(self.standard_score_entries[subject].get())
                    except ValueError:
                        max_score = 100
                    
                    # 등급별 표점 데이터 (1-9등급)
                    grade_std_scores = {}
                    for grade in range(1, 10):
                        try:
                            value = float(self.grade_standard_scores[subject][grade].get())
                            grade_std_scores[grade] = value
                        except ValueError:
                            # 기본값 설정
                            grade_std_scores[grade] = max_score * (1 - (grade-1) * 0.1)
                    
                    grade_cutoff_data[subject] = grade_cutoffs
                    standard_scores[subject] = max_score
                    grade_standard_scores[subject] = grade_std_scores
            
            # 데이터 처리기에 설정
            processor.set_grade_cutoff_data(grade_cutoff_data)
            processor.set_standard_scores(standard_scores)
            processor.set_grade_standard_scores(grade_standard_scores)
            
            # 데이터 처리
            self.log_result("데이터 처리 중...")
            self.processed_data = processor.process_all_data()
            
            self.log_result(f"처리 완료! 총 {len(self.processed_data)}명의 학생 데이터가 처리되었습니다.")
            
            self.pdf_button.config(state="normal")
            self.progress_var.set("데이터 처리 완료")
            
        except Exception as e:
            self.log_result(f"오류 발생: {str(e)}")
            messagebox.showerror("오류", f"데이터 처리 중 오류가 발생했습니다:\n{str(e)}")
        finally:
            self.progress_bar.stop()
            self.process_button.config(state="normal")
            
    def upload_grade_cutoff_csv(self):
        """등급컷 CSV 파일 업로드"""
        try:
            from tkinter import filedialog
            import pandas as pd
            
            # CSV 파일 선택
            file_path = filedialog.askopenfilename(
                title="등급컷 CSV 파일 선택",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
            )
            
            if not file_path:
                return
            
            # CSV 파일 읽기
            df = pd.read_csv(file_path, encoding='utf-8-sig')
            
            # 데이터 검증 (영어 컬럼명)
            required_columns = ['Subject_Name', 'Subject_Code', 'Grade_1_Cutoff', 'Grade_2_Cutoff', 
                              'Grade_3_Cutoff', 'Grade_4_Cutoff', 'Grade_5_Cutoff', 'Grade_6_Cutoff', 
                              'Grade_7_Cutoff', 'Grade_8_Cutoff', 'Grade_9_Cutoff']
            
            for col in required_columns:
                if col not in df.columns:
                    messagebox.showerror("오류", f"필수 컬럼이 없습니다: {col}")
                    return
            
            # 과목명 매핑 (영어 → 한글)
            subject_mapping = {
                'Korean': '국어',
                'Language_and_Media': '언어와 매체',
                'Speech_and_Writing': '화법과 작문',
                'Math': '수학',
                'Probability_and_Statistics': '확률과 통계',
                'Calculus': '미적분',
                'Geometry': '기하',
                'English': '영어',
                'Korean_History': '한국사',
                'Life_and_Ethics': '생활과 윤리',
                'Ethics_and_Ideology': '윤리와 사상',
                'Korean_Geography': '한국지리',
                'World_Geography': '세계지리',
                'East_Asian_History': '동아시아사',
                'World_History': '세계사',
                'Economics': '경제',
                'Politics_and_Law': '정치와 법',
                'Social_Culture': '사회·문화',
                'Physics_I': '물리학 I',
                'Chemistry_I': '화학 I',
                'Biology_I': '생명과학 I',
                'Earth_Science_I': '지구과학 I',
                'Physics_II': '물리학 II',
                'Chemistry_II': '화학 II',
                'Biology_II': '생명과학 II',
                'Earth_Science_II': '지구과학 II'
            }
            
            # GUI에 데이터 로드
            loaded_count = 0
            for _, row in df.iterrows():
                subject_eng = row['Subject_Name']
                if subject_eng in subject_mapping:
                    subject_kor = subject_mapping[subject_eng]
                    if subject_kor in self.grade_cutoff_entries:
                        # 등급컷 데이터 로드
                        for grade in range(1, 10):
                            col_name = f'Grade_{grade}_Cutoff'
                            if col_name in row and pd.notna(row[col_name]):
                                self.grade_cutoff_entries[subject_kor][grade].delete(0, tk.END)
                                self.grade_cutoff_entries[subject_kor][grade].insert(0, str(int(row[col_name])))
                        loaded_count += 1
            
            self.log_result(f"등급컷 CSV 업로드 완료: {loaded_count}개 과목")
            messagebox.showinfo("업로드 완료", f"등급컷 CSV 파일이 업로드되었습니다.\n({loaded_count}개 과목)")
            
        except Exception as e:
            self.log_result(f"등급컷 CSV 업로드 오류: {str(e)}")
            messagebox.showerror("오류", f"등급컷 CSV 업로드 중 오류가 발생했습니다:\n{str(e)}")
            
    def generate_pdfs(self):
        """PDF 생성"""
        try:
            self.progress_var.set("PDF 생성 중...")
            self.progress_bar.start()
            self.pdf_button.config(state="disabled")
            
            self.log_result("[시작] PDF 생성 시작...")
            
            # HTML 기반 PDF 생성기 초기화
            try:
                pdf_generator = HTMLPDFGenerator()
                self.log_result("[완료] PDF 생성기 초기화 완료")
            except Exception as e:
                raise Exception(f"PDF 생성기 초기화 실패: {str(e)}")
            
            # 출력 폴더 생성
            output_dir = "output"
            try:
                if not os.path.exists(output_dir):
                    os.makedirs(output_dir)
                    self.log_result(f"[폴더] 출력 폴더 생성: {output_dir}")
                else:
                    self.log_result(f"[폴더] 기존 출력 폴더 사용: {output_dir}")
            except Exception as e:
                raise Exception(f"출력 폴더 생성 실패: {str(e)}")
                
            # PDF 제목 가져오기
            pdf_title = self.pdf_title_entry.get().strip()
            if not pdf_title:
                pdf_title = "학생 성적표"
                self.log_result(f"[제목] PDF 제목: {pdf_title} (기본값)")
            else:
                self.log_result(f"[제목] PDF 제목: {pdf_title}")
                
            # 각 학생별 PDF 생성
            total_students = len(self.processed_data)
            self.log_result(f"[학생] 총 {total_students}명의 학생 PDF 생성 시작...")
            
            success_count = 0
            error_count = 0
            
            for i, (student_id, student_data) in enumerate(self.processed_data.items()):
                try:
                    self.log_result(f"[생성] PDF 생성 중... ({i+1}/{total_students}) - {student_data['name']}")
                    
                    # 학생 데이터 검증
                    if not student_data.get('name'):
                        self.log_result(f"[경고] {student_id}: 학생 이름이 없습니다.")
                        error_count += 1
                        continue
                    
                    if not student_data.get('subjects'):
                        self.log_result(f"[경고] {student_data['name']}: 과목 데이터가 없습니다.")
                        error_count += 1
                        continue
                    
                    # PDF 생성 (HTML 저장 옵션 포함)
                    save_html = self.save_html_var.get()
                    pdf_generator.generate_html_based_pdf(student_data, output_dir, pdf_title, save_html)
                    success_count += 1
                    self.log_result(f"[완료] {student_data['name']} PDF 생성 완료")
                    
                except Exception as e:
                    error_count += 1
                    self.log_result(f"[오류] {student_data.get('name', 'Unknown')} PDF 생성 실패: {str(e)}")
                    continue
            
            # 결과 요약
            self.log_result(f"[결과] PDF 생성 완료!")
            self.log_result(f"  [성공] 성공: {success_count}개")
            if error_count > 0:
                self.log_result(f"  [실패] 실패: {error_count}개")
            self.log_result(f"[위치] 저장 위치: {output_dir}")
            
            self.progress_var.set("PDF 생성 완료")
            
            # 성공 메시지
            if success_count > 0:
                messagebox.showinfo("완료", f"PDF 생성이 완료되었습니다!\n\n성공: {success_count}개\n실패: {error_count}개\n\n저장 위치: {output_dir}")
            else:
                messagebox.showerror("오류", "PDF 생성에 실패했습니다. 로그를 확인해주세요.")
            
        except Exception as e:
            import traceback
            error_details = traceback.format_exc()
            self.log_result(f"[오류] PDF 생성 중 치명적 오류: {str(e)}")
            self.log_result(f"상세 오류:\n{error_details}")
            messagebox.showerror("오류", f"PDF 생성 중 치명적 오류가 발생했습니다:\n{str(e)}")
        finally:
            self.progress_bar.stop()
            self.pdf_button.config(state="normal")
            
    def log_result(self, message):
        """결과 로그 출력"""
        self.result_text.insert(tk.END, f"{message}\n")
        self.result_text.see(tk.END)
        self.root.update()

    def upload_standard_scores_csv(self):
        """표점 CSV 파일 업로드"""
        try:
            from tkinter import filedialog
            import pandas as pd
            
            # CSV 파일 선택
            file_path = filedialog.askopenfilename(
                title="표점 CSV 파일 선택",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
            )
            
            if not file_path:
                return
            
            # CSV 파일 읽기
            df = pd.read_csv(file_path, encoding='utf-8-sig')
            
            # 데이터 검증 (영어 컬럼명)
            required_columns = ['Subject_Name', 'subject_code', 'Grade_1_Score', 'Grade_2_Score', 
                              'Grade_3_Score', 'Grade_4_Score', 'Grade_5_Score', 'Grade_6_Score', 
                              'Grade_7_Score', 'Grade_8_Score', 'Grade_9_Score']
            
            for col in required_columns:
                if col not in df.columns:
                    messagebox.showerror("오류", f"필수 컬럼이 없습니다: {col}")
                    return
            
            # 과목명 매핑 (영어 → 한글)
            subject_mapping = {
                'Korean': '국어',
                'Language_and_Media': '언어와 매체',
                'Speech_and_Writing': '화법과 작문',
                'Math': '수학',
                'Probability_and_Statistics': '확률과 통계',
                'Calculus': '미적분',
                'Geometry': '기하',
                'English': '영어',
                'Korean_History': '한국사',
                'Life_and_Ethics': '생활과 윤리',
                'Ethics_and_Ideology': '윤리와 사상',
                'Korean_Geography': '한국지리',
                'World_Geography': '세계지리',
                'East_Asian_History': '동아시아사',
                'World_History': '세계사',
                'Economics': '경제',
                'Politics_and_Law': '정치와 법',
                'Social_Culture': '사회·문화',
                'Physics_I': '물리학 I',
                'Chemistry_I': '화학 I',
                'Biology_I': '생명과학 I',
                'Earth_Science_I': '지구과학 I',
                'Physics_II': '물리학 II',
                'Chemistry_II': '화학 II',
                'Biology_II': '생명과학 II',
                'Earth_Science_II': '지구과학 II'
            }
            
            # GUI에 데이터 로드
            loaded_count = 0
            for _, row in df.iterrows():
                subject_eng = row['Subject_Name']
                if subject_eng in subject_mapping:
                    subject_kor = subject_mapping[subject_eng]
                    if subject_kor in self.grade_standard_scores:
                        # 등급별 표점 로드
                        for grade in range(1, 10):
                            col_name = f'Grade_{grade}_Score'
                            if col_name in row and pd.notna(row[col_name]):
                                self.grade_standard_scores[subject_kor][grade].delete(0, tk.END)
                                self.grade_standard_scores[subject_kor][grade].insert(0, str(int(row[col_name])))
                        loaded_count += 1
            
            self.log_result(f"표점 CSV 업로드 완료: {loaded_count}개 과목")
            messagebox.showinfo("업로드 완료", f"표점 CSV 파일이 업로드되었습니다.\n({loaded_count}개 과목)")
            
        except Exception as e:
            error_msg = f"표점 CSV 업로드 중 오류: {str(e)}"
            self.log_result(f"❌ {error_msg}")
            messagebox.showerror("업로드 오류", error_msg)
            import traceback
            traceback.print_exc()

def main():
    root = tk.Tk()
    app = ScoringSystemGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
