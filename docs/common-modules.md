# 공통 모듈 설계 문서

> **설계 목적**: 페이지 단위 병렬 개발을 위한 공통 모듈 사전 정의
> **설계 원칙**: 오버엔지니어링 배제, 문서 기반 실용적 설계, 코드 충돌 최소화

---

## 1. 개요

### 1.1 문서 목적
본 문서는 페이지 단위 병렬 개발을 시작하기 전에 구현해야 할 공통 모듈을 정의합니다. 모든 페이지에서 공통적으로 사용될 로직, 컴포넌트, 유틸리티를 사전에 정의하여 개발 과정에서 코드 충돌을 방지합니다.

### 1.2 범위
- **Backend**: 인증, 데이터베이스 모델, 공통 유틸리티, 에러 핸들링
- **Frontend**: 인증, API 클라이언트, 공통 컴포넌트, 레이아웃, 테마

### 1.3 제외 사항
- 페이지별 특화 로직 (각 페이지에서 개별 구현)
- 비즈니스 로직 세부 구현 (유스케이스별로 개별 구현)

---

## 2. Backend 공통 모듈

### 2.1 프로젝트 구조

```
backend/
├── config/                      # Django 프로젝트 설정
│   ├── settings/
│   │   ├── base.py             # 공통 설정
│   │   ├── dev.py              # 개발 환경 설정
│   │   └── prod.py             # 프로덕션 환경 설정
│   ├── urls.py                 # 전역 URL 라우팅
│   ├── wsgi.py
│   └── asgi.py
├── core/                        # 프로젝트 전역 공통 모듈
│   ├── exceptions.py           # 커스텀 예외 클래스
│   ├── middleware.py           # 커스텀 미들웨어
│   └── pagination.py           # 공통 페이지네이션
├── apps/
│   ├── users/                  # 사용자 인증 앱
│   │   ├── models.py
│   │   ├── domain/
│   │   ├── application/
│   │   ├── presentation/
│   │   └── infrastructure/
│   └── data_dashboard/         # 데이터 대시보드 앱
│       ├── models.py
│       ├── domain/
│       ├── application/
│       ├── presentation/
│       └── infrastructure/
├── utils/                       # 범용 유틸리티
│   ├── formatters.py           # 데이터 포맷 변환
│   ├── validators.py           # 데이터 검증
│   └── date_utils.py           # 날짜 관련 유틸리티
├── manage.py
└── requirements.txt
```

---

### 2.2 공통 모듈 상세

#### 2.2.1 config/settings/ - 환경 설정

**파일**: `backend/config/settings/base.py`

**목적**: 전체 프로젝트의 기본 설정 정의

**주요 내용**:
```python
# 필수 설정 항목
- SECRET_KEY: Django 비밀 키
- ALLOWED_HOSTS: 허용 호스트
- INSTALLED_APPS: 설치된 앱 목록
  - django.contrib.admin
  - django.contrib.auth
  - django.contrib.contenttypes
  - django.contrib.sessions
  - django.contrib.messages
  - django.contrib.staticfiles
  - rest_framework
  - corsheaders
  - apps.users
  - apps.data_dashboard
- MIDDLEWARE: 미들웨어 설정
  - corsheaders.middleware.CorsMiddleware
  - django.middleware.security.SecurityMiddleware
  - django.middleware.common.CommonMiddleware
  - django.middleware.csrf.CsrfViewMiddleware
  - core.middleware.ClerkAuthenticationMiddleware
- DATABASE: PostgreSQL 설정
- REST_FRAMEWORK: DRF 기본 설정
  - DEFAULT_AUTHENTICATION_CLASSES
  - DEFAULT_PERMISSION_CLASSES
  - DEFAULT_PAGINATION_CLASS
- CORS_SETTINGS: CORS 설정
```

**파일**: `backend/config/settings/dev.py`
```python
from .base import *

DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1']
```

**파일**: `backend/config/settings/prod.py`
```python
from .base import *

DEBUG = False
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(',')
```

---

#### 2.2.2 core/exceptions.py - 커스텀 예외

**목적**: 프로젝트 전역에서 사용할 커스텀 예외 클래스 정의

**주요 내용**:
```python
class BaseAPIException(Exception):
    """기본 API 예외 클래스"""
    default_message = "An error occurred"
    default_code = "error"
    status_code = 400

class ValidationError(BaseAPIException):
    """데이터 유효성 검증 실패"""
    default_message = "Validation failed"
    default_code = "validation_error"
    status_code = 400

class AuthenticationError(BaseAPIException):
    """인증 실패"""
    default_message = "Authentication failed"
    default_code = "authentication_error"
    status_code = 401

class PermissionDeniedError(BaseAPIException):
    """권한 없음"""
    default_message = "Permission denied"
    default_code = "permission_denied"
    status_code = 403

class NotFoundError(BaseAPIException):
    """리소스 없음"""
    default_message = "Resource not found"
    default_code = "not_found"
    status_code = 404

class FileProcessingError(BaseAPIException):
    """파일 처리 오류"""
    default_message = "File processing failed"
    default_code = "file_processing_error"
    status_code = 422
```

**사용처**: 모든 유스케이스, 서비스, 뷰에서 공통 사용

---

#### 2.2.3 core/middleware.py - Clerk 인증 미들웨어

**목적**: Clerk JWT 토큰 검증 및 사용자 인증 처리

**주요 내용**:
```python
class ClerkAuthenticationMiddleware:
    """
    Clerk JWT 토큰을 검증하고 request.user에 사용자 정보 주입
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Authorization 헤더에서 JWT 토큰 추출
        auth_header = request.headers.get('Authorization', '')

        if auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
            try:
                # Clerk JWT 검증 (Clerk SDK 활용)
                decoded_token = verify_clerk_token(token)
                clerk_id = decoded_token.get('sub')

                # Django User 모델에서 사용자 조회
                user = User.objects.get(clerk_id=clerk_id)
                request.user = user
            except Exception as e:
                request.user = AnonymousUser()
        else:
            request.user = AnonymousUser()

        response = self.get_response(request)
        return response
```

**사용처**: 모든 API 요청에 자동 적용

---

#### 2.2.4 core/pagination.py - 공통 페이지네이션

**목적**: API 응답 페이지네이션 표준화

**주요 내용**:
```python
from rest_framework.pagination import PageNumberPagination

class StandardResultsSetPagination(PageNumberPagination):
    """
    표준 페이지네이션 클래스
    - 페이지당 20개 항목 (기본)
    - 최대 100개까지 조회 가능
    """
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100
```

