# 보안 개선 사항

## 🔒 적용된 보안 강화

### 1. **경로 순회 공격 (Path Traversal) 방지**

**문제점:**
```python
# 위험한 코드
file_path = os.path.join(folder, filename)  
# filename이 "../../../etc/passwd" 같은 경우 위험
```

**해결:**
```python
def is_safe_path(base_path, target_path):
    """경로 순회 공격 방지"""
    base = os.path.abspath(base_path)
    target = os.path.abspath(target_path)
    return target.startswith(base)

# 모든 파일 접근 시 검증
if not is_safe_path(base_folder, file_path):
    abort(403)
```

---

### 2. **SECRET_KEY 하드코딩 제거**

**문제점:**
```python
# 위험한 코드
app.config['SECRET_KEY'] = 'your-secret-key-here'
```

**해결:**
```python
# 환경 변수 사용 또는 랜덤 생성
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or secrets.token_hex(32)
```

---

### 3. **파일명 검증 강화**

**문제점:**
```python
# 부족한 검증
filename = secure_filename(file.filename)
```

**해결:**
```python
def sanitize_filename(filename):
    """파일명 안전성 검증"""
    filename = secure_filename(filename)
    name, ext = os.path.splitext(filename)
    if len(name) > 100:  # 길이 제한
        name = name[:100]
    return f"{name}{ext}"
```

---

### 4. **화이트리스트 방식 파일 다운로드**

**문제점:**
```python
# 위험한 코드
@app.route('/download-sample/<filename>')
def download_sample(filename):
    file_path = os.path.join(folder, filename)  # 모든 파일 접근 가능
```

**해결:**
```python
# 허용된 파일만 다운로드
allowed_samples = {
    'sample_grade_cutoff.csv',
    'sample_korean.csv',
    # ...
}

if filename not in allowed_samples:
    abort(403)
```

---

### 5. **에러 정보 노출 방지**

**문제점:**
```python
# 위험한 코드
except Exception as e:
    return jsonify({'error': str(e)}), 500  # 상세한 에러 노출
```

**해결:**
```python
# 안전한 처리
except Exception as e:
    print(f"[ERROR] 내부 오류: {str(e)}")  # 로그에만 기록
    return jsonify({'error': '처리 중 오류가 발생했습니다.'}), 500  # 일반 메시지
```

---

### 6. **DoS 공격 방지**

**문제점:**
```python
# 위험한 코드
for idx, row in processed_data.iterrows():  # 무제한 처리
    generate_pdf(row)
```

**해결:**
```python
# 처리 개수 제한
if len(processed_data) > 1000:
    return jsonify({'error': '한 번에 최대 1000명까지만 처리할 수 있습니다.'}), 400
```

---

### 7. **동시성 문제 해결**

**문제점:**
```python
# 위험한 코드
data_processor = DataProcessor()  # 전역 변수, 동시 접속 시 충돌
```

**해결:**
```python
# 세션별 데이터 프로세서
data_processors = {}

def get_session_data_processor():
    session_id = request.remote_addr
    if session_id not in data_processors:
        data_processors[session_id] = DataProcessor()
    return data_processors[session_id]
```

---

### 8. **입력 검증 강화**

**문제점:**
```python
# 위험한 코드
pdf_title = data.get('pdf_title')  # 무제한 길이
```

**해결:**
```python
# 길이 제한
pdf_title = data.get('pdf_title', '모의고사 성적표')[:100]
student_name = str(student_name)[:50]
```

---

## 🛡️ 추가 보안 권장사항

### 1. **HTTPS 사용**
```bash
# 프로덕션 환경에서는 반드시 HTTPS 사용
gunicorn --certfile=cert.pem --keyfile=key.pem app:app
```

### 2. **Rate Limiting 추가**
```python
from flask_limiter import Limiter

limiter = Limiter(
    app,
    key_func=lambda: request.remote_addr,
    default_limits=["200 per day", "50 per hour"]
)
```

### 3. **CORS 설정**
```python
from flask_cors import CORS

CORS(app, resources={
    r"/api/*": {
        "origins": ["https://yourdomain.com"]
    }
})
```

### 4. **파일 업로드 스캔**
```python
# 바이러스 스캔 (ClamAV 등)
import pyclamd

cd = pyclamd.ClamdUnixSocket()
if cd.scan_file(filepath):
    # 위험한 파일
    os.remove(filepath)
```

### 5. **환경 변수 사용**
```bash
# .env 파일
SECRET_KEY=your-secret-key-here
DATABASE_URL=postgresql://...
ALLOWED_HOSTS=yourdomain.com
```

---

## 📋 보안 체크리스트

- [x] 경로 순회 공격 방지
- [x] SECRET_KEY 안전하게 관리
- [x] 파일명 검증
- [x] 화이트리스트 방식 접근 제어
- [x] 에러 정보 노출 방지
- [x] DoS 공격 방지 (처리량 제한)
- [x] 동시성 문제 해결
- [x] 입력 검증 강화
- [ ] HTTPS 설정 (프로덕션)
- [ ] Rate Limiting (프로덕션)
- [ ] CORS 설정 (프로덕션)
- [ ] 파일 스캔 (옵션)

---

## 🔐 프로덕션 배포 시 추가 조치

1. **디버그 모드 비활성화**
   ```python
   app.run(debug=False)
   ```

2. **로깅 설정**
   ```python
   import logging
   logging.basicConfig(
       filename='app.log',
       level=logging.INFO,
       format='%(asctime)s %(levelname)s: %(message)s'
   )
   ```

3. **데이터베이스 사용**
   - 파일 기반 대신 데이터베이스 사용
   - 민감한 데이터 암호화

4. **정기 보안 업데이트**
   ```bash
   pip list --outdated
   pip install --upgrade <package>
   ```

---

## 📞 보안 문제 발견 시

보안 취약점을 발견하신 경우:
1. 즉시 관리자에게 연락
2. 상세한 내용과 재현 방법 전달
3. 공개하지 말 것

---

**마지막 업데이트**: 2025-11-03
**보안 등급**: ⭐⭐⭐⭐☆ (4/5)


