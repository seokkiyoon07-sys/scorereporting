# 프로젝트 구조 정리 가이드

## 현재 상황

현재 폴더에 두 가지 버전의 성적 관리 시스템이 있습니다:

1. **Python GUI 버전** (기존)
   - Tkinter 기반 데스크톱 애플리케이션
   - 폴더: `scoring system` (현재 폴더)

2. **웹 버전** (새로 클론함)
   - Flask 기반 웹 애플리케이션
   - Railway 배포 가능
   - 폴더: `scorereporting` (하위 폴더)

## 권장 구조 정리 방법

### 옵션 1: 상위 폴더로 이동 (권장)

```
C:\code\
├── scoring-system-desktop\    # Python GUI 버전
│   ├── main.py
│   ├── data_processor.py
│   └── ...
│
└── scoring-system-web\         # 웹 버전
    ├── app.py
    ├── templates/
    └── ...
```

### 옵션 2: 현재 위치 유지, 명확한 네이밍

```
C:\code\scoring system\
├── [기존 파일들 - Python GUI 버전]
│   ├── main.py
│   └── ...
│
└── web-version\               # 웹 버전을 별도 폴더로 이동
    ├── app.py
    ├── templates/
    └── ...
```

### 옵션 3: 완전 분리

각각 독립적인 프로젝트로 완전히 분리:
- Python GUI: `C:\code\scoring-system-desktop`
- 웹 버전: `C:\code\scoring-system-web`

## 각 버전의 특징

### Python GUI 버전 (기존)
- ✅ 로컬 실행 가능 (설치 불필요)
- ✅ 오프라인 사용 가능
- ✅ Windows 실행 파일 (.exe) 제공
- ✅ 사용자 친화적인 GUI

**사용 시나리오**: 
- 학원 내부에서 사용
- 인터넷 연결 없이 사용
- 단일 컴퓨터에서 실행

### 웹 버전 (새로 클론)
- ✅ 웹 브라우저로 접근 가능
- ✅ 여러 사용자가 동시 접근 가능
- ✅ Railway/Heroku 등 클라우드 배포 가능
- ✅ 모바일에서도 접근 가능

**사용 시나리오**:
- 인터넷이 있는 환경
- 여러 사용자가 동시에 사용
- 클라우드에 배포하여 어디서나 접근

## 다음 단계

원하시는 옵션을 선택하시면 해당 구조로 정리해드리겠습니다.

