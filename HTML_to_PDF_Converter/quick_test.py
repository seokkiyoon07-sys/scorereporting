"""
빠른 HTML → PDF 변환 테스트
문제 진단 및 해결
"""

import os
import sys
from playwright_pdf_converter import html_string_to_pdf_sync

def quick_test():
    """빠른 변환 테스트"""
    print("HTML → PDF 변환기 빠른 테스트")
    print("=" * 40)
    
    # 간단한 HTML
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>테스트</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            h1 { color: blue; }
        </style>
    </head>
    <body>
        <h1>HTML → PDF 변환 테스트</h1>
        <p>이것은 간단한 테스트입니다.</p>
        <p>한글 테스트: 안녕하세요!</p>
    </body>
    </html>
    """
    
    try:
        print("1. HTML 내용 생성 완료")
        print(f"   HTML 크기: {len(html)} 문자")
        
        print("2. PDF 변환 시작...")
        success = html_string_to_pdf_sync(html, "quick_test.pdf")
        
        if success and os.path.exists("quick_test.pdf"):
            size = os.path.getsize("quick_test.pdf")
            print(f"3. [SUCCESS] 변환 성공!")
            print(f"   PDF 크기: {size:,} bytes")
            print(f"   파일 위치: {os.path.abspath('quick_test.pdf')}")
            
            # 파일 삭제
            os.remove("quick_test.pdf")
            print("4. 테스트 파일 정리 완료")
            return True
        else:
            print("3. [ERROR] 변환 실패")
            return False
            
    except Exception as e:
        print(f"3. [ERROR] 변환 오류: {str(e)}")
        return False

def check_environment():
    """환경 확인"""
    print("\n환경 확인")
    print("-" * 20)
    
    # Python 버전
    print(f"Python 버전: {sys.version}")
    
    # Playwright 설치 확인
    try:
        from playwright.sync_api import sync_playwright
        print("Playwright: [OK] 설치됨")
        
        # Chromium 확인
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            print("Chromium: [OK] 실행 가능")
            browser.close()
            
    except Exception as e:
        print(f"Playwright: [ERROR] {str(e)}")
        return False
    
    return True

def main():
    """메인 함수"""
    print("HTML → PDF 변환기 빠른 진단")
    print("=" * 50)
    
    # 환경 확인
    env_ok = check_environment()
    
    if not env_ok:
        print("\n[ERROR] 환경 설정에 문제가 있습니다.")
        print("Playwright 설치 및 Chromium 브라우저 설치를 확인해주세요.")
        print("\n설치 명령어:")
        print("pip install playwright")
        print("python -m playwright install chromium")
        return
    
    # 변환 테스트
    test_ok = quick_test()
    
    if test_ok:
        print("\n[SUCCESS] HTML → PDF 변환기가 정상 작동합니다!")
        print("문제가 지속되면 TROUBLESHOOTING_GUIDE.md를 참고하세요.")
    else:
        print("\n[ERROR] 변환에 문제가 있습니다.")
        print("TROUBLESHOOTING_GUIDE.md를 참고하여 문제를 해결하세요.")

if __name__ == "__main__":
    main()

