import pandas as pd
import random
import os

def generate_sample_data():
    """샘플 데이터 생성"""
    
    # 학생 목록
    students = [
        "김철수", "이영희", "박민수", "최지영", "정수현",
        "강동원", "윤서연", "임태호", "한소영", "조현우"
    ]
    
    # 과목별 데이터 생성
    subjects = ["국어", "수학", "영어", "한국사", "탐구1", "탐구2"]
    subject_codes = ["01", "02", "03", "04", "11", "12"]  # 탐구1, 탐구2는 임시 코드
    
    for i, subject in enumerate(subjects):
        data = []
        
        for student in students:
            # 랜덤 점수 생성 (0-100)
            total_score = random.randint(60, 100)
            correct_count = random.randint(15, 25)
            
            # 오답 번호 생성 (1-30 중에서 랜덤하게)
            wrong_count = 30 - correct_count
            wrong_answers = random.sample(range(1, 31), wrong_count)
            wrong_answers_str = ','.join(map(str, sorted(wrong_answers)))
            
            data.append({
                '이름': student,
                '선택과목': subject,
                '선택과목코드': subject_codes[i],
                '총점': total_score,
                '정답수': correct_count,
                '오답번호': wrong_answers_str
            })
        
        # CSV 파일로 저장
        df = pd.DataFrame(data)
        filename = f"sample_{subject}.csv"
        df.to_csv(filename, index=False, encoding='utf-8-sig')
        print(f"{filename} 생성 완료")
    
    # 등급컷 데이터 생성
    grade_cutoff_data = []
    
    # 모든 과목 코드 (01-28)
    all_codes = ["01", "02", "03", "04", "11", "12", "13", "14", "15", "16", "17", "18", "19", 
                 "21", "22", "23", "24", "25", "26", "27", "28"]
    
    for code in all_codes:
        # 등급별 컷 생성 (1등급이 가장 높은 점수)
        cuts = []
        for grade in range(1, 10):
            if grade == 1:
                cut = random.randint(90, 100)
            elif grade == 2:
                cut = random.randint(80, 89)
            elif grade == 3:
                cut = random.randint(70, 79)
            elif grade == 4:
                cut = random.randint(60, 69)
            elif grade == 5:
                cut = random.randint(50, 59)
            elif grade == 6:
                cut = random.randint(40, 49)
            elif grade == 7:
                cut = random.randint(30, 39)
            elif grade == 8:
                cut = random.randint(20, 29)
            else:  # 9등급
                cut = random.randint(0, 19)
            
            cuts.append(cut)
        
        # 표점과 백분위 생성
        standard_scores = []
        percentiles = []
        
        for grade in range(1, 10):
            # 표점 (등급이 높을수록 높은 표점)
            if grade == 1:
                std_score = random.randint(90, 100)
                percentile = random.randint(90, 100)
            elif grade == 2:
                std_score = random.randint(80, 89)
                percentile = random.randint(80, 89)
            elif grade == 3:
                std_score = random.randint(70, 79)
                percentile = random.randint(70, 79)
            elif grade == 4:
                std_score = random.randint(60, 69)
                percentile = random.randint(60, 69)
            elif grade == 5:
                std_score = random.randint(50, 59)
                percentile = random.randint(50, 59)
            elif grade == 6:
                std_score = random.randint(40, 49)
                percentile = random.randint(40, 49)
            elif grade == 7:
                std_score = random.randint(30, 39)
                percentile = random.randint(30, 39)
            elif grade == 8:
                std_score = random.randint(20, 29)
                percentile = random.randint(20, 29)
            else:  # 9등급
                std_score = random.randint(0, 19)
                percentile = random.randint(0, 19)
            
            standard_scores.append(std_score)
            percentiles.append(percentile)
        
        # 데이터 행 생성
        row = {'과목코드': code}
        
        # 등급컷 추가
        for i, cut in enumerate(cuts):
            row[f'{i+1}등급컷'] = cut
        
        # 표점 추가
        for i, score in enumerate(standard_scores):
            row[f'{i+1}등급표점'] = score
        
        # 백분위 추가
        for i, percentile in enumerate(percentiles):
            row[f'{i+1}등급백분위'] = percentile
        
        grade_cutoff_data.append(row)
    
    # 등급컷 데이터를 DataFrame으로 변환하고 CSV로 저장
    grade_df = pd.DataFrame(grade_cutoff_data)
    grade_df.to_csv("sample_grade_cutoff.csv", index=False, encoding='utf-8-sig')
    print("sample_grade_cutoff.csv 생성 완료")
    
    print("\n샘플 데이터 생성 완료!")
    print("생성된 파일들:")
    print("- sample_국어.csv")
    print("- sample_수학.csv") 
    print("- sample_영어.csv")
    print("- sample_한국사.csv")
    print("- sample_탐구1.csv")
    print("- sample_탐구2.csv")
    print("- sample_grade_cutoff.csv")

if __name__ == "__main__":
    generate_sample_data()

