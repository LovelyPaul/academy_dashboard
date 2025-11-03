# Supabase 데이터베이스 설정 가이드

## 1. Supabase 프로젝트 설정

### 1.1 데이터베이스 연결 정보 확인

1. Supabase Dashboard 로그인: https://supabase.com/dashboard
2. 프로젝트 선택: `uzsexjgqglhwsbmrmymu`
3. **Settings** → **Database** 메뉴로 이동
4. **Connection string** 섹션에서 정보 확인

### 1.2 .env.local 파일 설정

`.env.local` 파일에 다음 정보가 설정되어 있는지 확인:

```env
# Supabase API Keys
NEXT_PUBLIC_SUPABASE_URL=https://uzsexjgqglhwsbmrmymu.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJhbGc...
SUPABASE_SERVICE_ROLE_KEY=eyJhbGc...
SUPABASE_URL=https://uzsexjgqglhwsbmrmymu.supabase.co

# Clerk Authentication
CLERK_SECRET_KEY=sk_test_...

# Supabase PostgreSQL Database (Direct Connection)
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=your_actual_password
DB_HOST=db.uzsexjgqglhwsbmrmymu.supabase.co
DB_PORT=5432
```

⚠️ **중요**: `DB_PASSWORD`를 실제 Supabase 데이터베이스 비밀번호로 변경하세요!

---

## 2. 데이터베이스 마이그레이션

### 방법 1: Supabase SQL Editor 사용 (권장)

가장 간단하고 안전한 방법입니다.

#### 단계:

1. **Supabase Dashboard**에서 **SQL Editor** 메뉴로 이동
2. **New query** 버튼 클릭
3. `supabase_migration.sql` 파일의 내용을 복사하여 붙여넣기
4. **Run** 버튼 클릭하여 실행
5. 실행 결과 확인:
   - 성공: "Success. No rows returned"
   - 또는 마지막 검증 쿼리 결과 표시

#### 생성되는 테이블:
- ✅ `users` - 사용자 계정 (Clerk 연동)
- ✅ `students` - 학생 명단
- ✅ `publications` - 논문 발표 데이터
- ✅ `research_budget_data` - 연구비 집행 데이터
- ✅ `department_kpis` - 학과별 KPI
- ✅ `upload_history` - 파일 업로드 이력
- ✅ `django_migrations` - Django 마이그레이션 기록

### 방법 2: Django Migration 명령 사용

데이터베이스 연결이 정상적으로 작동하는 경우 사용합니다.

```bash
# 가상환경 활성화
source venv/bin/activate

# 환경변수 설정
export DJANGO_SETTINGS_MODULE=config.settings.dev

# 마이그레이션 적용
python manage.py migrate

# 결과 확인
python manage.py showmigrations
```

---

## 3. 연결 테스트

### 3.1 Python 스크립트로 테스트

```bash
cd backend
source venv/bin/activate

python -c "
import os
import django
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv('.env.local')

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')
import sys
sys.path.insert(0, str(Path.cwd()))
django.setup()

from django.db import connection

# Test connection
with connection.cursor() as cursor:
    cursor.execute('SELECT version();')
    print('✅ Database connection successful!')
    print(f'PostgreSQL: {cursor.fetchone()[0][:80]}')

    cursor.execute('SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = \\'public\\';')
    table_count = cursor.fetchone()[0]
    print(f'✅ Tables in database: {table_count}')
"
```

### 3.2 Django 관리 명령으로 테스트

```bash
python manage.py dbshell
```

성공하면 PostgreSQL 프롬프트가 표시됩니다:
```
psql (14.x)
Type "help" for help.

postgres=>
```

테스트 쿼리:
```sql
-- 테이블 목록 확인
\dt

-- 특정 테이블 구조 확인
\d users
\d students
\d publications

-- 테이블 레코드 수 확인
SELECT 'users' as table_name, COUNT(*) FROM users
UNION ALL
SELECT 'students', COUNT(*) FROM students
UNION ALL
SELECT 'publications', COUNT(*) FROM publications
UNION ALL
SELECT 'research_budget_data', COUNT(*) FROM research_budget_data
UNION ALL
SELECT 'department_kpis', COUNT(*) FROM department_kpis
UNION ALL
SELECT 'upload_history', COUNT(*) FROM upload_history;

-- 종료
\q
```

---

## 4. 마이그레이션 파일 정보

### 생성된 Django 마이그레이션 파일:

1. **`apps/users/migrations/0001_initial.py`**
   - User 모델 생성
   - Clerk 연동 필드 (clerk_id)
   - 인덱스: clerk_id, email

2. **`apps/data_dashboard/migrations/0001_initial.py`**
   - 5개 모델 생성: DepartmentKPI, Publication, ResearchBudgetData, Student, UploadHistory
   - 기본 인덱스 설정

