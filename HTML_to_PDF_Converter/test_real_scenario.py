"""
실제 사용 시나리오 테스트
성적표 HTML → PDF 변환 테스트
"""

import os
import sys
from playwright_pdf_converter import html_string_to_pdf_sync, html_file_to_pdf_sync

def test_score_report_conversion():
    """성적표 변환 테스트"""
    print("=== 성적표 HTML → PDF 변환 테스트 ===")
    
    # 실제 성적표 HTML 내용 (간단한 버전)
    score_html = """
    <!DOCTYPE html>
    <html lang="ko">
    <head>
        <meta charset="utf-8">
        <title>학생 성적표</title>
        <style>
            @page {
                size: A4;
                margin: 20mm;
            }
            
            body {
                font-family: 'Malgun Gothic', '맑은 고딕', sans-serif;
                margin: 0;
                padding: 0;
                font-size: 12px;
                line-height: 1.4;
            }
            
            .header {
                text-align: center;
                margin-bottom: 20px;
                border-bottom: 2px solid #333;
                padding-bottom: 10px;
            }
            
            .header h1 {
                font-size: 18px;
                margin: 0;
                color: #333;
            }
            
            .student-info {
                margin-bottom: 20px;
            }
            
            .student-info table {
                width: 100%;
                border-collapse: collapse;
                margin-bottom: 10px;
            }
            
            .student-info td {
                padding: 5px 10px;
                border: 1px solid #ccc;
            }
            
            .student-info td:first-child {
                background: #f5f5f5;
                font-weight: bold;
                width: 120px;
            }
            
            .scores-table {
                width: 100%;
                border-collapse: collapse;
                margin-top: 20px;
            }
            
            .scores-table th,
            .scores-table td {
                border: 1px solid #333;
                padding: 8px;
                text-align: center;
            }
            
            .scores-table th {
                background: #333;
                color: white;
                font-weight: bold;
            }
            
            .scores-table tr:nth-child(even) {
                background: #f9f9f9;
            }
            
            .footer {
                margin-top: 30px;
                text-align: center;
                font-size: 10px;
                color: #666;
            }
        </style>
    </head>
    <body>
        <div class="header">
            <h1>학생 성적표</h1>
        </div>
        
        <div class="student-info">
            <table>
                <tr>
                    <td>학원명</td>
                    <td>SN독학기숙학원</td>
                </tr>
                <tr>
                    <td>학생명</td>
                    <td>홍길동</td>
                </tr>
                <tr>
                    <td>학번</td>
                    <td>2024001</td>
                </tr>
            </table>
        </div>
        
        <table class="scores-table">
            <thead>
                <tr>
                    <th>과목</th>
                    <th>원점수</th>
                    <th>표준점수</th>
                    <th>백분위</th>
                    <th>등급</th>
                    <th>오답번호</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>국어</td>
                    <td>90</td>
                    <td>85.5</td>
                    <td>78</td>
                    <td>2</td>
                    <td>3, 11, 12</td>
                </tr>
                <tr>
                    <td>수학</td>
                    <td>88</td>
                    <td>82.3</td>
                    <td>75</td>
                    <td>2</td>
                    <td>5, 8, 15</td>
                </tr>
                <tr>
                    <td>영어</td>
                    <td>92</td>
                    <td>0</td>
                    <td>0</td>
                    <td>1</td>
                    <td>2, 7</td>
                </tr>
                <tr>
                    <td>한국사</td>
                    <td>45</td>
                    <td>0</td>
                    <td>0</td>
                    <td>1</td>
                    <td>1, 4</td>
                </tr>
                <tr>
                    <td>탐구1</td>
                    <td>48</td>
                    <td>89.2</td>
                    <td>82</td>
                    <td>2</td>
                    <td>6, 9</td>
                </tr>
                <tr>
                    <td>탐구2</td>
                    <td>46</td>
                    <td>87.8</td>
                    <td>79</td>
                    <td>2</td>
                    <td>3, 8</td>
                </tr>
            </tbody>
        </table>
        
        <div class="footer">
            <p>본 프로그램은 SN독학기숙학원이 개발하였습니다.</p>
        </div>
    </body>
    </html>
    """
    
    try:
        print("성적표 HTML 내용 생성 완료")
        print(f"HTML 크기: {len(score_html)} 문자")
        
        # PDF 변환
        output_pdf = "score_report_test.pdf"
        print(f"PDF 변환 시작: {output_pdf}")
        
        success = html_string_to_pdf_sync(score_html, output_pdf)
        
        if success and os.path.exists(output_pdf):
            file_size = os.path.getsize(output_pdf)
            print(f"[OK] 성적표 변환 성공!")
            print(f"파일 크기: {file_size:,} bytes")
            print(f"파일 위치: {os.path.abspath(output_pdf)}")
            return True
        else:
            print("[ERROR] 성적표 변환 실패")
            return False
            
    except Exception as e:
        print(f"[ERROR] 성적표 변환 오류: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_large_html_conversion():
    """큰 HTML 파일 변환 테스트"""
    print("\n=== 큰 HTML 파일 변환 테스트 ===")
    
    # 큰 HTML 내용 생성
    large_html = """
    <!DOCTYPE html>
    <html lang="ko">
    <head>
        <meta charset="utf-8">
        <title>큰 문서 테스트</title>
        <style>
            body { font-family: 'Malgun Gothic', sans-serif; margin: 20px; }
            .section { margin: 20px 0; padding: 15px; border: 1px solid #ccc; }
            table { width: 100%; border-collapse: collapse; margin: 10px 0; }
            th, td { border: 1px solid #333; padding: 8px; text-align: center; }
            th { background: #f0f0f0; }
        </style>
    </head>
    <body>
        <h1>큰 문서 변환 테스트</h1>
    """
    
    # 많은 내용 추가
    for i in range(50):
        large_html += f"""
        <div class="section">
            <h2>섹션 {i+1}</h2>
            <p>이것은 테스트 섹션 {i+1}입니다. 한글 폰트와 레이아웃이 제대로 적용되는지 확인합니다.</p>
            <table>
                <tr><th>항목</th><th>값</th><th>설명</th></tr>
                <tr><td>번호</td><td>{i+1}</td><td>테스트 데이터</td></tr>
                <tr><td>점수</td><td>{85 + (i % 15)}</td><td>성적 정보</td></tr>
                <tr><td>등급</td><td>{1 + (i % 9)}</td><td>등급 정보</td></tr>
            </table>
        </div>
        """
    
    large_html += """
    </body>
    </html>
    """
    
    try:
        print(f"큰 HTML 내용 생성: {len(large_html):,} 문자")
        
        # PDF 변환
        output_pdf = "large_document_test.pdf"
        success = html_string_to_pdf_sync(large_html, output_pdf)
        
        if success and os.path.exists(output_pdf):
            file_size = os.path.getsize(output_pdf)
            print(f"[OK] 큰 문서 변환 성공!")
            print(f"파일 크기: {file_size:,} bytes")
            return True
        else:
            print("[ERROR] 큰 문서 변환 실패")
            return False
            
    except Exception as e:
        print(f"[ERROR] 큰 문서 변환 오류: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_multiple_conversions():
    """여러 파일 동시 변환 테스트"""
    print("\n=== 여러 파일 동시 변환 테스트 ===")
    
    html_contents = [
        ("report1.html", "<html><body><h1>보고서 1</h1><p>첫 번째 보고서입니다.</p></body></html>"),
        ("report2.html", "<html><body><h1>보고서 2</h1><p>두 번째 보고서입니다.</p></body></html>"),
        ("report3.html", "<html><body><h1>보고서 3</h1><p>세 번째 보고서입니다.</p></body></html>")
    ]
    
    try:
        # HTML 파일들 생성
        for filename, content in html_contents:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"HTML 파일 생성: {filename}")
        
        # 각각 PDF로 변환
        success_count = 0
        for filename, _ in html_contents:
            pdf_name = filename.replace('.html', '.pdf')
            success = html_file_to_pdf_sync(filename, pdf_name)
            
            if success and os.path.exists(pdf_name):
                file_size = os.path.getsize(pdf_name)
                print(f"[OK] {filename} → {pdf_name} ({file_size:,} bytes)")
                success_count += 1
            else:
                print(f"[ERROR] {filename} 변환 실패")
        
        print(f"\n변환 결과: {success_count}/{len(html_contents)} 성공")
        return success_count == len(html_contents)
        
    except Exception as e:
        print(f"[ERROR] 여러 파일 변환 오류: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def cleanup_test_files():
    """테스트 파일들 정리"""
    import shutil
    
    files_to_remove = [
        "score_report_test.pdf",
        "large_document_test.pdf",
        "report1.html", "report1.pdf",
        "report2.html", "report2.pdf", 
        "report3.html", "report3.pdf"
    ]
    
    for file in files_to_remove:
        if os.path.exists(file):
            os.remove(file)
            print(f"파일 삭제: {file}")

def main():
    """메인 테스트 함수"""
    print("실제 사용 시나리오 테스트")
    print("=" * 50)
    
    # 1. 성적표 변환 테스트
    score_ok = test_score_report_conversion()
    
    # 2. 큰 HTML 변환 테스트
    large_ok = test_large_html_conversion()
    
    # 3. 여러 파일 변환 테스트
    multiple_ok = test_multiple_conversions()
    
    # 결과 요약
    print("\n" + "=" * 50)
    print("실제 사용 시나리오 테스트 결과")
    print("=" * 50)
    print(f"성적표 변환: {'[OK] 성공' if score_ok else '[ERROR] 실패'}")
    print(f"큰 문서 변환: {'[OK] 성공' if large_ok else '[ERROR] 실패'}")
    print(f"여러 파일 변환: {'[OK] 성공' if multiple_ok else '[ERROR] 실패'}")
    
    if all([score_ok, large_ok, multiple_ok]):
        print("\n[SUCCESS] 모든 실제 사용 시나리오 테스트 통과!")
        print("HTML → PDF 변환기가 정상적으로 작동합니다.")
    else:
        print("\n[WARNING] 일부 시나리오에서 문제가 발생했습니다.")
        print("문제를 확인하고 해결해주세요.")
    
    # 정리
    cleanup_test_files()
    print("\n테스트 파일 정리 완료")

if __name__ == "__main__":
    main()

