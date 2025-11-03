-- ============================================================
-- Supabase Database Migration Script
-- Generated for University Dashboard Project
-- Date: 2025-11-03
-- ============================================================

-- ============================================================
-- PART 1: Users Table (from apps/users/migrations/0001_initial.py)
-- ============================================================

-- Create users table
CREATE TABLE IF NOT EXISTS users (
    id BIGSERIAL PRIMARY KEY,
    password VARCHAR(128) NOT NULL,
    last_login TIMESTAMP WITH TIME ZONE,
    is_superuser BOOLEAN NOT NULL DEFAULT FALSE,
    username VARCHAR(150) NOT NULL UNIQUE,
    first_name VARCHAR(150) NOT NULL DEFAULT '',
    last_name VARCHAR(150) NOT NULL DEFAULT '',
    email VARCHAR(254) NOT NULL DEFAULT '',
    is_staff BOOLEAN NOT NULL DEFAULT FALSE,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    date_joined TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    clerk_id VARCHAR(255) NOT NULL UNIQUE,
    role VARCHAR(20) NOT NULL DEFAULT 'user'
);

-- Create indexes for users table
CREATE INDEX IF NOT EXISTS users_clerk_i_2e31a7_idx ON users(clerk_id);
CREATE INDEX IF NOT EXISTS users_email_4b85f2_idx ON users(email);

-- Add comments for users table
COMMENT ON TABLE users IS 'User accounts synchronized with Clerk authentication';
COMMENT ON COLUMN users.clerk_id IS 'Clerk User ID for authentication';
COMMENT ON COLUMN users.role IS 'User role: admin or user';

-- ============================================================
-- PART 2: Data Dashboard Tables (from apps/data_dashboard/migrations/0001_initial.py)
-- ============================================================

-- Create department_kpis table
CREATE TABLE IF NOT EXISTS department_kpis (
    id BIGSERIAL PRIMARY KEY,
    year INTEGER NOT NULL,
    college VARCHAR(100) NOT NULL,
    department VARCHAR(100) NOT NULL,
    employment_rate NUMERIC(5, 2),
    full_time_faculty INTEGER,
    visiting_faculty INTEGER,
    tech_transfer_revenue NUMERIC(12, 2),
    intl_conference_count INTEGER,
    CONSTRAINT department_kpis_unique UNIQUE (year, college, department)
);

-- Create indexes for department_kpis table
CREATE INDEX IF NOT EXISTS department__year_4bff5e_idx ON department_kpis(year);
CREATE INDEX IF NOT EXISTS department__departm_460480_idx ON department_kpis(department);

-- Add comments for department_kpis table
COMMENT ON TABLE department_kpis IS 'Department KPI metrics by year';
COMMENT ON COLUMN department_kpis.employment_rate IS 'Employment rate (%)';
COMMENT ON COLUMN department_kpis.tech_transfer_revenue IS 'Technology transfer revenue (hundred million won)';

-- Create publications table
CREATE TABLE IF NOT EXISTS publications (
    id BIGSERIAL PRIMARY KEY,
    publication_id VARCHAR(50) NOT NULL UNIQUE,
    publication_date DATE NOT NULL,
    college VARCHAR(100) NOT NULL,
    department VARCHAR(100) NOT NULL,
    title TEXT NOT NULL,
    primary_author VARCHAR(100) NOT NULL,
    co_authors TEXT,
    journal_name VARCHAR(255) NOT NULL,
    journal_grade VARCHAR(50),
    impact_factor NUMERIC(5, 2),
    is_project_linked BOOLEAN NOT NULL DEFAULT FALSE
);

-- Create indexes for publications table
CREATE INDEX IF NOT EXISTS publication_publica_38baa4_idx ON publications(publication_date);
CREATE INDEX IF NOT EXISTS publication_journal_5dc8eb_idx ON publications(journal_grade);

-- Add comments for publications table
COMMENT ON TABLE publications IS 'Research publications and papers';
COMMENT ON COLUMN publications.co_authors IS 'Co-authors (semicolon-separated)';
COMMENT ON COLUMN publications.is_project_linked IS 'Whether linked to research project';

-- Create research_budget_data table
CREATE TABLE IF NOT EXISTS research_budget_data (
    id BIGSERIAL PRIMARY KEY,
    execution_id VARCHAR(50) NOT NULL UNIQUE,
    project_number VARCHAR(50) NOT NULL,
    project_name VARCHAR(255) NOT NULL,
    principal_investigator VARCHAR(100) NOT NULL,
    department VARCHAR(100) NOT NULL,
    funding_agency VARCHAR(255) NOT NULL,
    total_budget BIGINT NOT NULL,
    execution_date DATE NOT NULL,
    execution_item VARCHAR(255) NOT NULL,
    execution_amount BIGINT NOT NULL,
    status VARCHAR(50) NOT NULL,
    note TEXT
);

-- Create indexes for research_budget_data table
CREATE INDEX IF NOT EXISTS research_bu_project_5b4320_idx ON research_budget_data(project_number);
CREATE INDEX IF NOT EXISTS research_bu_departm_c4ec24_idx ON research_budget_data(department);
CREATE INDEX IF NOT EXISTS research_bu_executi_cc2b94_idx ON research_budget_data(execution_date);

