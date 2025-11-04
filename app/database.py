import sqlite3
import os
from typing import List, Dict, Any
from app.models import Status, Location, Company, Department


class Database:
    def __init__(self, db_path: str = None):
        if db_path is None:
            db_path = "/tmp/employees.db" if os.path.exists("/tmp") else "employees.db"
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        print(f"📁 Initializing database at: {self.db_path}")

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS employees (
                id TEXT PRIMARY KEY,
                organization_id TEXT NOT NULL,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                email TEXT NOT NULL,
                status TEXT NOT NULL CHECK(status IN ('active', 'not_started', 'terminated')),
                department TEXT NOT NULL,
                location TEXT NOT NULL,
                company TEXT NOT NULL,
                position TEXT NOT NULL,
                phone TEXT,
                hire_date TEXT,
                termination_date TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        cursor.execute('CREATE INDEX IF NOT EXISTS idx_org_id ON employees(organization_id)')
        cursor.execute('CREATE INDEX idx_search_comprehensive ON employees(organization_id, status, department, location, company, position)')
        cursor.execute('CREATE INDEX idx_name ON employees(first_name, last_name)')

        # Insert sample data if empty
        cursor.execute('SELECT COUNT(*) FROM employees')
        if cursor.fetchone()[0] == 0:
            self.insert_sample_data(cursor)

        conn.commit()
        conn.close()

    def insert_sample_data(self, cursor):
        sample_employees = []

        positions = [
            "Software Engineer", "Senior Software Engineer", "Product Manager",
            "UX Designer", "Data Scientist", "DevOps Engineer", "QA Engineer",
            "Technical Lead", "Engineering Manager", "Frontend Developer",
            "Backend Developer", "Full Stack Developer", "System Architect"
        ]

        # Organization 1 sample data
        for i in range(200):
            status = Status.ACTIVE if i % 3 == 0 else Status.NOT_STARTED if i % 3 == 1 else Status.TERMINATED
            company = Company.HQ.value if i % 3 == 0 else Company.BRANCH_1.value if i % 3 == 1 else Company.BRANCH_2.value
            location = Location.NEW_YORK.value if i % 4 == 0 else Location.LONDON.value if i % 4 == 1 else Location.TOKYO.value if i % 4 == 2 else Location.VIETNAM.value
            department = Department.ENGINEERING.value if i % 5 == 0 else Department.MARKETING.value if i % 5 == 1 else Department.SALES.value if i % 5 == 2 else Department.HR.value if i % 5 == 3 else Department.FINANCE.value


            sample_employees.append((
                f"e_org1_{i}",
                f"Kha{i}",
                f"Phan{i}",
                f"kha.phan{i}@org1.com",
                status.value,
                department,
                location,
                company,
                positions[i % len(positions)],
                f"+1-555-{i:04d}",
                "2023-01-15",
                "2024-01-15" if status == Status.TERMINATED else None,
                "org_1"
            ))

        # Organization 2 sample data
        for i in range(200):
            company = Company.SUBSIDIARY_1.value if i % 2 == 0 else Company.SUBSIDIARY_2.value
            location = Location.LONDON.value if i % 3 == 0 else Location.BERLIN.value if i % 3 == 1 else Location.PARIS.value
            status = Status.ACTIVE if i % 4 == 0 else Status.NOT_STARTED if i % 4 == 1 else Status.TERMINATED
            department = Department.MARKETING.value if i % 4 == 0 else Department.SALES.value if i % 4 == 1 else Department.OPERATIONS.value if i % 4 == 2 else Department.IT.value

            sample_employees.append((
                f"emp_org2_{i}",
                f"andy{i}",
                f"Smith{i}",
                f"andy.nguyen{i}@org2.com",
                status.value,
                department,
                location,
                company,
                positions[(i + 5) % len(positions)],
                f"+44-20-{i:04d}",
                "2023-02-20",
                "2024-02-20" if status == Status.TERMINATED else None,
                "org_2"
            ))

        cursor.executemany('''
            INSERT INTO employees 
            (id, first_name, last_name, email, status, department, location, company, position, phone, hire_date, termination_date, organization_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', sample_employees)

    def search_employees(self, organization_id: str, filters: Dict[str, Any],
                         limit: int, offset: int) -> tuple[List[Dict[str, Any]], int]:

        where_conditions = ["organization_id = ?"]
        params = [organization_id]

        if filters.get('query'):
            where_conditions.append(
                "(first_name LIKE ? OR last_name LIKE ? OR email LIKE ? OR position LIKE ?)"
            )
            search_term = f"%{filters['query']}%"
            params.extend([search_term, search_term, search_term, search_term])

        if filters.get('status'):
            if isinstance(filters['status'], list):
                placeholders = ','.join(['?' for _ in filters['status']])
                where_conditions.append(f"status IN ({placeholders})")
                params.extend(filters['status'])
            else:
                where_conditions.append("status = ?")
                params.append(filters['status'])

        if filters.get('department'):
            if isinstance(filters['department'], list):
                placeholders = ','.join(['?' for _ in filters['department']])
                where_conditions.append(f"department IN ({placeholders})")
                params.extend(filters['department'])
            else:
                where_conditions.append("department = ?")
                params.append(filters['department'])

        if filters.get('location'):
            if isinstance(filters['location'], list):
                placeholders = ','.join(['?' for _ in filters['location']])
                where_conditions.append(f"location IN ({placeholders})")
                params.extend(filters['location'])
            else:
                where_conditions.append("location = ?")
                params.append(filters['location'])

        if filters.get('company'):
            if isinstance(filters['company'], list):
                placeholders = ','.join(['?' for _ in filters['company']])
                where_conditions.append(f"company IN ({placeholders})")
                params.extend(filters['company'])
            else:
                where_conditions.append("company = ?")
                params.append(filters['company'])

        if filters.get('position'):
            where_conditions.append("position LIKE ?")
            params.append(f"%{filters['position']}%")

        where_clause = " AND ".join(where_conditions)

        count_query = f"SELECT COUNT(*) FROM employees WHERE {where_clause}"

        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(count_query, params)
        total_count = cursor.fetchone()[0]

        search_query = f"""
            SELECT * FROM employees 
            WHERE {where_clause}
            ORDER BY first_name, last_name
            LIMIT ? OFFSET ?
        """
        params.extend([limit, offset])

        cursor.execute(search_query, params)
        rows = cursor.fetchall()

        employees = [dict(row) for row in rows]
        conn.close()

        return employees, total_count

    def get_available_filters(self, organization_id: str) -> Dict[str, List[str]]:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        available_filters = {}

        cursor.execute("SELECT DISTINCT status FROM employees WHERE organization_id = ? ORDER BY status", (organization_id,))
        available_filters['status'] = [row[0] for row in cursor.fetchall()]

        cursor.execute("SELECT DISTINCT location FROM employees WHERE organization_id = ? ORDER BY location", (organization_id,))
        available_filters['locations'] = [row[0] for row in cursor.fetchall()]

        cursor.execute("SELECT DISTINCT company FROM employees WHERE organization_id = ? ORDER BY company", (organization_id,))
        available_filters['companies'] = [row[0] for row in cursor.fetchall()]

        cursor.execute("SELECT DISTINCT department FROM employees WHERE organization_id = ? ORDER BY department", (organization_id,))
        available_filters['departments'] = [row[0] for row in cursor.fetchall()]

        cursor.execute("""
            SELECT DISTINCT position FROM employees 
            WHERE organization_id = ? 
            ORDER BY position
            LIMIT 20
        """, (organization_id,))
        available_filters['positions'] = [row[0] for row in cursor.fetchall()]

        conn.close()
        return available_filters


db = Database()