**사용처**: 리스트 조회 API (업로드 히스토리, 사용자 목록 등)

---

#### 2.2.5 apps/users/ - 사용자 인증 앱

**파일**: `backend/apps/users/models.py`

**목적**: Clerk 사용자 동기화를 위한 User 모델

**주요 내용**:
```python
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """
    Clerk 사용자 정보를 동기화하는 User 모델
    """
    clerk_id = models.CharField(
        max_length=255,
        unique=True,
        db_index=True,
        help_text="Clerk User ID"
    )
    role = models.CharField(
        max_length=20,
        choices=[('admin', 'Admin'), ('user', 'User')],
        default='user',
        help_text="사용자 권한"
    )

    class Meta:
        db_table = 'users'
        indexes = [
            models.Index(fields=['clerk_id']),
            models.Index(fields=['email']),
        ]
```

**파일**: `backend/apps/users/infrastructure/repositories.py`

**목적**: User 모델 CRUD 인터페이스

**주요 내용**:
```python
class UserRepository:
    """User 모델 저장소"""

    def get_by_clerk_id(self, clerk_id: str) -> User:
        """Clerk ID로 사용자 조회"""

    def create_user(self, clerk_id: str, email: str, **kwargs) -> User:
        """사용자 생성"""

    def update_user(self, user: User, **kwargs) -> User:
        """사용자 정보 업데이트"""

    def delete_user(self, user: User) -> None:
        """사용자 삭제"""
```

**파일**: `backend/apps/users/application/use_cases.py`

**목적**: Clerk Webhook 이벤트 처리

**주요 내용**:
```python
class UserWebhookUseCase:
    """
    Clerk Webhook 이벤트를 처리하여 사용자 동기화
    """
    def handle_event(self, event_type: str, event_data: dict):
        """
        이벤트 타입별 처리:
        - user.created: 신규 사용자 생성
        - user.updated: 사용자 정보 업데이트
        - user.deleted: 사용자 삭제
        """
```

**파일**: `backend/apps/users/infrastructure/clerk_webhook_views.py`

**목적**: Clerk Webhook 엔드포인트

**주요 내용**:
```python
@csrf_exempt
def clerk_webhook_handler(request):
    """
    Clerk Webhook 요청 처리
    - Webhook 서명 검증 (svix 라이브러리)
    - UserWebhookUseCase 호출
    """
```

**사용처**: 모든 페이지에서 인증이 필요한 API 호출 시 사용

---

#### 2.2.6 apps/data_dashboard/models.py - 데이터 모델

**목적**: database.md에 정의된 모든 테이블을 Django 모델로 구현

**주요 모델**:
```python
# 1. DepartmentKPI 모델
class DepartmentKPI(models.Model):
    """학과별 KPI 데이터"""
    year = models.IntegerField()
    college = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    employment_rate = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    full_time_faculty = models.IntegerField(null=True)
    visiting_faculty = models.IntegerField(null=True)
    tech_transfer_revenue = models.DecimalField(max_digits=12, decimal_places=2, null=True)
    intl_conference_count = models.IntegerField(null=True)

    class Meta:
        db_table = 'department_kpis'
        unique_together = [['year', 'college', 'department']]
        indexes = [
            models.Index(fields=['year']),
            models.Index(fields=['department']),
        ]

# 2. Publication 모델
class Publication(models.Model):
    """논문 정보"""
    publication_id = models.CharField(max_length=50, unique=True, db_index=True)
    publication_date = models.DateField()
    college = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    title = models.TextField()
    primary_author = models.CharField(max_length=100)
    co_authors = models.TextField(null=True, blank=True)
    journal_name = models.CharField(max_length=255)
    journal_grade = models.CharField(max_length=50, null=True)
    impact_factor = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    is_project_linked = models.BooleanField(default=False)

    class Meta:
        db_table = 'publications'
        indexes = [
            models.Index(fields=['publication_date']),
            models.Index(fields=['journal_grade']),
        ]

# 3. Student 모델
class Student(models.Model):
    """학생 정보"""
    PROGRAM_CHOICES = [
        ('학사', '학사'),
        ('석사', '석사'),
        ('박사', '박사'),
    ]

    ENROLLMENT_CHOICES = [
        ('재학', '재학'),
        ('휴학', '휴학'),
        ('졸업', '졸업'),
        ('자퇴', '자퇴'),
        ('제적', '제적'),
    ]

    student_id = models.CharField(max_length=20, unique=True, db_index=True)
    name = models.CharField(max_length=100)
    college = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    grade = models.IntegerField(null=True)
    program_type = models.CharField(max_length=50, choices=PROGRAM_CHOICES)
    enrollment_status = models.CharField(max_length=50, choices=ENROLLMENT_CHOICES)
    gender = models.CharField(max_length=10, null=True)
    admission_year = models.IntegerField()
    advisor = models.CharField(max_length=100, null=True)
    email = models.EmailField(null=True)

    class Meta:
        db_table = 'students'
        indexes = [
            models.Index(fields=['department']),
            models.Index(fields=['enrollment_status']),
        ]

# 4. ResearchBudgetData 모델
class ResearchBudgetData(models.Model):
    """연구과제 및 예산 통합 데이터"""
    STATUS_CHOICES = [
        ('집행완료', '집행완료'),
        ('처리중', '처리중'),
        ('취소', '취소'),
    ]

    execution_id = models.CharField(max_length=50, unique=True, db_index=True)
    project_number = models.CharField(max_length=50)
    project_name = models.CharField(max_length=255)
    principal_investigator = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    funding_agency = models.CharField(max_length=255)
    total_budget = models.BigIntegerField()
    execution_date = models.DateField()
    execution_item = models.CharField(max_length=255)
    execution_amount = models.BigIntegerField()
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)
    note = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'research_budget_data'
        indexes = [
            models.Index(fields=['project_number']),
            models.Index(fields=['department']),
            models.Index(fields=['execution_date']),
        ]

# 5. UploadHistory 모델
class UploadHistory(models.Model):
    """파일 업로드 이력"""
    FILE_TYPE_CHOICES = [
        ('department_kpi', 'Department KPI'),
        ('publication_list', 'Publication List'),
        ('research_project_data', 'Research Project Data'),
        ('student_roster', 'Student Roster'),
    ]

    STATUS_CHOICES = [
        ('success', 'Success'),
        ('failed', 'Failed'),
    ]

    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    file_name = models.CharField(max_length=255)
    file_type = models.CharField(max_length=50, choices=FILE_TYPE_CHOICES)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)
    records_processed = models.IntegerField(default=0)
    error_message = models.TextField(null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'upload_history'
        indexes = [
            models.Index(fields=['-uploaded_at']),
        ]
```

