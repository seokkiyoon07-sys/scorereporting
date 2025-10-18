"""
HTML 파일을 한번에 PDF로 변환하는 배치 처리 도구
폴더 내 모든 HTML 파일을 PDF로 일괄 변환
"""

import os
import sys
import time
from pathlib import Path
from playwright_pdf_converter import html_file_to_pdf_sync

def batch_html_to_pdf(input_folder: str, output_folder: str = None, 
                     recursive: bool = False, overwrite: bool = False):
    """
    폴더 내 모든 HTML 파일을 PDF로 일괄 변환
    
    Args:
        input_folder: HTML 파일들이 있는 입력 폴더
        output_folder: PDF 출력 폴더 (없으면 입력 폴더와 동일)
        recursive: 하위 폴더까지 재귀적으로 검색
        overwrite: 기존 PDF 파일 덮어쓰기 여부
    """
    
    # 입력 폴더 확인
    if not os.path.exists(input_folder):
        print(f"❌ 오류: 입력 폴더를 찾을 수 없습니다 - {input_folder}")
        return False
    
    # 출력 폴더 설정
    if output_folder is None:
        output_folder = input_folder
    else:
        os.makedirs(output_folder, exist_ok=True)
    
    print(f"입력 폴더: {input_folder}")
    print(f"출력 폴더: {output_folder}")
    print(f"재귀 검색: {'예' if recursive else '아니오'}")
    print(f"덮어쓰기: {'예' if overwrite else '아니오'}")
    print("-" * 50)
    
    # HTML 파일 찾기
    html_files = []
    if recursive:
        # 재귀적으로 모든 하위 폴더 검색
        for root, dirs, files in os.walk(input_folder):
            for file in files:
                if file.lower().endswith('.html'):
                    html_files.append(os.path.join(root, file))
    else:
        # 현재 폴더만 검색
        for file in os.listdir(input_folder):
            if file.lower().endswith('.html'):
                html_files.append(os.path.join(input_folder, file))
    
    if not html_files:
        print("HTML 파일을 찾을 수 없습니다.")
        return False
    
    print(f"발견된 HTML 파일: {len(html_files)}개")
    print()
    
    # 변환 시작
    success_count = 0
    error_count = 0
    start_time = time.time()
    
    for i, html_file in enumerate(html_files, 1):
        try:
            # 상대 경로 계산
            rel_path = os.path.relpath(html_file, input_folder)
            print(f"[{i}/{len(html_files)}] 처리 중: {rel_path}")
            
            # 출력 파일명 생성
            base_name = os.path.splitext(os.path.basename(html_file))[0]
            pdf_name = f"{base_name}.pdf"
            
            # 출력 경로 설정
            if recursive:
                # 하위 폴더 구조 유지
                rel_dir = os.path.dirname(rel_path)
                if rel_dir:
                    pdf_dir = os.path.join(output_folder, rel_dir)
                    os.makedirs(pdf_dir, exist_ok=True)
                    pdf_path = os.path.join(pdf_dir, pdf_name)
                else:
                    pdf_path = os.path.join(output_folder, pdf_name)
            else:
                pdf_path = os.path.join(output_folder, pdf_name)
            
            # 기존 파일 확인
            if os.path.exists(pdf_path) and not overwrite:
                print(f"  건너뛰기 (이미 존재): {pdf_name}")
                continue
            
            # PDF 변환
            success = html_file_to_pdf_sync(html_file, pdf_path)
            
            if success:
                file_size = os.path.getsize(pdf_path)
                print(f"  성공: {pdf_name} ({file_size:,} bytes)")
                success_count += 1
            else:
                print(f"  실패: {pdf_name}")
                error_count += 1
                
        except Exception as e:
            print(f"  오류: {str(e)}")
            error_count += 1
        
        print()
    
    # 결과 요약
    end_time = time.time()
    elapsed_time = end_time - start_time
    
    print("=" * 50)
    print("변환 결과 요약")
    print("=" * 50)
    print(f"성공: {success_count}개")
    print(f"실패: {error_count}개")
    print(f"전체: {len(html_files)}개")
    print(f"소요시간: {elapsed_time:.2f}초")
    print(f"출력 폴더: {os.path.abspath(output_folder)}")
    
    return success_count > 0

def convert_single_html(html_file: str, output_pdf: str = None):
    """
    단일 HTML 파일을 PDF로 변환
    
    Args:
        html_file: 변환할 HTML 파일 경로
        output_pdf: 출력 PDF 파일 경로 (없으면 자동 생성)
    """
    if not os.path.exists(html_file):
        print(f"오류: HTML 파일을 찾을 수 없습니다 - {html_file}")
        return False
    
    # 출력 파일명 자동 생성
    if output_pdf is None:
        base_name = os.path.splitext(os.path.basename(html_file))[0]
        output_dir = os.path.dirname(html_file)
        output_pdf = os.path.join(output_dir, f"{base_name}.pdf")
    
    print(f"HTML 파일: {html_file}")
    print(f"PDF 파일: {output_pdf}")
    print("-" * 30)
    
    # PDF 변환
    success = html_file_to_pdf_sync(html_file, output_pdf)
    
    if success:
        file_size = os.path.getsize(output_pdf)
        print(f"변환 완료!")
        print(f"파일 크기: {file_size:,} bytes")
        print(f"저장 위치: {os.path.abspath(output_pdf)}")
        return True
    else:
        print("변환 실패")
        return False

def main():
    """메인 함수 - 명령행 인터페이스"""
    print("HTML → PDF 배치 변환 도구")
    print("=" * 40)
    
    if len(sys.argv) < 2:
        print("사용법:")
        print("  python batch_html_to_pdf.py <입력폴더> [출력폴더] [옵션]")
        print()
        print("옵션:")
        print("  -r, --recursive    하위 폴더까지 재귀 검색")
        print("  -o, --overwrite    기존 PDF 파일 덮어쓰기")
        print()
        print("예시:")
        print("  python batch_html_to_pdf.py ./html_files")
        print("  python batch_html_to_pdf.py ./html_files ./pdf_output")
        print("  python batch_html_to_pdf.py ./html_files ./pdf_output -r -o")
        return
    
    # 명령행 인수 파싱
    input_folder = sys.argv[1]
    output_folder = sys.argv[2] if len(sys.argv) > 2 else None
    recursive = '-r' in sys.argv or '--recursive' in sys.argv
    overwrite = '-o' in sys.argv or '--overwrite' in sys.argv
    
    # 배치 변환 실행
    success = batch_html_to_pdf(input_folder, output_folder, recursive, overwrite)
    
    if success:
        print("\n배치 변환이 완료되었습니다!")
    else:
        print("\n일부 파일 변환에 실패했습니다.")

if __name__ == "__main__":
    main()
