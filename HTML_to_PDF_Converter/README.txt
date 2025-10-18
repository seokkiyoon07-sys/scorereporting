HTML → PDF 변환기 v1.0
=====================

📋 프로그램 개요
- HTML 파일을 고품질 PDF로 변환하는 도구
- Playwright 기반 브라우저 엔진 사용
- GUI 및 명령행 인터페이스 지원

🚀 주요 기능

✅ GUI 인터페이스
- 사용자 친화적인 그래픽 인터페이스
- 드래그 앤 드롭 지원
- 실시간 진행 상황 표시

✅ 배치 처리
- 폴더 내 모든 HTML 파일 일괄 변환
- 하위 폴더 재귀 검색 지원
- 폴더 구조 유지

✅ 고품질 PDF 생성
- Playwright Chromium 엔진 사용
- 한글 폰트 완벽 지원
- CSS 스타일 보존
- A4 페이지 최적화

📁 파일 구성

- HTML_to_PDF_Converter.exe (메인 프로그램)
- batch_html_to_pdf.py (명령행 도구)
- playwright_pdf_converter.py (변환 엔진)
- test_batch_conversion.py (테스트 스크립트)
- HTML_to_PDF_Guide.txt (상세 가이드)

🔧 사용 방법

1. GUI 사용:
   - HTML_to_PDF_Converter.exe 실행
   - 입력/출력 폴더 선택
   - 옵션 설정 후 변환 시작

2. 명령행 사용:
   python batch_html_to_pdf.py <입력폴더> [출력폴더] [옵션]

3. 프로그래밍 사용:
   from batch_html_to_pdf import batch_html_to_pdf
   batch_html_to_pdf("./html_files", "./pdf_output")

⚠️ 시스템 요구사항

- Windows 10/11
- 최소 4GB RAM 권장
- 인터넷 연결 (Playwright 브라우저 다운로드)

📊 지원 파일 형식

- HTML 파일 (.html)
- CSS 스타일시트 포함
- JavaScript 지원
- 한글 폰트 완벽 지원

📞 문의
본 프로그램은 SN독학기숙학원이 개발하였습니다.

버전: 1.0.0
빌드일: 2025-10-18