**사용처**: 모든 데이터 조회 및 저장 로직에서 사용

---

#### 2.2.7 apps/data_dashboard/infrastructure/file_parsers.py - 엑셀 파싱

**목적**: 업로드된 엑셀 파일 파싱 로직

**주요 내용**:
```python
import pandas as pd
from typing import List, Dict
from core.exceptions import FileProcessingError

class ExcelParser:
    """엑셀 파일 파싱 기본 클래스"""

    def parse(self, file_path: str) -> pd.DataFrame:
        """엑셀 파일을 DataFrame으로 변환"""
        try:
            df = pd.read_excel(file_path)
            return df
        except Exception as e:
            raise FileProcessingError(f"Failed to parse Excel file: {e}")

    def validate_columns(self, df: pd.DataFrame, required_columns: List[str]) -> bool:
        """필수 컬럼 존재 여부 검증"""
        missing_columns = set(required_columns) - set(df.columns)
        if missing_columns:
            raise FileProcessingError(f"Missing required columns: {missing_columns}")
        return True

class DepartmentKPIParser(ExcelParser):
    """학과 KPI 엑셀 파서"""
    REQUIRED_COLUMNS = ['year', 'college', 'department', 'employment_rate', ...]

    def parse_to_dict(self, file_path: str) -> List[Dict]:
        """엑셀을 Dict 리스트로 변환"""
        df = self.parse(file_path)
        self.validate_columns(df, self.REQUIRED_COLUMNS)
        return df.to_dict('records')

class PublicationParser(ExcelParser):
    """논문 엑셀 파서"""
    REQUIRED_COLUMNS = ['publication_id', 'publication_date', 'title', ...]

class StudentParser(ExcelParser):
    """학생 엑셀 파서"""
    REQUIRED_COLUMNS = ['student_id', 'name', 'college', 'department', ...]

class ResearchBudgetParser(ExcelParser):
    """연구과제/예산 엑셀 파서"""
    REQUIRED_COLUMNS = ['execution_id', 'project_number', 'project_name', ...]
```

**사용처**: 데이터 업로드 페이지 (유스케이스 9)

---

#### 2.2.8 utils/ - 범용 유틸리티

**파일**: `backend/utils/formatters.py`

**목적**: 데이터 포맷 변환 헬퍼 함수

**주요 내용**:
```python
def format_currency(amount: int) -> str:
    """금액을 포맷팅 (1,000,000 -> "1,000,000원")"""
    return f"{amount:,}원"

def format_percentage(value: float) -> str:
    """퍼센트 포맷팅 (85.5 -> "85.5%")"""
    return f"{value}%"

def format_date(date) -> str:
    """날짜 포맷팅 (2024-01-01 -> "2024년 1월 1일")"""
    return date.strftime("%Y년 %m월 %d일")
```

**파일**: `backend/utils/validators.py`

**목적**: 데이터 유효성 검증

**주요 내용**:
```python
def validate_year(year: int) -> bool:
    """연도 유효성 검증 (2000-2100)"""
    return 2000 <= year <= 2100

def validate_email(email: str) -> bool:
    """이메일 형식 검증"""
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def validate_file_extension(filename: str, allowed_extensions: List[str]) -> bool:
    """파일 확장자 검증"""
    extension = filename.rsplit('.', 1)[-1].lower()
    return extension in allowed_extensions
```

**파일**: `backend/utils/date_utils.py`

**목적**: 날짜 관련 유틸리티

**주요 내용**:
```python
from datetime import datetime, timedelta

def get_current_year() -> int:
    """현재 연도 반환"""
    return datetime.now().year

def get_date_range(start_date, end_date):
    """날짜 범위 생성"""
    return pd.date_range(start_date, end_date)

def parse_date_string(date_string: str, format: str = "%Y-%m-%d") -> datetime:
    """문자열을 날짜로 변환"""
    return datetime.strptime(date_string, format)
```

**사용처**: 모든 뷰, 유스케이스, 시리얼라이저에서 공통 사용

---

### 2.3 Backend 공통 모듈 요약

| 모듈 | 파일 | 목적 | 사용처 |
|------|------|------|--------|
| 설정 | config/settings/ | 환경별 설정 관리 | 전역 |
| 예외 | core/exceptions.py | 커스텀 예외 클래스 | 전역 |
| 미들웨어 | core/middleware.py | Clerk 인증 처리 | 전역 |
| 페이지네이션 | core/pagination.py | API 응답 페이지네이션 | 리스트 API |
| User 모델 | apps/users/models.py | Clerk 사용자 동기화 | 인증 관련 |
| Webhook | apps/users/infrastructure/ | Clerk 이벤트 처리 | 회원가입/로그인 |
| 데이터 모델 | apps/data_dashboard/models.py | 모든 데이터 테이블 | 전역 |
| 파일 파싱 | apps/data_dashboard/infrastructure/file_parsers.py | 엑셀 파싱 | 업로드 페이지 |
| 유틸리티 | utils/ | 범용 헬퍼 함수 | 전역 |

---

## 3. Frontend 공통 모듈

### 3.1 프로젝트 구조

