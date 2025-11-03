"""
Excel file parsers for different data types.
Following the common-modules.md specification.
Implements parser classes for all 4 data file types.
"""
import logging
import pandas as pd
from typing import List, Dict
from core.exceptions import FileProcessingError

logger = logging.getLogger(__name__)


class ExcelParser:
    """
    Base Excel file parser class.
    Provides common functionality for all parser implementations.
    """

    def parse(self, file_path: str) -> pd.DataFrame:
        """
        Parse Excel or CSV file to DataFrame.

        Args:
            file_path: Path to Excel or CSV file

        Returns:
            Parsed DataFrame

        Raises:
            FileProcessingError: If parsing fails
        """
        try:
            # Detect file type by extension
            if file_path.lower().endswith('.csv'):
                df = pd.read_csv(file_path)
                logger.info(f"Successfully parsed CSV file: {file_path}")
            else:
                df = pd.read_excel(file_path)
                logger.info(f"Successfully parsed Excel file: {file_path}")
            return df
        except Exception as e:
            logger.error(f"Failed to parse file {file_path}: {e}")
            raise FileProcessingError(f"Failed to parse file: {e}")

    def validate_columns(self, df: pd.DataFrame, required_columns: List[str]) -> bool:
        """
        Validate that all required columns exist in DataFrame.

        Args:
            df: DataFrame to validate
            required_columns: List of required column names

        Returns:
            True if all columns exist

        Raises:
            FileProcessingError: If required columns are missing
        """
        missing_columns = set(required_columns) - set(df.columns)
        if missing_columns:
            error_msg = f"Missing required columns: {missing_columns}"
            logger.error(error_msg)
            raise FileProcessingError(error_msg)
        return True

    def validate_data_types(self, df: pd.DataFrame, type_mapping: Dict) -> List[Dict]:
        """
        Validate data types match expected schema.

        Args:
            df: DataFrame to validate
            type_mapping: Dictionary mapping column names to expected types

        Returns:
            List of validation errors (empty if all valid)
        """
        errors = []
        for col, expected_type in type_mapping.items():
            if col not in df.columns:
                continue

            for idx, value in df[col].items():
                if pd.isna(value):
                    continue

                try:
                    if expected_type == int:
                        int(value)
                    elif expected_type == float:
                        float(value)
                    elif expected_type == str:
                        str(value)
                except (ValueError, TypeError):
                    errors.append({
                        'row': idx + 2,  # +2 for Excel (1-indexed) and header row
                        'column': col,
                        'message': f"Invalid data type. Expected {expected_type.__name__}, got {type(value).__name__}",
                        'severity': 'error'
                    })
        return errors

    def detect_duplicates(self, df: pd.DataFrame, unique_columns: List[str]) -> List[int]:
        """
        Detect duplicate rows based on unique columns.

        Args:
            df: DataFrame to check
            unique_columns: List of column names that should be unique together

        Returns:
            List of row indices that are duplicates
        """
        if not unique_columns:
            return []

        # Find duplicates based on unique columns
        mask = df.duplicated(subset=unique_columns, keep='first')
        duplicate_indices = df[mask].index.tolist()

        if duplicate_indices:
            logger.warning(f"Found {len(duplicate_indices)} duplicate rows based on columns {unique_columns}")

        return duplicate_indices

    def clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Clean whitespace and handle null values.

        Args:
            df: DataFrame to clean

        Returns:
            Cleaned DataFrame
        """
        # Strip whitespace from string columns
        for col in df.select_dtypes(include=['object']).columns:
            df[col] = df[col].apply(lambda x: x.strip() if isinstance(x, str) else x)

        return df

    def parse_to_dict(self, file_path: str, required_columns: List[str]) -> List[Dict]:
        """
        Parse Excel file and convert to list of dictionaries.

        Args:
            file_path: Path to Excel file
            required_columns: List of required column names

        Returns:
            List of dictionaries representing rows

        Raises:
            FileProcessingError: If parsing or validation fails
        """
        df = self.parse(file_path)
        self.validate_columns(df, required_columns)

        # Clean data
        df = self.clean_data(df)

        # Replace NaN with None for JSON compatibility
        df = df.where(pd.notnull(df), None)

        return df.to_dict('records')


class DepartmentKPIParser(ExcelParser):
    """
    Parser for Department KPI Excel files.
    Expects columns: year, college, department, employment_rate, full_time_faculty,
                     visiting_faculty, tech_transfer_revenue, intl_conference_count
    Supports both English and Korean column names.
    """

    REQUIRED_COLUMNS = [
        'year',
        'college',
        'department',
        'employment_rate',
        'full_time_faculty',
        'visiting_faculty',
        'tech_transfer_revenue',
        'intl_conference_count'
    ]

    # Korean to English column mapping
    COLUMN_MAPPING = {
        '연도': 'year',
        '평가년도': 'year',  # Alternative column name
        '단과대학': 'college',
        '학과': 'department',
        '취업률': 'employment_rate',
        '졸업생 취업률 (%)': 'employment_rate',  # Alternative column name
        '전임교원수': 'full_time_faculty',
        '전임교원 수 (명)': 'full_time_faculty',  # Alternative column name
        '겸임교원수': 'visiting_faculty',
        '초빙교원 수 (명)': 'visiting_faculty',  # Alternative column name
        '기술이전수익': 'tech_transfer_revenue',
        '연간 기술이전 수입액 (억원)': 'tech_transfer_revenue',  # Alternative column name
        '국제학술대회수': 'intl_conference_count',
        '국제학술대회 개최 횟수': 'intl_conference_count'  # Alternative column name
    }

    def translate_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Translate Korean column names to English.

        Args:
            df: DataFrame with potentially Korean column names

        Returns:
            DataFrame with English column names
        """
        columns_renamed = {}
        for col in df.columns:
            if col in self.COLUMN_MAPPING:
                columns_renamed[col] = self.COLUMN_MAPPING[col]

        if columns_renamed:
            logger.info(f"Translating Korean columns: {columns_renamed}")
            df = df.rename(columns=columns_renamed)

        return df

    def parse_to_dict(self, file_path: str) -> List[Dict]:
        """
        Parse Department KPI Excel file.

        Args:
            file_path: Path to Excel file

        Returns:
            List of dictionaries with department KPI data
        """
        logger.info(f"Parsing Department KPI file: {file_path}")

        # Parse file first
        df = self.parse(file_path)

        # Translate Korean columns if present
        df = self.translate_columns(df)

        # Validate columns (now in English)
        self.validate_columns(df, self.REQUIRED_COLUMNS)

        # Clean data
        df = self.clean_data(df)

        # Replace NaN with None for JSON compatibility
        df = df.where(pd.notnull(df), None)

        return df.to_dict('records')


