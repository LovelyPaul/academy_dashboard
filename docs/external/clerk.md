Clerk 연동 최종 문서: 대학교 대시보드 프로젝트

이 문서는 제안된 기술 스택(React.js 프런트엔드, Django DRF 백엔드)에 Clerk를 연동하기 위한 최종 가이드라인을 제공합니다. Layered Architecture 및 SOLID 원칙을 준수하며, SDK, Webhook, API 연동에 필요한 상세 정보를 포함합니다.
[Clerk 연동 개요]
Clerk는 대학교 대시보드 프로젝트의 사용자 인증 및 관리 기능을 담당합니다. 사용자 로그인, 회원가입, 프로필 관리 등의 기능은 Clerk가 제공하는 UI와 SDK를 통해 프런트엔드에 통합되며, 백엔드는 Webhook을 통해 Clerk의 사용자 데이터를 동기화하고 필요시 API를 통해 직접 사용자 정보를 관리합니다.
연동할 수단 요약:
SDK (Frontend - React.js): 사용자 인증 UI 렌더링, 인증 상태 관리, 백엔드 API 호출을 위한 인증 토큰 확보.
Webhook (Backend - Django DRF): Clerk의 사용자 이벤트(생성, 업데이트, 삭제)를 수신하여 백엔드 DB의 사용자 정보를 동기화.
API (Backend - Django DRF): 백엔드에서 Clerk의 사용자 정보를 직접 조회, 생성, 수정, 삭제하는 프로그래밍적 제어 (선택적이지만, 관리자 기능 등 고려 시 권장).
1. SDK 연동 (Frontend - React.js)
1.1. 사용할 기능
사용자 인증 UI: 로그인(SignIn), 회원가입(SignUp), 사용자 프로필(UserProfile) 등의 Clerk UI 컴포넌트 렌더링.
인증 상태 관리: useUser, useAuth 훅을 통해 현재 로그인한 사용자 정보, 인증 상태(isSignedIn), 세션 정보 접근.
조건부 UI 렌더링: SignedIn, SignedOut 컴포넌트를 사용하여 로그인 여부에 따른 UI 표시.
세션 토큰 획득: 백엔드 API 호출 시 사용될 JWT(JSON Web Token) 세션 토큰 획득(getToken()).
1.2. 설치/세팅 방법
라이브러리 설치:
code
Bash
cd frontend
npm install @clerk/clerk-react axios # axios는 API 호출에 필요
환경 변수 설정:
frontend/.env.local 파일 생성 및 Clerk Publishable Key 추가 (Clerk 대시보드 "API Keys"에서 발급).
frontend/.env.local 예시:
code
Code
REACT_APP_CLERK_PUBLISHABLE_KEY="pk_live_YOUR_CLERK_PUBLISHABLE_KEY"
REACT_APP_API_BASE_URL="http://localhost:8000/api" # 백엔드 API 기본 URL
1.3. 인증 정보 관리 방법
Publishable Key (pk_live_XXXX): 이 키는 클라이언트 측 코드에 안전하게 노출될 수 있는 키입니다. frontend/.env.local에 저장하며, 빌드 시 번들링되어 클라이언트에서 사용됩니다.
1.4. 호출 방법 (코드 예시)
code
Jsx
// frontend/src/index.js
import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import { ClerkProvider } from '@clerk/clerk-react';

const PUBLISHABLE_KEY = process.env.REACT_APP_CLERK_PUBLISHABLE_KEY;
if (!PUBLISHABLE_KEY) {
  throw new Error('Missing Publishable Key from .env.local');
}

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <ClerkProvider publishableKey={PUBLISHABLE_KEY}>
      <App />
    </ClerkProvider>
  </React.StrictMode>
);
code
Jsx
// frontend/src/pages/LoginPage.js
import React from 'react';
import { SignIn } from '@clerk/clerk-react';
import { Box, Typography } from '@mui/material';