```
frontend/
├── public/
│   ├── index.html
│   └── favicon.ico
├── src/
│   ├── api/                     # API 클라이언트
│   │   ├── client.js           # Axios 인스턴스
│   │   ├── authApi.js          # 인증 API
│   │   └── dashboardApi.js     # 대시보드 API
│   ├── components/              # 재사용 가능한 UI 컴포넌트
│   │   ├── common/
│   │   │   ├── Button.jsx
│   │   │   ├── Card.jsx
│   │   │   ├── Table.jsx
│   │   │   └── Loading.jsx
│   │   └── charts/
│   │       ├── BarChart.jsx
│   │       ├── LineChart.jsx
│   │       ├── PieChart.jsx
│   │       └── KPICard.jsx
│   ├── layouts/                 # 페이지 레이아웃
│   │   ├── MainLayout.jsx      # 메인 레이아웃 (헤더, 사이드바)
│   │   └── AuthLayout.jsx      # 인증 페이지 레이아웃
│   ├── pages/                   # 페이지 컴포넌트 (병렬 개발)
│   │   ├── LoginPage.jsx
│   │   ├── SignUpPage.jsx
│   │   ├── DashboardPage.jsx
│   │   ├── PerformancePage.jsx
│   │   ├── PapersPage.jsx
│   │   ├── StudentsPage.jsx
│   │   ├── BudgetPage.jsx
│   │   └── UploadPage.jsx
│   ├── hooks/                   # 커스텀 훅
│   │   ├── useAuth.js          # 인증 관련
│   │   ├── useApiClient.js     # API 클라이언트
│   │   └── useDashboard.js     # 대시보드 데이터
│   ├── services/                # 클라이언트 로직
│   │   └── dataTransformer.js  # 데이터 변환
│   ├── utils/                   # 유틸리티
│   │   ├── formatters.js       # 데이터 포맷팅
│   │   └── validators.js       # 유효성 검증
│   ├── styles/                  # 스타일
│   │   ├── theme.js            # MUI 테마
│   │   └── global.css          # 전역 스타일
│   ├── App.jsx
│   └── index.jsx
├── .env
├── package.json
└── README.md
```

---

### 3.2 공통 모듈 상세

#### 3.2.1 api/client.js - Axios 인스턴스

**목적**: 백엔드 API 호출을 위한 Axios 설정

**주요 내용**:
```javascript
import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000/api';

// 인증이 필요 없는 기본 클라이언트
export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10000,
});

// 인증이 필요한 클라이언트 (Clerk 토큰 포함)
export const createAuthenticatedClient = (token) => {
  return axios.create({
    baseURL: API_BASE_URL,
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`,
    },
    timeout: 10000,
  });
};

// 응답 인터셉터 (에러 처리)
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response) {
      // 서버 응답 에러
      console.error('API Error:', error.response.data);
    } else if (error.request) {
      // 요청 전송 실패
      console.error('Network Error:', error.request);
    }
    return Promise.reject(error);
  }
);
```

**사용처**: 모든 API 호출

---

#### 3.2.2 hooks/useAuth.js - 인증 훅

**목적**: Clerk 인증 상태 관리

**주요 내용**:
```javascript
import { useUser, useAuth as useClerkAuth } from '@clerk/clerk-react';

export const useAuth = () => {
  const { user, isLoaded, isSignedIn } = useUser();
  const { getToken, signOut } = useClerkAuth();

  return {
    user,
    isLoaded,
    isSignedIn,
    getToken,
    signOut,
  };
};
```

**사용처**: 모든 보호된 페이지 (대시보드, 업로드 등)

---

#### 3.2.3 hooks/useApiClient.js - API 클라이언트 훅

**목적**: 인증 토큰이 포함된 API 클라이언트 제공

**주요 내용**:
```javascript
import { useAuth } from './useAuth';
import { createAuthenticatedClient, apiClient } from '../api/client';

export const useApiClient = () => {
  const { getToken } = useAuth();

  const getAuthenticatedClient = async () => {
    const token = await getToken();
    return createAuthenticatedClient(token);
  };

  return {
    getAuthenticatedClient,
    publicClient: apiClient,
  };
};
```

**사용처**: 모든 페이지에서 API 호출 시 사용

---

#### 3.2.4 components/common/ - 공통 UI 컴포넌트

**파일**: `Button.jsx`

**목적**: 재사용 가능한 버튼 컴포넌트

**주요 내용**:
```javascript
import { Button as MuiButton } from '@mui/material';

export const Button = ({ children, variant = 'contained', color = 'primary', ...props }) => {
  return (
    <MuiButton variant={variant} color={color} {...props}>
      {children}
    </MuiButton>
  );
};
```

**파일**: `Card.jsx`

**목적**: 재사용 가능한 카드 컴포넌트

**주요 내용**:
```javascript
import { Card as MuiCard, CardContent, CardHeader } from '@mui/material';

export const Card = ({ title, children, ...props }) => {
  return (
    <MuiCard {...props}>
      {title && <CardHeader title={title} />}
      <CardContent>{children}</CardContent>
    </MuiCard>
  );
};
```

**파일**: `Table.jsx`

**목적**: 재사용 가능한 테이블 컴포넌트

**주요 내용**:
```javascript
import { Table as MuiTable, TableBody, TableCell, TableHead, TableRow } from '@mui/material';

export const Table = ({ columns, data }) => {
  return (
    <MuiTable>
      <TableHead>
        <TableRow>
          {columns.map((col) => (
            <TableCell key={col.id}>{col.label}</TableCell>
          ))}
        </TableRow>
      </TableHead>
      <TableBody>
        {data.map((row, index) => (
          <TableRow key={index}>
            {columns.map((col) => (
              <TableCell key={col.id}>{row[col.id]}</TableCell>
            ))}
          </TableRow>
        ))}
      </TableBody>
    </MuiTable>
  );
};
```

**파일**: `Loading.jsx`

**목적**: 로딩 인디케이터

**주요 내용**:
```javascript
import { CircularProgress, Box } from '@mui/material';

export const Loading = () => {
  return (
    <Box display="flex" justifyContent="center" alignItems="center" minHeight="200px">
      <CircularProgress />
    </Box>
  );
};
```

**사용처**: 모든 페이지

---

#### 3.2.5 components/charts/ - 차트 컴포넌트

**파일**: `KPICard.jsx`

**목적**: KPI 카드 컴포넌트

**주요 내용**:
```javascript
import { Card, CardContent, Typography } from '@mui/material';

export const KPICard = ({ title, value, subtitle }) => {
  return (
    <Card>
      <CardContent>
        <Typography variant="h6" color="textSecondary">
          {title}
        </Typography>
        <Typography variant="h3" component="div">
          {value}
        </Typography>
        {subtitle && (
          <Typography variant="body2" color="textSecondary">
            {subtitle}
          </Typography>
        )}
      </CardContent>
    </Card>
  );
};
```

**파일**: `BarChart.jsx`

**목적**: 막대 차트 컴포넌트 (Chart.js)

**주요 내용**:
```javascript
import { Bar } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend } from 'chart.js';

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

export const BarChart = ({ data, options }) => {
  return <Bar data={data} options={options} />;
};
```

**파일**: `LineChart.jsx`

**목적**: 라인 차트 컴포넌트 (Chart.js)

**주요 내용**:
```javascript
import { Line } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend } from 'chart.js';

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend);