3. **`apps/data_dashboard/migrations/0002_initial.py`**
   - UploadHistory에 user 외래 키 추가
   - 추가 인덱스 생성
   - unique_together 제약 조건

### SQL 스크립트:

- **`supabase_migration.sql`**: Supabase SQL Editor에서 직접 실행 가능한 전체 마이그레이션 스크립트

---

## 5. 테이블 스키마

### 5.1 Users
```sql
- id (BIGSERIAL, PK)
- username (VARCHAR 150, UNIQUE)
- email (VARCHAR 254)
- clerk_id (VARCHAR 255, UNIQUE) -- Clerk 인증 ID
- role (VARCHAR 20) -- 'admin' or 'user'
- password, is_staff, is_active, date_joined 등
```

### 5.2 Students
```sql
- id (BIGSERIAL, PK)
- student_id (VARCHAR 20, UNIQUE)
- name (VARCHAR 100)
- college (VARCHAR 100)
- department (VARCHAR 100)
- grade (INTEGER) -- 0 for graduate school
- program_type (VARCHAR 50) -- '학사', '석사', '박사'
- enrollment_status (VARCHAR 50) -- '재학', '휴학', '졸업', etc.
- admission_year (INTEGER)
```

### 5.3 Publications
```sql
- id (BIGSERIAL, PK)
- publication_id (VARCHAR 50, UNIQUE)
- publication_date (DATE)
- title (TEXT)
- primary_author (VARCHAR 100)
- journal_name (VARCHAR 255)
- journal_grade (VARCHAR 50)
- impact_factor (NUMERIC 5,2)
```

### 5.4 Research Budget Data
```sql
- id (BIGSERIAL, PK)
- execution_id (VARCHAR 50, UNIQUE)
- project_number (VARCHAR 50)
- project_name (VARCHAR 255)
- principal_investigator (VARCHAR 100)
- total_budget (BIGINT) -- KRW
- execution_amount (BIGINT) -- KRW
- status (VARCHAR 50) -- '집행완료', '처리중', '취소'
```

### 5.5 Department KPIs
```sql
- id (BIGSERIAL, PK)
- year (INTEGER)
- college (VARCHAR 100)
- department (VARCHAR 100)
- employment_rate (NUMERIC 5,2)
- full_time_faculty (INTEGER)
- tech_transfer_revenue (NUMERIC 12,2)
- UNIQUE(year, college, department)
```

### 5.6 Upload History
```sql
- id (BIGSERIAL, PK)
- file_name (VARCHAR 255)
- file_type (VARCHAR 50)
- status (VARCHAR 50) -- 'success' or 'failed'
- records_processed (INTEGER)
- uploaded_at (TIMESTAMP)
- user_id (BIGINT, FK → users)
```

---

## 6. 트러블슈팅

### 문제 1: 연결 실패 (Host not found)
```
Error: could not translate host name to address
```

**해결책**:
1. `.env.local`의 `DB_HOST` 확인
2. Supabase Dashboard에서 정확한 호스트 주소 복사
3. 일반적으로: `db.{project-ref}.supabase.co`

### 문제 2: 인증 실패
```
Error: password authentication failed
```

**해결책**:
1. Supabase Dashboard → Settings → Database
2. "Reset database password" 클릭하여 새 비밀번호 생성
3. `.env.local`의 `DB_PASSWORD` 업데이트

### 문제 3: 연결 거부
```
Error: connection refused
```

**해결책**:
1. 포트 번호 확인 (Direct: 5432, Pooler: 6543)
2. `.env.local`의 `DB_PORT` 확인
3. Direct connection 사용 권장 (PORT=5432)

### 문제 4: 테이블이 이미 존재
```
Error: relation "users" already exists
```

**해결책**:
- SQL 스크립트는 `IF NOT EXISTS` 사용하므로 안전하게 재실행 가능
- 또는 Django migrate 명령 사용

---

## 7. 다음 단계

마이그레이션 완료 후:

1. ✅ **슈퍼유저 생성** (선택사항):
   ```bash
   python manage.py createsuperuser
   ```

2. ✅ **Django Admin 접속 테스트**:
   ```bash
   python manage.py runserver
   # http://localhost:8000/admin/ 접속
   ```

3. ✅ **API 테스트**:
   ```bash
   # 개발 서버 실행
   python manage.py runserver

   # API 엔드포인트 테스트
   curl http://localhost:8000/api/dashboard/students/
   ```

4. ✅ **단위 테스트 실행**:
   ```bash
   pytest apps/data_dashboard/tests/unit/ -v
   ```

---

## 8. 참고 자료

- [Supabase Documentation](https://supabase.com/docs)
- [Django Migrations](https://docs.djangoproject.com/en/4.2/topics/migrations/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)

---

**작성일**: 2025년 11월 3일
**업데이트**: 마이그레이션 파일 생성 완료
