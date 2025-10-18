"""
Playwright를 사용한 HTML → PDF 변환기
최신 CSS/폰트/레이아웃을 그대로 유지하면서 PDF 생성
"""

import asyncio
import urllib.parse
from pathlib import Path
from playwright.async_api import async_playwright
from typing import Optional


class PlaywrightPDFConverter:
    """Playwright 기반 PDF 변환기"""
    
    def __init__(self):
        self.browser = None
        self.page = None
    
    async def __aenter__(self):
        """비동기 컨텍스트 매니저 진입"""
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(
            headless=True,  # 헤드리스 모드
            args=['--no-sandbox', '--disable-dev-shm-usage']  # 안정성 향상
        )
        self.page = await self.browser.new_page()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """비동기 컨텍스트 매니저 종료"""
        if self.browser:
            await self.browser.close()
        if hasattr(self, 'playwright'):
            await self.playwright.stop()
    
    async def html_file_to_pdf(self, input_html: str, output_pdf: str, 
                              format: str = "A4", margin: dict = None) -> bool:
        """
        HTML 파일을 PDF로 변환
        
        Args:
            input_html: 입력 HTML 파일 경로
            output_pdf: 출력 PDF 파일 경로
            format: 페이지 형식 (A4, Letter 등)
            margin: 여백 설정
            
        Returns:
            bool: 변환 성공 여부
        """
        try:
            # 로컬 파일 경로를 file:// URI로 변환
            html_path = Path(input_html).resolve().as_uri()
            await self.page.goto(html_path)
            
            # PDF 생성 옵션
            pdf_options = {
                "path": output_pdf,
                "format": format,
                "print_background": True,
                "prefer_css_page_size": True
            }
            
            # 여백 설정
            if margin is None:
                margin = {
                    "top": "12mm",
                    "right": "12mm", 
                    "bottom": "12mm",
                    "left": "12mm"
                }
            pdf_options["margin"] = margin
            
            await self.page.pdf(**pdf_options)
            return True
            
        except Exception as e:
            print(f"HTML 파일 → PDF 변환 오류: {str(e)}")
            return False
    
    async def html_string_to_pdf(self, html_string: str, output_pdf: str,
                                format: str = "A4", margin: dict = None) -> bool:
        """
        HTML 문자열을 PDF로 변환
        
        Args:
            html_string: HTML 문자열
            output_pdf: 출력 PDF 파일 경로
            format: 페이지 형식 (A4, Letter 등)
            margin: 여백 설정
            
        Returns:
            bool: 변환 성공 여부
        """
        try:
            # HTML 문자열을 data URL로 변환
            data_url = "data:text/html;charset=utf-8," + urllib.parse.quote(html_string)
            await self.page.goto(data_url)
            
            # PDF 생성 옵션
            pdf_options = {
                "path": output_pdf,
                "format": format,
                "print_background": True,
                "prefer_css_page_size": True
            }
            
            # 여백 설정
            if margin is None:
                margin = {
                    "top": "12mm",
                    "right": "12mm",
                    "bottom": "12mm", 
                    "left": "12mm"
                }
            pdf_options["margin"] = margin
            
            await self.page.pdf(**pdf_options)
            return True
            
        except Exception as e:
            print(f"HTML 문자열 → PDF 변환 오류: {str(e)}")
            return False


# 동기 래퍼 함수들
def html_file_to_pdf_sync(input_html: str, output_pdf: str, 
                          format: str = "A4", margin: dict = None) -> bool:
    """HTML 파일을 PDF로 변환 (동기 버전)"""
    async def _convert():
        async with PlaywrightPDFConverter() as converter:
            return await converter.html_file_to_pdf(input_html, output_pdf, format, margin)
    
    return asyncio.run(_convert())


def html_string_to_pdf_sync(html_string: str, output_pdf: str,
                            format: str = "A4", margin: dict = None) -> bool:
    """HTML 문자열을 PDF로 변환 (동기 버전)"""
    async def _convert():
        async with PlaywrightPDFConverter() as converter:
            return await converter.html_string_to_pdf(html_string, output_pdf, format, margin)
    
    return asyncio.run(_convert())


# 사용 예시
if __name__ == "__main__":
    # HTML 파일 → PDF 테스트
    print("HTML 파일 → PDF 변환 테스트...")
    success = html_file_to_pdf_sync("test.html", "output.pdf")
    print(f"변환 결과: {'성공' if success else '실패'}")
    
    # HTML 문자열 → PDF 테스트
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>테스트</title>
        <style>
            body { font-family: 'Noto Sans KR', sans-serif; }
            h1 { color: #333; }
        </style>
    </head>
    <body>
        <h1>한글 테스트</h1>
        <p>이것은 Playwright PDF 변환 테스트입니다.</p>
    </body>
    </html>
    """
    
    print("HTML 문자열 → PDF 변환 테스트...")
    success = html_string_to_pdf_sync(html_content, "string_output.pdf")
    print(f"변환 결과: {'성공' if success else '실패'}")