const LoginPage = () => {
  return (
    <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '100vh', flexDirection: 'column' }}>
      <Typography variant="h4" component="h1" gutterBottom>대시보드 로그인</Typography>
      <SignIn path="/sign-in" routing="path" signUpUrl="/sign-up" />
    </Box>
  );
};
export default LoginPage;
code
JavaScript
// frontend/src/hooks/useApiClient.js
import { useAuth } from '@clerk/clerk-react';
import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000/api';

const createApiClient = (token) => {
  return axios.create({
    baseURL: API_BASE_URL,
    headers: {
      'Content-Type': 'application/json',
      ...(token && { Authorization: `Bearer ${token}` }),
    },
  });
};

export const useApiClient = () => {
  const { getToken } = useAuth(); // Clerk JWT 토큰을 가져오는 훅

  const getAuthenticatedClient = async () => {
    const token = await getToken(); // 비동기로 토큰 획득
    return createApiClient(token);
  };

  return { getAuthenticatedClient, createApiClientWithoutAuth: createApiClient(null) };
};

// 사용 예시 (컴포넌트 내):
// import { useApiClient } from '../hooks/useApiClient';
// const DashboardPage = () => {
//   const { getAuthenticatedClient } = useApiClient();
//   useEffect(() => {
//     const fetchData = async () => {
//       const client = await getAuthenticatedClient();
//       const response = await client.get('/dashboard/data/');
//       // ... 데이터 처리
//     };
//     fetchData();
//   }, [getAuthenticatedClient]);
// };
2. Webhook 연동 (Backend - Django DRF)
2.1. 사용할 기능
사용자 데이터 동기화: Clerk에서 user.created, user.updated, user.deleted 등의 이벤트가 발생할 때마다 백엔드로 알림을 받아 Django User 모델과 PostgreSQL 데이터베이스에 사용자 정보를 동기화합니다.
백엔드 기반 비즈니스 로직 트리거: 신규 사용자 생성 시 기본 대시보드 설정, 권한 부여 등 백엔드에서 처리해야 할 비즈니스 로직을 실행합니다.
2.2. 설치/세팅 방법
라이브러리 설치:
code
Bash
cd backend
pip install svix # Webhook 서명 검증 라이브러리
환경 변수 설정:
backend/.env 파일에 Clerk Webhook Secret 추가 (Clerk 대시보드 "Webhooks"에서 엔드포인트 생성 후 발급).
backend/.env 예시:
code
Code
CLERK_WEBHOOK_SECRET="whsec_YOUR_CLERK_WEBHOOK_SECRET"
Clerk Webhook 엔드포인트 등록:
Clerk 대시보드의 "Webhooks" 메뉴에서 "Add endpoint"를 클릭합니다.
Endpoint URL: https://your-domain.com/api/webhooks/clerk/ (로컬 테스트 시 ngrok으로 생성한 공개 URL 사용)
Events to send: user.created, user.updated, user.deleted를 선택합니다.
엔드포인트 생성 후 Webhook Secret을 복사하여 backend/.env에 저장합니다.
2.3. 인증 정보 관리 방법
Webhook Secret (whsec_XXXX): Clerk Webhook 요청의 유효성을 검증하는 데 사용되는 비밀 키입니다. backend/.env에 저장하며, 절대 외부에 노출되어서는 안 됩니다.
2.4. 호출 방법 (코드 예시)
code
Python
# backend/apps/users/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    # Clerk 사용자 ID를 저장할 필드 추가 (unique 하여 중복 방지)
    clerk_id = models.CharField(max_length=255, unique=True, null=True, blank=True)
    # 필요한 경우 다른 Clerk 관련 필드 추가
    # 예를 들어, Clerk의 primary_email_address를 사용하려면 AbstractUser의 email 필드를 그대로 활용

    # AbstractUser의 username을 사용하지 않고 이메일을 주 식별자로 사용하려면
    # USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = []
    # 위 설정을 User 모델 외부에 추가해야 합니다 (settings.py 등)
code
Python
# backend/apps/users/infrastructure/clerk_webhook_views.py
import json
from django.conf import settings
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from svix.webhooks import Webhook, WebhookVerificationError
import logging

