# Clerk Webhook 설정 가이드

Clerk에서 사용자가 생성/업데이트/삭제될 때 Django 백엔드에 자동으로 동기화하기 위한 Webhook 설정 방법입니다.

## 1. Django Webhook Endpoint 생성

이미 구현되어 있는 webhook endpoint를 사용합니다:
- URL: `POST /api/webhooks/clerk/`
- 파일: `backend/apps/users/views.py` (ClerkWebhookView)

### Webhook이 처리하는 이벤트:
- `user.created`: 새 사용자 생성
- `user.updated`: 사용자 정보 업데이트
- `user.deleted`: 사용자 삭제

## 2. ngrok으로 로컬 서버 공개 (개발 환경)

로컬 Django 서버를 인터넷에 공개하기 위해 ngrok 사용:

```bash
# ngrok 설치 (Mac)
brew install ngrok

# ngrok 실행 (Django 서버가 8000 포트에서 실행 중이어야 함)
ngrok http 8000
```

ngrok 실행 후 나오는 URL을 복사하세요:
```
Forwarding   https://xxxx-xxx-xxx-xxx.ngrok-free.app -> http://localhost:8000
```

## 3. Clerk Dashboard에서 Webhook 설정

### 3.1 Clerk Dashboard 접속
1. https://dashboard.clerk.com/ 접속
2. 프로젝트 선택

### 3.2 Webhook 생성
1. 좌측 메뉴에서 **"Webhooks"** 클릭
2. **"+ Add Endpoint"** 버튼 클릭

### 3.3 Endpoint URL 입력
```
https://YOUR-NGROK-URL.ngrok-free.app/api/webhooks/clerk/
```
예시:
```
https://abc123-xxx.ngrok-free.app/api/webhooks/clerk/
```

### 3.4 이벤트 선택
다음 이벤트를 체크:
- ✅ `user.created`
- ✅ `user.updated`
- ✅ `user.deleted`

### 3.5 Signing Secret 복사
1. Webhook 생성 후 **"Signing Secret"** 복사
2. 이 값을 `.env` 파일에 추가:

```bash
# backend/.env 또는 backend/.env.local
CLERK_WEBHOOK_SECRET=whsec_xxxxxxxxxxxxxxxxxxxxx
```

### 3.6 저장
**"Create"** 버튼 클릭

## 4. Django 설정 확인

### 4.1 settings.py 확인
```python
# backend/config/settings.py
CLERK_WEBHOOK_SECRET = os.getenv('CLERK_WEBHOOK_SECRET', '')
```

### 4.2 URL 설정 확인
```python
# backend/config/urls.py
urlpatterns = [
    path('api/webhooks/', include('apps.users.webhook_urls')),
]
```

## 5. Webhook 테스트

### 5.1 Django 서버 실행
```bash
cd backend
source venv/bin/activate
python manage.py runserver
```

### 5.2 ngrok 실행 (다른 터미널)
```bash
ngrok http 8000
```

### 5.3 Clerk Dashboard에서 테스트
1. Webhooks 페이지에서 생성한 endpoint 클릭
2. **"Testing"** 탭 선택
3. **"Send Example"** 클릭하여 `user.created` 이벤트 전송

### 5.4 Django 로그 확인
```bash
# Django 서버 터미널에서 확인
[날짜] "POST /api/webhooks/clerk/ HTTP/1.1" 200
User created from webhook: email@example.com
```

## 6. 실제 사용자로 테스트

### 6.1 기존 사용자 동기화
현재 Clerk에 있는 사용자를 수동으로 Django DB에 추가:

```bash
python manage.py shell
```

```python
from apps.users.models import User

# 사용자 생성 (Clerk에서 확인한 정보로)
User.objects.create(
    clerk_id='user_xxxxxxxxxxxxx',  # Clerk User ID
    email='your-email@example.com',
    username='your-username',
    first_name='Your',
    last_name='Name'
)
```

### 6.2 새 사용자로 테스트
1. 프론트엔드에서 **로그아웃**
2. 새 이메일로 **회원가입**
3. Django 로그에서 webhook이 자동으로 User 생성하는지 확인

## 7. 프로덕션 환경 설정

### 7.1 실제 도메인 사용
ngrok 대신 실제 서버 도메인 사용:
```
https://api.yourdomain.com/api/webhooks/clerk/
```

### 7.2 HTTPS 필수
Clerk Webhook은 HTTPS만 지원하므로 SSL 인증서 필요

### 7.3 환경 변수 설정
프로덕션 서버에 `CLERK_WEBHOOK_SECRET` 환경 변수 설정

## 8. 트러블슈팅

### Webhook이 호출되지 않는 경우
1. **ngrok URL 확인**: ngrok을 재시작하면 URL이 변경되므로 Clerk Dashboard에서 URL 업데이트
2. **Django 서버 확인**: `python manage.py runserver`가 실행 중인지 확인
3. **방화벽 확인**: 8000 포트가 열려있는지 확인

### Signature 검증 실패
1. `.env` 파일의 `CLERK_WEBHOOK_SECRET`이 올바른지 확인
2. Clerk Dashboard에서 Signing Secret 다시 복사

### User 중복 생성
- `clerk_id` 필드가 unique하므로 중복 생성 방지됨
- 로그에서 `User created from webhook` 메시지 확인

## 9. 현재 상태 확인

### 데이터베이스에 User가 있는지 확인
```bash
python manage.py shell -c "from apps.users.models import User; print('Total users:', User.objects.count())"
```

### Webhook 로그 확인
```bash
# Django 서버 로그에서 확인
tail -f logs/django.log
```

## 10. 임시 해결책 (Webhook 설정 전)

Webhook 설정이 완료될 때까지 middleware에서 자동으로 User 생성하도록 설정 가능:
- 파일: `backend/core/middleware.py`
- JWT 토큰에서 clerk_id를 추출하여 User가 없으면 자동 생성

단, 이 방법은 개발 단계에서만 사용하고 프로덕션에서는 반드시 Webhook 사용 권장.
