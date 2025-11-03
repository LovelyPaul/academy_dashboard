# Railway 전체 배포 가이드 (프론트엔드 + 백엔드)

하나의 Railway 프로젝트에서 프론트엔드와 백엔드를 모두 배포하는 가이드입니다.

---

## 배포 구조

```
Railway Project: academy-dashboard
├── Service 1: Backend (Django)
│   ├── Root Directory: /backend
│   └── URL: https://backend-production.railway.app
└── Service 2: Frontend (React)
    ├── Root Directory: /frontend
    └── URL: https://frontend-production.railway.app
```

---

## Step 1: Railway 프로젝트 생성

### 1-1. Railway 로그인
1. https://railway.app 접속
2. **GitHub 계정으로 로그인**

### 1-2. 새 프로젝트 생성
1. Dashboard에서 **"New Project"** 클릭
2. **"Deploy from GitHub repo"** 선택
3. `LovelyPaul/academy_dashboard` 레포지터리 선택
4. **"Deploy Now"** 클릭

Railway가 자동으로 첫 번째 서비스를 생성합니다.

---

## Step 2: 백엔드 서비스 설정

### 2-1. 서비스 이름 변경
1. 생성된 서비스 클릭
2. **Settings** → **Service Name**을 `backend`로 변경

### 2-2. Root Directory 설정
1. **Settings** → **Build** 섹션
2. **Root Directory**: `/backend` 입력
3. **Save** 클릭

### 2-3. 백엔드 환경 변수 설정
**Variables** 탭에서 다음 환경 변수 추가:

#### Django 설정
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
**⚠️ 실제 Supabase 값으로 변경하세요**
```
DB_NAME=postgres
```
```
DB_USER=postgres
```
```
DB_PASSWORD=YOUR_SUPABASE_PASSWORD
```
```
DB_HOST=db.uzsexjgqglhwsbmrmymu.supabase.co
```
```
DB_PORT=5432
```

#### Clerk 인증
**⚠️ 실제 Clerk 키로 변경하세요**
```
CLERK_SECRET_KEY=YOUR_CLERK_SECRET_KEY
```

#### CORS 설정 (임시)
```
CORS_ALLOW_ALL_ORIGINS=True
```

### 2-4. 백엔드 배포 확인
1. **Deployments** 탭에서 빌드 진행 확인
2. 성공 후 **Settings** → **Domains**에서 URL 확인
3. 백엔드 URL 복사 (예: `https://backend-production.railway.app`)

### 2-5. Health Check
```bash
curl https://backend-production.railway.app/api/health/
```

---

## Step 3: 프론트엔드 서비스 추가

### 3-1. 새 서비스 생성
1. Railway 프로젝트 대시보드로 돌아가기
2. **"+ New"** 버튼 클릭
3. **"GitHub Repo"** 선택
4. 같은 레포지터리 `LovelyPaul/academy_dashboard` 선택

### 3-2. 서비스 이름 변경
1. 새 서비스 클릭
2. **Settings** → **Service Name**을 `frontend`로 변경

### 3-3. Root Directory 설정
1. **Settings** → **Build** 섹션
2. **Root Directory**: `/frontend` 입력
3. **Save** 클릭

### 3-4. 프론트엔드 환경 변수 설정
**Variables** 탭에서 다음 환경 변수 추가:

#### API 연결
**⚠️ Step 2-4에서 복사한 백엔드 URL 사용**
```
REACT_APP_API_URL=https://backend-production.railway.app
```

#### Clerk 공개 키
**⚠️ 실제 Clerk 공개 키로 변경하세요**
```
REACT_APP_CLERK_PUBLISHABLE_KEY=YOUR_CLERK_PUBLISHABLE_KEY
```

#### 빌드 최적화
```
GENERATE_SOURCEMAP=false
```

### 3-5. 프론트엔드 배포 확인
1. **Deployments** 탭에서 빌드 진행 확인
2. 성공 후 **Settings** → **Domains**에서 URL 확인
3. 프론트엔드 URL 복사 (예: `https://frontend-production.railway.app`)

---

## Step 4: 백엔드 CORS 업데이트

프론트엔드 URL을 얻었으므로 백엔드 CORS를 업데이트합니다.

### 4-1. 백엔드 서비스로 이동
Railway 프로젝트 → **backend** 서비스 클릭

### 4-2. 환경 변수 업데이트
**Variables** 탭에서:

