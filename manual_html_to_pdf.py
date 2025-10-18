"""
수동 HTML → PDF 변환 도구
HTML 파일을 직접 PDF로 변환하는 스크립트
"""

import os
from playwright_pdf_converter import html_file_to_pdf_sync, html_string_to_pdf_sync

def convert_html_file_to_pdf(html_file_path: str, output_pdf_path: str = None):
    """
    HTML 파일을 PDF로 변환
    
    Args:
        html_file_path: 변환할 HTML 파일 경로
        output_pdf_path: 출력할 PDF 파일 경로 (없으면 자동 생성)
    """
    if not os.path.exists(html_file_path):
        print(f"오류: HTML 파일을 찾을 수 없습니다 - {html_file_path}")
        return False
    
    # 출력 파일명 자동 생성
    if output_pdf_path is None:
        base_name = os.path.splitext(os.path.basename(html_file_path))[0]
        output_pdf_path = f"{base_name}.pdf"
    
    print(f"HTML 파일 변환 중: {html_file_path}")
    print(f"출력 PDF: {output_pdf_path}")
    
    # Playwright로 변환
    success = html_file_to_pdf_sync(html_file_path, output_pdf_path)
    
    if success:
        file_size = os.path.getsize(output_pdf_path)
        print(f"변환 완료! 파일 크기: {file_size:,} bytes")
        print(f"저장 위치: {os.path.abspath(output_pdf_path)}")
        return True
    else:
        print("변환 실패")
        return False

def convert_html_string_to_pdf(html_content: str, output_pdf_path: str):
    """
    HTML 문자열을 PDF로 변환
    
    Args:
        html_content: HTML 문자열
        output_pdf_path: 출력할 PDF 파일 경로
    """
    print(f"HTML 문자열을 PDF로 변환 중...")
    print(f"출력 PDF: {output_pdf_path}")
    
    # Playwright로 변환
    success = html_string_to_pdf_sync(html_content, output_pdf_path)
    
    if success:
        file_size = os.path.getsize(output_pdf_path)
        print(f"변환 완료! 파일 크기: {file_size:,} bytes")
        print(f"저장 위치: {os.path.abspath(output_pdf_path)}")
        return True
    else:
        print("변환 실패")
        return False

def batch_convert_html_files(html_directory: str, output_directory: str = None):
    """
    폴더 내 모든 HTML 파일을 PDF로 일괄 변환
    
    Args:
        html_directory: HTML 파일들이 있는 폴더
        output_directory: PDF 출력 폴더 (없으면 HTML 폴더와 동일)
    """
    if not os.path.exists(html_directory):
        print(f"오류: 폴더를 찾을 수 없습니다 - {html_directory}")
        return
    
    if output_directory is None:
        output_directory = html_directory
    else:
        os.makedirs(output_directory, exist_ok=True)
    
    # HTML 파일 찾기
    html_files = [f for f in os.listdir(html_directory) if f.lower().endswith('.html')]
    
    if not html_files:
        print("HTML 파일을 찾을 수 없습니다.")
        return
    
    print(f"{len(html_files)}개 HTML 파일 발견")
    print(f"출력 폴더: {output_directory}")
    
    success_count = 0
    for html_file in html_files:
        html_path = os.path.join(html_directory, html_file)
        pdf_name = os.path.splitext(html_file)[0] + '.pdf'
        pdf_path = os.path.join(output_directory, pdf_name)
        
        print(f"\n변환 중: {html_file}")
        if convert_html_file_to_pdf(html_path, pdf_path):
            success_count += 1
    
    print(f"\n변환 완료: {success_count}/{len(html_files)}개 파일")

# 사용 예시
if __name__ == "__main__":
    print("HTML → PDF 변환 도구")
    print("=" * 50)
    
    # 예시 1: 단일 HTML 파일 변환
    print("\n1. 단일 HTML 파일 변환 예시:")
    print("convert_html_file_to_pdf('report.html', 'report.pdf')")
    
    # 예시 2: HTML 문자열 변환
    print("\n2. HTML 문자열 변환 예시:")
    sample_html = """
    <!DOCTYPE html>
    <html>
    <head><meta charset="utf-8"><title>테스트</title></head>
    <body><h1>한글 테스트</h1><p>PDF 변환 테스트입니다.</p></body>
    </html>
    """
    print("convert_html_string_to_pdf(sample_html, 'test.pdf')")
    
    # 예시 3: 일괄 변환
    print("\n3. 폴더 내 모든 HTML 파일 일괄 변환:")
    print("batch_convert_html_files('./html_files/', './pdf_output/')")
    
    print("\n사용법:")
    print("1. HTML 파일 경로를 지정하여 변환")
    print("2. 폴더 경로를 지정하여 일괄 변환")
    print("3. 브라우저에서 Ctrl+P로 수동 변환도 가능")
