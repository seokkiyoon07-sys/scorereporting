import pandas as pd
import numpy as np
from typing import Dict, List, Any

class DataProcessor:
    def __init__(self):
        self.subject_data = {}
        self.grade_cutoff_data = None
        self.standard_scores = {}
        self.student_names = {}  # 수험번호 -> 이름 매핑
        # 과목 코드 매핑
        self.subject_codes = {
            # 국어 영역
            "화법과 작문": "1",
            "언어와 매체": "2",
            
            # 수학 영역
            "확률과 통계": "1",
            "미분과 적분": "2",
            "기하": "3",
            
            # 영어
            "영어": "1",
            
            # 한국사
            "한국사": "1",
            
            # 사회탐구 영역 (11-19)
            "생활과 윤리": "11",
            "윤리와 사상": "12",
            "한국지리": "13",
            "세계지리": "14",
            "동아시아사": "15",
            "세계사": "16",
            "경제": "17",
            "정치와 법": "18",
            "사회·문화": "19",
            
            # 과학탐구 영역 (20-27)
            "물리학Ⅰ": "20",
            "화학Ⅰ": "21",
            "생명과학Ⅰ": "22",
            "지구과학Ⅰ": "23",
            "물리학Ⅱ": "24",
            "화학Ⅱ": "25",
            "생명과학Ⅱ": "26",
            "지구과학Ⅱ": "27"
        }
        
    def load_subject_data(self, subject: str, file_path: str):
        """과목별 데이터 로드"""
        try:
            print(f"[파일] {subject} 파일 로드 시작: {file_path}")
            
            # 파일 존재 확인
            import os
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"파일이 존재하지 않습니다: {file_path}")
            
            # 파일 크기 확인
            file_size = os.path.getsize(file_path)
            if file_size == 0:
                raise ValueError(f"파일이 비어있습니다: {file_path}")
            
            print(f"[크기] 파일 크기: {file_size} bytes")
            
            # 파일 확장자에 따라 읽기 방법 결정
            if file_path.endswith('.csv'):
                print("[읽기] CSV 파일 읽기 시도...")
                try:
                    df = pd.read_csv(file_path, encoding='utf-8-sig')
                except UnicodeDecodeError:
                    print("[경고] UTF-8 인코딩 실패, 다른 인코딩 시도...")
                    try:
                        df = pd.read_csv(file_path, encoding='cp949')
                    except UnicodeDecodeError:
                        df = pd.read_csv(file_path, encoding='latin-1')
            elif file_path.endswith('.xlsx'):
                print("[읽기] Excel 파일 읽기 시도...")
                df = pd.read_excel(file_path)
            else:
                raise ValueError(f"지원하지 않는 파일 형식입니다. 지원 형식: .csv, .xlsx, 현재: {file_path.split('.')[-1]}")
            
            print(f"[데이터] 로드된 데이터 행 수: {len(df)}")
            print(f"[데이터] 로드된 데이터 컬럼: {list(df.columns)}")
            
            # 필수 컬럼 확인
            required_columns = ['수험번호', '과목코드', '총점', '만점', '정답수', '오답번호']
            missing_columns = [col for col in required_columns if col not in df.columns]
            
            if missing_columns:
                available_columns = list(df.columns)
                raise ValueError(f"필수 컬럼이 누락되었습니다.\n누락된 컬럼: {missing_columns}\n사용 가능한 컬럼: {available_columns}")
            
            print("[확인] 필수 컬럼 확인 완료")
            
            # 데이터 정리
            print("[정리] 데이터 정리 시작...")
            original_count = len(df)
            df = df.dropna(subset=['수험번호', '총점'])  # 수험번호와 총점이 있는 행만 유지
            cleaned_count = len(df)
            
            if cleaned_count < original_count:
                print(f"[경고] {original_count - cleaned_count}개 행이 빈 데이터로 제거되었습니다.")
            
            # 숫자 데이터 변환
            print("[변환] 숫자 데이터 변환 중...")
            try:
                df['총점'] = pd.to_numeric(df['총점'], errors='coerce')
                invalid_scores = df['총점'].isna().sum()
                if invalid_scores > 0:
                    print(f"[경고] {invalid_scores}개의 총점 데이터가 유효하지 않습니다.")
            except Exception as e:
                raise ValueError(f"총점 데이터 변환 오류: {str(e)}")
            
            try:
                df['만점'] = pd.to_numeric(df['만점'], errors='coerce')
                invalid_maxes = df['만점'].isna().sum()
                if invalid_maxes > 0:
                    print(f"[경고] {invalid_maxes}개의 만점 데이터가 유효하지 않습니다.")
            except Exception as e:
                raise ValueError(f"만점 데이터 변환 오류: {str(e)}")
            
            try:
                df['과목코드'] = df['과목코드'].astype(str)
            except Exception as e:
                raise ValueError(f"과목코드 데이터 변환 오류: {str(e)}")
            
            # 최종 데이터 검증
            final_count = len(df)
            if final_count == 0:
                raise ValueError("유효한 데이터가 없습니다. 모든 행이 빈 데이터이거나 잘못된 형식입니다.")
            
            self.subject_data[subject] = df
            print(f"[완료] {subject} 데이터 로드 완료: {final_count}명")
            
            # 샘플 데이터 출력
            print(f"[샘플] 샘플 데이터 (처음 3행):")
            print(df.head(3).to_string())
            
        except FileNotFoundError as e:
            raise Exception(f"[오류] 파일 오류: {str(e)}")
        except ValueError as e:
            raise Exception(f"[오류] 데이터 형식 오류: {str(e)}")
        except Exception as e:
            import traceback
            error_details = traceback.format_exc()
            raise Exception(f"[오류] {subject} 데이터 로드 중 예상치 못한 오류:\n{str(e)}\n\n상세 오류:\n{error_details}")
            
    def load_student_names(self, file_path: str):
        """학생명 파일 로드 (수험번호 -> 이름 매핑)"""
        try:
            print(f"[학생명] 파일 로드 시작: {file_path}")
            
            if file_path.endswith('.csv'):
                try:
                    df = pd.read_csv(file_path, encoding='utf-8-sig')
                except UnicodeDecodeError:
                    df = pd.read_csv(file_path, encoding='cp949')
            elif file_path.endswith('.xlsx'):
                df = pd.read_excel(file_path)
            else:
                raise ValueError("지원하지 않는 파일 형식입니다. (.csv 또는 .xlsx만 가능)")
            
            # 필수 컬럼 확인
            if '수험번호' not in df.columns:
                raise ValueError(f"필수 컬럼이 누락되었습니다: ['수험번호']")
            
            # 이름 컬럼 찾기 (이름 또는 성명)
            name_column = None
            if '이름' in df.columns:
                name_column = '이름'
            elif '성명' in df.columns:
                name_column = '성명'
            else:
                raise ValueError(f"필수 컬럼이 누락되었습니다: ['이름' 또는 '성명']\n현재 컬럼: {df.columns.tolist()}")
            
            print(f"[학생명] 사용 컬럼: 수험번호, {name_column}")
            
            # 수험번호 -> 이름 매핑 딕셔너리 생성
            self.student_names = dict(zip(df['수험번호'].astype(str), df[name_column]))
            
            print(f"[학생명] 데이터 로드 완료: {len(self.student_names)}명")
            print(f"[샘플] 첫 3명: {list(self.student_names.items())[:3]}")
            
        except Exception as e:
            import traceback
            error_details = traceback.format_exc()
            raise Exception(f"학생명 데이터 로드 중 오류:\n{str(e)}\n\n상세:\n{error_details}")
    
    def load_grade_cutoff_data(self, file_path: str):
        """등급컷 및 표점 데이터 로드 (선택사항 포함)"""
        try:
            print(f"[등급컷] 파일 로드 시작: {file_path}")
            
            if file_path.endswith('.csv'):
                try:
                    df = pd.read_csv(file_path, encoding='utf-8-sig')
                except UnicodeDecodeError:
                    df = pd.read_csv(file_path, encoding='cp949')
            elif file_path.endswith('.xlsx'):
                df = pd.read_excel(file_path)
            else:
                raise ValueError("지원하지 않는 파일 형식입니다. (.csv 또는 .xlsx만 가능)")
            
            print(f"[등급컷] 로드된 컬럼: {list(df.columns)}")
            print(f"[등급컷] 데이터 행 수: {len(df)}")
            
            # 필수 컬럼 확인 (과목명, 과목코드만 필수)
            required_columns = ['과목명', '과목코드']
            missing_columns = [col for col in required_columns if col not in df.columns]
            
            if missing_columns:
                raise ValueError(f"필수 컬럼이 누락되었습니다: {missing_columns}")
            
            # 선택 컬럼 확인
            optional_groups = {
                '등급컷': ['1등급컷', '2등급컷', '3등급컷', '4등급컷', '5등급컷', '6등급컷', '7등급컷', '8등급컷', '9등급컷'],
                '표준점수': ['만점표점', '1등급표점', '2등급표점', '3등급표점', '4등급표점', '5등급표점', '6등급표점', '7등급표점', '8등급표점', '9등급표점'],
                '백분위': ['1등급백분위', '2등급백분위', '3등급백분위', '4등급백분위', '5등급백분위', '6등급백분위', '7등급백분위', '8등급백분위', '9등급백분위']
            }
            
            available_data = []
            for group_name, columns in optional_groups.items():
                has_columns = any(col in df.columns for col in columns)
                if has_columns:
                    available_data.append(group_name)
            
            print(f"[등급컷] 사용 가능한 데이터: {', '.join(available_data) if available_data else '없음'}")
            
            # 등급컷 데이터 저장
            self.grade_cutoff_data = df
            print(f"[등급컷] 데이터 로드 완료: {len(df)}개 과목")
            
            # 샘플 데이터 출력
            print(f"[샘플] 첫 3개 과목:")
            for idx, row in df.head(3).iterrows():
                print(f"  - {row['과목명']} ({row['과목코드']})")
            
        except Exception as e:
            import traceback
            error_details = traceback.format_exc()
            raise Exception(f"등급컷 데이터 로드 중 오류:\n{str(e)}\n\n상세:\n{error_details}")
            
    def set_grade_cutoff_data(self, grade_cutoff_data: Dict[str, Dict[int, float]]):
        """등급컷 데이터 직접 설정"""
        self.grade_cutoff_data = grade_cutoff_data
        
    def set_standard_scores(self, standard_scores: Dict[str, float]):
        """표준점수 데이터 직접 설정"""
        self.standard_scores = standard_scores
        
    def set_grade_standard_scores(self, grade_standard_scores: Dict[str, Dict[int, float]]):
        """등급별 표준점수 데이터 직접 설정"""
        self.grade_standard_scores = grade_standard_scores
            
    def process_all_data(self) -> Dict[str, Any]:
        """모든 데이터 처리 및 통합"""
        try:
            print("[처리] 전체 데이터 처리 시작...")
            
            if not self.student_names:
                raise Exception("[오류] 학생명 데이터가 로드되지 않았습니다. 먼저 학생명 파일을 업로드해주세요.")
            
            if not self.subject_data:
                raise Exception("[오류] 과목 데이터가 로드되지 않았습니다. 먼저 과목 파일을 업로드해주세요.")
            
            print(f"[학생명] 로드된 학생 수: {len(self.student_names)}명")
            print(f"[과목] 로드된 과목 수: {len(self.subject_data)}")
            for subject in self.subject_data.keys():
                print(f"  - {subject}: {len(self.subject_data[subject])}명")
            
            if self.grade_cutoff_data is None:
                print("[경고] 등급컷 데이터가 설정되지 않았습니다. 기본값을 사용합니다.")
                # 기본 등급컷 설정
                self._set_default_grade_cutoffs()
            else:
                print("[확인] 등급컷 데이터 확인 완료")
            
            # 학생별 데이터 통합
            print("[통합] 학생별 데이터 통합 시작...")
            student_data = {}
            processed_students = 0
            skipped_students = 0
            
            for subject, df in self.subject_data.items():
                print(f"[처리] {subject} 데이터 처리 중...")
                
                for idx, row in df.iterrows():
                    try:
                        # 수험번호로 학생 이름 찾기
                        try:
                            exam_number = str(row['수험번호']).strip()
                            
                            # 빈 수험번호 처리
                            if not exam_number or exam_number == 'nan' or exam_number == 'None':
                                print(f"[경고] 행 {idx}: 빈 수험번호 건너뜀 (과목: {subject})")
                                skipped_students += 1
                                continue
                            
                            # 학생명 파일에서 이름 찾기
                            if exam_number not in self.student_names:
                                print(f"[경고] 행 {idx}: 수험번호 '{exam_number}'에 해당하는 학생명을 찾을 수 없습니다 (과목: {subject})")
                                skipped_students += 1
                                continue
                            
                            student_name = self.student_names[exam_number]
                            
                            # 빈 이름, NaN, None 처리
                            if not student_name or student_name == 'nan' or student_name == 'None':
                                print(f"[경고] 행 {idx}: 빈 이름 건너뜀 (수험번호: {exam_number}, 과목: {subject})")
                                skipped_students += 1
                                continue
                            
                            # 특수문자나 이상한 문자 처리
                            if len(student_name) > 20 or any(char in student_name for char in ['<', '>', '|', '?', '*']):
                                print(f"[경고] 행 {idx}: 이상한 이름 형식 '{student_name}' 건너뜀 (과목: {subject})")
                                skipped_students += 1
                                continue
                                
                        except Exception as e:
                            print(f"[경고] 행 {idx}: 수험번호/이름 처리 오류 (과목: {subject}): {str(e)}")
                            import traceback
                            traceback.print_exc()
                            skipped_students += 1
                            continue
                        
                        # 학생 ID 생성 (수험번호 사용)
                        student_id = exam_number
                        
                        # 학생 데이터 초기화
                        if student_id not in student_data:
                            student_data[student_id] = {
                                'name': student_name,
                                'student_id': student_id,
                                'subjects': {}
                            }
                        
                        # 과목 정보 저장 (결시 처리 포함)
                        try:
                            # 총점 처리 (결시 및 오류 상황 대응)
                            total_score = row['총점']
                            try:
                                if pd.isna(total_score) or total_score == '' or str(total_score).strip().lower() in ['결시', 'absent', '미응시', '불참', 'nan', 'none']:
                                    total_score = 0
                                    print(f"[결시] {student_name}: {subject} 결시 처리 (0점)")
                                else:
                                    total_score = float(total_score)
                                    # 음수나 비정상적인 점수 처리
                                    if total_score < 0:
                                        total_score = 0
                                        print(f"[경고] {student_name}: {subject} 음수 점수 0으로 처리")
                                    elif total_score > 100:
                                        print(f"[경고] {student_name}: {subject} 100점 초과 점수 {total_score}")
                            except (ValueError, TypeError) as e:
                                print(f"[경고] {student_name}: {subject} 총점 변환 오류 '{total_score}' -> 0점 처리")
                                total_score = 0
                            
                            # 정답수 처리 (결시 및 오류 상황 대응)
                            correct_count = row['정답수']
                            try:
                                if pd.isna(correct_count) or correct_count == '' or str(correct_count).strip().lower() in ['결시', 'absent', '미응시', '불참', 'nan', 'none']:
                                    correct_count = 0
                                else:
                                    correct_count = float(correct_count)
                                    # 음수나 비정상적인 정답수 처리
                                    if correct_count < 0:
                                        correct_count = 0
                                    elif correct_count > 50:  # 일반적인 최대 문제 수
                                        print(f"[경고] {student_name}: {subject} 비정상적인 정답수 {correct_count}")
                            except (ValueError, TypeError) as e:
                                print(f"[경고] {student_name}: {subject} 정답수 변환 오류 '{correct_count}' -> 0개 처리")
                                correct_count = 0
                            
                            subject_info = {
                                'subject_name': str(row['선택과목']).strip() if pd.notna(row['선택과목']) else '',
                                'subject_code': str(row['선택과목코드']).strip() if pd.notna(row['선택과목코드']) else '',
                                'total_score': total_score,
                                'correct_count': correct_count,
                                'wrong_answers': self._parse_wrong_answers(row['오답번호'])
                            }
                        except Exception as e:
                            print(f"[경고] 과목 정보 저장 오류 (학생: {student_name}, 과목: {subject}): {str(e)}")
                            # 기본값으로 설정
                            subject_info = {
                                'subject_name': '',
                                'subject_code': '',
                                'total_score': 0,
                                'correct_count': 0,
                                'wrong_answers': []
                            }
                        
                        student_data[student_id]['subjects'][subject] = subject_info
                        processed_students += 1
                        
                    except Exception as e:
                        print(f"[오류] 행 {idx} 처리 오류 (학생: {student_name if 'student_name' in locals() else 'Unknown'}, 과목: {subject}): {str(e)}")
                        print(f"[오류] 오류 타입: {type(e).__name__}")
                        print(f"[오류] 오류 상세: {str(e)}")
                        import traceback
                        print(f"[오류] 스택 트레이스:")
                        traceback.print_exc()
                        skipped_students += 1
                        continue
            
            print(f"[통합] 데이터 통합 완료: {processed_students}개 처리, {skipped_students}개 건너뜀")
            
            if not student_data:
                raise Exception("[오류] 처리된 학생 데이터가 없습니다. 모든 데이터가 유효하지 않거나 오류가 발생했습니다.")
            
            # 등급 및 표점 계산
            print("[계산] 등급 및 표점 계산 시작...")
            calculation_errors = 0
            
            for student_id, student_info in student_data.items():
                for subject, subject_info in student_info['subjects'].items():
                    try:
                        grade_info = self._calculate_grade_and_score(subject_info)
                        subject_info.update(grade_info)
                    except Exception as e:
                        print(f"[오류] 등급 계산 오류 (학생: {student_info['name']}, 과목: {subject}): {str(e)}")
                        calculation_errors += 1
                        # 기본값 설정
                        subject_info.update({
                            'grade': 9,
                            'standard_score': 0,
                            'percentile': 0
                        })
            
            if calculation_errors > 0:
                print(f"[경고] {calculation_errors}개의 등급 계산에서 오류가 발생했습니다. 기본값으로 설정되었습니다.")
            
            print(f"[완료] 전체 데이터 처리 완료: {len(student_data)}명의 학생")
            return student_data
            
        except Exception as e:
            import traceback
            error_details = traceback.format_exc()
            raise Exception(f"[오류] 데이터 처리 중 오류 발생:\n{str(e)}\n\n상세 오류:\n{error_details}")
    
    def _set_default_grade_cutoffs(self):
        """기본 등급컷 설정"""
        self.grade_cutoff_data = {}
        self.standard_scores = {}
        self.grade_standard_scores = {}
        
        # 모든 과목에 대한 기본 등급컷 설정 (기본 과목 + 선택과목)
        all_subjects = [
            "국어", "언어와 매체", "화법과 작문",
            "수학", "확률과 통계", "미적분", "기하",
            "영어", "한국사",
            "생활과 윤리", "윤리와 사상", "한국지리", "세계지리", "동아시아사", "세계사", "경제", "정치와 법", "사회·문화",
            "물리학 I", "화학 I", "생명과학 I", "지구과학 I", "물리학 II", "화학 II", "생명과학 II", "지구과학 II"
        ]
        
        for subject in all_subjects:
            if subject == "영어":
                # 영어: 90, 80, 70, 60, 50, 40, 30, 20, 0
                self.grade_cutoff_data[subject] = {i: 90 - (i-1)*10 for i in range(1, 10)}
                self.standard_scores[subject] = 0
                self.grade_standard_scores[subject] = {i: 0 for i in range(1, 10)}
            elif subject == "한국사":
                # 한국사: 40, 35, 30, 25, 20, 15, 10, 5, 0
                self.grade_cutoff_data[subject] = {i: 40 - (i-1)*5 for i in range(1, 10)}
                self.standard_scores[subject] = 0
                self.grade_standard_scores[subject] = {i: 0 for i in range(1, 10)}
            else:
                # 기타 과목: 90, 80, 70, 60, 50, 40, 30, 20, 0
                self.grade_cutoff_data[subject] = {i: 90 - (i-1)*10 for i in range(1, 10)}
                self.standard_scores[subject] = 100
                self.grade_standard_scores[subject] = {i: 100 - (i-1)*10 for i in range(1, 10)}
        
    def _generate_student_id(self, name: str) -> str:
        """학생 ID 생성 (이름 기반) - 강화된 오류 처리"""
        try:
            # 이름 정리 (다양한 공백 문자 처리)
            clean_name = str(name).strip()
            
            # 빈 이름 처리
            if not clean_name:
                print(f"[경고] 빈 이름으로 ID 생성 시도")
                return f"STU_EMPTY_{hash(name) % 10000}"
            
            # 특수 문자 제거 및 정리
            clean_name = clean_name.replace(' ', '_').replace('\t', '_').replace('\n', '_').replace('\r', '_')
            
            # 연속된 언더스코어 정리
            while '__' in clean_name:
                clean_name = clean_name.replace('__', '_')
            
            # 앞뒤 언더스코어 제거
            clean_name = clean_name.strip('_')
            
            # 최종 검증
            if not clean_name or len(clean_name) == 0:
                print(f"[경고] 정리 후 빈 이름: '{name}' -> '{clean_name}'")
                return f"STU_EMPTY_{hash(name) % 10000}"
            
            student_id = f"STU_{clean_name}"
            return student_id
            
        except Exception as e:
            print(f"[오류] 학생 ID 생성 오류 (이름: '{name}'): {str(e)}")
            import traceback
            traceback.print_exc()
            return f"STU_ERROR_{hash(name) % 10000}"
        
    def _parse_wrong_answers(self, wrong_answers_str) -> List[int]:
        """오답 번호 파싱 - 결시 및 빈 데이터 처리"""
        try:
            # None, NaN, 빈 문자열 처리
            if pd.isna(wrong_answers_str) or wrong_answers_str == '' or wrong_answers_str is None:
                return []
            
            # 문자열로 변환
            wrong_answers_str = str(wrong_answers_str).strip()
            
            # 결시 표시 처리
            if wrong_answers_str.lower() in ['결시', 'absent', '미응시', '불참']:
                return []
            
            # 쉼표로 구분된 번호들을 정수 리스트로 변환
            wrong_answers = []
            for num_str in wrong_answers_str.split(','):
                num_str = num_str.strip()
                if num_str.isdigit():
                    wrong_answers.append(int(num_str))
            return wrong_answers
        except Exception as e:
            print(f"[경고] 오답번호 파싱 오류: {wrong_answers_str} -> {str(e)}")
            return []
            
    def _calculate_grade_and_score(self, subject_info: Dict) -> Dict:
        """등급 및 표점 계산 - 과목코드만으로 검증"""
        try:
            total_score = subject_info['total_score']
            subject_code = subject_info.get('subject_code', '')
            
            # 결시 처리 (0점인 경우)
            if total_score == 0:
                return {
                    'grade': 9,
                    'standard_score': 0,
                    'percentile': 0
                }
            
            # 과목코드로만 매칭 (과목명은 무시)
            matched_subject = None
            
            if subject_code and self.grade_cutoff_data:
                for key, code in self.subject_codes.items():
                    # 숫자와 문자열 모두 지원
                    subject_code_str = str(subject_code).strip()
                    code_str = str(code).strip()
                    
                    # 소수점 제거 (5.0 -> 5)
                    if '.' in subject_code_str:
                        subject_code_str = subject_code_str.split('.')[0]
                    
                    # 한 자리 숫자를 두 자리로 변환 (7 -> 07)
                    if len(subject_code_str) == 1:
                        subject_code_str = f"0{subject_code_str}"
                    
                    if subject_code_str == code_str and key in self.grade_cutoff_data:
                        matched_subject = key
                        break
            
            # 등급컷 데이터가 있으면 계산
            if matched_subject and self.grade_cutoff_data:
                grade_cutoffs = self.grade_cutoff_data[matched_subject]
                max_standard_score = self.standard_scores.get(matched_subject, 100)
                
                # 등급 계산
                grade = self._calculate_grade_from_cutoffs(total_score, grade_cutoffs)
                
                # 표점 및 백분위 계산
                standard_score, percentile = self._calculate_standard_score_and_percentile_new(
                    total_score, grade, grade_cutoffs, max_standard_score
                )
                
                return {
                    'grade': grade,
                    'standard_score': standard_score,
                    'percentile': percentile
                }
            
            # 등급컷 데이터가 없으면 원점수만 표시
            return {
                'grade': None,
                'standard_score': None,
                'percentile': None
            }
            
        except Exception as e:
            # 오류가 발생해도 원점수는 표시
            return {
                'grade': None,
                'standard_score': None,
                'percentile': None
            }
            
    def _calculate_grade_from_cutoffs(self, score: float, grade_cutoffs: Dict[int, float]) -> int:
        """등급컷을 사용한 등급 계산 (1-9등급)"""
        for grade in range(1, 10):
            if score >= grade_cutoffs.get(grade, 0):
                return grade
        return 9  # 모든 등급컷보다 낮으면 9등급
            
    def _calculate_standard_score_and_percentile_new(self, score: float, grade: int, 
                                                   grade_cutoffs: Dict[int, float], 
                                                   max_standard_score: float) -> tuple:
        """표준점수 및 백분위 계산 (등급별 표점 사용)"""
        try:
            # 한국사와 영어는 표점과 백분위 없음
            if max_standard_score == 0:
                return None, None
            
            # 등급별 표점이 설정되어 있는지 확인
            subject_name = None
            for key in self.grade_standard_scores.keys():
                if key in str(score) or str(score) in key:  # 임시로 점수로 찾기
                    subject_name = key
                    break
            
            if subject_name and subject_name in self.grade_standard_scores:
                grade_std_scores = self.grade_standard_scores[subject_name]
                
                # 등급별 표점 사용
                if grade in grade_std_scores:
                    base_standard_score = grade_std_scores[grade]
                    
                    # 등급 내에서 선형 보간
                    if grade > 1:
                        lower_grade = grade - 1
                        if lower_grade in grade_std_scores:
                            lower_cutoff = grade_cutoffs.get(lower_grade, 0)
                            upper_cutoff = grade_cutoffs.get(grade, 0)
                            
                            if upper_cutoff > lower_cutoff:
                                # 등급 내에서의 비율 계산
                                ratio = (score - upper_cutoff) / (lower_cutoff - upper_cutoff)
                                ratio = max(0, min(1, ratio))  # 0-1 범위로 제한
                                
                                lower_std_score = grade_std_scores[lower_grade]
                                standard_score = base_standard_score + (lower_std_score - base_standard_score) * ratio
                            else:
                                standard_score = base_standard_score
                        else:
                            standard_score = base_standard_score
                    else:
                        standard_score = base_standard_score
                else:
                    # 기본 계산
                    standard_score = max_standard_score * (1 - (grade-1) * 0.1)
            else:
                # 기본 계산 (등급별 표점이 없는 경우)
                standard_score = max_standard_score * (1 - (grade-1) * 0.1)
            
            # 백분위 계산 (등급 기반)
            percentile_map = {1: 95, 2: 85, 3: 75, 4: 65, 5: 55, 6: 45, 7: 35, 8: 25, 9: 15}
            percentile = percentile_map.get(grade, 50)
                
            return int(standard_score), percentile
            
        except Exception as e:
            print(f"표준점수 계산 오류: {str(e)}")
            return None, None
            
    def _calculate_grade(self, score: float, cutoff_data: pd.Series) -> int:
        """등급 계산"""
        # 등급컷 데이터에서 1등급부터 9등급까지의 컷 확인
        for grade in range(1, 10):
            cutoff_col = f'{grade}등급컷'
            if cutoff_col in cutoff_data and not pd.isna(cutoff_data[cutoff_col]):
                if score >= cutoff_data[cutoff_col]:
                    return grade
        return 9  # 기본값
        
    def _calculate_standard_score_and_percentile(self, score: float, grade: int, cutoff_data: pd.Series) -> tuple:
        """표점 및 백분위 계산"""
        try:
            # 표점 계산 (등급별 표점)
            standard_score_col = f'{grade}등급표점'
            if standard_score_col in cutoff_data and not pd.isna(cutoff_data[standard_score_col]):
                standard_score = cutoff_data[standard_score_col]
            else:
                standard_score = None
                
            # 백분위 계산 (등급별 백분위)
            percentile_col = f'{grade}등급백분위'
            if percentile_col in cutoff_data and not pd.isna(cutoff_data[percentile_col]):
                percentile = cutoff_data[percentile_col]
            else:
                percentile = None
                
            return standard_score, percentile
            
        except Exception as e:
            print(f"표점/백분위 계산 오류: {str(e)}")
            return None, None
