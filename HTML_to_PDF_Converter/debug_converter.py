"""
HTML → PDF 변환기 디버그 스크립트
문제 진단 및 해결
"""

import os
import sys
from playwright_pdf_converter import html_string_to_pdf_sync, html_file_to_pdf_sync

def test_playwright_installation():
    """Playwright 설치 상태 확인"""
    print("=== Playwright 설치 상태 확인 ===")
    
    try:
        from playwright.sync_api import sync_playwright
        print("[OK] Playwright 모듈 임포트 성공")
        
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            print("[OK] Chromium 브라우저 실행 성공")
            browser.close()
            print("[OK] 브라우저 종료 성공")
        
        return True
        
    except Exception as e:
        print(f"[ERROR] Playwright 오류: {str(e)}")
        return False

def test_simple_html_conversion():
    """간단한 HTML 변환 테스트"""
    print("\n=== 간단한 HTML 변환 테스트 ===")
    
    # 간단한 HTML 내용
    html_content = """
    <!DOCTYPE html>
    <html lang="ko">
    <head>
        <meta charset="utf-8">
        <title>테스트</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            h1 { color: #333; }
        </style>
    </head>
    <body>
        <h1>HTML → PDF 변환 테스트</h1>
        <p>이것은 간단한 테스트입니다.</p>
        <p>한글도 테스트: 안녕하세요!</p>
    </body>
    </html>
    """
    
    try:
        output_pdf = "debug_test.pdf"
        print(f"HTML 내용 길이: {len(html_content)} 문자")
        print(f"출력 PDF: {output_pdf}")
        
        success = html_string_to_pdf_sync(html_content, output_pdf)
        
        if success and os.path.exists(output_pdf):
            file_size = os.path.getsize(output_pdf)
            print(f"[OK] 변환 성공! 파일 크기: {file_size:,} bytes")
            return True
        else:
            print("[ERROR] 변환 실패")
            return False
            
    except Exception as e:
        print(f"[ERROR] 변환 오류: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_file_conversion():
    """파일 변환 테스트"""
    print("\n=== 파일 변환 테스트 ===")
    
    # 테스트 HTML 파일 생성
    html_content = """
    <!DOCTYPE html>
    <html lang="ko">
    <head>
        <meta charset="utf-8">
        <title>파일 테스트</title>
        <style>
            body { font-family: 'Malgun Gothic', sans-serif; margin: 20px; }
            .header { background: #f0f0f0; padding: 10px; border-radius: 5px; }
            table { border-collapse: collapse; width: 100%; margin: 20px 0; }
            th, td { border: 1px solid #333; padding: 8px; text-align: center; }
            th { background: #333; color: white; }
        </style>
    </head>
    <body>
        <div class="header">
            <h1>파일 변환 테스트</h1>
            <p>이것은 파일에서 PDF로 변환하는 테스트입니다.</p>
        </div>
        
        <table>
            <tr><th>항목</th><th>값</th></tr>
            <tr><td>이름</td><td>홍길동</td></tr>
            <tr><td>나이</td><td>25</td></tr>
            <tr><td>직업</td><td>개발자</td></tr>
        </table>
        
        <p>한글 폰트와 CSS 스타일이 제대로 적용되는지 확인합니다.</p>
    </body>
    </html>
    """
    
    try:
        # HTML 파일 저장
        html_file = "debug_test.html"
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"HTML 파일 생성: {html_file}")
        
        # PDF 변환
        output_pdf = "debug_file_test.pdf"
        success = html_file_to_pdf_sync(html_file, output_pdf)
        
        if success and os.path.exists(output_pdf):
            file_size = os.path.getsize(output_pdf)
            print(f"[OK] 파일 변환 성공! 파일 크기: {file_size:,} bytes")
            
            # 정리
            if os.path.exists(html_file):
                os.remove(html_file)
                print(f"임시 HTML 파일 삭제: {html_file}")
            
            return True
        else:
            print("[ERROR] 파일 변환 실패")
            return False
            
    except Exception as e:
        print(f"[ERROR] 파일 변환 오류: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_batch_conversion():
    """배치 변환 테스트"""
    print("\n=== 배치 변환 테스트 ===")
    
    try:
        from batch_html_to_pdf import batch_html_to_pdf
        
        # 테스트 HTML 파일들 생성
        test_folder = "debug_test_html"
        os.makedirs(test_folder, exist_ok=True)
        
        html_files = [
            ("test1.html", "<html><body><h1>테스트 1</h1><p>첫 번째 파일</p></body></html>"),
            ("test2.html", "<html><body><h1>테스트 2</h1><p>두 번째 파일</p></body></html>"),
            ("test3.html", "<html><body><h1>테스트 3</h1><p>세 번째 파일</p></body></html>")
        ]
        
        for filename, content in html_files:
            filepath = os.path.join(test_folder, filename)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
        
        print(f"테스트 HTML 파일 {len(html_files)}개 생성 완료")
        
        # 배치 변환 실행
        output_folder = "debug_test_pdf"
        success = batch_html_to_pdf(test_folder, output_folder, recursive=False, overwrite=True)
        
        if success:
            pdf_files = [f for f in os.listdir(output_folder) if f.endswith('.pdf')]
            print(f"[OK] 배치 변환 성공! 생성된 PDF: {len(pdf_files)}개")
            for pdf_file in pdf_files:
                file_path = os.path.join(output_folder, pdf_file)
                file_size = os.path.getsize(file_path)
                print(f"  - {pdf_file} ({file_size:,} bytes)")
            return True
        else:
            print("[ERROR] 배치 변환 실패")
            return False
            
    except Exception as e:
        print(f"[ERROR] 배치 변환 오류: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def cleanup_test_files():
    """테스트 파일들 정리"""
    import shutil
    
    files_to_remove = [
        "debug_test.pdf",
        "debug_file_test.pdf"
    ]
    
    folders_to_remove = [
        "debug_test_html",
        "debug_test_pdf"
    ]
    
    for file in files_to_remove:
        if os.path.exists(file):
            os.remove(file)
            print(f"파일 삭제: {file}")
    
    for folder in folders_to_remove:
        if os.path.exists(folder):
            shutil.rmtree(folder)
            print(f"폴더 삭제: {folder}")

def main():
    """메인 디버그 함수"""
    print("HTML → PDF 변환기 디버그")
    print("=" * 40)
    
    # 1. Playwright 설치 확인
    playwright_ok = test_playwright_installation()
    
    # 2. 간단한 HTML 변환 테스트
    simple_ok = test_simple_html_conversion()
    
    # 3. 파일 변환 테스트
    file_ok = test_file_conversion()
    
    # 4. 배치 변환 테스트
    batch_ok = test_batch_conversion()
    
    # 결과 요약
    print("\n" + "=" * 40)
    print("디버그 결과 요약")
    print("=" * 40)
    print(f"Playwright 설치: {'[OK] 성공' if playwright_ok else '[ERROR] 실패'}")
    print(f"간단한 HTML 변환: {'[OK] 성공' if simple_ok else '[ERROR] 실패'}")
    print(f"파일 변환: {'[OK] 성공' if file_ok else '[ERROR] 실패'}")
    print(f"배치 변환: {'[OK] 성공' if batch_ok else '[ERROR] 실패'}")
    
    if all([playwright_ok, simple_ok, file_ok, batch_ok]):
        print("\n[SUCCESS] 모든 테스트 통과! 변환기가 정상 작동합니다.")
    else:
        print("\n[WARNING] 일부 테스트 실패. 문제를 확인해주세요.")
    
    # 정리
    cleanup_test_files()
    print("\n테스트 파일 정리 완료")

if __name__ == "__main__":
    main()
