# Railway 백엔드 배포 - 단계별 가이드

Django 백엔드를 Railway에 배포하는 실행 가이드입니다.

---

## Step 1: Railway 프로젝트 생성

### 1-1. Railway 로그인
- https://railway.app 접속
- **GitHub 계정으로 로그인**

### 1-2. 새 프로젝트 생성
1. Dashboard에서 **"New Project"** 클릭
2. **"Deploy from GitHub repo"** 선택
3. `LovelyPaul/academy_dashboard` 레포지터리 선택
4. **"Deploy Now"** 클릭

Railway가 자동으로 레포지터리를 감지하고 빌드를 시작합니다.

---

## Step 2: 환경 변수 설정

Railway Dashboard에서 배포된 프로젝트 선택 → **"Variables"** 탭으로 이동

### 복사해서 붙여넣기 (한 줄씩 추가)

#### Django 기본 설정
```
DJANGO_SETTINGS_MODULE=config.settings.prod
```

```
SECRET_KEY=jw+@l07gu*e$hl64g0d!s=na(782+uj9$tf1k)yyy&\8v=pw)f
```

```
DEBUG=False
```

```
ALLOWED_HOSTS=*.railway.app
```

#### 데이터베이스 (Supabase)
**⚠️ 주의: 아래 값들은 실제 Supabase 값으로 변경하세요**

```
DB_NAME=postgres
```

```
DB_USER=postgres
```

```
DB_PASSWORD=YOUR_SUPABASE_PASSWORD_HERE
```

```
DB_HOST=db.uzsexjgqglhwsbmrmymu.supabase.co
```

```
DB_PORT=5432
```

#### Clerk 인증
**⚠️ 주의: 실제 Clerk 키로 변경하세요**

```
CLERK_SECRET_KEY=YOUR_CLERK_SECRET_KEY_HERE
```

#### CORS 설정 (임시 - 전체 허용)
```
CORS_ALLOW_ALL_ORIGINS=True
```

**나중에 프론트엔드 배포 후 업데이트할 항목:**
- `ALLOWED_HOSTS`: 프론트엔드 도메인 추가
- `CORS_ALLOWED_ORIGINS`: 특정 프론트엔드 URL로 변경
- `CLERK_WEBHOOK_SECRET`: Clerk webhook 설정 후 추가

---

## Step 3: 배포 확인

### 3-1. 빌드 로그 확인
Railway Dashboard → **"Deployments"** 탭
- 빌드 진행 상황 실시간 확인
- 에러 발생 시 로그에서 원인 확인

### 3-2. 배포 URL 확인
Railway Dashboard → **"Settings"** → **"Domains"**
- 자동 생성된 URL 확인: `https://your-app.railway.app`
- 이 URL을 복사해두세요 (Clerk webhook 설정에 필요)

### 3-3. Health Check
터미널에서 배포 확인:
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

## Step 4: Supabase 연결 정보 확인

### Supabase Dashboard에서 확인
1. https://supabase.com/dashboard 접속
2. 프로젝트 선택
3. **Settings** → **Database**
4. **Connection String** 섹션에서 다음 정보 확인:
   - Host: `db.uzsexjgqglhwsbmrmymu.supabase.co`
   - Database name: `postgres`
   - Port: `5432`
   - User: `postgres`
   - Password: **"Show password"** 클릭하여 복사

Railway Variables에 정확히 입력하세요.

---

## Step 5: Clerk 키 확인

### Clerk Dashboard에서 확인
1. https://dashboard.clerk.com 접속
2. 프로젝트 선택
3. **API Keys** 메뉴
4. **Secret Keys** 섹션에서 `CLERK_SECRET_KEY` 복사
   - 형식: `sk_live_...` 또는 `sk_test_...`

Railway Variables에 입력하세요.

---

## Step 6: 데이터베이스 마이그레이션 확인

Railway는 `Procfile`의 `release` 명령으로 자동 마이그레이션을 실행합니다.

### 수동 확인 (선택사항)
Railway CLI 설치:
```bash
npm install -g @railway/cli
```

Railway 로그인 및 프로젝트 연결:
```bash
railway login
railway link
```

마이그레이션 상태 확인:
```bash
railway run python manage.py showmigrations
```

---

## Step 7: Clerk Webhook 설정

### 7-1. Railway 배포 URL 확인
Railway Dashboard → Settings → Domains에서 URL 복사
- 예: `https://academy-dashboard-production.railway.app`

