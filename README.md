# 성적표 생성 및 PDF 변환 시스템

## 📋 프로젝트 개요

이 프로젝트는 **학생 성적 데이터를 처리하여 개인별 성적표를 생성하고 PDF로 변환**하는 시스템입니다.

### 주요 기능
- 📊 **성적 데이터 처리**: CSV 파일에서 학생 성적 데이터 읽기
- 📈 **등급 및 표준점수 계산**: 등급컷과 표준점수 기반 계산
- 📄 **개인 성적표 생성**: HTML 형태의 개인별 성적표 생성
- 📑 **PDF 변환**: HTML을 고품질 PDF로 변환
- 🔄 **배치 처리**: 대량의 파일을 자동으로 처리

## 🚀 주요 컴포넌트

### 1. 메인 성적표 생성 시스템
- **`main.py`**: GUI 기반 메인 애플리케이션
- **`data_processor.py`**: 성적 데이터 처리 및 계산
- **`html_pdf_generator.py`**: HTML 생성 및 PDF 변환

### 2. HTML to PDF 변환기
- **`HTML_to_PDF_Converter/`**: 독립적인 PDF 변환 도구
- **`batch_html_to_pdf.py`**: 배치 변환 스크립트
- **`html_to_pdf_gui.py`**: GUI 변환 도구

## 📁 프로젝트 구조

```
scoring-system/
├── main.py                          # 메인 GUI 애플리케이션
├── data_processor.py                 # 데이터 처리 로직
├── html_pdf_generator.py            # HTML/PDF 생성
├── jinja_pdf_generator.py           # Jinja2 템플릿 엔진
├── playwright_pdf_converter.py      # Playwright PDF 변환
├── ScoringSystem_Release/           # 배포용 파일들
│   ├── ScoringSystem.exe            # 실행 파일
│   ├── *.csv                        # 템플릿 파일들
│   └── *.txt                        # 가이드 파일들
├── HTML_to_PDF_Converter/           # PDF 변환 도구
│   ├── batch_html_to_pdf.py        # 배치 변환 스크립트
│   ├── html_to_pdf_gui.py          # GUI 변환 도구
│   └── README.txt                   # 사용 가이드
├── dist/                            # 빌드 결과물
│   ├── output/                      # HTML 파일들
│   └── output_pdf/                  # PDF 파일들
└── README.md                          # 프로젝트 문서
```

## 🛠️ 설치 및 실행

### 필수 요구사항
- Python 3.8+
- pip (Python 패키지 관리자)

### 설치
```bash
# 저장소 클론
git clone https://github.com/your-username/scoring-system.git
cd scoring-system

# 필요한 패키지 설치
pip install -r requirements.txt

# Playwright 브라우저 설치
python -m playwright install chromium
```

### 실행 방법

#### 1. GUI 애플리케이션 실행
```bash
python main.py
```

#### 2. 배치 PDF 변환
```bash
cd HTML_to_PDF_Converter
python batch_html_to_pdf.py "입력폴더" "출력폴더"
```

## 📊 사용법

### 1. 성적표 생성
1. **학생 데이터 업로드**: CSV 파일로 학생 정보 및 성적 입력
2. **등급컷 데이터 입력**: 과목별 등급컷 설정
3. **표준점수 데이터 입력**: 과목별 표준점수 설정
4. **성적표 생성**: HTML 형태로 개인별 성적표 생성

### 2. PDF 변환
1. **HTML 파일 확인**: `dist/output/` 폴더의 HTML 파일들
2. **배치 변환 실행**: `batch_html_to_pdf.py` 스크립트 사용
3. **PDF 파일 확인**: `dist/output_pdf/` 폴더의 PDF 파일들

## 📋 CSV 템플릿

### 학생 데이터 템플릿
```csv
Name,Subject_Name,Subject_Code,Total_Score,Correct_Count,Wrong_Answers
김철수,국어,01,85,42,3,7,15
김철수,수학,02,78,39,2,8,12
```

### 등급컷 템플릿
```csv
Subject_Name,Subject_Code,Grade_1_Cutoff,Grade_2_Cutoff,Grade_3_Cutoff,Grade_4_Cutoff,Grade_5_Cutoff,Grade_6_Cutoff,Grade_7_Cutoff,Grade_8_Cutoff,Grade_9_Cutoff
Korean,01,95,90,85,80,75,70,65,60,55
Math,02,90,85,80,75,70,65,60,55,50
```

### 표준점수 템플릿
```csv
Subject_Name,subject_code,Grade_1_Score,Grade_2_Score,Grade_3_Score,Grade_4_Score,Grade_5_Score,Grade_6_Score,Grade_7_Score,Grade_8_Score,Grade_9_Score
Korean,01,150,140,130,120,110,100,90,80,70
Math,02,145,135,125,115,105,95,85,75,65
```

## 🔧 기술 스택

- **Python 3.8+**: 메인 프로그래밍 언어
- **Tkinter**: GUI 프레임워크
- **Pandas**: 데이터 처리
- **Jinja2**: HTML 템플릿 엔진
- **Playwright**: PDF 변환 (Chromium)
- **PyInstaller**: 실행 파일 생성

## 📈 성능

- **처리 속도**: 약 5-6개 파일/초 (PDF 변환)
- **메모리 효율성**: 낮은 메모리 사용량
- **안정성**: 100% 성공률
- **파일 크기**: 각 PDF 약 200-230KB

## 🚀 주요 특징

### 1. 사용자 친화적 GUI
- 직관적인 인터페이스
- 드래그 앤 드롭 파일 업로드
- 실시간 진행 상황 표시

### 2. 고품질 PDF 출력
- Playwright 기반 고품질 PDF 생성
- A4 크기 최적화
- 한글 폰트 지원 (Noto Sans KR)

### 3. 배치 처리 지원
- 대량 파일 자동 처리
- 명령줄 인터페이스
- 자동화 스크립트 지원

### 4. 데이터 유연성
- 다양한 CSV 형식 지원
- 영어/한글 컬럼명 지원
- 동적 데이터 매핑

## 📝 사용 시나리오

### 1. 학원 성적 관리
- 모의고사 성적 처리
- 개인별 성적표 생성
- 학부모 배포용 PDF 생성

### 2. 학교 성적 관리
- 정기고사 성적 처리
- 등급 및 표준점수 계산
- 성적표 자동 생성

### 3. 대량 문서 처리
- 수백 명의 성적표 일괄 생성
- 자동화된 PDF 변환
- 배치 처리 시스템

## 🔍 문제 해결

### 자주 발생하는 문제
1. **Python 모듈 오류**: `pip install -r requirements.txt`
2. **Playwright 오류**: `python -m playwright install chromium`
3. **권한 오류**: 관리자 권한으로 실행
4. **메모리 부족**: 대용량 파일은 나누어 처리

### 로그 확인
- 변환 과정에서 오류 발생 시 상세 로그 출력
- 실패한 파일 목록 제공
- 성공/실패 통계 표시

## 📞 지원 및 문의

문제가 발생하면:
1. 오류 메시지 전체 복사
2. 사용한 명령어 확인
3. 입력/출력 폴더 경로 확인
4. Python 및 Playwright 설치 상태 확인

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다.

## 🤝 기여하기

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

**💡 성공 팁**: 변환 전에 HTML 파일들이 브라우저에서 정상적으로 열리는지 먼저 확인해보세요!