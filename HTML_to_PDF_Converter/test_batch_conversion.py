"""
HTML 배치 변환 테스트 스크립트
"""

import os
from batch_html_to_pdf import batch_html_to_pdf, convert_single_html

def create_test_html_files():
    """테스트용 HTML 파일들 생성"""
    test_folder = "test_html_files"
    os.makedirs(test_folder, exist_ok=True)
    
    # 테스트 HTML 파일 1
    html1 = """
    <!DOCTYPE html>
    <html lang="ko">
    <head>
        <meta charset="utf-8">
        <title>테스트 문서 1</title>
        <style>
            body { font-family: 'Noto Sans KR', sans-serif; margin: 20px; }
            h1 { color: #2c3e50; }
            .content { background: #ecf0f1; padding: 15px; border-radius: 5px; }
        </style>
    </head>
    <body>
        <h1>테스트 문서 1</h1>
        <div class="content">
            <p>이것은 첫 번째 테스트 HTML 파일입니다.</p>
            <p>한글 폰트와 CSS 스타일이 적용되었습니다.</p>
        </div>
    </body>
    </html>
    """
    
    # 테스트 HTML 파일 2
    html2 = """
    <!DOCTYPE html>
    <html lang="ko">
    <head>
        <meta charset="utf-8">
        <title>테스트 문서 2</title>
        <style>
            body { font-family: 'Malgun Gothic', sans-serif; margin: 20px; }
            h1 { color: #e74c3c; }
            table { border-collapse: collapse; width: 100%; }
            th, td { border: 1px solid #333; padding: 8px; text-align: center; }
            th { background: #3498db; color: white; }
        </style>
    </head>
    <body>
        <h1>테스트 문서 2</h1>
        <table>
            <tr><th>항목</th><th>값</th></tr>
            <tr><td>이름</td><td>홍길동</td></tr>
            <tr><td>나이</td><td>25</td></tr>
            <tr><td>직업</td><td>개발자</td></tr>
        </table>
    </body>
    </html>
    """
    
    # 테스트 HTML 파일 3
    html3 = """
    <!DOCTYPE html>
    <html lang="ko">
    <head>
        <meta charset="utf-8">
        <title>테스트 문서 3</title>
        <style>
            body { font-family: 'Noto Sans KR', sans-serif; margin: 20px; }
            h1 { color: #27ae60; }
            .highlight { background: #f39c12; color: white; padding: 5px; }
        </style>
    </head>
    <body>
        <h1>테스트 문서 3</h1>
        <p>이것은 <span class="highlight">세 번째</span> 테스트 HTML 파일입니다.</p>
        <p>다양한 스타일과 색상이 적용되었습니다.</p>
    </body>
    </html>
    """
    
    # HTML 파일들 저장
    with open(os.path.join(test_folder, "test1.html"), 'w', encoding='utf-8') as f:
        f.write(html1)
    
    with open(os.path.join(test_folder, "test2.html"), 'w', encoding='utf-8') as f:
        f.write(html2)
    
    with open(os.path.join(test_folder, "test3.html"), 'w', encoding='utf-8') as f:
        f.write(html3)
    
    print(f"테스트 HTML 파일 생성 완료: {test_folder}")
    return test_folder

def test_single_conversion():
    """단일 파일 변환 테스트"""
    print("\n=== 단일 파일 변환 테스트 ===")
    
    # 기존 sample_report.html 사용
    if os.path.exists("sample_report.html"):
        success = convert_single_html("sample_report.html", "single_test.pdf")
        if success:
            print("단일 파일 변환 성공!")
        else:
            print("단일 파일 변환 실패!")
    else:
        print("sample_report.html 파일이 없습니다.")

def test_batch_conversion():
    """배치 변환 테스트"""
    print("\n=== 배치 변환 테스트 ===")
    
    # 테스트 HTML 파일들 생성
    test_folder = create_test_html_files()
    output_folder = "test_pdf_output"
    
    # 배치 변환 실행
    success = batch_html_to_pdf(test_folder, output_folder, recursive=False, overwrite=True)
    
    if success:
        print("배치 변환 성공!")
        
        # 결과 파일들 확인
        pdf_files = [f for f in os.listdir(output_folder) if f.endswith('.pdf')]
        print(f"생성된 PDF 파일: {len(pdf_files)}개")
        for pdf_file in pdf_files:
            file_path = os.path.join(output_folder, pdf_file)
            file_size = os.path.getsize(file_path)
            print(f"  - {pdf_file} ({file_size:,} bytes)")
    else:
        print("배치 변환 실패!")

def cleanup_test_files():
    """테스트 파일들 정리"""
    import shutil
    
    folders_to_remove = ["test_html_files", "test_pdf_output"]
    files_to_remove = ["single_test.pdf"]
    
    for folder in folders_to_remove:
        if os.path.exists(folder):
            shutil.rmtree(folder)
            print(f"폴더 삭제: {folder}")
    
    for file in files_to_remove:
        if os.path.exists(file):
            os.remove(file)
            print(f"파일 삭제: {file}")

if __name__ == "__main__":
    print("HTML 배치 변환 테스트")
    print("=" * 30)
    
    try:
        # 단일 파일 변환 테스트
        test_single_conversion()
        
        # 배치 변환 테스트
        test_batch_conversion()
        
        print("\n모든 테스트 완료!")
        
        # 정리 여부 확인
        response = input("\n테스트 파일들을 정리하시겠습니까? (y/n): ")
        if response.lower() in ['y', 'yes', '예']:
            cleanup_test_files()
            print("정리 완료!")
        
    except Exception as e:
        print(f"테스트 중 오류 발생: {str(e)}")
        import traceback
        traceback.print_exc()