export const LineChart = ({ data, options }) => {
  return <Line data={data} options={options} />;
};
```

**파일**: `PieChart.jsx`

**목적**: 파이 차트 컴포넌트 (Chart.js)

**주요 내용**:
```javascript
import { Pie } from 'react-chartjs-2';
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js';

ChartJS.register(ArcElement, Tooltip, Legend);

export const PieChart = ({ data, options }) => {
  return <Pie data={data} options={options} />;
};
```

**사용처**: 대시보드 페이지, 분석 페이지

---

#### 3.2.6 layouts/MainLayout.jsx - 메인 레이아웃

**목적**: 헤더, 사이드바, 푸터를 포함한 메인 레이아웃

**주요 내용**:
```javascript
import { Box, AppBar, Toolbar, Typography, Drawer, List, ListItem, ListItemText } from '@mui/material';
import { useAuth } from '../hooks/useAuth';
import { useNavigate } from 'react-router-dom';

const DRAWER_WIDTH = 240;

export const MainLayout = ({ children }) => {
  const { user, signOut } = useAuth();
  const navigate = useNavigate();

  const menuItems = [
    { label: '대시보드', path: '/dashboard' },
    { label: '실적 분석', path: '/dashboard/performance' },
    { label: '논문 분석', path: '/dashboard/papers' },
    { label: '학생 분석', path: '/dashboard/students' },
    { label: '예산 분석', path: '/dashboard/budget' },
    { label: '데이터 업로드', path: '/admin/upload' },
  ];

  const handleLogout = () => {
    signOut();
    navigate('/sign-in');
  };

  return (
    <Box sx={{ display: 'flex' }}>
      {/* AppBar (헤더) */}
      <AppBar position="fixed" sx={{ zIndex: (theme) => theme.zIndex.drawer + 1 }}>
        <Toolbar>
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            대학교 데이터 대시보드
          </Typography>
          <Typography variant="body1" sx={{ mr: 2 }}>
            {user?.email}
          </Typography>
          <button onClick={handleLogout}>로그아웃</button>
        </Toolbar>
      </AppBar>

      {/* Drawer (사이드바) */}
      <Drawer
        variant="permanent"
        sx={{
          width: DRAWER_WIDTH,
          flexShrink: 0,
          '& .MuiDrawer-paper': { width: DRAWER_WIDTH, boxSizing: 'border-box' },
        }}
      >
        <Toolbar />
        <Box sx={{ overflow: 'auto' }}>
          <List>
            {menuItems.map((item) => (
              <ListItem button key={item.path} onClick={() => navigate(item.path)}>
                <ListItemText primary={item.label} />
              </ListItem>
            ))}
          </List>
        </Box>
      </Drawer>

      {/* 메인 컨텐츠 */}
      <Box component="main" sx={{ flexGrow: 1, p: 3 }}>
        <Toolbar />
        {children}
      </Box>
    </Box>
  );
};
```

**사용처**: 모든 대시보드 페이지

---

#### 3.2.7 layouts/AuthLayout.jsx - 인증 레이아웃

**목적**: 로그인, 회원가입 페이지용 레이아웃

**주요 내용**:
```javascript
import { Box, Container } from '@mui/material';

export const AuthLayout = ({ children }) => {
  return (
    <Box
      sx={{
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        minHeight: '100vh',
        bgcolor: 'background.default',
      }}
    >
      <Container maxWidth="sm">{children}</Container>
    </Box>
  );
};
```

**사용처**: 로그인, 회원가입 페이지

---

#### 3.2.8 services/dataTransformer.js - 데이터 변환

**목적**: API 응답 데이터를 차트 라이브러리 형식으로 변환

**주요 내용**:
```javascript
/**
 * 막대 차트 데이터 변환
 * @param {Array} data - API 응답 데이터
 * @param {string} labelKey - 레이블 키
 * @param {string} valueKey - 값 키
 */
export const transformToBarChartData = (data, labelKey, valueKey) => {
  return {
    labels: data.map((item) => item[labelKey]),
    datasets: [
      {
        label: valueKey,
        data: data.map((item) => item[valueKey]),
        backgroundColor: 'rgba(75, 192, 192, 0.6)',
      },
    ],
  };
};

/**
 * 라인 차트 데이터 변환
 * @param {Array} data - API 응답 데이터
 * @param {string} labelKey - 레이블 키
 * @param {string} valueKey - 값 키
 */
export const transformToLineChartData = (data, labelKey, valueKey) => {
  return {
    labels: data.map((item) => item[labelKey]),
    datasets: [
      {
        label: valueKey,
        data: data.map((item) => item[valueKey]),
        borderColor: 'rgb(75, 192, 192)',
        tension: 0.1,
      },
    ],
  };
};

/**
 * 파이 차트 데이터 변환
 * @param {Array} data - API 응답 데이터
 * @param {string} labelKey - 레이블 키
 * @param {string} valueKey - 값 키
 */
export const transformToPieChartData = (data, labelKey, valueKey) => {
  return {
    labels: data.map((item) => item[labelKey]),
    datasets: [
      {
        data: data.map((item) => item[valueKey]),
        backgroundColor: [
          'rgba(255, 99, 132, 0.6)',
          'rgba(54, 162, 235, 0.6)',
          'rgba(255, 206, 86, 0.6)',
          'rgba(75, 192, 192, 0.6)',
          'rgba(153, 102, 255, 0.6)',
        ],
      },
    ],
  };
};
```

**사용처**: 모든 차트를 사용하는 페이지

---

#### 3.2.9 utils/ - 유틸리티

**파일**: `utils/formatters.js`

**목적**: 데이터 포맷팅 헬퍼 함수

**주요 내용**:
```javascript
/**
 * 숫자를 천단위 콤마 형식으로 변환
 * @param {number} num
 */
export const formatNumber = (num) => {
  return num.toLocaleString('ko-KR');
};

/**
 * 금액 포맷팅
 * @param {number} amount
 */
export const formatCurrency = (amount) => {
  return `${formatNumber(amount)}원`;
};

/**
 * 퍼센트 포맷팅
 * @param {number} value
 */
export const formatPercentage = (value) => {
  return `${value.toFixed(1)}%`;
};

/**
 * 날짜 포맷팅
 * @param {string} dateString
 */
export const formatDate = (dateString) => {
  const date = new Date(dateString);
  return date.toLocaleDateString('ko-KR', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  });
};
```

**파일**: `utils/validators.js`

**목적**: 클라이언트 측 유효성 검증

**주요 내용**:
```javascript
/**
 * 이메일 형식 검증
 * @param {string} email
 */
