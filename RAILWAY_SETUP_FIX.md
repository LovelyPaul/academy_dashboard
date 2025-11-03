# Railway 배포 설정 수정 가이드

Railway에서 모노레포를 배포할 때 **Root Directory 설정이 필수**입니다.

---

## 문제 증상

```
⚠ Script start.sh not found
✖ Railpack could not determine how to build the app.
```

또는

```
/bin/bash: line 1: pip: command not found
```

---

## 해결 방법: Railway 웹 대시보드에서 Root Directory 설정

### 1단계: Railway Dashboard 접속
https://railway.app/project/3b540bed-abd3-439f-8652-c18f0fd695ad

### 2단계: 서비스 설정

1. 배포된 서비스 클릭 (현재 서비스 이름 확인)
2. **Settings** 탭 클릭
3. 아래로 스크롤하여 **Source** 또는 **Service** 섹션 찾기

### 3단계: Root Directory 설정

**중요**: 다음 설정을 정확히 입력하세요

```
Root Directory: backend
```

또는

```
Root Directory: /backend
```

> **주의**: 앞에 슬래시(/)가 있어도 되고 없어도 됩니다. Railway가 자동으로 처리합니다.

### 4단계: Watch Paths 설정 (선택사항)

```
Watch Paths: backend/**
```

이렇게 설정하면 `backend/` 디렉토리의 변경사항만 감지하여 재배포합니다.

### 5단계: 저장 및 재배포

1. 설정 저장 (보통 자동 저장됨)
2. **Deployments** 탭으로 이동
3. 자동으로 재배포 시작됨
4. 또는 **"Redeploy"** 버튼 클릭

---

## 설정 확인

Railway가 올바르게 인식하면:

### 빌드 로그 예시
```
✓ Detecting runtime: Python 3.9.6
✓ Installing dependencies from requirements.txt
✓ Installing: Django==4.2.7
✓ Installing: djangorestframework==3.14.0
✓ Installing: gunicorn==21.2.0
✓ Build completed successfully
```

### 배포 로그 예시
```
✓ Starting application
✓ Running release command: python manage.py migrate --noinput
✓ Starting web server: gunicorn config.wsgi --bind 0.0.0.0:$PORT
✓ Health check passed: /api/health/
```

---

## 스크린샷 가이드

Railway Settings 화면에서 찾아야 할 섹션:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Settings
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  Service Settings
    Service Name: [입력된 이름]

  Source
    Repository: LovelyPaul/academy_dashboard
    Branch: main
    Root Directory: [backend 입력]     ← 여기!
    Watch Paths: [backend/** 입력]     ← 선택사항

  Build
    Builder: NIXPACKS (자동 감지)
    Build Command: (비워두기)

  Deploy
    Start Command: (비워두기 - Procfile 사용)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Root Directory가 보이지 않는 경우

### 방법 1: 서비스 재생성
1. 현재 서비스 삭제
2. **"+ New Service"** 클릭
3. **"GitHub Repo"** 선택
4. 레포지터리 선택 후
5. **"Configure"** 클릭
6. Root Directory 입력: `backend`

### 방법 2: nixpacks.toml 파일 사용

`backend/nixpacks.toml` 파일이 이미 존재하면 Railway가 자동으로 인식합니다.

현재 `backend/railway.json`이 있으므로 Railway가 자동으로 설정을 읽어야 합니다.

---

## 환경 변수 설정 (Root Directory 설정 후)

Root Directory를 `backend`로 설정한 후:

Railway Dashboard → **Variables** 탭:

```bash
# Django
DJANGO_SETTINGS_MODULE=config.settings.prod
SECRET_KEY=jw+@l07gu*e$hl64g0d!s=na(782+uj9$tf1k)yyy&\8v=pw)f
DEBUG=False
ALLOWED_HOSTS=*.railway.app

# Database (Supabase - 실제 값으로 변경)
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=YOUR_SUPABASE_PASSWORD
DB_HOST=db.uzsexjgqglhwsbmrmymu.supabase.co
DB_PORT=5432

# Clerk (실제 값으로 변경)
CLERK_SECRET_KEY=YOUR_CLERK_SECRET_KEY

# CORS (임시)
CORS_ALLOW_ALL_ORIGINS=True
```

---

## 배포 성공 확인

### 1. Deployments 탭
- Status: **SUCCESS** (녹색)
- Build Time: 약 2-3분
- 에러 없이 완료

### 2. Settings → Domains
- URL이 생성됨: `https://xxxx.railway.app`

### 3. Health Check 테스트
```bash
curl https://your-app.railway.app/api/health/
```

예상 응답:
```json
{
  "status": "healthy",
  "database": "connected"
}
```

---

## 여전히 실패하는 경우

### 확인 사항

1. **Root Directory 정확성**
   - `backend` (슬래시 없이)
   - 또는 `/backend` (슬래시 포함)
   - 대소문자 정확히 일치

2. **backend/ 디렉토리 내용 확인**
   ```
   backend/
   ├── Procfile             ✓
   ├── railway.json         ✓
   ├── runtime.txt          ✓
   ├── requirements.txt     ✓
   └── manage.py            ✓
   ```

3. **GitHub 최신 코드 확인**
   - 최신 커밋이 push되었는지 확인
   - Railway가 올바른 브랜치를 보고 있는지 확인

4. **환경 변수 누락 확인**
   - 최소한 `DJANGO_SETTINGS_MODULE` 필요
   - `DB_PASSWORD`, `CLERK_SECRET_KEY` 필수

---

## Railway Settings UI 위치

Railway Dashboard에서:

```
왼쪽 사이드바
  ├─ Overview
  ├─ Deployments
  ├─ Metrics
  ├─ Variables      ← 환경 변수 설정
  ├─ Settings       ← Root Directory 설정
  └─ Logs
```

**Settings** 탭을 클릭하면 **Source** 섹션에서 **Root Directory**를 찾을 수 있습니다.

---

## 요약

1. ✅ Railway Dashboard 접속
2. ✅ Settings → Source → Root Directory: `backend`
3. ✅ 저장 및 재배포 대기
4. ✅ Variables 탭에서 환경 변수 설정
5. ✅ Deployments 탭에서 성공 확인
6. ✅ Health check URL 테스트

---

**작성일:** 2025년 11월 3일
**목적:** Railway Root Directory 설정 가이드
