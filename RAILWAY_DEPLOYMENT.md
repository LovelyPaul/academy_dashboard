# Railway 백엔드 배포 가이드

## 배포 전략

**백엔드(Django)**: Railway
**프론트엔드(React)**: Vercel 또는 Netlify (별도 배포)

## 문제 해결

### 원래 에러 원인
```
/bin/bash: line 1: pip: command not found
```

**원인**:
- Python 베이스 이미지 없이 pip 명령 실행 시도
- railway.json에서 NIXPACKS 빌더 사용 시 환경 설정 누락

**해결 방법**:
1. `backend/Dockerfile` 생성 (Python 3.12 베이스 이미지)
2. `backend/railway.json`을 DOCKERFILE 빌더로 변경
3. Railway에서 backend 폴더를 Root Directory로 설정

## 배포 단계

### 1. 환경 변수 설정 (Railway Dashboard)

Railway 프로젝트 설정에서 다음 환경 변수를 추가하세요:

```bash
# Django 설정
DJANGO_SECRET_KEY=<your-secret-key>
DEBUG=False
ALLOWED_HOSTS=*.railway.app,yourdomain.com

# 데이터베이스 (Railway PostgreSQL)
DATABASE_URL=<railway-postgres-connection-string>

# Supabase (이미 사용 중인 경우)
SUPABASE_URL=<your-supabase-url>
SUPABASE_KEY=<your-supabase-key>
SUPABASE_SERVICE_KEY=<your-supabase-service-key>

# Clerk 인증
CLERK_SECRET_KEY=<your-clerk-secret-key>
CLERK_PUBLISHABLE_KEY=<your-clerk-publishable-key>
CLERK_WEBHOOK_SECRET=<your-clerk-webhook-secret>

# CORS 설정
CORS_ALLOWED_ORIGINS=https://yourfrontend.vercel.app,https://yourdomain.com

# 프론트엔드 URL (선택사항)
FRONTEND_URL=https://yourfrontend.vercel.app
```

### 2. Railway 프로젝트 설정

**중요**: Railway 대시보드에서 Root Directory 설정

1. Railway 대시보드 → 프로젝트 선택
2. **"Settings"** 탭 클릭
3. **"Root Directory"** 설정을 `backend`로 변경
4. **"Deploy"** 버튼 클릭

### 3. Git Push로 배포

```bash
# 변경사항 커밋
git add backend/Dockerfile backend/.dockerignore backend/railway.json
git commit -m "feat: Railway 백엔드 전용 배포 설정"

# Railway에 푸시 (Railway가 자동으로 배포 시작)
git push origin main
```

### 3. Railway CLI 사용 (선택사항)

```bash
# Railway CLI 설치
npm install -g @railway/cli

# 로그인
railway login

# 프로젝트 연결
railway link

# 로컬 환경 변수 동기화
railway variables

# 수동 배포
railway up
```

### 4. 배포 후 확인사항

1. **데이터베이스 마이그레이션**:
   ```bash
   # Railway 대시보드에서 또는 CLI로
   railway run python backend/manage.py migrate
   ```

2. **Superuser 생성**:
   ```bash
   railway run python backend/manage.py createsuperuser
   ```

3. **정적 파일 수집** (이미 Dockerfile에 포함됨):
   ```bash
   python manage.py collectstatic --noinput
   ```

## Dockerfile 구조 설명

### Stage 1: Frontend 빌드
```dockerfile
FROM node:18-alpine AS frontend-build
```
- React 앱을 빌드하여 정적 파일 생성
- 최종 이미지 크기 절약을 위해 멀티스테이지 빌드 사용

### Stage 2: Backend + Frontend 통합
```dockerfile
FROM python:3.12-slim
```
- Django 백엔드와 빌드된 프론트엔드를 하나의 이미지로 결합
- Gunicorn으로 Django 서버 실행

## 트러블슈팅

### 빌드 실패 시

1. **Python 버전 확인**:
   - requirements.txt의 패키지들이 Python 3.12와 호환되는지 확인

2. **Node 버전 확인**:
   - package.json의 engines 필드 확인

3. **메모리 부족**:
   ```json
   // railway.json에 추가
   "build": {
     "builder": "DOCKERFILE",
     "dockerfilePath": "Dockerfile"
   }
   ```

### 런타임 에러

1. **환경 변수 누락**:
   - Railway 대시보드에서 모든 필수 환경 변수 확인

2. **데이터베이스 연결 실패**:
   - DATABASE_URL이 올바르게 설정되었는지 확인
   - PostgreSQL 플러그인이 프로젝트에 연결되어 있는지 확인

3. **CORS 에러**:
   - CORS_ALLOWED_ORIGINS에 프론트엔드 도메인 추가

## 대안: 백엔드만 배포 (권장)

프론트엔드는 Vercel에, 백엔드만 Railway에 배포하는 것이 더 효율적일 수 있습니다.

### backend/Dockerfile (백엔드 전용)
```dockerfile
FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

RUN apt-get update && apt-get install -y postgresql-client && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

RUN python manage.py collectstatic --noinput --clear || true

EXPOSE 8000

CMD ["gunicorn", "config.wsgi", "--bind", "0.0.0.0:8000", "--workers", "2"]
```

### 프론트엔드 배포 (Vercel)
```bash
cd frontend
vercel --prod
```

## 참고 링크

- [Railway 공식 문서](https://docs.railway.app/)
- [Django 배포 체크리스트](https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/)
- [Gunicorn 설정](https://docs.gunicorn.org/en/stable/settings.html)
