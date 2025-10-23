# Score Report System

학생 성적 관리 및 성적표 생성 시스템입니다.

## 🚀 주요 기능

- **CSV 데이터 업로드**: 학생 성적 데이터를 CSV 파일로 업로드
- **성적표 생성**: HTML 기반 성적표 자동 생성
- **PDF 변환**: HTML을 PDF로 변환하여 출력
- **배치 처리**: 여러 학생의 성적표를 한번에 생성

## 📋 시스템 구성

### 핵심 컴포넌트
- `main.py`: 메인 GUI 애플리케이션
- `data_processor.py`: 데이터 처리 및 계산 로직
- `html_pdf_generator.py`: HTML to PDF 변환기
- `jinja_pdf_generator.py`: Jinja2 템플릿 기반 PDF 생성

### HTML to PDF 변환기
- `playwright_pdf_converter.py`: Playwright 기반 PDF 변환
- `batch_html_to_pdf.py`: 배치 변환 처리
- `HTML_to_PDF_Converter/`: 독립 실행 가능한 변환기

## 🛠️ 설치 및 실행

### 요구사항
- Python 3.8+
- Playwright
- Jinja2
- pandas
- tkinter

### 설치
```bash
pip install -r requirements.txt
playwright install chromium
```

### 실행
```bash
# 메인 애플리케이션
python main.py

# HTML to PDF 변환기 GUI
python HTML_to_PDF_Converter/html_to_pdf_gui.py

# 배치 변환
python batch_html_to_pdf.py input_folder output_folder
```

## 📊 데이터 형식

### 학생 성적 CSV 형식
```csv
이름,선택과목,선택과목코드,총점,정답수,오답번호
김철수,언어와매체,5,95,43/45,"12, 19"
```

### 과목 코드 체계
- **국어 영역**: 01(국어), 05(언어와매체), 06(화법과작문)
- **수학 영역**: 02(수학), 03(확률과통계), 04(미적분), 09(기하)
- **언어**: 07(영어)
- **한국사**: 08
- **사회탐구**: 11-19 (생활과윤리, 윤리와사상, 한국지리 등)
- **과학탐구**: 21-28 (물리학I, 화학I, 생명과학I 등)

## 🎯 사용법

1. **성적 데이터 준비**: CSV 형식으로 학생 성적 데이터 준비
2. **등급컷 설정**: 각 과목별 등급컷 및 표준점수 설정
3. **성적표 생성**: GUI에서 데이터 업로드 후 성적표 생성
4. **PDF 변환**: HTML 성적표를 PDF로 변환

## 📁 프로젝트 구조

```
scoring-system/
├── main.py                          # 메인 애플리케이션
├── data_processor.py               # 데이터 처리
├── html_pdf_generator.py           # HTML to PDF 변환
├── jinja_pdf_generator.py          # Jinja2 PDF 생성
├── playwright_pdf_converter.py     # Playwright 변환기
├── batch_html_to_pdf.py            # 배치 변환
├── templates/                      # HTML 템플릿
│   └── report.html
├── HTML_to_PDF_Converter/          # 독립 변환기
│   ├── html_to_pdf_gui.py
│   └── playwright_pdf_converter.py
├── sample_*.csv                    # 샘플 데이터
└── requirements.txt                # 의존성
```

## 🔧 개발 정보

- **개발자**: SN독학기숙학원
- **버전**: 2.0.0
- **빌드일**: 2025-01-27

## 📞 문의

본 프로그램은 SN독학기숙학원이 개발하였습니다.