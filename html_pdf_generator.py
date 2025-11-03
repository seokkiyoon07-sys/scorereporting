# -*- coding: utf-8 -*-

import os
from typing import Dict, Any
import webbrowser
import tempfile
import html
from playwright.sync_api import sync_playwright

class HTMLPDFGenerator:
    def __init__(self):
        pass
        
    def _sanitize_filename(self, filename: str) -> str:
        """파일명에서 특수문자 제거 및 안전하게 처리"""
        import re
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
    
    def generate_html_based_pdf(self, student_data: Dict[str, Any], output_dir: str, pdf_title: str = "학생 성적표", save_html: bool = False):
        """Jinja2 템플릿 + Playwright 헤드리스 PDF 생성"""
        try:
            # 새로운 Jinja2 기반 PDF 생성기 사용
            from jinja_pdf_generator import JinjaPDFGenerator
            jinja_generator = JinjaPDFGenerator()
            jinja_generator.generate_pdf(student_data, output_dir, pdf_title, save_html)
            
        except Exception as e:
            print(f"Jinja2 PDF 생성 실패: {str(e)}")
            print("기존 HTML 방식으로 폴백합니다.")
            self._create_html_fallback(student_data, output_dir, pdf_title, save_html)
            
    def _create_html_fallback(self, student_data: Dict[str, Any], output_dir: str, pdf_title: str, save_html: bool = False):
        """PDF 생성 실패 시 HTML 파일로 폴백"""
        try:
            student_name = student_data['name']
            student_id = student_data['student_id']
            # 파일명 안전 처리
            safe_name = self._sanitize_filename(student_name)
            safe_id = self._sanitize_filename(student_id)
            html_filename = f"{safe_name}_{safe_id}.html"
            html_filepath = os.path.join(output_dir, html_filename)
            
            html_content = self._create_html_template(student_data, pdf_title)
            
            with open(html_filepath, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            # HTML 파일만 생성 (브라우저 열지 않음)
            print(f"PDF 생성 실패. HTML 파일로 저장: {html_filename}")
            print(f"HTML 파일 위치: {os.path.abspath(html_filepath)}")
            if save_html:
                print(f"HTML 파일이 output 폴더에 저장되었습니다.")
            else:
                print(f"HTML 파일을 수동으로 브라우저에서 열어서 Ctrl+P로 PDF 저장하세요.")
            
        except Exception as e:
            print(f"HTML 폴백 생성 오류: {str(e)}")
            raise
    
    def _format_wrong_answers(self, wrong_answers):
        """오답번호를 문자열로 포맷팅"""
        try:
            if isinstance(wrong_answers, str):
                return wrong_answers
            elif isinstance(wrong_answers, list):
                return ', '.join(map(str, wrong_answers))
            else:
                return str(wrong_answers)
        except Exception as e:
            return str(wrong_answers)
            
    def _create_html_template(self, student_data: Dict[str, Any], pdf_title: str) -> str:
        """HTML 템플릿 생성"""
        # 학생 정보 추출 (HTML 이스케이프 처리)
        student_name = html.escape(str(student_data['name']))
        student_id = html.escape(str(student_data['student_id']))
        pdf_title_escaped = html.escape(str(pdf_title))
        
        # 과목별 데이터 정리 (HTML 이스케이프 처리)
        subjects_data = {}
        for subject, info in student_data['subjects'].items():
            # 한국사와 영어는 표점과 백분위 없음
            if subject in ['한국사', '영어']:
                subjects_data[subject] = {
                    'raw': str(int(info.get('total_score', 0))),
                    'std': '—',
                    'percent': '—',
                    'grade': html.escape(str(info.get('grade', '—'))),
                    'testees': '—',
                    'subject_name': html.escape(str(info.get('subject_name', ''))),
                    'wrong_answers': html.escape(self._format_wrong_answers(info.get('wrong_answers', [])))
                }
            else:
                # None 값들을 적절히 처리
                standard_score = info.get('standard_score')
                percentile = info.get('percentile')
                grade = info.get('grade')
                
                subjects_data[subject] = {
                    'raw': str(int(info.get('total_score', 0))),
                    'std': html.escape(str(standard_score)) if standard_score is not None else '—',
                    'percent': html.escape(str(percentile)) if percentile is not None else '—',
                    'grade': html.escape(str(grade)) if grade is not None else '—',
                    'testees': '—',
                    'subject_name': html.escape(str(info.get('subject_name', ''))),
                    'wrong_answers': html.escape(self._format_wrong_answers(info.get('wrong_answers', [])))
                }
        
        html_content = f"""<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{pdf_title_escaped}</title>
  <style>
    /* --------- 기본 설정 --------- */
    :root{{
      --ink:#0e0f12;            /* 본문 텍스트/선 색 */
      --muted:#60646c;          /* 보조 텍스트 */
      --grid:#1e2330;           /* 테이블 선 */
      --bg:#ffffff;             /* 바탕 */
      --accent:#111827;         /* 제목 */
      --gap:10px;               /* 외곽 여백 단위 */
    }}
    *{{box-sizing:border-box}}
    html,body{{height:100%}}
    body{{margin:0;background:var(--bg);color:var(--ink);font:14px/1.4 "Pretendard","Noto Sans KR",system-ui,-apple-system,Segoe UI,Roboto,Helvetica,Arial,"Apple SD Gothic Neo","Malgun Gothic",sans-serif}}

    .page{{max-width:900px;display:flex;flex-direction:column;justify-content:flex-start;margin:0 auto;padding:20px;border:1px solid #dcdfe4;border-radius:10px;box-shadow:0 8px 24px rgba(0,0,0,.06)}}

    /* 제목 */
    .title{{display:flex;align-items:baseline;gap:10px;justify-content:center;margin:0 0 16px}}
    .title h1{{font-size:26px;letter-spacing:.2px;margin:0;color:var(--accent);font-weight:800}}
    .title .sub{{font-size:14px;color:var(--muted)}}

    /* 정보 표 상단 (수험번호/성명 등) */
    table{{border-collapse:collapse;width:100%}}
    .grid{{border:2px solid var(--grid)}}
    .grid th,.grid td{{border:1.5px solid var(--grid);padding:8px 10px}}
    .grid th{{background:#f7f8fb;font-weight:700;text-align:center}}
    .grid .c{{text-align:center}}

    .meta{{margin-bottom:14px}}
    .meta th{{width:96px;white-space:nowrap}}
    .meta td{{min-width:100px}}

    /* 메인 성적 표 */
    .scores thead th{{font-size:13px}}
    .scores .area{{width:88px}}
    .scores .subcol{{background:#fafafc;font-weight:600}}

    .scores thead .group-2{{background:#f2f4f8;font-weight:700}}

    /* 헤더 하단 소제목 (국어/수학 선택과목 표기용) */
    .thstack{{display:flex;flex-direction:column;align-items:center;line-height:1.2}}
    .thstack small{{font-size:11px;color:var(--muted);font-weight:600;margin-top:2px}}
     
    /* 대각선 비적용(제2외국어·한문) 셀 표현 */
    .na{{position:relative;color:#444}}
    .na:before{{content:none}}
    .na span{{position:relative;z-index:1}}
    .num{{font-variant-numeric:tabular-nums}}

    .wrong{{margin-top:10px}}
    .wrong-grid{{display:grid;grid-template-columns:160px 1fr;column-gap:8px;row-gap:6px;align-items:center}}
    .wrong-grid .label{{font-weight:700;text-align:right;padding-right:6px;color:var(--ink)}}
    .wrong-grid .box{{min-height:28px;border:1px dashed var(--grid);padding:6px 8px;border-radius:6px;word-break:break-word}}
    .wrong-grid .box[contenteditable]{{outline:none}}
    

    @page{{size:A4 portrait;margin:14mm}}
    @media print{{
      body{{background:#fff}}
      .page{{
        box-shadow:none;border:none;
        width:auto;max-width:900px;
        height:calc(297mm - 28mm);max-height:calc(297mm - 28mm);
        margin:auto;
        padding:0;overflow:hidden;break-inside:avoid
      }}
      .title{{margin:6mm 0 4mm}}
      .grid th,.grid td{{padding:4px 6px}}
    }}
  </style>
</head>
<body>
  <div class="page">
    <div class="title">
      <h1>{pdf_title_escaped}</h1>
    </div>

    <table class="grid meta">
      <colgroup>
        <col style="width:110px" />
        <col style="width:180px" />
        <col style="width:70px" />
        <col style="width:110px" />
        <col style="width:90px" />
        <col style="width:200px" />
        <col style="width:70px" />
        <col style="width:70px" />
      </colgroup>
      <tr>
        <th>수험번호</th>
        <td class="num">{student_id}</td>
        <th>성&nbsp;&nbsp;명</th>
        <td>{student_name}</td>
        <th>성별</th>
        <td></td>
        <th>반</th>
        <td class="c"></td>
      </tr>
      <tr>
        <th>생년월일</th>
        <td></td>
        <th>시 · 도</th>
        <td></td>
        <th>학교명(학원명)</th>
        <td>SN독학기숙학원</td>
        <th>번호</th>
        <td class="c"></td>
      </tr>
    </table>

    <table class="grid scores">
      <colgroup>
        <col style="width:80px" />
        <col style="width:140px" />
        <col style="width:140px" />
        <col style="width:140px" />
        <col style="width:140px" />
        <col style="width:140px" />
        <col style="width:140px" />
        <col style="width:180px" />
      </colgroup>
      <thead>
        <tr>
          <th class="area">영역</th>
          <th>한국사</th>
          <th><div class="thstack"><span>국어</span><small>{subjects_data.get('국어', {}).get('subject_name', '')}</small></div></th>
          <th><div class="thstack"><span>수학</span><small>{subjects_data.get('수학', {}).get('subject_name', '')}</small></div></th>
          <th>영어</th>
          <th class="group-2">{subjects_data.get('탐구1', {}).get('subject_name', '')}</th>
          <th class="group-2">{subjects_data.get('탐구2', {}).get('subject_name', '')}</th>
          <th>제2외국어·한문</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th class="subcol">원점수</th>
          <td class="c num">{subjects_data.get('한국사', {}).get('raw', '—')}</td>
          <td class="c num">{subjects_data.get('국어', {}).get('raw', '—')}</td>
          <td class="c num">{subjects_data.get('수학', {}).get('raw', '—')}</td>
          <td class="c num">{subjects_data.get('영어', {}).get('raw', '—')}</td>
          <td class="c num">{subjects_data.get('탐구1', {}).get('raw', '—')}</td>
          <td class="c num">{subjects_data.get('탐구2', {}).get('raw', '—')}</td>
          <td class="c num">—</td>
        </tr>

        <tr>
          <th class="subcol">표준점수</th>
          <td class="c num">{subjects_data.get('한국사', {}).get('std', '—')}</td>
          <td class="c num">{subjects_data.get('국어', {}).get('std', '—')}</td>
          <td class="c num">{subjects_data.get('수학', {}).get('std', '—')}</td>
          <td class="c num">{subjects_data.get('영어', {}).get('std', '—')}</td>
          <td class="c num">{subjects_data.get('탐구1', {}).get('std', '—')}</td>
          <td class="c num">{subjects_data.get('탐구2', {}).get('std', '—')}</td>
          <td class="c num">—</td>
        </tr>

        <tr>
          <th class="subcol">백분위</th>
          <td class="c num">{subjects_data.get('한국사', {}).get('percent', '—')}</td>
          <td class="c num">{subjects_data.get('국어', {}).get('percent', '—')}</td>
          <td class="c num">{subjects_data.get('수학', {}).get('percent', '—')}</td>
          <td class="c num">{subjects_data.get('영어', {}).get('percent', '—')}</td>
          <td class="c num">{subjects_data.get('탐구1', {}).get('percent', '—')}</td>
          <td class="c num">{subjects_data.get('탐구2', {}).get('percent', '—')}</td>
          <td class="c num">—</td>
        </tr>

        <tr>
          <th class="subcol">등&nbsp;&nbsp;급</th>
          <td class="c num">{subjects_data.get('한국사', {}).get('grade', '—')}</td>
          <td class="c num">{subjects_data.get('국어', {}).get('grade', '—')}</td>
          <td class="c num">{subjects_data.get('수학', {}).get('grade', '—')}</td>
          <td class="c num">{subjects_data.get('영어', {}).get('grade', '—')}</td>
          <td class="c num">{subjects_data.get('탐구1', {}).get('grade', '—')}</td>
          <td class="c num">{subjects_data.get('탐구2', {}).get('grade', '—')}</td>
          <td class="c num">—</td>
        </tr>

        <tr>
          <th class="subcol">응시자수</th>
          <td class="c num">—</td>
          <td class="c num">—</td>
          <td class="c num">—</td>
          <td class="c num">—</td>
          <td class="c num">—</td>
          <td class="c num">—</td>
          <td class="c num">—</td>
        </tr>
      </tbody>
    </table>

    <section class="wrong">
      <h3 style="margin:10px 0 6px;font-size:14px;color:var(--accent);">과목별 오답번호</h3>
      <div class="wrong-grid">
        <div class="label">한국사</div>
        <div class="box">{subjects_data.get('한국사', {}).get('wrong_answers', '')}</div>

        <div class="label">국어(언어와 매체)</div>
        <div class="box">{subjects_data.get('국어', {}).get('wrong_answers', '')}</div>

        <div class="label">수학(미적분)</div>
        <div class="box">{subjects_data.get('수학', {}).get('wrong_answers', '')}</div>

        <div class="label">영어</div>
        <div class="box">{subjects_data.get('영어', {}).get('wrong_answers', '')}</div>

        <div class="label">{subjects_data.get('탐구1', {}).get('subject_name', '')}</div>
        <div class="box">{subjects_data.get('탐구1', {}).get('wrong_answers', '')}</div>

        <div class="label">{subjects_data.get('탐구2', {}).get('subject_name', '')}</div>
        <div class="box">{subjects_data.get('탐구2', {}).get('wrong_answers', '')}</div>

        <div class="label">제2외국어·한문</div>
        <div class="box">—</div>
      </div>
    </section>

    <p style="margin-top:8px;color:#7b8190;font-size:12px">본 프로그램은 SN독학기숙학원이 개발하였습니다.</p>
  </div>
</body>
</html>"""
        
        return html_content