from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os
from typing import Dict, Any
# weasyprint import 제거됨

class PDFGenerator:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.setup_korean_font()
        self.setup_custom_styles()
        
    def setup_korean_font(self):
        """한글 폰트 설정"""
        try:
            # Windows 시스템 폰트 사용
            pdfmetrics.registerFont(TTFont('MalgunGothic', 'C:/Windows/Fonts/malgun.ttf'))
            self.korean_font = 'MalgunGothic'
        except:
            try:
                # 대체 폰트 시도
                pdfmetrics.registerFont(TTFont('NotoSansKR', 'C:/Windows/Fonts/gulim.ttc'))
                self.korean_font = 'NotoSansKR'
            except:
                # 기본 폰트 사용
                self.korean_font = 'Helvetica'
                print("한글 폰트를 찾을 수 없습니다. 기본 폰트를 사용합니다.")
        
    def setup_custom_styles(self):
        """커스텀 스타일 설정"""
        # 제목 스타일 (기존 Title 스타일 수정)
        if 'Title' in self.styles:
            self.styles['Title'].fontName = self.korean_font
            self.styles['Title'].fontSize = 18
            self.styles['Title'].spaceAfter = 20
            self.styles['Title'].alignment = TA_CENTER
            self.styles['Title'].textColor = colors.darkblue
        else:
            self.styles.add(ParagraphStyle(
                name='Title',
                parent=self.styles['Heading1'],
                fontName=self.korean_font,
                fontSize=18,
                spaceAfter=20,
                alignment=TA_CENTER,
                textColor=colors.darkblue
            ))
        
        # 부제목 스타일
        if 'SubTitle' in self.styles:
            self.styles['SubTitle'].fontName = self.korean_font
            self.styles['SubTitle'].fontSize = 14
            self.styles['SubTitle'].spaceAfter = 10
            self.styles['SubTitle'].alignment = TA_LEFT
            self.styles['SubTitle'].textColor = colors.darkgreen
        else:
            self.styles.add(ParagraphStyle(
                name='SubTitle',
                parent=self.styles['Heading2'],
                fontName=self.korean_font,
                fontSize=14,
                spaceAfter=10,
                alignment=TA_LEFT,
                textColor=colors.darkgreen
            ))
        
        # 일반 텍스트 스타일 (기존 Normal 스타일 수정)
        if 'CustomNormal' in self.styles:
            self.styles['CustomNormal'].fontName = self.korean_font
            self.styles['CustomNormal'].fontSize = 10
            self.styles['CustomNormal'].spaceAfter = 6
            self.styles['CustomNormal'].alignment = TA_LEFT
        else:
            self.styles.add(ParagraphStyle(
                name='CustomNormal',
                parent=self.styles['Normal'],
                fontName=self.korean_font,
                fontSize=10,
                spaceAfter=6,
                alignment=TA_LEFT
            ))
        
    def generate_student_report(self, student_data: Dict[str, Any], output_dir: str, pdf_title: str = "학생 성적표"):
        """학생별 성적표 PDF 생성 (수능 평가원 형식)"""
        try:
            # 파일명 생성
            student_name = student_data['name']
            student_id = student_data['student_id']
            filename = f"{student_name}_{student_id}.pdf"
            filepath = os.path.join(output_dir, filename)
            
            # PDF 문서 생성
            doc = SimpleDocTemplate(filepath, pagesize=A4, 
                                   rightMargin=1*cm, leftMargin=1*cm,
                                   topMargin=1*cm, bottomMargin=1*cm)
            story = []
            
            # 제목
            story.append(Paragraph(pdf_title, self.styles['Title']))
            story.append(Spacer(1, 20))
            
            # 수능 평가원 형식의 성적표 테이블 생성
            score_table = self._create_suneung_style_table(student_data)
            story.append(score_table)
            story.append(Spacer(1, 20))
            
            # 오답 분석
            story.append(Paragraph("오답 분석", self.styles['SubTitle']))
            story.append(Spacer(1, 10))
            
            # 오답 분석 테이블 생성
            wrong_answers_table = self._create_wrong_answers_table(student_data)
            story.append(wrong_answers_table)
            
            # PDF 생성
            doc.build(story)
            print(f"PDF 생성 완료: {filename}")
            
        except Exception as e:
            print(f"PDF 생성 오류 ({student_data['name']}): {str(e)}")
            raise
            
    def _create_suneung_style_table(self, student_data: Dict[str, Any]) -> Table:
        """수능 평가원 형식의 성적표 테이블 생성"""
        # 학생 정보 행
        student_name = student_data['name']
        student_id = student_data['student_id']
        
        # 테이블 데이터 구성
        table_data = []
        
        # 헤더 행
        header_row = [
            Paragraph("수험번호", self.styles['CustomNormal']),
            Paragraph("성명", self.styles['CustomNormal']),
            Paragraph("성별", self.styles['CustomNormal']),
            Paragraph("생년월일", self.styles['CustomNormal']),
            Paragraph("시·도", self.styles['CustomNormal']),
            Paragraph("학교명(학원명)", self.styles['CustomNormal']),
            Paragraph("반", self.styles['CustomNormal']),
            Paragraph("번호", self.styles['CustomNormal'])
        ]
        table_data.append(header_row)
        
        # 학생 정보 데이터 행
        student_info_row = [
            Paragraph(student_id, self.styles['CustomNormal']),
            Paragraph(student_name, self.styles['CustomNormal']),
            Paragraph("남", self.styles['CustomNormal']),
            Paragraph("03.03.31.", self.styles['CustomNormal']),
            Paragraph("경기", self.styles['CustomNormal']),
            Paragraph("SN독학기숙학원", self.styles['CustomNormal']),
            Paragraph("2", self.styles['CustomNormal']),
            Paragraph("6", self.styles['CustomNormal'])
        ]
        table_data.append(student_info_row)
        
        # 빈 행 추가
        table_data.append([""] * 8)
        
        # 영역 헤더 행
        area_header_row = [
            Paragraph("영역", self.styles['CustomNormal']),
            Paragraph("한국사", self.styles['CustomNormal']),
            Paragraph("국어", self.styles['CustomNormal']),
            Paragraph("수학", self.styles['CustomNormal']),
            Paragraph("영어", self.styles['CustomNormal']),
            Paragraph("탐구", self.styles['CustomNormal']),
            Paragraph("제2외국어/한문", self.styles['CustomNormal']),
            Paragraph("", self.styles['CustomNormal'])
        ]
        table_data.append(area_header_row)
        
        # 선택과목 행
        selected_subjects_row = [
            Paragraph("선택과목", self.styles['CustomNormal']),
            Paragraph("", self.styles['CustomNormal']),
            Paragraph("", self.styles['CustomNormal']),
            Paragraph("", self.styles['CustomNormal']),
            Paragraph("", self.styles['CustomNormal']),
            Paragraph("", self.styles['CustomNormal']),
            Paragraph("", self.styles['CustomNormal']),
            Paragraph("", self.styles['CustomNormal'])
        ]
        table_data.append(selected_subjects_row)
        
        # 과목별 데이터 추가
        subjects_order = ["한국사", "국어", "수학", "영어", "탐구1", "탐구2"]
        
        for subject in subjects_order:
            if subject in student_data['subjects']:
                subject_info = student_data['subjects'][subject]
                selected_subject = subject_info.get('subject_name', '')
                total_score = subject_info.get('total_score', '')
                correct_count = subject_info.get('correct_count', '')
                grade = subject_info.get('grade', '')
                standard_score = subject_info.get('standard_score', '')
                percentile = subject_info.get('percentile', '')
                
                # 과목별 행 생성
                if subject == "한국사":
                    row = [
                        Paragraph("", self.styles['CustomNormal']),
                        Paragraph(str(total_score), self.styles['CustomNormal']),
                        Paragraph("", self.styles['CustomNormal']),
                        Paragraph("", self.styles['CustomNormal']),
                        Paragraph("", self.styles['CustomNormal']),
                        Paragraph("", self.styles['CustomNormal']),
                        Paragraph("", self.styles['CustomNormal']),
                        Paragraph("", self.styles['CustomNormal'])
                    ]
                elif subject == "국어":
                    row = [
                        Paragraph("", self.styles['CustomNormal']),
                        Paragraph("", self.styles['CustomNormal']),
                        Paragraph(str(total_score), self.styles['CustomNormal']),
                        Paragraph("", self.styles['CustomNormal']),
                        Paragraph("", self.styles['CustomNormal']),
                        Paragraph("", self.styles['CustomNormal']),
                        Paragraph("", self.styles['CustomNormal']),
                        Paragraph("", self.styles['CustomNormal'])
                    ]
                elif subject == "수학":
                    row = [
                        Paragraph("", self.styles['CustomNormal']),
                        Paragraph("", self.styles['CustomNormal']),
                        Paragraph("", self.styles['CustomNormal']),
                        Paragraph(str(total_score), self.styles['CustomNormal']),
                        Paragraph("", self.styles['CustomNormal']),
                        Paragraph("", self.styles['CustomNormal']),
                        Paragraph("", self.styles['CustomNormal']),
                        Paragraph("", self.styles['CustomNormal'])
                    ]
                elif subject == "영어":
                    row = [
                        Paragraph("", self.styles['CustomNormal']),
                        Paragraph("", self.styles['CustomNormal']),
                        Paragraph("", self.styles['CustomNormal']),
                        Paragraph("", self.styles['CustomNormal']),
                        Paragraph(str(total_score), self.styles['CustomNormal']),
                        Paragraph("", self.styles['CustomNormal']),
                        Paragraph("", self.styles['CustomNormal']),
                        Paragraph("", self.styles['CustomNormal'])
                    ]
                elif subject == "탐구1":
                    row = [
                        Paragraph("", self.styles['CustomNormal']),
                        Paragraph("", self.styles['CustomNormal']),
                        Paragraph("", self.styles['CustomNormal']),
                        Paragraph("", self.styles['CustomNormal']),
                        Paragraph("", self.styles['CustomNormal']),
                        Paragraph(str(total_score), self.styles['CustomNormal']),
                        Paragraph("", self.styles['CustomNormal']),
                        Paragraph("", self.styles['CustomNormal'])
                    ]
                elif subject == "탐구2":
                    row = [
                        Paragraph("", self.styles['CustomNormal']),
                        Paragraph("", self.styles['CustomNormal']),
                        Paragraph("", self.styles['CustomNormal']),
                        Paragraph("", self.styles['CustomNormal']),
                        Paragraph("", self.styles['CustomNormal']),
                        Paragraph("", self.styles['CustomNormal']),
                        Paragraph(str(total_score), self.styles['CustomNormal']),
                        Paragraph("", self.styles['CustomNormal'])
                    ]
                
                table_data.append(row)
        
        # 테이블 생성
        table = Table(table_data, colWidths=[2*cm, 2*cm, 2*cm, 2*cm, 2*cm, 2*cm, 2*cm, 2*cm])
        
        # 테이블 스타일 설정
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, -1), self.korean_font),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTNAME', (0, 1), (-1, -1), self.korean_font),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        
        return table
            
    def _create_grade_table(self, student_data: Dict[str, Any]) -> Table:
        """성적표 테이블 생성"""
        # 테이블 헤더
        table_data = [
            ['과목', '선택과목', '총점', '정답수', '등급', '표점', '백분위']
        ]
        
        # 과목별 데이터 추가
        for subject, subject_info in student_data['subjects'].items():
            row = [
                subject,
                subject_info.get('subject_name', ''),
                str(subject_info.get('total_score', '')),
                str(subject_info.get('correct_count', '')),
                str(subject_info.get('grade', '')),
                str(subject_info.get('standard_score', '')),
                str(subject_info.get('percentile', ''))
            ]
            table_data.append(row)
            
        # 테이블 생성
        table = Table(table_data, colWidths=[2*cm, 3*cm, 1.5*cm, 1.5*cm, 1*cm, 1.5*cm, 1.5*cm])
        
        # 테이블 스타일 설정
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        
        return table
        
    def _create_wrong_answers_table(self, student_data: Dict[str, Any]) -> Table:
        """오답 분석 테이블 생성"""
        # 테이블 헤더
        table_data = [
            ['과목', '오답 번호', '오답 개수']
        ]
        
        # 과목별 오답 데이터 추가
        for subject, subject_info in student_data['subjects'].items():
            wrong_answers = subject_info.get('wrong_answers', [])
            wrong_answers_str = ', '.join(map(str, wrong_answers)) if wrong_answers else '없음'
            wrong_count = len(wrong_answers)
            
            row = [
                subject,
                wrong_answers_str,
                str(wrong_count)
            ]
            table_data.append(row)
            
        # 테이블 생성
        table = Table(table_data, colWidths=[2*cm, 8*cm, 2*cm])
        
        # 테이블 스타일 설정
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        
        return table