class PublicationParser(ExcelParser):
    """
    Parser for Publication List Excel files.
    Expects columns: publication_id, publication_date, college, department, title,
                     primary_author, co_authors, journal_name, journal_grade,
                     impact_factor, is_project_linked
    Supports both English and Korean column names.
    """

    REQUIRED_COLUMNS = [
        'publication_id',
        'publication_date',
        'college',
        'department',
        'title',
        'primary_author',
        'co_authors',
        'journal_name',
        'journal_grade',
        'impact_factor',
        'is_project_linked'
    ]

    # Korean to English column mapping
    COLUMN_MAPPING = {
        '논문ID': 'publication_id',
        '게재일': 'publication_date',
        '발행일자': 'publication_date',  # Alternative column name
        '단과대학': 'college',
        '학과': 'department',
        '논문제목': 'title',
        '제목': 'title',  # Alternative column name
        '주저자': 'primary_author',
        '참여저자': 'co_authors',
        '공동저자': 'co_authors',  # Alternative column name
        '학술지명': 'journal_name',
        '저널명': 'journal_name',  # Alternative column name
        '저널등급': 'journal_grade',
        'Impact Factor': 'impact_factor',
        '임팩트팩터': 'impact_factor',  # Alternative column name
        '과제연계여부': 'is_project_linked'
    }

    def translate_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Translate Korean column names to English.

        Args:
            df: DataFrame with potentially Korean column names

        Returns:
            DataFrame with English column names
        """
        columns_renamed = {}
        for col in df.columns:
            if col in self.COLUMN_MAPPING:
                columns_renamed[col] = self.COLUMN_MAPPING[col]

        if columns_renamed:
            logger.info(f"Translating Korean columns: {columns_renamed}")
            df = df.rename(columns=columns_renamed)

        return df

    def parse_to_dict(self, file_path: str) -> List[Dict]:
        """
        Parse Publication Excel file.

        Args:
            file_path: Path to Excel file

        Returns:
            List of dictionaries with publication data
        """
        logger.info(f"Parsing Publication file: {file_path}")

        # Parse file first
        df = self.parse(file_path)

        # Translate Korean columns if present
        df = self.translate_columns(df)

        # Validate columns (now in English)
        self.validate_columns(df, self.REQUIRED_COLUMNS)

        # Clean data
        df = self.clean_data(df)

        # Replace NaN with None for JSON compatibility
        df = df.where(pd.notnull(df), None)

        data = df.to_dict('records')

        # Convert publication_date to string format and handle NaN values
        for item in data:
            if item.get('publication_date'):
                if isinstance(item['publication_date'], pd.Timestamp):
                    item['publication_date'] = item['publication_date'].strftime('%Y-%m-%d')

            # Convert is_project_linked to boolean
            if 'is_project_linked' in item and item['is_project_linked'] is not None:
                # Handle various boolean representations
                val = item['is_project_linked']
                if isinstance(val, str):
                    item['is_project_linked'] = val.upper() in ('Y', 'YES', 'TRUE', '1')
                else:
                    item['is_project_linked'] = bool(val)
            else:
                item['is_project_linked'] = False

            # Explicitly handle NaN values for numeric fields
            # impact_factor can be None (null=True in model)
            if 'impact_factor' in item:
                val = item['impact_factor']
                if pd.isna(val):  # Check for NaN
                    item['impact_factor'] = None

        return data


class StudentParser(ExcelParser):
    """
    Parser for Student Roster Excel files.
    Expects columns: student_id, name, college, department, grade, program_type,
                     enrollment_status, gender, admission_year, advisor, email
    Supports both English and Korean column names.
    """

    REQUIRED_COLUMNS = [
        'student_id',
        'name',
        'college',
        'department',
        'grade',
        'program_type',
        'enrollment_status',
        'gender',
        'admission_year',
        'advisor',
        'email'
    ]

    # Korean to English column mapping
    COLUMN_MAPPING = {
        '학번': 'student_id',
        '이름': 'name',
        '단과대학': 'college',
        '학과': 'department',
        '학년': 'grade',
        '과정구분': 'program_type',
        '학적상태': 'enrollment_status',
        '성별': 'gender',
        '입학년도': 'admission_year',
        '지도교수': 'advisor',
        '이메일': 'email'
    }

    def translate_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Translate Korean column names to English.

        Args:
            df: DataFrame with potentially Korean column names

        Returns:
            DataFrame with English column names
        """
        # Create reverse mapping for any columns that match Korean names
        columns_renamed = {}
        for col in df.columns:
            if col in self.COLUMN_MAPPING:
                columns_renamed[col] = self.COLUMN_MAPPING[col]

        if columns_renamed:
            logger.info(f"Translating Korean columns: {columns_renamed}")
            df = df.rename(columns=columns_renamed)

        return df

    def parse_to_dict(self, file_path: str) -> List[Dict]:
        """
        Parse Student Excel file.

        Args:
            file_path: Path to Excel file

        Returns:
            List of dictionaries with student data
        """
        logger.info(f"Parsing Student file: {file_path}")

        # Parse file first
        df = self.parse(file_path)

        # Translate Korean columns if present
        df = self.translate_columns(df)

        # Validate columns (now in English)
        self.validate_columns(df, self.REQUIRED_COLUMNS)

        # Clean data
        df = self.clean_data(df)

        # Replace NaN with None for JSON compatibility
        df = df.where(pd.notnull(df), None)

        return df.to_dict('records')


