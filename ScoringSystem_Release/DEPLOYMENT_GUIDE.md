# 성적관리 시스템 배포 가이드

## 📦 배포 파일 구성

### 🎯 메인 프로그램
- **`ScoringSystem.exe`** - 성적관리 시스템 (메인 프로그램)
- **`HTML_to_PDF_Converter.exe`** - HTML → PDF 변환기 (별도 프로그램)

### 📋 CSV 템플릿 파일들
- **`grade_cutoff_upload_template.csv`** - 등급컷 업로드 템플릿
- **`grade_standard_scores_upload_template.csv`** - 표점 업로드 템플릿  
- **`subject_codes_upload_template.csv`** - 과목코드 업로드 템플릿

### 📖 문서 파일들
- **`README.txt`** - 기본 사용법 안내
- **`CSV_Templates_Guide.txt`** - CSV 템플릿 사용 가이드
- **`DEPLOYMENT_GUIDE.md`** - 이 파일 (배포 가이드)

## 🚀 사용법

### 1. 메인 성적관리 시스템 사용
1. **`ScoringSystem.exe`** 실행
2. **과목별 점수 파일 업로드** (국어, 수학, 영어, 한국사, 탐구1, 탐구2)
3. **등급컷 및 표점 설정**:
   - GUI에서 직접 입력 또는
   - CSV 파일 업로드 (등급컷 CSV 업로드, 표점 CSV 업로드 버튼 사용)
4. **"데이터 처리"** 버튼 클릭
5. **"PDF 생성"** 버튼 클릭
6. **output 폴더**에서 PDF 파일 확인

### 2. HTML → PDF 변환기 사용
1. **`HTML_to_PDF_Converter.exe`** 실행
2. **HTML 파일 선택** 또는 **HTML 폴더 선택**
3. **출력 폴더 지정**
4. **"변환 시작"** 버튼 클릭
5. **PDF 파일 생성 완료**

## 📊 CSV 파일 형식

### 등급컷 업로드 템플릿
```
Subject_Name,Subject_Code,Grade_1_Cutoff,Grade_2_Cutoff,...,Grade_9_Cutoff
Korean,01,90,80,70,60,50,40,30,20,0
Language_and_Media,05,90,80,70,60,50,40,30,20,0
...
```

### 표점 업로드 템플릿  
```
Subject_Name,Subject_Code,Grade_1_Score,Grade_2_Score,...,Grade_9_Score
Korean,01,100,90,80,70,60,50,40,30,20
Language_and_Media,05,100,90,80,70,60,50,40,30,20
...
```

### 과목코드 업로드 템플릿
```
Subject_Name,Subject_Code,Category
Korean,01,Language
Language_and_Media,05,Language
Math,02,Mathematics
...
```

## 🔧 주요 기능

### 메인 성적관리 시스템
- ✅ **과목별 점수 파일 업로드** (CSV/Excel)
- ✅ **등급컷 및 표점 설정** (GUI 입력 또는 CSV 업로드)
- ✅ **표준점수 및 백분위 계산**
- ✅ **등급 자동 계산**
- ✅ **개별 PDF 성적표 생성**
- ✅ **HTML 파일 저장 옵션**

### HTML → PDF 변환기
- ✅ **단일 HTML 파일 변환**
- ✅ **폴더 내 모든 HTML 파일 일괄 변환**
- ✅ **고품질 PDF 출력** (Playwright 기반)
- ✅ **한글 폰트 지원**
- ✅ **CSS 스타일 완벽 재현**

## 📁 폴더 구조

```
ScoringSystem_Release/
├── ScoringSystem.exe                    # 메인 프로그램
├── HTML_to_PDF_Converter.exe           # PDF 변환기
├── grade_cutoff_upload_template.csv    # 등급컷 템플릿
├── grade_standard_scores_upload_template.csv  # 표점 템플릿
├── subject_codes_upload_template.csv   # 과목코드 템플릿
├── README.txt                          # 사용법 안내
├── CSV_Templates_Guide.txt             # CSV 가이드
└── DEPLOYMENT_GUIDE.md                 # 배포 가이드
```

## ⚠️ 주의사항

### 시스템 요구사항
- **Windows 10/11** (64비트)
- **메모리**: 최소 4GB RAM 권장
- **디스크**: 최소 1GB 여유 공간

### 파일 경로
- **한글이나 특수문자가 포함된 경로** 사용 금지
- **영문 경로** 사용 권장 (예: `C:\ScoringSystem\`)

### 데이터 파일
- **CSV 파일**: UTF-8 인코딩 권장
- **Excel 파일**: .xlsx 형식 지원
- **파일 크기**: 과목당 최대 10MB 권장

## 🆘 문제 해결

### 일반적인 문제
1. **EXE 파일이 실행되지 않음**
   - Windows Defender 실시간 보호 일시 해제
   - 관리자 권한으로 실행

2. **PDF 생성 실패**
   - output 폴더 권한 확인
   - 디스크 공간 확인

3. **CSV 업로드 실패**
   - 파일 형식 확인 (UTF-8 인코딩)
   - 컬럼명 정확성 확인

### 지원
- **문제 발생 시**: 상세한 오류 메시지와 함께 문의
- **재현 가능한 예제** 제공 시 더 빠른 해결 가능

## 📈 업데이트 내역

### v2.0 (최신)
- ✅ **CSV 업로드 기능** 추가
- ✅ **HTML → PDF 변환기** 분리
- ✅ **영어 템플릿** 제공
- ✅ **과목코드 기반 매칭** 개선
- ✅ **오류 처리** 강화

### v1.0
- ✅ 기본 성적관리 기능
- ✅ PDF 생성 기능
- ✅ GUI 인터페이스

---

**🎉 성적관리 시스템 v2.0 배포 완료!**

**모든 기능이 정상 작동하며, CSV 업로드와 HTML → PDF 변환 기능이 추가되었습니다.**