1. `CORS_ALLOW_ALL_ORIGINS` **삭제**
2. 다음 환경 변수 **추가**:

```
CORS_ALLOWED_ORIGINS=https://frontend-production.railway.app
```

```
ALLOWED_HOSTS=*.railway.app,frontend-production.railway.app
```

**⚠️ 실제 프론트엔드 URL로 변경하세요**

### 4-3. 재배포
환경 변수 변경 후 자동으로 재배포됩니다.

---

## Step 5: Clerk Webhook 설정

### 5-1. Clerk Dashboard 접속
1. https://dashboard.clerk.com 로그인
2. 프로젝트 선택
3. **Webhooks** 메뉴 클릭

### 5-2. Webhook Endpoint 추가
1. **"+ Add Endpoint"** 클릭
2. **Endpoint URL** 입력:
   ```
   https://backend-production.railway.app/api/webhooks/clerk/
   ```
   **⚠️ 실제 백엔드 URL로 변경하세요**

3. **Events to listen** 선택:
   - ✅ `user.created`
   - ✅ `user.updated`
   - ✅ `user.deleted`

4. **Create** 클릭

### 5-3. Signing Secret 복사
Webhook 생성 후 **"Signing Secret"** 복사 (형식: `whsec_...`)

### 5-4. 백엔드 환경 변수에 추가
Railway → **backend** 서비스 → **Variables** 탭:
```
CLERK_WEBHOOK_SECRET=whsec_xxxxxxxxxxxxx
```

### 5-5. Webhook 테스트
1. Clerk Dashboard → Webhooks → 생성한 endpoint 클릭
2. **"Testing"** 탭 → **"Send Example"** 클릭
3. Railway **backend** 서비스 → **Logs** 탭에서 확인:
   ```
   [INFO] User created from webhook: test@example.com
   ```

---

## Step 6: 배포 테스트

### 6-1. 프론트엔드 접속
브라우저에서 프론트엔드 URL 접속:
```
https://frontend-production.railway.app
```

### 6-2. Clerk 로그인 테스트
1. 프론트엔드에서 로그인 시도
2. Clerk 로그인 화면 표시 확인
3. 로그인 후 대시보드 표시 확인

### 6-3. API 연동 테스트
1. Students 페이지 접속
2. 데이터 로딩 확인
3. 파일 업로드 테스트

### 6-4. 백엔드 로그 확인
Railway → **backend** 서비스 → **Logs** 탭:
- API 요청 로그 확인
- 에러가 없는지 확인

---

## 배포 완료 체크리스트

### 백엔드 (Django)
- [ ] Railway 프로젝트 생성 및 백엔드 서비스 설정
- [ ] Root Directory `/backend` 설정
- [ ] 모든 환경 변수 설정 완료
- [ ] 배포 성공 및 URL 확인
- [ ] Health check API 정상 응답
- [ ] Supabase 데이터베이스 연결 확인
- [ ] Clerk webhook 설정 및 테스트 성공

### 프론트엔드 (React)
- [ ] 프론트엔드 서비스 추가
- [ ] Root Directory `/frontend` 설정
- [ ] 환경 변수 설정 (API URL, Clerk 키)
- [ ] 배포 성공 및 URL 확인
- [ ] 프론트엔드 화면 정상 표시
- [ ] 백엔드 API 연동 확인

### 통합 테스트
- [ ] CORS 설정 정상 동작
- [ ] Clerk 로그인 정상 동작
- [ ] 모든 페이지 접속 확인
- [ ] 파일 업로드 기능 테스트

---

## 환경 변수 요약

### 백엔드 환경 변수
```bash
# Django
DJANGO_SETTINGS_MODULE=config.settings.prod
SECRET_KEY=jw+@l07gu*e$hl64g0d!s=na(782+uj9$tf1k)yyy&\8v=pw)f
DEBUG=False
ALLOWED_HOSTS=*.railway.app,frontend-production.railway.app

# Database
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=YOUR_SUPABASE_PASSWORD
DB_HOST=db.uzsexjgqglhwsbmrmymu.supabase.co
DB_PORT=5432

# Clerk
CLERK_SECRET_KEY=YOUR_CLERK_SECRET_KEY
CLERK_WEBHOOK_SECRET=whsec_xxxxxxxxxxxxx

# CORS
CORS_ALLOWED_ORIGINS=https://frontend-production.railway.app
```

