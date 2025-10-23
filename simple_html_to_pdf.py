#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
간단한 HTML to PDF 변환기
사용법: python simple_html_to_pdf.py <HTML파일경로> [출력PDF경로]
"""

import sys
import os
from playwright.sync_api import sync_playwright

def convert_html_to_pdf(html_file, output_pdf=None):
    """HTML 파일을 PDF로 변환"""
    
    # 출력 파일명 자동 생성
    if output_pdf is None:
        base_name = os.path.splitext(os.path.basename(html_file))[0]
        output_dir = os.path.dirname(html_file)
        output_pdf = os.path.join(output_dir, f"{base_name}.pdf")
    
    print(f"입력 HTML: {html_file}")
    print(f"출력 PDF: {output_pdf}")
    
    try:
        with sync_playwright() as p:
            # 브라우저 시작
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            
            # HTML 파일 로드
            html_path = os.path.abspath(html_file)
            file_url = f"file:///{html_path.replace(os.sep, '/')}"
            page.goto(file_url)
            
            # PDF 생성
            page.pdf(
                path=output_pdf,
                format="A4",
                print_background=True,
                margin={
                    "top": "12mm",
                    "right": "12mm", 
                    "bottom": "12mm",
                    "left": "12mm"
                }
            )
            
            browser.close()
            
            # 파일 크기 확인
            if os.path.exists(output_pdf):
                file_size = os.path.getsize(output_pdf)
                print(f"변환 완료! 파일 크기: {file_size:,} bytes")
                return True
            else:
                print("변환 실패: PDF 파일이 생성되지 않았습니다.")
                return False
                
    except Exception as e:
        print(f"변환 오류: {str(e)}")
        return False

def main():
    """메인 함수"""
    if len(sys.argv) < 2:
        print("사용법: python simple_html_to_pdf.py <HTML파일경로> [출력PDF경로]")
        print("예시: python simple_html_to_pdf.py test.html")
        print("예시: python simple_html_to_pdf.py test.html output.pdf")
        return
    
    html_file = sys.argv[1]
    output_pdf = sys.argv[2] if len(sys.argv) > 2 else None
    
    # HTML 파일 존재 확인
    if not os.path.exists(html_file):
        print(f"오류: HTML 파일을 찾을 수 없습니다 - {html_file}")
        return
    
    # 변환 실행
    success = convert_html_to_pdf(html_file, output_pdf)
    
    if success:
        print("HTML to PDF 변환이 성공적으로 완료되었습니다!")
    else:
        print("HTML to PDF 변환에 실패했습니다.")

if __name__ == "__main__":
    main()
