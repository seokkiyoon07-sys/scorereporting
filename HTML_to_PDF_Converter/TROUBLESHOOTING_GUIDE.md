# HTML → PDF 변환기 문제 해결 가이드

## 🚨 "하나도 변환하지 못한다" 문제 해결

### 1. 기본 확인사항

#### ✅ Playwright 설치 확인
```bash
# Playwright 설치 확인
python -c "from playwright.sync_api import sync_playwright; print('Playwright 설치됨')"

# Chromium 브라우저 설치 확인
python -m playwright install chromium
```

#### ✅ 파일 권한 확인
- HTML 파일이 읽기 가능한지 확인
- 출력 폴더가 쓰기 가능한지 확인
- 파일 경로에 한글이나 특수문자가 없는지 확인

### 2. 일반적인 문제와 해결방법

#### 🔧 문제 1: "Playwright 설치되지 않음"
**증상**: `ModuleNotFoundError: No module named 'playwright'`
**해결방법**:
```bash
pip install playwright
python -m playwright install chromium
```

#### 🔧 문제 2: "Chromium 브라우저 없음"
**증상**: `Browser executable not found`
**해결방법**:
```bash
python -m playwright install chromium
```

#### 🔧 문제 3: "파일 경로 오류"
**증상**: `FileNotFoundError` 또는 `PermissionError`
**해결방법**:
- 파일 경로에 한글, 공백, 특수문자 제거
- 절대 경로 사용
- 관리자 권한으로 실행

#### 🔧 문제 4: "메모리 부족"
**증상**: 변환 중 프로그램 종료
**해결방법**:
- 큰 HTML 파일을 작은 단위로 분할
- 시스템 메모리 확인
- 다른 프로그램 종료

#### 🔧 문제 5: "한글 폰트 문제"
**증상**: PDF에서 한글이 깨짐
**해결방법**:
- 시스템에 한글 폰트 설치 (맑은 고딕, 나눔고딕 등)
- CSS에서 폰트 지정: `font-family: 'Malgun Gothic', sans-serif;`

### 3. 단계별 디버깅

#### Step 1: 기본 변환 테스트
```bash
cd HTML_to_PDF_Converter
python debug_converter.py
```

#### Step 2: 실제 시나리오 테스트
```bash
python test_real_scenario.py
```

#### Step 3: GUI 테스트
```bash
python html_to_pdf_gui.py
```

#### Step 4: 배치 변환 테스트
```bash
python batch_html_to_pdf.py
```

### 4. 로그 확인

#### 상세 오류 메시지 확인
- GUI에서 "상세 로그" 옵션 활성화
- 콘솔 출력에서 오류 메시지 확인
- `debug_converter.py` 실행하여 단계별 확인

#### 파일 상태 확인
```bash
# HTML 파일 존재 확인
dir *.html

# PDF 파일 생성 확인  
dir *.pdf

# 파일 크기 확인
dir *.pdf | findstr "bytes"
```

### 5. 고급 문제 해결

#### 🔧 문제 6: "CSS 스타일 적용 안됨"
**해결방법**:
- CSS에서 `@page` 규칙 사용
- `print_background=True` 옵션 확인
- 인라인 스타일 사용

#### 🔧 문제 7: "JavaScript 실행 안됨"
**해결방법**:
- Playwright는 JavaScript 지원
- `page.wait_for_load_state('networkidle')` 사용
- 동적 콘텐츠 로딩 대기

#### 🔧 문제 8: "큰 파일 변환 실패"
**해결방법**:
- 파일을 작은 단위로 분할
- 메모리 사용량 모니터링
- 배치 처리 사용

### 6. 성능 최적화

#### 변환 속도 향상
- 헤드리스 모드 사용 (`headless=True`)
- 불필요한 리소스 로딩 방지
- CSS 최적화

#### 메모리 사용량 최적화
- 변환 후 브라우저 인스턴스 정리
- 큰 파일은 스트리밍 처리
- 가비지 컬렉션 강제 실행

### 7. 지원되는 파일 형식

#### ✅ 지원되는 HTML 기능
- CSS 스타일 (인라인, 외부, 내장)
- JavaScript (동적 콘텐츠)
- 한글 폰트
- 테이블, 이미지, 링크
- 페이지 나누기 (`page-break`)

#### ❌ 제한사항
- 일부 복잡한 CSS 애니메이션
- 플래시 콘텐츠
- 일부 브라우저 전용 기능

### 8. 문제 신고 시 포함할 정보

#### 필수 정보
1. **오류 메시지**: 정확한 오류 텍스트
2. **환경 정보**: Windows 버전, Python 버전
3. **파일 정보**: HTML 파일 크기, 내용 유형
4. **재현 단계**: 문제 발생 과정
5. **로그 파일**: 상세 로그 내용

#### 디버그 정보 수집
```bash
# 시스템 정보
python --version
pip list | findstr playwright

# 변환 테스트
python debug_converter.py > debug_log.txt 2>&1
```

### 9. 자주 묻는 질문 (FAQ)

#### Q: "변환이 시작되지 않아요"
A: Playwright 설치 및 Chromium 브라우저 설치 확인

#### Q: "PDF가 생성되지 않아요"  
A: 출력 폴더 권한 및 경로 확인

#### Q: "한글이 깨져요"
A: 시스템 한글 폰트 설치 및 CSS 폰트 지정

#### Q: "변환이 너무 느려요"
A: 파일 크기 확인 및 메모리 사용량 모니터링

#### Q: "일부 스타일이 적용되지 않아요"
A: CSS `@page` 규칙 및 `print_background` 옵션 확인

### 10. 연락처 및 지원

#### 문제 해결이 안 될 때
1. **디버그 로그** 수집
2. **재현 가능한 최소 예제** 작성  
3. **시스템 환경 정보** 수집
4. **단계별 재현 과정** 기록

#### 추가 도움
- GitHub Issues에 문제 보고
- 상세한 오류 메시지와 함께 문의
- 재현 가능한 예제 파일 제공