### 프론트엔드 환경 변수
```bash
# API
REACT_APP_API_URL=https://backend-production.railway.app

# Clerk
REACT_APP_CLERK_PUBLISHABLE_KEY=YOUR_CLERK_PUBLISHABLE_KEY

# Build
GENERATE_SOURCEMAP=false
```

---

## 트러블슈팅

### 문제 1: 프론트엔드에서 API 호출 실패 (CORS 에러)

**증상:**
```
Access to fetch at 'https://backend-production.railway.app' has been blocked by CORS policy
```

**해결:**
1. 백엔드 환경 변수 확인:
   - `CORS_ALLOWED_ORIGINS`에 정확한 프론트엔드 URL 포함
   - 프로토콜(https://) 포함 확인
2. 백엔드 재배포

### 문제 2: 프론트엔드 빌드 실패

**증상:**
```
Module not found: Can't resolve 'serve'
```

**해결:**
`frontend/package.json`에 `serve` 패키지 추가 확인

### 문제 3: 백엔드 500 에러

**로그 확인:**
Railway → backend 서비스 → Logs 탭

**일반적인 원인:**
- 환경 변수 누락
- Supabase 연결 정보 오류
- Clerk 키 오류

### 문제 4: Clerk 로그인 실패

**확인 사항:**
1. Clerk Dashboard → API Keys에서 공개 키 확인
2. 프론트엔드 환경 변수 `REACT_APP_CLERK_PUBLISHABLE_KEY` 확인
3. Clerk Dashboard → Allowed Origins에 프론트엔드 URL 추가

---

## 커스텀 도메인 설정 (선택사항)

### Railway 커스텀 도메인
각 서비스마다 커스텀 도메인을 설정할 수 있습니다.

#### 백엔드 도메인 설정
1. Railway → backend 서비스 → Settings → Domains
2. **"Custom Domain"** 클릭
3. 도메인 입력 (예: `api.yourdomain.com`)
4. DNS에 CNAME 레코드 추가

#### 프론트엔드 도메인 설정
1. Railway → frontend 서비스 → Settings → Domains
2. **"Custom Domain"** 클릭
3. 도메인 입력 (예: `dashboard.yourdomain.com`)
4. DNS에 CNAME 레코드 추가

#### 커스텀 도메인 사용 시 환경 변수 업데이트
**백엔드:**
```
ALLOWED_HOSTS=*.railway.app,dashboard.yourdomain.com
CORS_ALLOWED_ORIGINS=https://dashboard.yourdomain.com
```

**프론트엔드:**
```
REACT_APP_API_URL=https://api.yourdomain.com
```

**Clerk Dashboard:**
- Webhooks → Endpoint URL: `https://api.yourdomain.com/api/webhooks/clerk/`
- Allowed Origins: `https://dashboard.yourdomain.com` 추가

---

## 모니터링 및 로그

### Railway 로그 확인
각 서비스의 **Logs** 탭에서 실시간 로그 확인

### 백엔드 로그
```bash
railway logs --service backend
```

### 프론트엔드 로그
```bash
railway logs --service frontend
```

---

## 배포 후 업데이트

### GitHub에 Push하면 자동 배포
```bash
git add .
git commit -m "Update feature"
git push origin main
```

Railway가 자동으로 변경사항을 감지하고 재배포합니다.

---

## 비용 관리

Railway는 무료 플랜에서 다음을 제공합니다:
- $5 무료 크레딧 (매월)
- 500시간 실행 시간

프로덕션 사용 시 Pro 플랜 고려:
- $20/월 (종량제)
- 무제한 프로젝트 및 서비스

---

## 중요 링크

- **Railway Dashboard**: https://railway.app/dashboard
- **Supabase Dashboard**: https://supabase.com/dashboard
- **Clerk Dashboard**: https://dashboard.clerk.com
- **GitHub Repository**: https://github.com/LovelyPaul/academy_dashboard

---

## 다음 단계

배포 완료 후:
1. ✅ 커스텀 도메인 설정 (선택사항)
2. ✅ Clerk 환경별 설정 (개발/프로덕션 분리)
3. ✅ 모니터링 도구 연동 (Sentry, LogRocket 등)
4. ✅ 백업 및 복구 전략 수립
5. ✅ CI/CD 파이프라인 최적화

---

**작성일:** 2025년 11월 3일
**목적:** Railway 프론트엔드 + 백엔드 통합 배포 가이드