class ResearchBudgetParser(ExcelParser):
    """
    Parser for Research Project Data Excel files.
    Expects columns: execution_id, project_number, project_name, principal_investigator,
                     department, funding_agency, total_budget, execution_date,
                     execution_item, execution_amount, status, note
    Supports both English and Korean column names.
    """

    REQUIRED_COLUMNS = [
        'execution_id',
        'project_number',
        'project_name',
        'principal_investigator',
        'department',
        'funding_agency',
        'total_budget',
        'execution_date',
        'execution_item',
        'execution_amount',
        'status',
        'note'
    ]

    # Korean to English column mapping
    COLUMN_MAPPING = {
        '집행ID': 'execution_id',
        '과제번호': 'project_number',
        '과제명': 'project_name',
        '연구책임자': 'principal_investigator',
        '소속학과': 'department',
        '지원기관': 'funding_agency',
        '총연구비': 'total_budget',
        '집행일자': 'execution_date',
        '집행항목': 'execution_item',
        '집행금액': 'execution_amount',
        '상태': 'status',
        '비고': 'note'
    }

    def translate_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Translate Korean column names to English.

        Args:
            df: DataFrame with potentially Korean column names

        Returns:
            DataFrame with English column names
        """
        # Create reverse mapping for any columns that match Korean names
        columns_renamed = {}
        for col in df.columns:
            if col in self.COLUMN_MAPPING:
                columns_renamed[col] = self.COLUMN_MAPPING[col]

        if columns_renamed:
            logger.info(f"Translating Korean columns: {columns_renamed}")
            df = df.rename(columns=columns_renamed)

        return df

    def parse_to_dict(self, file_path: str) -> List[Dict]:
        """
        Parse Research Budget Excel file.

        Args:
            file_path: Path to Excel file

        Returns:
            List of dictionaries with research budget data
        """
        logger.info(f"Parsing Research Budget file: {file_path}")

        # Parse file first
        df = self.parse(file_path)

        # Translate Korean columns if present
        df = self.translate_columns(df)

        # Validate columns (now in English)
        self.validate_columns(df, self.REQUIRED_COLUMNS)

        # Clean data
        df = self.clean_data(df)

        # Replace NaN with None for JSON compatibility
        df = df.where(pd.notnull(df), None)

        data = df.to_dict('records')

        # Convert execution_date to string format
        for item in data:
            if item.get('execution_date'):
                if isinstance(item['execution_date'], pd.Timestamp):
                    item['execution_date'] = item['execution_date'].strftime('%Y-%m-%d')

        return data


class ParserFactory:
    """
    Factory class for creating appropriate parser based on file type.
    Follows OCP (Open/Closed Principle) - easy to extend with new parsers.
    """

    @staticmethod
    def get_parser(file_type: str) -> ExcelParser:
        """
        Get appropriate parser for given file type.

        Args:
            file_type: Type of file ('department_kpi', 'publication_list',
                      'student_roster', 'research_project_data')

        Returns:
            Appropriate parser instance

        Raises:
            FileProcessingError: If file type is unknown
        """
        parsers = {
            'department_kpi': DepartmentKPIParser,
            'publication_list': PublicationParser,
            'student_roster': StudentParser,
            'research_project_data': ResearchBudgetParser
        }

        parser_class = parsers.get(file_type)
        if not parser_class:
            raise FileProcessingError(
                f"Unknown file type: {file_type}. "
                f"Supported types: {', '.join(parsers.keys())}"
            )

        return parser_class()

    @staticmethod
    def detect_file_type(columns: List[str]) -> str:
        """
        Detect file type based on column names.
        Supports both English and Korean column names.

        Args:
            columns: List of column names from Excel file

        Returns:
            Detected file type

        Raises:
            FileProcessingError: If file type cannot be determined
        """
        column_set = set(columns)

        # Check each parser's required columns (English)
        if set(DepartmentKPIParser.REQUIRED_COLUMNS).issubset(column_set):
            return 'department_kpi'
        elif set(PublicationParser.REQUIRED_COLUMNS).issubset(column_set):
            return 'publication_list'
        elif set(StudentParser.REQUIRED_COLUMNS).issubset(column_set):
            return 'student_roster'
        elif set(ResearchBudgetParser.REQUIRED_COLUMNS).issubset(column_set):
            return 'research_project_data'

        # Check for Korean column names by translating and checking if all required columns are present
        # Try DepartmentKPIParser
        parser = DepartmentKPIParser()
        df_temp = pd.DataFrame(columns=columns)
        df_translated = parser.translate_columns(df_temp)
        if set(DepartmentKPIParser.REQUIRED_COLUMNS).issubset(set(df_translated.columns)):
            logger.info("Detected Korean column names for department KPI")
            return 'department_kpi'

        # Try PublicationParser
        parser = PublicationParser()
        df_temp = pd.DataFrame(columns=columns)
        df_translated = parser.translate_columns(df_temp)
        if set(PublicationParser.REQUIRED_COLUMNS).issubset(set(df_translated.columns)):
            logger.info("Detected Korean column names for publication list")
            return 'publication_list'

        # Try StudentParser
        parser = StudentParser()
        df_temp = pd.DataFrame(columns=columns)
        df_translated = parser.translate_columns(df_temp)
        if set(StudentParser.REQUIRED_COLUMNS).issubset(set(df_translated.columns)):
            logger.info("Detected Korean column names for student roster")
            return 'student_roster'

        # Try ResearchBudgetParser
        parser = ResearchBudgetParser()
        df_temp = pd.DataFrame(columns=columns)
        df_translated = parser.translate_columns(df_temp)
        if set(ResearchBudgetParser.REQUIRED_COLUMNS).issubset(set(df_translated.columns)):
            logger.info("Detected Korean column names for research project data")
            return 'research_project_data'

        # If no match found, raise error
        raise FileProcessingError(
            f"Could not detect file type from columns: {columns}. "
            "File must match one of the supported formats."
        )
