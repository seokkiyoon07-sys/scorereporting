from flask import Flask, render_template, request, send_file, jsonify, redirect, url_for, abort
import os
import pandas as pd
from werkzeug.utils import secure_filename
from data_processor import DataProcessor
from jinja_pdf_generator import JinjaPDFGenerator
import shutil
from datetime import datetime
import secrets
import re

app = Flask(__name__, static_folder='static')

# SECRET_KEY를 환경 변수에서 가져오거나 랜덤 생성
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or secrets.token_hex(32)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['OUTPUT_FOLDER'] = 'outputs'
app.config['SAMPLE_FOLDER'] = 'static/samples'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# 업로드 폴더 생성
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)
os.makedirs(app.config['SAMPLE_FOLDER'], exist_ok=True)

# 허용된 파일 확장자
ALLOWED_EXTENSIONS = {'csv', 'xlsx'}

# 안전한 파일명 패턴 (알파벳, 숫자, 언더스코어, 하이픈, 한글만 허용)
SAFE_FILENAME_PATTERN = re.compile(r'^[\w\-가-힣]+\.[\w]+$')

def allowed_file(filename):
    """파일 확장자 검증"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def is_safe_path(base_path, target_path):
    """경로 순회 공격 방지"""
    base = os.path.abspath(base_path)
    target = os.path.abspath(target_path)
    return target.startswith(base)

def sanitize_filename(filename):
    """파일명 안전성 검증 및 정리"""
    # 위험한 문자 제거
    filename = secure_filename(filename)
    # 파일명 길이 제한
    name, ext = os.path.splitext(filename)
    if len(name) > 100:
        name = name[:100]
    return f"{name}{ext}"

# 세션별 데이터 프로세서 (동시성 문제 해결)
data_processors = {}
pdf_generator = JinjaPDFGenerator()

def get_session_data_processor():
    """세션별 데이터 프로세서 반환"""
    session_id = request.remote_addr  # 실제로는 session ID 사용 권장
    if session_id not in data_processors:
        data_processors[session_id] = DataProcessor()
    return data_processors[session_id]

@app.route('/')
def index():
    """메인 페이지"""
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_files():
    """파일 업로드 처리"""
    try:
        print("[업로드] 파일 업로드 요청 받음")
        print(f"[업로드] 요청 파일 목록: {list(request.files.keys())}")
        
        data_processor = get_session_data_processor()
        
        # 학생명 파일 확인 (필수)
        if 'student_names' not in request.files:
            print("[오류] 학생명 파일이 요청에 포함되지 않음")
            return jsonify({'error': '학생명 파일이 필요합니다.'}), 400
        
        student_names_file = request.files['student_names']
        
        # 파일명 검증
        if not student_names_file.filename:
            return jsonify({'error': '학생명 파일명이 비어있습니다.'}), 400
        
        # 학생명 파일 저장
        if student_names_file and allowed_file(student_names_file.filename):
            filename = sanitize_filename(student_names_file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            
            # 경로 안전성 확인
            if not is_safe_path(app.config['UPLOAD_FOLDER'], filepath):
                return jsonify({'error': '유효하지 않은 파일 경로입니다.'}), 400
            
            student_names_file.save(filepath)
            print(f"[업로드] 학생명 파일 저장 완료: {filepath}")
            
            # 학생명 데이터 로드
            data_processor.load_student_names(filepath)
            print(f"[업로드] 학생명 데이터 로드 완료: {len(data_processor.student_names)}명")
        else:
            return jsonify({'error': '유효하지 않은 학생명 파일입니다.'}), 400
        
        # 등급컷 파일 확인 (선택사항)
        if 'grade_cutoff' in request.files:
            grade_cutoff_file = request.files['grade_cutoff']
            
            if grade_cutoff_file and grade_cutoff_file.filename and allowed_file(grade_cutoff_file.filename):
                filename = sanitize_filename(grade_cutoff_file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                
                # 경로 안전성 확인
                if is_safe_path(app.config['UPLOAD_FOLDER'], filepath):
                    grade_cutoff_file.save(filepath)
                    # 등급컷 데이터 로드
                    data_processor.load_grade_cutoff_data(filepath)
                    print("[INFO] 등급컷 파일 업로드 완료")
        
        # 과목 파일들 처리
        subject_files = {}
        for key in request.files:
            if key.startswith('subject_'):
                subject_name = key.replace('subject_', '')
                file = request.files[key]
                
                if file and file.filename and allowed_file(file.filename):
                    filename = sanitize_filename(file.filename)
                    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    
                    # 경로 안전성 확인
                    if not is_safe_path(app.config['UPLOAD_FOLDER'], filepath):
                        continue
                    
                    file.save(filepath)
                    subject_files[subject_name] = filepath
        
        # 과목 데이터 로드
        for subject_name, filepath in subject_files.items():
            data_processor.load_subject_data(subject_name, filepath)
        
        print(f"[업로드] 업로드 완료 - 과목 수: {len(subject_files)}")
        return jsonify({
            'success': True,
            'message': f'✅ {len(subject_files)}개 과목 파일이 업로드되었습니다.',
            'subjects': list(subject_files.keys())
        })
    
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"[ERROR] 파일 업로드 오류: {str(e)}")
        print(f"[ERROR] 상세 오류:\n{error_details}")
        return jsonify({'error': f'파일 업로드 중 오류가 발생했습니다.\n\n{str(e)}'}), 500

@app.route('/process', methods=['POST'])
def process_data():
    """데이터 처리 및 성적표 생성"""
    try:
        data_processor = get_session_data_processor()
        
        # 요청 데이터
        data = request.json
        if not data:
            return jsonify({'error': '요청 데이터가 없습니다.'}), 400
        
        # 입력 검증
        pdf_title = data.get('pdf_title', '모의고사 성적표')[:100]  # 길이 제한
        exam_name = data.get('exam_name', '2024학년도 모의고사')[:100]  # 길이 제한
        
        # 데이터 처리
        try:
            processed_data = data_processor.process_all_data()
        except Exception as e:
            # process_all_data에서 발생한 오류를 그대로 전달
            raise e
        
        if processed_data is None or processed_data.empty:
            return jsonify({'error': '⚠️ 처리할 학생 데이터가 없습니다!\n\n파일 업로드 상태를 확인하거나\n파일 형식이 올바른지 확인해주세요.'}), 400
        
        # 학생 수 제한 (DoS 방지)
        if len(processed_data) > 1000:
            return jsonify({'error': '한 번에 최대 1000명까지만 처리할 수 있습니다.'}), 400
        
        # 출력 폴더 생성
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_dir = os.path.join(app.config['OUTPUT_FOLDER'], timestamp)
        os.makedirs(output_dir, exist_ok=True)
        
        # PDF 생성
        generated_files = []
        failed_count = 0
        
        for idx, row in processed_data.iterrows():
            try:
                student_data = row.to_dict()
                
                # 파일명 안전하게 생성
                student_name = str(student_data.get('이름', f'student_{idx}'))[:50]
                student_id = str(student_data.get('학번', idx))[:50]
                safe_name = sanitize_filename(f"{student_name}_{student_id}.pdf")
                
                output_file = os.path.join(output_dir, safe_name)
                
                # 경로 안전성 확인
                if not is_safe_path(output_dir, output_file):
                    print(f"[경고] 안전하지 않은 경로: {output_file}")
                    failed_count += 1
                    continue
                
                # PDF 생성
                pdf_generator.generate_pdf(student_data, output_file, pdf_title, exam_name)
                generated_files.append(os.path.basename(output_file))
                
            except Exception as e:
                print(f"[ERROR] 학생 {idx} PDF 생성 오류: {str(e)}")
                failed_count += 1
                continue
        
        # 생성된 파일이 하나도 없으면 오류
        if len(generated_files) == 0:
            return jsonify({'error': f'❌ 성적표 생성에 실패했습니다.\n\n총 {len(processed_data)}명 중 {failed_count}명 실패\n\n파일 형식을 확인하거나 서버 로그를 확인해주세요.'}), 500
        
        message = f'✅ {len(generated_files)}개의 성적표가 생성되었습니다!'
        if failed_count > 0:
            message += f'\n\n⚠️ {failed_count}개는 생성 실패했습니다.'
        
        return jsonify({
            'success': True,
            'message': message,
            'files': generated_files,
            'output_dir': timestamp
        })
    
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"[ERROR] 데이터 처리 오류: {str(e)}")
        print(f"[ERROR] 상세 오류:\n{error_details}")
        
        # 사용자에게 더 자세한 오류 메시지 제공
        error_message = str(e)
        if "학생명 데이터가 로드되지 않았습니다" in error_message:
            return jsonify({'error': '⚠️ 학생명 파일을 먼저 업로드해주세요!\n\n학생명 파일(수험번호, 이름)이 필요합니다.'}), 400
        elif "과목 데이터가 로드되지 않았습니다" in error_message:
            return jsonify({'error': '⚠️ 과목 파일을 먼저 업로드해주세요!\n\n최소 하나 이상의 과목 파일이 필요합니다.'}), 400
        elif "처리할 데이터가 없습니다" in error_message:
            return jsonify({'error': '⚠️ 처리할 학생 데이터가 없습니다!\n\n파일을 다시 확인해주세요.'}), 400
        else:
            return jsonify({'error': f'데이터 처리 중 오류가 발생했습니다.\n\n오류 내용: {error_message}'}), 500

@app.route('/download/<output_dir>/<filename>')
def download_file(output_dir, filename):
    """생성된 PDF 다운로드"""
    try:
        # 입력 검증 - 경로 순회 공격 방지
        output_dir = secure_filename(output_dir)
        filename = secure_filename(filename)
        
        # 파일 경로 구성
        file_path = os.path.join(app.config['OUTPUT_FOLDER'], output_dir, filename)
        
        # 경로 안전성 확인
        if not is_safe_path(app.config['OUTPUT_FOLDER'], file_path):
            abort(403)  # Forbidden
        
        # 파일 존재 확인
        if not os.path.exists(file_path):
            abort(404)  # Not Found
        
        return send_file(file_path, as_attachment=True, download_name=filename)
        
    except Exception as e:
        print(f"[ERROR] 파일 다운로드 오류: {str(e)}")
        abort(500)

@app.route('/download-sample/<filename>')
def download_sample(filename):
    """샘플 파일 다운로드"""
    try:
        # 화이트리스트 방식으로 허용된 샘플 파일만 다운로드
        allowed_samples = {
            'sample_grade_cutoff.csv',
            'sample_students.csv',
            'sample_korean.csv',
            'sample_math.csv',
            'sample_english.csv',
            'sample_history.csv',
            'sample_inquiry.csv'
        }
        
        # 파일명 검증
        if filename not in allowed_samples:
            abort(403)  # Forbidden
        
        # 파일 경로 구성
        file_path = os.path.join(app.config['SAMPLE_FOLDER'], filename)
        
        # 경로 안전성 확인
        if not is_safe_path(app.config['SAMPLE_FOLDER'], file_path):
            abort(403)
        
        # 파일 존재 확인
        if not os.path.exists(file_path):
            abort(404)
        
        return send_file(file_path, as_attachment=True, download_name=filename)
        
    except Exception as e:
        print(f"[ERROR] 샘플 파일 다운로드 오류: {str(e)}")
        abort(500)

@app.route('/preview', methods=['POST'])
def preview_report():
    """성적표 미리보기 (HTML)"""
    try:
        data_processor = get_session_data_processor()
        
        data = request.json
        if not data:
            return jsonify({'error': '요청 데이터가 없습니다.'}), 400
        
        student_name = data.get('student_name')
        if not student_name:
            return jsonify({'error': '학생 이름이 필요합니다.'}), 400
        
        # 처리된 데이터에서 학생 찾기
        processed_data = data_processor.process_all_data()
        
        if processed_data is None or processed_data.empty:
            return jsonify({'error': '처리된 데이터가 없습니다.'}), 400
        
        student_records = processed_data[processed_data['이름'] == student_name]
        
        if student_records.empty:
            return jsonify({'error': '해당 학생을 찾을 수 없습니다.'}), 404
        
        student_data = student_records.iloc[0].to_dict()
        
        # HTML 렌더링
        return render_template('report.html', 
                             student=student_data,
                             report={
                                 'exam_name': data.get('exam_name', '모의고사')[:100],
                                 'issued_at': datetime.now().strftime('%Y-%m-%d')
                             },
                             scores=format_scores_for_template(student_data))
    
    except Exception as e:
        print(f"[ERROR] 미리보기 오류: {str(e)}")
        return jsonify({'error': '미리보기 생성 중 오류가 발생했습니다.'}), 500

@app.route('/list-students', methods=['GET'])
def list_students():
    """업로드된 데이터의 학생 목록 반환"""
    try:
        data_processor = get_session_data_processor()
        processed_data = data_processor.process_all_data()
        
        if processed_data is None or processed_data.empty:
            return jsonify({'students': []})
        
        students = processed_data['이름'].unique().tolist()
        
        # 목록 크기 제한
        if len(students) > 1000:
            students = students[:1000]
        
        return jsonify({'students': students})
    
    except Exception as e:
        print(f"[ERROR] 학생 목록 조회 오류: {str(e)}")
        return jsonify({'error': '학생 목록 조회 중 오류가 발생했습니다.'}), 500

@app.route('/clear-data', methods=['POST'])
def clear_data():
    """업로드된 데이터 초기화"""
    try:
        # 세션 데이터 프로세서 초기화
        session_id = request.remote_addr
        if session_id in data_processors:
            del data_processors[session_id]
        
        # 업로드 폴더 비우기 (보안: 안전하게 처리)
        upload_folder = app.config['UPLOAD_FOLDER']
        if os.path.exists(upload_folder):
            # 업로드 폴더 내의 파일만 삭제
            for filename in os.listdir(upload_folder):
                file_path = os.path.join(upload_folder, filename)
                
                # 경로 안전성 확인
                if not is_safe_path(upload_folder, file_path):
                    continue
                
                try:
                    if os.path.isfile(file_path):
                        os.unlink(file_path)
                except Exception as e:
                    print(f"[WARNING] 파일 삭제 실패: {file_path} - {str(e)}")
        
        return jsonify({'success': True, 'message': '데이터가 초기화되었습니다.'})
    
    except Exception as e:
        print(f"[ERROR] 데이터 초기화 오류: {str(e)}")
        return jsonify({'error': '데이터 초기화 중 오류가 발생했습니다.'}), 500

def format_scores_for_template(student_data):
    """템플릿에 맞게 점수 데이터 포맷"""
    scores = []
    subjects = ['국어', '수학', '영어', '한국사', '탐구1', '탐구2']
    
    for subject in subjects:
        if f'{subject}_원점수' in student_data:
            scores.append({
                'subject': subject,
                'raw': student_data.get(f'{subject}_원점수', '-'),
                'std': student_data.get(f'{subject}_표준점수', '-'),
                'percentile': student_data.get(f'{subject}_백분위', '-'),
                'grade': student_data.get(f'{subject}_등급', '-')
            })
    
    return scores

if __name__ == '__main__':
    print("=" * 60)
    print("성적 관리 시스템 웹 서버가 시작되었습니다!")
    print("브라우저에서 http://localhost:8080 으로 접속하세요.")
    print("=" * 60)
    app.run(debug=True, host='0.0.0.0', port=8080)