export const isValidEmail = (email) => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
};

/**
 * 파일 확장자 검증
 * @param {File} file
 * @param {Array} allowedExtensions
 */
export const isValidFileExtension = (file, allowedExtensions) => {
  const extension = file.name.split('.').pop().toLowerCase();
  return allowedExtensions.includes(extension);
};

/**
 * 파일 크기 검증
 * @param {File} file
 * @param {number} maxSizeMB
 */
export const isValidFileSize = (file, maxSizeMB) => {
  const maxSizeBytes = maxSizeMB * 1024 * 1024;
  return file.size <= maxSizeBytes;
};
```

**사용처**: 모든 폼, 파일 업로드

---

#### 3.2.10 styles/theme.js - MUI 테마

**목적**: 전역 MUI 테마 설정

**주요 내용**:
```javascript
import { createTheme } from '@mui/material/styles';

export const theme = createTheme({
  palette: {
    primary: {
      main: '#1976d2',
    },
    secondary: {
      main: '#dc004e',
    },
    background: {
      default: '#f5f5f5',
    },
  },
  typography: {
    fontFamily: '"Noto Sans KR", "Roboto", "Helvetica", "Arial", sans-serif',
    h1: {
      fontSize: '2.5rem',
      fontWeight: 700,
    },
    h2: {
      fontSize: '2rem',
      fontWeight: 600,
    },
    h3: {
      fontSize: '1.75rem',
      fontWeight: 600,
    },
  },
  components: {
    MuiButton: {
      styleOverrides: {
        root: {
          textTransform: 'none',
        },
      },
    },
  },
});
```

**사용처**: `App.jsx`에서 ThemeProvider로 감싸기

---

### 3.3 Frontend 공통 모듈 요약

| 모듈 | 파일 | 목적 | 사용처 |
|------|------|------|--------|
| API 클라이언트 | api/client.js | Axios 인스턴스 | 전역 |
| 인증 훅 | hooks/useAuth.js | Clerk 인증 상태 | 전역 |
| API 훅 | hooks/useApiClient.js | 인증 토큰 API | 전역 |
| 공통 컴포넌트 | components/common/ | 버튼, 카드, 테이블 등 | 전역 |
| 차트 컴포넌트 | components/charts/ | 막대/라인/파이 차트, KPI 카드 | 대시보드 |
| 메인 레이아웃 | layouts/MainLayout.jsx | 헤더, 사이드바 | 대시보드 페이지 |
| 인증 레이아웃 | layouts/AuthLayout.jsx | 로그인 페이지 | 인증 페이지 |
| 데이터 변환 | services/dataTransformer.js | 차트 데이터 변환 | 대시보드 |
| 유틸리티 | utils/ | 포맷팅, 검증 | 전역 |
| 테마 | styles/theme.js | MUI 테마 | 전역 |

---

## 4. 페이지별 의존성 맵

### 4.1 Backend 페이지별 의존성

| 페이지 (API 엔드포인트) | 의존 모듈 |
|------------------------|-----------|
| 회원가입/로그인 | User 모델, Clerk Webhook, UserWebhookUseCase |
| 메인 대시보드 | DepartmentKPI, Publication, Student, ResearchBudgetData 모델 |
| 실적 분석 | DepartmentKPI, ResearchBudgetData 모델 |
| 논문 분석 | Publication 모델 |
| 학생 분석 | Student 모델 |
| 예산 분석 | ResearchBudgetData 모델 |
| 데이터 업로드 | 모든 모델, ExcelParser 클래스, UploadHistory 모델 |
| 업로드 히스토리 | UploadHistory 모델 |

### 4.2 Frontend 페이지별 의존성

| 페이지 | 의존 모듈 |
|--------|-----------|
| 로그인 | AuthLayout, useAuth |
| 회원가입 | AuthLayout, useAuth |
| 메인 대시보드 | MainLayout, useApiClient, KPICard, BarChart, LineChart, PieChart, dataTransformer |
| 실적 분석 | MainLayout, useApiClient, BarChart, LineChart, dataTransformer |
| 논문 분석 | MainLayout, useApiClient, BarChart, PieChart, dataTransformer |
| 학생 분석 | MainLayout, useApiClient, BarChart, PieChart, dataTransformer |
| 예산 분석 | MainLayout, useApiClient, PieChart, LineChart, dataTransformer |
| 데이터 업로드 | MainLayout, useApiClient, Table, validators |

---

## 5. 구현 순서 및 검증 체크리스트

### 5.1 Backend 구현 순서

1. **프로젝트 초기화 (Phase 0)**
   - [ ] Django 프로젝트 생성
   - [ ] requirements.txt 작성 및 라이브러리 설치
   - [ ] config/settings/ 환경별 설정 작성
   - [ ] PostgreSQL 데이터베이스 연결 테스트

2. **공통 모듈 구현 (Phase 1)**
   - [ ] core/exceptions.py 커스텀 예외 클래스 작성
   - [ ] core/middleware.py Clerk 인증 미들웨어 작성
   - [ ] core/pagination.py 페이지네이션 클래스 작성
   - [ ] utils/ 유틸리티 함수 작성

3. **사용자 인증 (Phase 2)**
   - [ ] apps/users/models.py User 모델 작성
   - [ ] apps/users/infrastructure/repositories.py UserRepository 작성
   - [ ] apps/users/domain/services.py UserService 작성
   - [ ] apps/users/application/use_cases.py UserWebhookUseCase 작성
   - [ ] apps/users/infrastructure/clerk_webhook_views.py Webhook 엔드포인트 작성
   - [ ] Clerk Webhook 테스트

4. **데이터 모델 (Phase 3)**
   - [ ] apps/data_dashboard/models.py 모든 모델 작성
   - [ ] Migration 생성 및 적용
   - [ ] 데이터베이스 테이블 생성 확인

5. **파일 파싱 (Phase 4)**
   - [ ] apps/data_dashboard/infrastructure/file_parsers.py 파서 클래스 작성
   - [ ] 샘플 엑셀 파일로 파싱 테스트

### 5.2 Frontend 구현 순서

1. **프로젝트 초기화 (Phase 0)**
   - [ ] React 프로젝트 생성 (Create React App)
   - [ ] package.json 라이브러리 설치
   - [ ] .env 파일 작성 (Clerk Publishable Key)
   - [ ] Clerk ClerkProvider 설정

2. **공통 모듈 구현 (Phase 1)**
   - [ ] api/client.js Axios 인스턴스 작성
   - [ ] hooks/useAuth.js 인증 훅 작성
   - [ ] hooks/useApiClient.js API 클라이언트 훅 작성
   - [ ] styles/theme.js MUI 테마 작성
   - [ ] App.jsx에서 ThemeProvider 설정

3. **공통 컴포넌트 (Phase 2)**
   - [ ] components/common/ 기본 컴포넌트 작성
   - [ ] components/charts/ 차트 컴포넌트 작성
   - [ ] Chart.js 라이브러리 설정 확인

4. **레이아웃 (Phase 3)**
   - [ ] layouts/MainLayout.jsx 메인 레이아웃 작성
   - [ ] layouts/AuthLayout.jsx 인증 레이아웃 작성
   - [ ] 라우팅 설정 (React Router)

5. **유틸리티 (Phase 4)**
   - [ ] utils/formatters.js 포맷팅 함수 작성
   - [ ] utils/validators.js 검증 함수 작성
   - [ ] services/dataTransformer.js 데이터 변환 함수 작성

### 5.3 검증 체크리스트

#### Backend 검증

- [ ] **인증**: Clerk Webhook 이벤트 수신 및 User 생성 확인
- [ ] **미들웨어**: Authorization 헤더 검증 및 request.user 주입 확인
- [ ] **모델**: 모든 테이블 생성 및 제약 조건 확인
- [ ] **파싱**: 엑셀 파일 업로드 및 파싱 성공 확인
- [ ] **API**: 샘플 API 엔드포인트 호출 테스트

#### Frontend 검증

- [ ] **인증**: Clerk 로그인 및 토큰 획득 확인
- [ ] **API**: Backend API 호출 및 응답 수신 확인
- [ ] **레이아웃**: MainLayout 헤더, 사이드바 렌더링 확인
- [ ] **차트**: 샘플 데이터로 차트 렌더링 확인
- [ ] **테마**: MUI 테마 적용 확인

---

## 6. 페이지 개발 가이드라인

### 6.1 Backend 페이지 개발 시 주의사항

**각 페이지(API 엔드포인트)는 다음 구조를 따라야 합니다:**

```
apps/data_dashboard/
├── presentation/
│   ├── views.py              # API 엔드포인트 (ViewSet)
│   ├── serializers.py        # 직렬화/역직렬화
│   └── urls.py               # URL 라우팅
├── application/
│   └── use_cases.py          # 유스케이스 (비즈니스 흐름)
├── domain/
│   └── services.py           # 비즈니스 로직
└── infrastructure/
    └── repositories.py       # 데이터 저장소 인터페이스