from ..application.use_cases import UserWebhookUseCase

logger = logging.getLogger(__name__)

@csrf_exempt # Webhook은 CSRF 보호가 필요 없음
def clerk_webhook_handler(request):
    if request.method != 'POST':
        return HttpResponseBadRequest("Only POST requests are allowed.")

    webhook_secret = settings.CLERK_WEBHOOK_SECRET
    if not webhook_secret:
        logger.error("CLERK_WEBHOOK_SECRET is not set in settings.")
        return HttpResponseBadRequest("Webhook secret not configured.")

    headers = request.headers
    payload = request.body.decode('utf-8')

    svix_id = headers.get('svix-id')
    svix_timestamp = headers.get('svix-timestamp')
    svix_signature = headers.get('svix-signature')

    if not svix_id or not svix_timestamp or not svix_signature:
        logger.warning("Missing Svix headers in webhook request.")
        return HttpResponseBadRequest("Missing Svix headers.")

    try:
        wh = Webhook(webhook_secret)
        evt = wh.verify(payload, {
            "svix-id": svix_id,
            "svix-timestamp": svix_timestamp,
            "svix-signature": svix_signature,
        })
    except WebhookVerificationError as e:
        logger.error(f"Webhook signature verification failed: {e}")
        return HttpResponseBadRequest(f"Invalid Webhook signature: {e}")
    except Exception as e:
        logger.error(f"Error during webhook verification: {e}")
        return HttpResponseBadRequest(f"Webhook verification error: {e}")

    event_type = evt.get('type')
    event_data = evt.get('data')

    try:
        use_case = UserWebhookUseCase()
        use_case.handle_event(event_type, event_data)
        return JsonResponse({"status": "success", "event_type": event_type}, status=200)
    except Exception as e:
        logger.error(f"Error processing Clerk webhook event {event_type}: {e}", exc_info=True)
        return JsonResponse({"status": "error", "message": str(e)}, status=500)
code
Python
# backend/apps/users/application/use_cases.py
import logging
from ..domain.services import UserService
from ..infrastructure.repositories import UserRepository

logger = logging.getLogger(__name__)

class UserWebhookUseCase:
    def __init__(self, user_service: UserService = None, user_repository: UserRepository = None):
        self.user_repository = user_repository or UserRepository()
        self.user_service = user_service or UserService(self.user_repository)

    def handle_event(self, event_type: str, event_data: dict):
        clerk_id = event_data.get('id')
        email_addresses = event_data.get('email_addresses', [])
        email = email_addresses[0]['email_address'] if email_addresses else None
        first_name = event_data.get('first_name')
        last_name = event_data.get('last_name')

        if not clerk_id or not email:
            logger.error(f"Invalid Clerk webhook event data: missing clerk_id or email for type {event_type}")
            return

        if event_type == 'user.created':
            self.user_service.create_user_from_clerk(
                clerk_id=clerk_id,
                email=email,
                first_name=first_name,
                last_name=last_name
            )
        elif event_type == 'user.updated':
            self.user_service.update_user_from_clerk(
                clerk_id=clerk_id,
                email=email,
                first_name=first_name,
                last_name=last_name
            )
        elif event_type == 'user.deleted':
            self.user_service.delete_user_from_clerk(clerk_id=clerk_id)
        else:
            logger.warning(f"Unhandled Clerk webhook event type: {event_type}")
UserService는 UserWebhookUseCase로부터 호출되어 실제 비즈니스 로직(사용자 생성, 업데이트, 삭제)을 수행합니다.
UserRepository는 UserService에서 호출되어 데이터베이스와의 직접적인 상호작용을 처리합니다.
code
Python
# backend/apps/users/domain/services.py
import logging
from django.db import transaction
from ..infrastructure.repositories import UserRepository # 추상 인터페이스를 따르는 구현체

logger = logging.getLogger(__name__)

