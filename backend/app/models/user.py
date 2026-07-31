from app import bcrypt, get_db_connection
from config import DEFAULT_ADMIN_EMAIL, DEFAULT_ADMIN_PASSWORD, DEFAULT_ADMIN_USERNAME


class User:
    VALID_ROLES = {'admin', 'user'}
    VALID_STATUSES = {'active', 'inactive'}

    @staticmethod
    def create_table():
        conn = get_db_connection()
        cur = conn.cursor()
        try:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    username VARCHAR(50) NOT NULL UNIQUE,
                    email VARCHAR(100) NOT NULL UNIQUE,
                    password VARCHAR(255) NOT NULL,
                    role VARCHAR(20) NOT NULL DEFAULT 'user',
                    status VARCHAR(20) NOT NULL DEFAULT 'active',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
            cur.execute("ALTER TABLE users ADD COLUMN IF NOT EXISTS role VARCHAR(20) NOT NULL DEFAULT 'user';")
            cur.execute("ALTER TABLE users ADD COLUMN IF NOT EXISTS status VARCHAR(20) NOT NULL DEFAULT 'active';")
            cur.execute("UPDATE users SET role = 'admin' WHERE LOWER(username) = 'admin';")
            conn.commit()
            print("[INFO] users table created or already exists.")
        except Exception as exc:
            conn.rollback()
            print(f"[ERROR] Failed to create users table: {exc}")
            raise
        finally:
            cur.close()
            conn.close()

    @staticmethod
    def _row_to_dict(row):
        if not row:
            return None
        return {
            'id': row[0],
            'username': row[1],
            'email': row[2],
            'password': row[3],
            'role': row[4],
            'status': row[5],
            'created_at': row[6]
        }

    @staticmethod
    def find_by_username(username):
        conn = get_db_connection()
        cur = conn.cursor()
        try:
            cur.execute("""
                SELECT id, username, email, password, role, status, created_at
                FROM users
                WHERE username = %s;
            """, (username,))
            return User._row_to_dict(cur.fetchone())
        finally:
            cur.close()
            conn.close()

    @staticmethod
    def find_by_email(email):
        conn = get_db_connection()
        cur = conn.cursor()
        try:
            cur.execute("""
                SELECT id, username, email, password, role, status, created_at
                FROM users
                WHERE email = %s;
            """, (email,))
            return User._row_to_dict(cur.fetchone())
        finally:
            cur.close()
            conn.close()

    @staticmethod
    def get_user_by_id(user_id):
        conn = get_db_connection()
        cur = conn.cursor()
        try:
            cur.execute("""
                SELECT id, username, email, password, role, status, created_at
                FROM users
                WHERE id = %s;
            """, (user_id,))
            return User._row_to_dict(cur.fetchone())
        finally:
            cur.close()
            conn.close()

    @staticmethod
    def create_user(username, email, password, role='user', status='active'):
        if username and username.strip().lower() == 'admin':
            role = 'admin'
        role = role if role in User.VALID_ROLES else 'user'
        status = status if status in User.VALID_STATUSES else 'active'
        conn = get_db_connection()
        cur = conn.cursor()
        hashed_pw = bcrypt.generate_password_hash(password).decode('utf-8')
        try:
            cur.execute("""
                INSERT INTO users (username, email, password, role, status)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id;
            """, (username, email, hashed_pw, role, status))
            user_id = cur.fetchone()[0]
            conn.commit()
            return user_id
        except Exception as exc:
            conn.rollback()
            print(f"[ERROR] Failed to create user: {exc}")
            return None
        finally:
            cur.close()
            conn.close()

    @staticmethod
    def ensure_admin_role(username):
        if not username or username.strip().lower() != 'admin':
            return

        conn = get_db_connection()
        cur = conn.cursor()
        try:
            cur.execute("""
                UPDATE users
                SET role = 'admin'
                WHERE LOWER(username) = 'admin'
                  AND role <> 'admin';
            """)
            conn.commit()
        except Exception as exc:
            conn.rollback()
            print(f"[ERROR] Failed to ensure admin role: {exc}")
        finally:
            cur.close()
            conn.close()

    @staticmethod
    def get_all_users(search='', role='', status=''):
        conn = get_db_connection()
        cur = conn.cursor()
        conditions = []
        params = []

        if search:
            conditions.append("(u.username ILIKE %s OR u.email ILIKE %s)")
            params.extend([f"%{search}%", f"%{search}%"])
        if role:
            conditions.append("u.role = %s")
            params.append(role)
        if status:
            conditions.append("u.status = %s")
            params.append(status)

        where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else ''

        try:
            cur.execute(f"""
                SELECT
                    u.id,
                    u.username,
                    u.email,
                    u.role,
                    u.status,
                    u.created_at,
                    COUNT(d.id) AS detection_count,
                    COALESCE(SUM(CASE
                        WHEN LOWER(COALESCE(d.predicted_class, '')) = 'no_chicken' THEN 0
                        ELSE COALESCE(d.chicken_count, 1)
                    END), 0) AS chicken_count
                FROM users u
                LEFT JOIN detections d
                    ON d.user_id = u.id
                    OR (d.user_id IS NULL AND d.username = u.username)
                {where_clause}
                GROUP BY u.id, u.username, u.email, u.role, u.status, u.created_at
                ORDER BY u.created_at DESC;
            """, params)
            rows = cur.fetchall()
            return [{
                'id': row[0],
                'username': row[1],
                'email': row[2],
                'role': row[3],
                'status': row[4],
                'created_at': row[5],
                'detection_count': int(row[6] or 0),
                'chicken_count': int(row[7] or 0)
            } for row in rows]
        except Exception as exc:
            print(f"[ERROR] Failed to fetch users: {exc}")
            return []
        finally:
            cur.close()
            conn.close()

    @staticmethod
    def update_user(user_id, username, email, role, status, password=None):
        conn = get_db_connection()
        cur = conn.cursor()
        try:
            if password:
                hashed_pw = bcrypt.generate_password_hash(password).decode('utf-8')
                cur.execute("""
                    UPDATE users
                    SET username = %s,
                        email = %s,
                        role = %s,
                        status = %s,
                        password = %s
                    WHERE id = %s;
                """, (username, email, role, status, hashed_pw, user_id))
            else:
                cur.execute("""
                    UPDATE users
                    SET username = %s,
                        email = %s,
                        role = %s,
                        status = %s
                    WHERE id = %s;
                """, (username, email, role, status, user_id))
            updated_rows = cur.rowcount

            cur.execute("""
                UPDATE detections
                SET username = %s
                WHERE user_id = %s;
            """, (username, user_id))
            conn.commit()
            return updated_rows > 0
        except Exception as exc:
            conn.rollback()
            print(f"[ERROR] Failed to update user: {exc}")
            return False
        finally:
            cur.close()
            conn.close()

    @staticmethod
    def set_status(user_id, status):
        conn = get_db_connection()
        cur = conn.cursor()
        try:
            cur.execute("""
                UPDATE users
                SET status = %s
                WHERE id = %s;
            """, (status, user_id))
            conn.commit()
            return cur.rowcount > 0
        except Exception as exc:
            conn.rollback()
            print(f"[ERROR] Failed to update user status: {exc}")
            return False
        finally:
            cur.close()
            conn.close()

    @staticmethod
    def delete_user(user_id):
        conn = get_db_connection()
        cur = conn.cursor()
        try:
            cur.execute("DELETE FROM users WHERE id = %s;", (user_id,))
            conn.commit()
            return cur.rowcount > 0
        except Exception as exc:
            conn.rollback()
            print(f"[ERROR] Failed to delete user: {exc}")
            return False
        finally:
            cur.close()
            conn.close()

    @staticmethod
    def get_total_users():
        conn = get_db_connection()
        cur = conn.cursor()
        try:
            cur.execute("SELECT COUNT(*) FROM users;")
            return int(cur.fetchone()[0] or 0)
        finally:
            cur.close()
            conn.close()

    @staticmethod
    def ensure_default_admin():
        existing = User.find_by_username(DEFAULT_ADMIN_USERNAME)
        if existing:
            if existing['role'] != 'admin' or existing['status'] != 'active':
                User.update_user(
                    existing['id'],
                    existing['username'],
                    existing['email'],
                    'admin',
                    'active'
                )
            return existing['id']

        admin_id = User.create_user(
            DEFAULT_ADMIN_USERNAME,
            DEFAULT_ADMIN_EMAIL,
            DEFAULT_ADMIN_PASSWORD,
            role='admin',
            status='active'
        )

        if admin_id:
            print(f"[INFO] Default admin created: username={DEFAULT_ADMIN_USERNAME}")
        return admin_id
