import os
import pathlib
import datetime
import re
from typing import Dict, Any, List
from jinja2 import Environment, FileSystemLoader, select_autoescape
from playwright.sync_api import sync_playwright
from playwright_pdf_converter import html_string_to_pdf_sync

class JinjaPDFGenerator:
    def __init__(self):
        self.base_dir = pathlib.Path(__file__).parent
        self.templates_dir = self.base_dir / "templates"
        self.out_dir = self.base_dir / "output"
        self.out_dir.mkdir(exist_ok=True)
        
        # Jinja2 환경 설정
        self.env = Environment(
            loader=FileSystemLoader(self.templates_dir),
            autoescape=select_autoescape(["html"])
        )
    
    def _sanitize_filename(self, filename: str) -> str:
        """파일명에서 특수문자 제거 및 안전하게 처리"""
        # 파일명으로 사용할 수 없는 문자 제거
        filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
        # 연속된 언더스코어 제거
        filename = re.sub(r'_+', '_', filename)
        # 앞뒤 공백 및 언더스코어 제거
        filename = filename.strip(' _')
        # 빈 문자열 처리
        if not filename:
            filename = "untitled"
        # 파일명 길이 제한 (Windows 최대 255자, 확장자 포함)
        if len(filename) > 200:
            filename = filename[:200]
        return filename
    
    def generate_pdf(self, student_data: Dict[str, Any], output_dir: str, pdf_title: str = "학생 성적표", save_html: bool = False):
        """Jinja2 템플릿 + Playwright로 PDF 생성"""
        try:
            # 데이터 변환
            student = {
                "name": student_data['name'],
                "sid": student_data['student_id']
            }
            
            # 성적 데이터 변환
            scores = []
            wrongs = {}
            
            for subject, info in student_data['subjects'].items():
                # 성적표 데이터
                scores.append({
                    "subject": info.get('subject_name', subject),
                    "raw": str(int(info.get('total_score', 0))),
                    "std": str(info.get('standard_score', '—')) if info.get('standard_score') is not None else '—',
                    "pr": str(info.get('percentile', '—')) if info.get('percentile') is not None else '—'
                })
                
                # 오답번호 데이터
                wrong_answers = info.get('wrong_answers', [])
                if isinstance(wrong_answers, list):
                    wrongs[subject] = [str(x) for x in wrong_answers]
                else:
                    wrongs[subject] = []
            
            # 리포트 컨텍스트
            report_ctx = {
                "student": student,
                "scores": scores,
                "wrongs": wrongs,
                "report": {
                    "exam_name": pdf_title,
                    "issued_at": datetime.date.today().isoformat(),
                },
            }
            
            # HTML 렌더링
            template = self.env.get_template("report.html")
            html_content = template.render(**report_ctx)
            
            # HTML 파일 저장 (옵션)
            if save_html:
                safe_name = self._sanitize_filename(student['name'])
                safe_sid = self._sanitize_filename(student['sid'])
                html_filename = f"{safe_name}_{safe_sid}.html"
                html_filepath = os.path.join(output_dir, html_filename)
                with open(html_filepath, 'w', encoding='utf-8') as f:
                    f.write(html_content)
                print(f"HTML 파일 저장: {html_filename}")
            
            # PDF 생성
            self._html_to_pdf(html_content, output_dir, student['name'], student['sid'])
            
        except Exception as e:
            print(f"PDF 생성 오류: {str(e)}")
            raise
    
    def _html_to_pdf(self, html_content: str, output_dir: str, student_name: str, student_id: str):
        """HTML을 PDF로 변환 (Playwright 변환기 사용)"""
        try:
            safe_name = self._sanitize_filename(student_name)
            safe_id = self._sanitize_filename(student_id)
            pdf_filename = f"{safe_name}_{safe_id}.pdf"
            pdf_path = os.path.join(output_dir, pdf_filename)
            
            # Playwright 변환기 사용
            success = html_string_to_pdf_sync(
                html_content, 
                pdf_path,
                format="A4",
                margin={
                    "top": "12mm", 
                    "right": "12mm", 
                    "bottom": "12mm", 
                    "left": "12mm"
                }
            )
            
            if success:
                print(f"PDF 생성 완료: {pdf_filename}")
            else:
                raise Exception("PDF 변환 실패")
                
        except Exception as e:
            print(f"PDF 변환 오류: {str(e)}")
            raise

if __name__ == "__main__":
    # 테스트
    test_data = {
        'name': '김철수',
        'student_id': 'STU_김철수',
        'subjects': {
            '국어': {
                'subject_name': '국어',
                'total_score': 85,
                'standard_score': 90,
                'percentile': 85,
                'grade': 2,
                'wrong_answers': [1, 5, 10]
            },
            '수학': {
                'subject_name': '수학',
                'total_score': 90,
                'standard_score': 100,
                'percentile': 95,
                'grade': 1,
                'wrong_answers': [2, 8]
            }
        }
    }
    
    generator = JinjaPDFGenerator()
    generator.generate_pdf(test_data, ".", "2024년 모의고사 성적표")
