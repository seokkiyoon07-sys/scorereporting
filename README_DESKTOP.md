# Score Report System - Desktop Version

## 🖥️ 데스크톱 GUI 버전 성적 관리 시스템

이 폴더는 **Tkinter 기반 데스크톱 애플리케이션**입니다.

## 🚀 주요 특징

- **오프라인 사용**: 인터넷 연결 없이 사용 가능
- **간단한 설치**: EXE 파일만 실행하면 됨
- **로컬 실행**: 서버 불필요
- **개인 사용**: 단일 컴퓨터에서 사용

## 📋 웹 버전과의 차이점

| 항목 | GUI 버전 | 웹 버전 |
|------|----------|---------|
| 실행 환경 | Tkinter (로컬) | Flask (웹 서버) |
| 설치 필요 | 없음 (EXE 실행) | 없음 (브라우저만) |
| 오프라인 사용 | ✅ 가능 | ❌ 불가능 |
| 다중 사용자 | ❌ 불가능 | ✅ 가능 |
| 배포 | 로컬 설치 | 클라우드 배포 |
| 접근성 | 단일 컴퓨터 | 인터넷 어디서나 |

## 🛠️ 실행 방법

### Python으로 직접 실행

```bash
# 의존성 설치
pip install -r requirements.txt

# Playwright 브라우저 설치
playwright install chromium

# 애플리케이션 실행
python main.py
```

### EXE 파일 실행

`ScoringSystem_Release/ScoringSystem.exe` 실행

## 📁 주요 파일

```
scoring system/
├── main.py                    # GUI 애플리케이션 메인
├── data_processor.py          # 데이터 처리 (웹 버전과 공통)
├── html_pdf_generator.py      # HTML to PDF 변환
├── jinja_pdf_generator.py     # Jinja2 PDF 생성 (웹 버전과 공통)
├── templates/                 # HTML 템플릿
│   └── report.html
├── ScoringSystem_Release/     # 배포용 EXE 파일
│   └── ScoringSystem.exe
└── requirements.txt           # Python 의존성
```

## 🔧 개발 정보

- **GUI 프레임워크**: Tkinter
- **PDF 생성**: Playwright
- **빌드 도구**: PyInstaller

## ⚠️ 주의사항

이 버전은 **데스크톱 환경**을 위해 개발되었습니다.
웹 환경이 필요하면 `scorereporting/` 폴더의 웹 버전을 사용하세요.