class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    @transaction.atomic
    def create_user_from_clerk(self, clerk_id: str, email: str, first_name: str, last_name: str):
        if self.user_repository.get_by_clerk_id(clerk_id):
            logger.info(f"User with clerk_id {clerk_id} already exists, skipping creation.")
            return

        user = self.user_repository.create_user(
            clerk_id=clerk_id,
            email=email,
            first_name=first_name,
            last_name=last_name,
            username=email # 또는 유니크한 값 생성 전략
        )
        logger.info(f"User {user.email} (Clerk ID: {clerk_id}) created successfully.")
        # 여기에 신규 사용자 대시보드 기본 설정 등의 비즈니스 로직 추가

    @transaction.atomic
    def update_user_from_clerk(self, clerk_id: str, email: str, first_name: str, last_name: str):
        user = self.user_repository.get_by_clerk_id(clerk_id)
        if user:
            self.user_repository.update_user(
                user=user,
                email=email,
                first_name=first_name,
                last_name=last_name
            )
            logger.info(f"User {user.email} (Clerk ID: {clerk_id}) updated successfully.")
        else:
            logger.warning(f"User with clerk_id {clerk_id} not found for update. Creating new user.")
            self.create_user_from_clerk(clerk_id, email, first_name, last_name)

    @transaction.atomic
    def delete_user_from_clerk(self, clerk_id: str):
        user = self.user_repository.get_by_clerk_id(clerk_id)
        if user:
            self.user_repository.delete_user(user)
            logger.info(f"User with clerk_id {clerk_id} deleted successfully.")
        else:
            logger.warning(f"User with clerk_id {clerk_id} not found for deletion.")
code
Python
# backend/apps/users/infrastructure/repositories.py
from django.contrib.auth import get_user_model
from django.db import IntegrityError # 중복 관련 에러 처리를 위해 임포트

User = get_user_model()

class UserRepository:
    def get_by_clerk_id(self, clerk_id: str):
        try:
            return User.objects.get(clerk_id=clerk_id)
        except User.DoesNotExist:
            return None

    def create_user(self, clerk_id: str, email: str, first_name: str = None, last_name: str = None, username: str = None):
        try:
            # username 필드가 Unique 제약 조건이 있다면 충돌 방지를 위한 전략 필요
            # 예를 들어, 이메일이 아닌 다른 고유한 값 조합
            # 또는 User 모델에 username 필드가 필요 없다면 제거
            return User.objects.create(
                clerk_id=clerk_id,
                email=email,
                first_name=first_name,
                last_name=last_name,
                username=username # AbstractUser는 username 필드가 필수이므로 적절히 채워야 함
            )
        except IntegrityError as e:
            logger.error(f"Integrity error creating user with clerk_id {clerk_id}, email {email}: {e}")
            raise ValueError(f"User creation failed due to data integrity issue: {e}")

    def update_user(self, user: User, email: str, first_name: str = None, last_name: str = None):
        user.email = email
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        return user

    def delete_user(self, user: User):
        user.delete()
code
Python
# backend/apps/users/presentation/urls.py
from django.urls import path
from ..infrastructure.clerk_webhook_views import clerk_webhook_handler