### 7-2. Clerk Dashboard 설정
1. Clerk Dashboard → **Webhooks** 메뉴
2. **"+ Add Endpoint"** 클릭
3. **Endpoint URL** 입력:
   ```
   https://your-app.railway.app/api/webhooks/clerk/
   ```
   (실제 Railway URL로 변경)

4. **Events to listen** 선택:
   - ✅ `user.created`
   - ✅ `user.updated`
   - ✅ `user.deleted`

5. **Create** 클릭

### 7-3. Signing Secret 복사
Webhook 생성 후 **"Signing Secret"** 표시됨
- 형식: `whsec_...`
- 이 값을 복사하세요

### 7-4. Railway 환경 변수 추가
Railway Dashboard → Variables 탭에서 추가:
```
CLERK_WEBHOOK_SECRET=whsec_xxxxxxxxxxxxx
```

### 7-5. 테스트
Clerk Dashboard → Webhooks → 생성한 endpoint 클릭
- **"Testing"** 탭에서 **"Send Example"** 클릭
- Railway **"Logs"** 탭에서 성공 메시지 확인:
  ```
  [INFO] User created from webhook: test@example.com
  ```

---

## Step 8: API 테스트

### Health Check
```bash
curl https://your-app.railway.app/api/health/
```

### Students API (인증 필요)
```bash
curl https://your-app.railway.app/api/dashboard/students/analytics/ \
  -H "Authorization: Bearer YOUR_CLERK_JWT_TOKEN"
```

### Upload API (인증 필요)
```bash
curl -X POST https://your-app.railway.app/api/dashboard/upload/upload/ \
  -H "Authorization: Bearer YOUR_CLERK_JWT_TOKEN" \
  -F "file=@test_student.csv"
```

---

## 트러블슈팅

### 문제 1: 500 Internal Server Error

**로그 확인:**
Railway Dashboard → **"Logs"** 탭

**일반적인 원인:**
1. 환경 변수 누락 또는 오타
2. Supabase 비밀번호 불일치
3. Clerk 키 오류

**해결:**
- Variables 탭에서 모든 환경 변수 재확인
- 특히 `DB_PASSWORD`, `CLERK_SECRET_KEY` 정확성 확인

### 문제 2: Database Connection Error

**에러 메시지:**
```
connection to server at "db.xxx.supabase.co", port 5432 failed
```

**해결:**
1. Supabase Dashboard에서 데이터베이스 연결 정보 재확인
2. `DB_HOST`가 정확한지 확인
3. `DB_PASSWORD` 공백 없이 정확히 입력했는지 확인

### 문제 3: Static Files 404

**원인:** WhiteNoise 설정 문제

**해결:**
```bash
railway run python manage.py collectstatic --noinput
```

### 문제 4: Clerk Webhook 실패

**로그 확인:**
Railway Logs에서 webhook 요청 확인

**일반적인 원인:**
1. Webhook URL 오타
2. `CLERK_WEBHOOK_SECRET` 불일치

**해결:**
- Clerk Dashboard에서 Webhook URL 재확인
- Signing Secret 다시 복사하여 Railway Variables에 업데이트

---

## 배포 완료 체크리스트

- [ ] Railway 프로젝트 생성 및 GitHub 연동
- [ ] 모든 환경 변수 설정 완료
- [ ] 배포 성공 및 URL 확인
- [ ] Health check API 정상 응답
- [ ] Supabase 데이터베이스 연결 확인
- [ ] Clerk webhook 설정 및 테스트 성공
- [ ] API 엔드포인트 테스트 완료

---

## 다음 단계

백엔드 배포 완료 후:

1. **프론트엔드 Vercel 배포**
   - 프론트엔드 환경 변수 설정:
     ```
     NEXT_PUBLIC_API_URL=https://your-app.railway.app
     NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=pk_live_xxx
     ```

2. **Railway CORS 설정 업데이트**
   - 프론트엔드 URL 확인 후:
     ```
     CORS_ALLOWED_ORIGINS=https://your-frontend.vercel.app
     ALLOWED_HOSTS=*.railway.app,your-frontend.vercel.app
     ```
   - `CORS_ALLOW_ALL_ORIGINS` 환경 변수 삭제

3. **커스텀 도메인 설정** (선택사항)
   - Railway Dashboard → Settings → Domains

---

## 중요 링크

- Railway Dashboard: https://railway.app/dashboard
- Supabase Dashboard: https://supabase.com/dashboard
- Clerk Dashboard: https://dashboard.clerk.com
- GitHub Repository: https://github.com/LovelyPaul/academy_dashboard

---

**작성일:** 2025년 11월 3일
**목적:** Railway 백엔드 단독 배포 가이드