```

**공통 모듈 사용 규칙:**
1. **예외 처리**: `core.exceptions`의 커스텀 예외 사용
2. **인증**: 미들웨어가 자동으로 `request.user` 주입
3. **페이지네이션**: 리스트 API는 `core.pagination.StandardResultsSetPagination` 사용
4. **유틸리티**: `utils/` 모듈 활용
5. **모델**: `apps/data_dashboard/models.py`의 정의된 모델만 사용

### 6.2 Frontend 페이지 개발 시 주의사항

**각 페이지는 다음 구조를 따라야 합니다:**

```jsx
// pages/ExamplePage.jsx
import { MainLayout } from '../layouts/MainLayout';
import { useApiClient } from '../hooks/useApiClient';
import { KPICard } from '../components/charts/KPICard';
import { transformToBarChartData } from '../services/dataTransformer';

const ExamplePage = () => {
  const { getAuthenticatedClient } = useApiClient();
  const [data, setData] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      const client = await getAuthenticatedClient();
      const response = await client.get('/endpoint/');
      setData(response.data);
    };
    fetchData();
  }, []);

  return (
    <MainLayout>
      {/* 페이지 컨텐츠 */}
    </MainLayout>
  );
};

export default ExamplePage;
```

**공통 모듈 사용 규칙:**
1. **레이아웃**: 모든 대시보드 페이지는 `MainLayout` 사용
2. **API 호출**: `useApiClient` 훅으로 인증된 클라이언트 사용
3. **차트**: `components/charts/` 컴포넌트 사용
4. **데이터 변환**: `services/dataTransformer.js` 함수 사용
5. **포맷팅**: `utils/formatters.js` 함수 사용

---

## 7. 코드 충돌 방지 전략

### 7.1 Backend 충돌 방지

**각 개발자가 작업할 파일 영역:**

| 페이지 | 작업 파일 | 공통 모듈 (읽기만) |
|--------|-----------|-------------------|
| 메인 대시보드 | presentation/views.py (DashboardViewSet) | models.py, core/*, utils/* |
| 실적 분석 | presentation/views.py (PerformanceViewSet) | models.py, core/*, utils/* |
| 논문 분석 | presentation/views.py (PapersViewSet) | models.py, core/*, utils/* |
| 학생 분석 | presentation/views.py (StudentsViewSet) | models.py, core/*, utils/* |
| 예산 분석 | presentation/views.py (BudgetViewSet) | models.py, core/*, utils/* |
| 데이터 업로드 | presentation/views.py (UploadViewSet) | models.py, file_parsers.py, core/*, utils/* |

**규칙:**
- 공통 모듈은 **읽기 전용**
- 각 ViewSet은 **별도의 클래스**로 정의
- URL 라우팅은 **별도의 router**로 등록

### 7.2 Frontend 충돌 방지

**각 개발자가 작업할 파일 영역:**

| 페이지 | 작업 파일 | 공통 모듈 (읽기만) |
|--------|-----------|-------------------|
| 로그인 | pages/LoginPage.jsx | AuthLayout, useAuth |
| 메인 대시보드 | pages/DashboardPage.jsx | MainLayout, useApiClient, charts/*, dataTransformer |
| 실적 분석 | pages/PerformancePage.jsx | MainLayout, useApiClient, charts/*, dataTransformer |
| 논문 분석 | pages/PapersPage.jsx | MainLayout, useApiClient, charts/*, dataTransformer |
| 학생 분석 | pages/StudentsPage.jsx | MainLayout, useApiClient, charts/*, dataTransformer |
| 예산 분석 | pages/BudgetPage.jsx | MainLayout, useApiClient, charts/*, dataTransformer |
| 데이터 업로드 | pages/UploadPage.jsx | MainLayout, useApiClient, Table, validators |

**규칙:**
- 공통 모듈은 **읽기 전용**
- 각 페이지는 **pages/ 디렉토리 내 별도 파일**
- 라우팅은 **App.jsx에서 한 번에 정의**

---

## 8. 환경 변수 및 설정

### 8.1 Backend 환경 변수

**파일**: `backend/.env`

```bash
# Django
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DB_NAME=university_dashboard
DB_USER=postgres
DB_PASSWORD=your-password
DB_HOST=localhost
DB_PORT=5432