urlpatterns = [
    path('webhooks/clerk/', clerk_webhook_handler, name='clerk_webhook'),
]
code
Python
# backend/config/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('backend.apps.users.presentation.urls')), # Clerk Webhook 포함
    # 다른 앱의 API 엔드포인트도 여기에 포함
    # path('api/data-dashboard/', include('backend.apps.data_dashboard.presentation.urls')),
]
3. API 연동 (Backend - Django DRF)
3.1. 사용할 기능
백엔드에서 사용자 정보 조회: Clerk에 있는 특정 사용자 정보를 백엔드에서 직접 조회 (예: 관리자 기능에서 사용).
사용자 메타데이터 업데이트: 백엔드 비즈니스 로직에 따라 Clerk에 저장된 사용자 public_metadata 또는 private_metadata를 업데이트 (예: 사용자 권한 변경).
프로그래밍 방식의 사용자 생성/삭제: 외부 시스템과의 연동 또는 특정 조건에 따라 Clerk에 사용자를 생성하거나 삭제.
3.2. 설치/세팅 방법
라이브러리 설치:
code
Bash
cd backend
pip install clerk-sdk-python # Python용 공식 Clerk SDK
환경 변수 설정:
backend/.env 파일에 Clerk Secret Key 추가 (Clerk 대시보드 "API Keys"에서 발급).
backend/.env 예시:
code
Code
CLERK_SECRET_KEY="sk_live_YOUR_CLERK_SECRET_KEY"
3.3. 인증 정보 관리 방법
Secret Key (sk_live_XXXX): Clerk API를 호출할 때 사용되는 비밀 키입니다. backend/.env에 저장하며, 절대 외부에 노출되어서는 안 됩니다.
3.4. 호출 방법 (코드 예시)
code
Python
# backend/apps/users/infrastructure/clerk_api_clients.py
from clerk import Clerk
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class ClerkAPIClient:
    def __init__(self):
        self.api_key = settings.CLERK_SECRET_KEY
        if not self.api_key:
            raise ValueError("CLERK_SECRET_KEY is not set in settings.")
        self.clerk_client = Clerk(self.api_key)

    def get_user(self, clerk_user_id: str):
        """Clerk에서 특정 사용자 정보를 조회합니다."""
        try:
            user = self.clerk_client.users.get_user(user_id=clerk_user_id)
            return user.to_dict() # SDK 객체를 딕셔너리로 변환하여 반환
        except Exception as e:
            logger.error(f"Clerk API Error getting user {clerk_user_id}: {e}")
            raise

    def update_user_metadata(self, clerk_user_id: str, public_metadata: dict = None, private_metadata: dict = None):
        """Clerk에서 사용자 메타데이터를 업데이트합니다."""
        try:
            updated_user = self.clerk_client.users.update_user(
                user_id=clerk_user_id,
                public_metadata=public_metadata,
                private_metadata=private_metadata
            )
            return updated_user.to_dict()
        except Exception as e:
            logger.error(f"Clerk API Error updating user metadata for {clerk_user_id}: {e}")
            raise

    def create_user(self, email_address: str, password: str = None, first_name: str = None, last_name: str = None):
        """Clerk에 새로운 사용자를 생성합니다."""
        try:
            new_user = self.clerk_client.users.create_user(
                email_address=[email_address], # 이메일 주소는 리스트로 전달
                password=password,
                first_name=first_name,
                last_name=last_name
            )
            return new_user.to_dict()
        except Exception as e:
            logger.error(f"Clerk API Error creating user {email_address}: {e}")
            raise

    def delete_user(self, clerk_user_id: str):
        """Clerk에서 사용자를 삭제합니다."""
        try:
            self.clerk_client.users.delete_user(user_id=clerk_user_id)
            logger.info(f"Clerk user {clerk_user_id} deleted successfully via API.")
            return True
        except Exception as e:
            logger.error(f"Clerk API Error deleting user {clerk_user_id}: {e}")
            raise
code
Python
# backend/apps/users/application/some_admin_use_case.py (예시)
import logging
from ..infrastructure.clerk_api_clients import ClerkAPIClient

logger = logging.getLogger(__name__)

class AdminUserManagementUseCase:
    def __init__(self, clerk_api_client: ClerkAPIClient = None):
        self.clerk_api_client = clerk_api_client or ClerkAPIClient()

    def update_user_role_in_clerk(self, clerk_user_id: str, new_role: str):
        """관리자 페이지에서 사용자 역할을 변경하고 Clerk의 메타데이터도 업데이트하는 예시"""
        try:
            # Clerk의 public_metadata에 사용자 역할을 저장한다고 가정
            updated_user_data = self.clerk_api_client.update_user_metadata(
                clerk_user_id=clerk_user_id,
                public_metadata={"role": new_role}
            )
            logger.info(f"Clerk user {clerk_user_id} role updated to {new_role}.")
            return updated_user_data
        except Exception as e:
            logger.error(f"Failed to update user role in Clerk for {clerk_user_id}: {e}")
            raise