import pandas as pd

def create_grade_cutoff_csv():
    """등급컷 CSV 파일 생성"""
    
    # 과목별 등급컷 데이터
    grade_cutoffs = {
        # 국어 영역
        "국어": [90, 80, 70, 60, 50, 40, 30, 20, 0],
        "언어와 매체": [90, 80, 70, 60, 50, 40, 30, 20, 0],
        "화법과 작문": [90, 80, 70, 60, 50, 40, 30, 20, 0],
        
        # 수학 영역
        "수학": [90, 80, 70, 60, 50, 40, 30, 20, 0],
        "확률과 통계": [90, 80, 70, 60, 50, 40, 30, 20, 0],
        "미적분": [90, 80, 70, 60, 50, 40, 30, 20, 0],
        "기하": [90, 80, 70, 60, 50, 40, 30, 20, 0],
        
        # 언어 영역 (표점 없음)
        "영어": [90, 80, 70, 60, 50, 40, 30, 20, 0],
        
        # 한국사 (표점 없음)
        "한국사": [40, 35, 30, 25, 20, 15, 10, 5, 0],
        
        # 사회탐구 영역 (50점 만점)
        "생활과 윤리": [45, 40, 35, 30, 25, 20, 15, 10, 0],
        "윤리와 사상": [45, 40, 35, 30, 25, 20, 15, 10, 0],
        "한국지리": [45, 40, 35, 30, 25, 20, 15, 10, 0],
        "세계지리": [45, 40, 35, 30, 25, 20, 15, 10, 0],
        "동아시아사": [45, 40, 35, 30, 25, 20, 15, 10, 0],
        "세계사": [45, 40, 35, 30, 25, 20, 15, 10, 0],
        "경제": [45, 40, 35, 30, 25, 20, 15, 10, 0],
        "정치와 법": [45, 40, 35, 30, 25, 20, 15, 10, 0],
        "사회·문화": [45, 40, 35, 30, 25, 20, 15, 10, 0],
        
        # 과학탐구 영역 (50점 만점)
        "물리학 I": [45, 40, 35, 30, 25, 20, 15, 10, 0],
        "화학 I": [45, 40, 35, 30, 25, 20, 15, 10, 0],
        "생명과학 I": [45, 40, 35, 30, 25, 20, 15, 10, 0],
        "지구과학 I": [45, 40, 35, 30, 25, 20, 15, 10, 0],
        "물리학 II": [45, 40, 35, 30, 25, 20, 15, 10, 0],
        "화학 II": [45, 40, 35, 30, 25, 20, 15, 10, 0],
        "생명과학 II": [45, 40, 35, 30, 25, 20, 15, 10, 0],
        "지구과학 II": [45, 40, 35, 30, 25, 20, 15, 10, 0]
    }
    
    # 표점 데이터 (영어, 한국사는 0)
    standard_scores = {
        "국어": 100, "언어와 매체": 100, "화법과 작문": 100,
        "수학": 100, "확률과 통계": 100, "미적분": 100, "기하": 100,
        "영어": 0, "한국사": 0,
        "생활과 윤리": 100, "윤리와 사상": 100, "한국지리": 100, "세계지리": 100,
        "동아시아사": 100, "세계사": 100, "경제": 100, "정치와 법": 100, "사회·문화": 100,
        "물리학 I": 100, "화학 I": 100, "생명과학 I": 100, "지구과학 I": 100,
        "물리학 II": 100, "화학 II": 100, "생명과학 II": 100, "지구과학 II": 100
    }
    
    # 등급별 표점 데이터
    grade_standard_scores = {}
    for subject, max_score in standard_scores.items():
        if max_score > 0:
            grade_standard_scores[subject] = [max_score - i*10 for i in range(9)]
        else:
            grade_standard_scores[subject] = [0] * 9
    
    # CSV 파일 생성
    data = []
    for subject in grade_cutoffs.keys():
        row = {
            '과목명': subject,
            '과목코드': get_subject_code(subject),
            '만점_표점': standard_scores[subject],
            '1등급컷': grade_cutoffs[subject][0],
            '2등급컷': grade_cutoffs[subject][1],
            '3등급컷': grade_cutoffs[subject][2],
            '4등급컷': grade_cutoffs[subject][3],
            '5등급컷': grade_cutoffs[subject][4],
            '6등급컷': grade_cutoffs[subject][5],
            '7등급컷': grade_cutoffs[subject][6],
            '8등급컷': grade_cutoffs[subject][7],
            '9등급컷': grade_cutoffs[subject][8],
            '1등급_표점': grade_standard_scores[subject][0],
            '2등급_표점': grade_standard_scores[subject][1],
            '3등급_표점': grade_standard_scores[subject][2],
            '4등급_표점': grade_standard_scores[subject][3],
            '5등급_표점': grade_standard_scores[subject][4],
            '6등급_표점': grade_standard_scores[subject][5],
            '7등급_표점': grade_standard_scores[subject][6],
            '8등급_표점': grade_standard_scores[subject][7],
            '9등급_표점': grade_standard_scores[subject][8]
        }
        data.append(row)
    
    df = pd.DataFrame(data)
    df.to_csv('등급컷_표점_데이터.csv', index=False, encoding='utf-8-sig')
    print("등급컷 CSV 파일이 생성되었습니다: 등급컷_표점_데이터.csv")
    
    # 샘플 데이터도 생성
    sample_data = {
        '이름': ['김철수', '이영희', '박민수'],
        '선택과목': ['국어', '수학', '물리학 I'],
        '선택과목코드': ['01', '02', '21'],
        '총점': [85, 90, 75],
        '정답수': [20, 22, 18],
        '오답번호': ['1, 5, 10', '2, 8', '3, 7, 12']
    }
    
    sample_df = pd.DataFrame(sample_data)
    sample_df.to_csv('샘플_학생_데이터.csv', index=False, encoding='utf-8-sig')
    print("샘플 학생 데이터 CSV 파일이 생성되었습니다: 샘플_학생_데이터.csv")

def get_subject_code(subject):
    """과목명으로 과목코드 반환"""
    codes = {
        "국어": "01", "언어와 매체": "05", "화법과 작문": "06",
        "수학": "02", "확률과 통계": "03", "미적분": "04", "기하": "09",
        "영어": "07", "한국사": "08",
        "생활과 윤리": "11", "윤리와 사상": "12", "한국지리": "13", "세계지리": "14",
        "동아시아사": "15", "세계사": "16", "경제": "17", "정치와 법": "18", "사회·문화": "19",
        "물리학 I": "21", "화학 I": "22", "생명과학 I": "23", "지구과학 I": "24",
        "물리학 II": "25", "화학 II": "26", "생명과학 II": "27", "지구과학 II": "28"
    }
    return codes.get(subject, "")

if __name__ == "__main__":
    create_grade_cutoff_csv()