# Clerk
CLERK_SECRET_KEY=sk_live_YOUR_CLERK_SECRET_KEY
CLERK_WEBHOOK_SECRET=whsec_YOUR_CLERK_WEBHOOK_SECRET

# CORS
CORS_ALLOWED_ORIGINS=http://localhost:3000
```

### 8.2 Frontend 환境 변수

**파일**: `frontend/.env`

```bash
# API
REACT_APP_API_BASE_URL=http://localhost:8000/api

# Clerk
REACT_APP_CLERK_PUBLISHABLE_KEY=pk_live_YOUR_CLERK_PUBLISHABLE_KEY
```

---

## 9. 최종 검증 체크리스트

### 9.1 공통 모듈 완성도 검증

**Backend:**
- [ ] config/settings/ 모든 환경 설정 완료
- [ ] core/ 모든 공통 유틸리티 완료
- [ ] apps/users/ 인증 관련 모든 기능 완료
- [ ] apps/data_dashboard/models.py 모든 모델 정의 완료
- [ ] apps/data_dashboard/infrastructure/file_parsers.py 모든 파서 완료
- [ ] utils/ 모든 유틸리티 함수 완료

**Frontend:**
- [ ] api/client.js Axios 설정 완료
- [ ] hooks/ 모든 커스텀 훅 완료
- [ ] components/common/ 모든 공통 컴포넌트 완료
- [ ] components/charts/ 모든 차트 컴포넌트 완료
- [ ] layouts/ 모든 레이아웃 완료
- [ ] services/dataTransformer.js 모든 변환 함수 완료
- [ ] utils/ 모든 유틸리티 함수 완료
- [ ] styles/theme.js 테마 설정 완료

### 9.2 병렬 개발 준비도 검증

**다음 질문에 모두 "예"라고 답할 수 있어야 합니다:**

1. [ ] Backend: 각 페이지 개발자가 공통 모델을 수정 없이 사용할 수 있는가?
2. [ ] Backend: 각 ViewSet이 독립적으로 작성 가능한가?
3. [ ] Backend: 공통 예외 처리가 모든 곳에서 동일하게 작동하는가?
4. [ ] Frontend: 각 페이지 개발자가 공통 컴포넌트를 수정 없이 사용할 수 있는가?
5. [ ] Frontend: 각 페이지가 MainLayout 없이 독립적으로 개발 가능한가?
6. [ ] Frontend: API 호출 로직이 표준화되어 있는가?
7. [ ] Frontend: 차트 컴포넌트가 모든 페이지에서 동일하게 작동하는가?
8. [ ] 공통: 환경 변수가 모두 정의되어 있는가?
9. [ ] 공통: README 또는 개발 가이드 문서가 작성되어 있는가?
10. [ ] 공통: Git 브랜치 전략이 정의되어 있는가?

### 9.3 최종 검증 (3회 반복 확인)

**1차 검증:**
- [ ] Backend 공통 모듈이 모든 페이지 개발에 충분한가?
- [ ] Frontend 공통 모듈이 모든 페이지 개발에 충분한가?
- [ ] 코드 충돌이 발생할 가능성이 있는가?

**2차 검증:**
- [ ] 페이지별 의존성 맵이 정확한가?
- [ ] 공통 모듈 수정 없이 페이지 개발이 가능한가?
- [ ] 누락된 공통 모듈이 있는가?

**3차 검증:**
- [ ] 모든 공통 모듈이 문서에 명시되어 있는가?
- [ ] 개발 가이드라인이 명확한가?
- [ ] 병렬 개발 시작 조건이 충족되었는가?

---

## 10. 요약

### 10.1 공통 모듈 개수

**Backend:**
- 설정 파일: 3개 (base, dev, prod)
- 공통 유틸리티: 4개 (exceptions, middleware, pagination, utils)
- 인증 관련: 5개 (User 모델, Repository, Service, UseCase, Webhook)
- 데이터 모델: 5개 (DepartmentKPI, Publication, Student, ResearchBudgetData, UploadHistory)
- 파일 파싱: 4개 (DepartmentKPIParser, PublicationParser, StudentParser, ResearchBudgetParser)
- **총 21개 파일**

**Frontend:**
- API 클라이언트: 2개 (client, hooks)
- 공통 컴포넌트: 4개 (Button, Card, Table, Loading)
- 차트 컴포넌트: 4개 (BarChart, LineChart, PieChart, KPICard)
- 레이아웃: 2개 (MainLayout, AuthLayout)
- 유틸리티: 3개 (formatters, validators, dataTransformer)
- 스타일: 1개 (theme)
- **총 16개 파일**

### 10.2 병렬 개발 가능 페이지

**Backend (API):**
1. 회원가입/로그인 (Clerk Webhook)
2. 메인 대시보드 (DashboardViewSet)
3. 실적 분석 (PerformanceViewSet)
4. 논문 분석 (PapersViewSet)
5. 학생 분석 (StudentsViewSet)
6. 예산 분석 (BudgetViewSet)
7. 데이터 업로드 (UploadViewSet)
8. 업로드 히스토리 (UploadHistoryViewSet)

**Frontend:**
1. 로그인 페이지 (LoginPage)
2. 회원가입 페이지 (SignUpPage)
3. 메인 대시보드 (DashboardPage)
4. 실적 분석 (PerformancePage)
5. 논문 분석 (PapersPage)
6. 학생 분석 (StudentsPage)
7. 예산 분석 (BudgetPage)
8. 데이터 업로드 (UploadPage)

**총 16개 페이지를 병렬로 개발 가능**

---

## 부록: 참조 문서

- [PRD](/Users/paul/edu/awesomedev/final_report/docs/prd.md)
- [Userflow](/Users/paul/edu/awesomedev/final_report/docs/userflow.md)
- [Database](/Users/paul/edu/awesomedev/final_report/docs/database.md)
- [Architecture](/Users/paul/edu/awesomedev/final_report/docs/architecture.md)
- [Tech Stack](/Users/paul/edu/awesomedev/final_report/docs/techstack.md)
- [Clerk 연동 가이드](/Users/paul/edu/awesomedev/final_report/docs/external/clerk.md)
