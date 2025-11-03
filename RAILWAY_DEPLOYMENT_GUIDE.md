# Railway 배포 가이드

Django 백엔드를 Railway에 배포하는 단계별 가이드입니다.

## 사전 준비

### 1. 필요한 계정
- ✅ GitHub 계정
- ✅ Railway 계정 (https://railway.app)
- ✅ Supabase 프로젝트
- ✅ Clerk 프로젝트

### 2. 레포지터리
- ✅ GitHub 레포지터리: `https://github.com/LovelyPaul/academy_dashboard.git`
- ✅ Branch: `main`

## 배포 파일 구성

다음 파일들이 이미 준비되어 있습니다:

### Backend 디렉토리
```
backend/
├── Procfile              # Railway 실행 명령
├── runtime.txt           # Python 버전 지정
├── railway.json          # Railway 설정
├── requirements.txt      # Python 패키지 (gunicorn, whitenoise 포함)
└── config/settings/
    ├── base.py          # 기본 설정
    ├── dev.py           # 개발 환경 설정
    └── prod.py          # 프로덕션 설정 (Railway용)
```

---

## Railway 배포 단계

### Step 1: Railway 프로젝트 생성

1. **Railway 로그인**
   - https://railway.app 접속
   - GitHub으로 로그인

2. **새 프로젝트 생성**
   - Dashboard에서 **"New Project"** 클릭
   - **"Deploy from GitHub repo"** 선택

3. **레포지터리 선택**
   - `LovelyPaul/academy_dashboard` 선택
   - **"Deploy Now"** 클릭

### Step 2: 환경 변수 설정

Railway Dashboard에서 **"Variables"** 탭으로 이동하여 다음 환경 변수들을 설정합니다:

#### Django 설정
```bash
# Django
DJANGO_SETTINGS_MODULE=config.settings.prod
SECRET_KEY=your-secret-key-here-change-this-in-production
DEBUG=False
ALLOWED_HOSTS=*.railway.app,your-frontend-domain.com
```

#### 데이터베이스 (Supabase)
```bash
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=your-supabase-db-password
DB_HOST=db.uzsexjgqglhwsbmrmymu.supabase.co
DB_PORT=5432
```

#### Clerk 인증
```bash
CLERK_SECRET_KEY=sk_live_your_clerk_secret_key
CLERK_WEBHOOK_SECRET=whsec_your_webhook_secret
```

#### CORS 설정
```bash
CORS_ALLOWED_ORIGINS=https://your-frontend-domain.com,https://your-frontend.vercel.app
```

**중요**:
- `SECRET_KEY`는 Django의 `python manage.py shell -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"` 명령으로 생성
- Supabase 비밀번호는 Supabase Dashboard에서 확인
- Clerk 키는 Clerk Dashboard에서 확인

### Step 3: Railway 빌드 및 배포

1. **자동 배포**
   - GitHub에 push하면 자동으로 Railway가 감지
   - Build 로그 확인: Railway Dashboard → **"Deployments"** 탭

2. **배포 확인**
   - 성공 시 `https://your-app.railway.app` 형식의 URL 생성
   - **"Settings"** → **"Domains"**에서 URL 확인

3. **헬스 체크**
   ```bash
   curl https://your-app.railway.app/api/health/
   ```

### Step 4: 데이터베이스 마이그레이션

Railway에서 자동으로 마이그레이션이 실행됩니다 (`Procfile`의 `release` 명령).

수동으로 확인하려면:
```bash
# Railway CLI 설치 (선택사항)
npm install -g @railway/cli

# Railway 로그인
railway login

# 프로젝트 연결
railway link

# 마이그레이션 실행
railway run python manage.py migrate
```

### Step 5: Static 파일 수집

Railway는 배포 시 자동으로 static 파일을 수집합니다.

수동 확인:
```bash
railway run python manage.py collectstatic --noinput
```

---

## Clerk Webhook 설정 (Railway 배포 후)

### 1. Railway URL 확인
- Railway Dashboard에서 배포 URL 복사
- 예: `https://your-app.railway.app`

### 2. Clerk Dashboard 설정

1. **Clerk Dashboard** 접속: https://dashboard.clerk.com
2. 프로젝트 선택
3. **"Webhooks"** 메뉴 클릭
4. **"+ Add Endpoint"** 클릭

### 3. Webhook Endpoint 추가
```
Endpoint URL: https://your-app.railway.app/api/webhooks/clerk/
```

### 4. 이벤트 선택
- ✅ `user.created`
- ✅ `user.updated`
- ✅ `user.deleted`

### 5. Signing Secret 복사
- Webhook 생성 후 **"Signing Secret"** 표시됨
- 이 값을 Railway 환경 변수에 추가:
  ```bash
  CLERK_WEBHOOK_SECRET=whsec_xxxxxxxxxxxxx
  ```

### 6. 테스트
1. Clerk Dashboard → Webhooks → 생성한 endpoint 클릭
2. **"Testing"** 탭에서 **"Send Example"** 클릭
3. Railway 로그에서 성공 확인:
   ```
   [INFO] User created from webhook: test@example.com
   ```

---

## 프론트엔드 설정 업데이트

Railway 배포 후 프론트엔드 환경 변수를 업데이트해야 합니다.

### Vercel 환경 변수
```bash
NEXT_PUBLIC_API_URL=https://your-app.railway.app
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=pk_live_your_clerk_key
CLERK_SECRET_KEY=sk_live_your_clerk_secret_key
```

### Local 개발 환경 (.env.local)
```bash
# Railway API (프로덕션)
NEXT_PUBLIC_API_URL=https://your-app.railway.app

# 또는 로컬 개발
NEXT_PUBLIC_API_URL=http://localhost:8000
```

---

## 배포 확인 및 테스트

### 1. API 엔드포인트 테스트
```bash
# Health check
curl https://your-app.railway.app/api/health/

# Students API (인증 필요)
curl https://your-app.railway.app/api/dashboard/students/analytics/ \
  -H "Authorization: Bearer YOUR_CLERK_JWT_TOKEN"
```

### 2. 로그 확인
Railway Dashboard → **"Logs"** 탭에서 실시간 로그 확인

### 3. 데이터베이스 연결 확인
```bash
railway run python manage.py shell

>>> from django.db import connection
>>> connection.ensure_connection()
>>> print("Database connected!")
```

---

## 트러블슈팅

### 문제 1: 500 Internal Server Error

**원인**: 환경 변수 누락 또는 잘못된 설정

**해결**:
1. Railway Dashboard → **"Variables"** 탭 확인
2. 모든 필수 환경 변수가 설정되었는지 확인
3. 로그에서 에러 메시지 확인

### 문제 2: Database Connection Error

**원인**: Supabase 연결 정보 오류

**해결**:
1. Supabase Dashboard → Settings → Database에서 연결 정보 확인
2. `DB_HOST`, `DB_PASSWORD` 다시 확인
3. Supabase에서 Railway IP가 허용되었는지 확인 (Supabase는 기본적으로 모든 IP 허용)

### 문제 3: Static Files 404

**원인**: WhiteNoise 설정 문제

**해결**:
1. `requirements.txt`에 `whitenoise` 포함 확인
2. `config/settings/prod.py`에 WhiteNoise middleware 설정 확인
3. Static 파일 수집:
   ```bash
   railway run python manage.py collectstatic --noinput
   ```

### 문제 4: CORS Error

**원인**: 프론트엔드 도메인이 CORS에 허용되지 않음

**해결**:
Railway 환경 변수에서 `CORS_ALLOWED_ORIGINS` 업데이트:
```bash
CORS_ALLOWED_ORIGINS=https://your-frontend.vercel.app,https://your-custom-domain.com
```

---

## 모니터링 및 유지보수

### 1. 배포 로그 확인
```bash
# Railway CLI 사용
railway logs
```

### 2. 데이터베이스 백업
Supabase는 자동 백업을 제공합니다:
- Supabase Dashboard → Settings → Backups

### 3. 배포 롤백
Railway Dashboard → Deployments → 이전 배포 선택 → **"Redeploy"**

---

## 다음 단계

배포 완료 후:

1. ✅ **Clerk Webhook 설정** (위 섹션 참조)
2. ✅ **프론트엔드 환경 변수 업데이트**
3. ✅ **커스텀 도메인 설정** (선택사항)
   - Railway Dashboard → Settings → Domains
4. ✅ **SSL 인증서 확인** (Railway가 자동 제공)
5. ✅ **모니터링 설정** (Railway 대시보드 또는 외부 서비스)

---

## 참고 자료

- [Railway Documentation](https://docs.railway.app/)
- [Django Deployment Checklist](https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/)
- [Supabase Documentation](https://supabase.com/docs)
- [Clerk Documentation](https://clerk.com/docs)

---

**작성일**: 2025년 11월 3일
**최종 업데이트**: Railway 배포 설정 완료
