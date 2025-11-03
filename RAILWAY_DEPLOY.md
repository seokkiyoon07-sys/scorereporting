# Railway 배포 가이드

## ✅ 배포 준비 완료

Railway에 배포하기 위한 모든 파일이 준비되었습니다!

---

## 📋 **배포 파일 목록**

- ✅ `Procfile` - Railway 실행 명령어
- ✅ `railway.json` - Railway 설정
- ✅ `requirements.txt` - Python 의존성
- ✅ `.gitignore` - Git 제외 파일
- ✅ `app.py` - Flask 애플리케이션 (보안 강화 완료)

---

## 🚀 **Railway 배포 방법**

### **1단계: GitHub에 Push**

```bash
# Git 초기화 (아직 안했다면)
git init

# 모든 파일 추가
git add .

# 커밋
git commit -m "Initial commit - 성적 관리 시스템"

# GitHub 저장소에 Push
git remote add origin https://github.com/your-username/scorereporting.git
git branch -M main
git push -u origin main
```

---

### **2단계: Railway 프로젝트 생성**

1. **Railway 접속**: https://railway.app
2. **"New Project" 클릭**
3. **"Deploy from GitHub repo" 선택**
4. **저장소 선택**: `seokkiyoon07-sys/scorereporting`
5. **자동 배포 시작** ✨

---

### **3단계: 환경 변수 설정 (선택)**

Railway 대시보드에서 환경 변수 추가:

```
SECRET_KEY=your-very-secret-key-here-32-characters-minimum
```

💡 **SECRET_KEY가 없어도 자동 생성되지만, 재시작 시 변경됩니다.**

---

## ⚠️ **주의사항**

### **1. 파일 시스템 제한**

Railway는 **임시 파일 시스템**을 사용합니다:
- ✅ `uploads/` 폴더에 파일 업로드 가능
- ✅ `outputs/` 폴더에 PDF 생성 가능
- ⚠️ **서버 재시작 시 모든 파일 삭제됨**

**해결책:**
- 파일을 바로 다운로드하세요
- 또는 S3/Cloudflare R2 같은 저장소 연동 필요

---

### **2. 메모리 관리**

Railway 무료 플랜:
- **메모리**: 512MB ~ 8GB (사용량 기반)
- **학생 수 제한**: 한 번에 최대 1000명 (코드에 이미 적용됨)

---

### **3. Playwright 브라우저**

Chromium 브라우저가 자동으로 설치됩니다:
- 📦 크기: ~130MB
- ⏱️ 첫 배포 시간: 5-10분

---

### **4. 세션 관리**

현재 IP 기반 세션:
- 동일 IP에서만 데이터 유지
- 서버 재시작 시 세션 초기화

**개선 방법:**
- Redis 세션 저장소 사용 (Railway Add-on)

---

## 💰 **Railway 요금**

### **무료 플랜**
- ✅ $5 크레딧/월
- ✅ 약 500시간 사용 가능
- ✅ Playwright 지원

### **사용량 예상**
```
시간당 사용량: ~$0.01
월 사용량 (24시간 운영): ~$7
권장: Hobby Plan ($5/월 + 사용량)
```

---

## 🔧 **배포 후 확인사항**

### **1. 배포 상태 확인**
```
Railway 대시보드 → Deployments → 로그 확인
```

### **2. 도메인 확인**
```
Railway가 자동으로 생성한 URL 확인
예: https://scorereporting-production.up.railway.app
```

### **3. 기능 테스트**
1. ✅ 메인 페이지 접속
2. ✅ 샘플 파일 다운로드
3. ✅ 파일 업로드
4. ✅ 성적표 생성

---

## 🌐 **커스텀 도메인 설정 (선택)**

Railway에서 자체 도메인 연결:

1. **Railway 대시보드** → **Settings** → **Domains**
2. **Add Custom Domain** 클릭
3. **도메인 입력**: `score.yourdomain.com`
4. **DNS 설정**:
   ```
   CNAME: score.yourdomain.com → your-app.up.railway.app
   ```

---

## 📊 **Railway vs 다른 플랫폼**

| 항목 | Railway | Render | Vercel |
|------|---------|--------|--------|
| **Flask 지원** | ✅ 완벽 | ✅ 완벽 | ⚠️ 제한적 |
| **Playwright** | ✅ 지원 | ✅ 지원 | ❌ 불가 |
| **파일 업로드** | ✅ 임시 | ✅ 임시 | ❌ 불가 |
| **무료 플랜** | $5 크레딧 | 750시간 | Serverless |
| **배포 시간** | 5분 | 10분 | 3분 |
| **추천도** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐☆ | ⭐⭐☆☆☆ |

**✅ Railway가 이 프로젝트에 최적!**

---

## 🔄 **자동 배포 설정**

GitHub에 Push할 때마다 자동 배포:

1. **Railway 대시보드** → **Settings**
2. **Auto Deploy** 활성화
3. **Branch 선택**: `main`

이제 코드를 Push하면 자동으로 배포됩니다! 🎉

---

## 🐛 **문제 해결**

### **배포 실패 시**

1. **로그 확인**
   ```
   Railway Dashboard → Deployments → View Logs
   ```

2. **일반적인 오류**
   - `playwright install` 실패 → railway.json 확인
   - 메모리 부족 → 처리량 줄이기
   - 포트 바인딩 오류 → Procfile 확인

3. **재배포**
   ```bash
   git commit --allow-empty -m "Redeploy"
   git push
   ```

---

## 📞 **배포 후 모니터링**

Railway 대시보드에서 확인:
- 🖥️ CPU 사용량
- 💾 메모리 사용량
- 📊 네트워크 트래픽
- 📜 애플리케이션 로그

---

## ✅ **배포 체크리스트**

- [x] GitHub 저장소 생성
- [x] Railway 계정 생성
- [x] Procfile 준비
- [x] railway.json 준비
- [x] requirements.txt 업데이트
- [x] .gitignore 설정
- [ ] GitHub에 Push
- [ ] Railway 프로젝트 생성
- [ ] 배포 확인
- [ ] 기능 테스트

---

## 🎉 **배포 준비 완료!**

이제 GitHub에 Push하고 Railway에서 배포하면 됩니다!

**예상 배포 시간**: 5-10분  
**예상 월 비용**: $5-10

궁금한 점이 있으면 언제든 질문하세요! 😊