-- Add comments for research_budget_data table
COMMENT ON TABLE research_budget_data IS 'Research project budget execution data';
COMMENT ON COLUMN research_budget_data.total_budget IS 'Total budget (KRW)';
COMMENT ON COLUMN research_budget_data.execution_amount IS 'Execution amount (KRW)';

-- Add check constraint for status
ALTER TABLE research_budget_data ADD CONSTRAINT research_budget_data_status_check
    CHECK (status IN ('집행완료', '처리중', '취소'));

-- Create students table
CREATE TABLE IF NOT EXISTS students (
    id BIGSERIAL PRIMARY KEY,
    student_id VARCHAR(20) NOT NULL UNIQUE,
    name VARCHAR(100) NOT NULL,
    college VARCHAR(100) NOT NULL,
    department VARCHAR(100) NOT NULL,
    grade INTEGER,
    program_type VARCHAR(50) NOT NULL,
    enrollment_status VARCHAR(50) NOT NULL,
    gender VARCHAR(10),
    admission_year INTEGER NOT NULL,
    advisor VARCHAR(100),
    email VARCHAR(254)
);

-- Create indexes for students table
CREATE INDEX IF NOT EXISTS students_departm_33c447_idx ON students(department);
CREATE INDEX IF NOT EXISTS students_enrollm_559cd0_idx ON students(enrollment_status);

-- Add comments for students table
COMMENT ON TABLE students IS 'Student roster and information';
COMMENT ON COLUMN students.grade IS 'Grade (0 for graduate school)';

-- Add check constraints for students
ALTER TABLE students ADD CONSTRAINT students_program_type_check
    CHECK (program_type IN ('학사', '석사', '박사'));

ALTER TABLE students ADD CONSTRAINT students_enrollment_status_check
    CHECK (enrollment_status IN ('재학', '휴학', '졸업', '자퇴', '제적'));

-- Create upload_history table
CREATE TABLE IF NOT EXISTS upload_history (
    id BIGSERIAL PRIMARY KEY,
    file_name VARCHAR(255) NOT NULL,
    file_type VARCHAR(50) NOT NULL,
    status VARCHAR(50) NOT NULL,
    records_processed INTEGER NOT NULL DEFAULT 0,
    error_message TEXT,
    uploaded_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    user_id BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE
);

-- Create indexes for upload_history table
CREATE INDEX IF NOT EXISTS upload_hist_uploade_2de21b_idx ON upload_history(uploaded_at DESC);

-- Add comments for upload_history table
COMMENT ON TABLE upload_history IS 'File upload history and processing status';

-- Add check constraints for upload_history
ALTER TABLE upload_history ADD CONSTRAINT upload_history_file_type_check
    CHECK (file_type IN ('department_kpi', 'publication_list', 'research_project_data', 'student_roster'));

ALTER TABLE upload_history ADD CONSTRAINT upload_history_status_check
    CHECK (status IN ('success', 'failed'));

-- ============================================================
-- PART 3: Django Required Tables
-- ============================================================

-- Create django_migrations table (required by Django)
CREATE TABLE IF NOT EXISTS django_migrations (
    id BIGSERIAL PRIMARY KEY,
    app VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    applied TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

-- Insert migration records
INSERT INTO django_migrations (app, name, applied) VALUES
    ('users', '0001_initial', NOW()),
    ('data_dashboard', '0001_initial', NOW()),
    ('data_dashboard', '0002_initial', NOW())
ON CONFLICT DO NOTHING;

-- ============================================================
-- PART 4: Sample Data (Optional - for testing)
-- ============================================================

-- You can add sample data here if needed for testing
-- Example:
-- INSERT INTO users (username, clerk_id, email, is_staff, is_active, role)
-- VALUES ('admin', 'clerk_test_admin', 'admin@example.com', true, true, 'admin');

-- ============================================================
-- PART 5: Verification Queries
-- ============================================================

-- Verify table creation
SELECT
    table_name,
    (SELECT COUNT(*) FROM information_schema.columns WHERE table_schema = 'public' AND columns.table_name = tables.table_name) as column_count
FROM information_schema.tables
WHERE table_schema = 'public'
    AND table_type = 'BASE TABLE'
    AND table_name IN ('users', 'department_kpis', 'publications', 'research_budget_data', 'students', 'upload_history')
ORDER BY table_name;

-- Verify indexes
SELECT
    tablename,
    indexname
FROM pg_indexes
WHERE schemaname = 'public'
    AND tablename IN ('users', 'department_kpis', 'publications', 'research_budget_data', 'students', 'upload_history')
ORDER BY tablename, indexname;

-- ============================================================
-- END OF MIGRATION SCRIPT
-- ============================================================

-- Notes:
-- 1. Run this script in Supabase SQL Editor
-- 2. All tables will be created with proper indexes and constraints
-- 3. Django migration records are automatically inserted
-- 4. You can verify successful migration using the verification queries at the end
