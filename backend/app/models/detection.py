from app import get_db_connection


class Detection:
    @staticmethod
    def create_table():
        conn = get_db_connection()
        cur = conn.cursor()
        try:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS detections (
                    id SERIAL PRIMARY KEY,
                    user_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
                    username VARCHAR(50),
                    image_name VARCHAR(255),
                    predicted_class VARCHAR(50) NOT NULL,
                    confidence FLOAT NOT NULL,
                    crd_prob FLOAT,
                    fowlpox_prob FLOAT,
                    healthy_prob FLOAT,
                    chicken_count INTEGER NOT NULL DEFAULT 1,
                    detected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
            cur.execute("ALTER TABLE detections ADD COLUMN IF NOT EXISTS user_id INTEGER REFERENCES users(id) ON DELETE SET NULL;")
            cur.execute("ALTER TABLE detections ADD COLUMN IF NOT EXISTS chicken_count INTEGER NOT NULL DEFAULT 1;")
            conn.commit()
            print("[INFO] detections table created or already exists.")
        except Exception as exc:
            conn.rollback()
            print(f"[ERROR] Failed to create detections table: {exc}")
            raise
        finally:
            cur.close()
            conn.close()

    @staticmethod
    def save_detection(username, image_name, predicted_class, confidence,
                       crd_prob, fowlpox_prob, healthy_prob, user_id=None,
                       chicken_count=1):
        conn = get_db_connection()
        cur = conn.cursor()
        try:
            cur.execute("""
                INSERT INTO detections
                (user_id, username, image_name, predicted_class,
                 confidence, crd_prob, fowlpox_prob, healthy_prob, chicken_count)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id;
            """, (
                user_id,
                username,
                image_name,
                predicted_class,
                confidence,
                crd_prob,
                fowlpox_prob,
                healthy_prob,
                chicken_count
            ))
            detection_id = cur.fetchone()[0]
            conn.commit()
            return detection_id
        except Exception as exc:
            conn.rollback()
            print(f"[ERROR] Failed to save detection: {exc}")
            return None
        finally:
            cur.close()
            conn.close()

    @staticmethod
    def get_all_detections(username=None, result_filter='', date_from='', date_to=''):
        conn = get_db_connection()
        cur = conn.cursor()
        conditions = []
        params = []

        if username:
            conditions.append("COALESCE(u.username, d.username) = %s")
            params.append(username)
        if result_filter:
            conditions.append("LOWER(d.predicted_class) = %s")
            params.append(result_filter.lower())
        if date_from:
            conditions.append("DATE(d.detected_at) >= %s")
            params.append(date_from)
        if date_to:
            conditions.append("DATE(d.detected_at) <= %s")
            params.append(date_to)

        where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else ''

        try:
            # [VET-FEEDBACK] LEFT JOIN to latest vet review per detection
            cur.execute(f"""
                SELECT
                    d.id,
                    d.user_id,
                    COALESCE(u.username, d.username) AS username,
                    COALESCE(u.email, '') AS email,
                    d.image_name,
                    d.predicted_class,
                    d.confidence,
                    d.crd_prob,
                    d.fowlpox_prob,
                    d.healthy_prob,
                    d.chicken_count,
                    d.detected_at,
                    vr.status            AS vet_status,
                    vr.risk_level        AS vet_risk_level,
                    vr.diagnosis_notes   AS vet_notes,
                    vr.recommended_action AS vet_action,
                    vr.reviewed_at       AS vet_reviewed_at,
                    vu.username          AS vet_username,
                    vr.needs_lab_test    AS vet_needs_lab_test,
                    vr.needs_farm_visit  AS vet_needs_farm_visit,
                    vr.needs_medication_change AS vet_needs_medication_change
                FROM detections d
                LEFT JOIN users u ON u.id = d.user_id
                LEFT JOIN LATERAL (
                    SELECT r.status, r.risk_level, r.diagnosis_notes,
                           r.recommended_action, r.reviewed_at,
                           r.vet_id,
                           r.needs_lab_test, r.needs_farm_visit,
                           r.needs_medication_change
                    FROM vet_reviews r
                    WHERE r.detection_id = d.id
                    ORDER BY r.reviewed_at DESC
                    LIMIT 1
                ) vr ON TRUE
                LEFT JOIN users vu ON vu.id = vr.vet_id
                {where_clause}
                ORDER BY d.detected_at DESC;
            """, params)
            rows = cur.fetchall()
            return [{
                'id': row[0],
                'user_id': row[1],
                'username': row[2],
                'email': row[3],
                'image_name': row[4],
                'predicted_class': row[5],
                'confidence': float(row[6]),
                'crd_prob': float(row[7] or 0),
                'fowlpox_prob': float(row[8] or 0),
                'healthy_prob': float(row[9] or 0),
                'chicken_count': int(row[10] or 0),
                'detected_at': row[11],
                # [VET-FEEDBACK] new vet review fields — None when no review exists
                'vet_status': row[12],
                'vet_risk_level': row[13],
                'vet_notes': row[14],
                'vet_action': row[15],
                'vet_reviewed_at': str(row[16]) if row[16] else None,
                'vet_username': row[17],
                'vet_needs_lab_test': bool(row[18]) if row[18] is not None else False,
                'vet_needs_farm_visit': bool(row[19]) if row[19] is not None else False,
                'vet_needs_medication_change': bool(row[20]) if row[20] is not None else False,
            } for row in rows]
        except Exception as exc:
            print(f"[ERROR] Failed to fetch detections: {exc}")
            return []
        finally:
            cur.close()
            conn.close()

    @staticmethod
    def get_statistics(username=None):
        conn = get_db_connection()
        cur = conn.cursor()
        try:
            if username:
                cur.execute("""
                    SELECT LOWER(d.predicted_class) AS predicted_class, COUNT(*) AS total
                    FROM detections d
                    LEFT JOIN users u ON u.id = d.user_id
                    WHERE COALESCE(u.username, d.username) = %s
                    GROUP BY LOWER(d.predicted_class);
                """, (username,))
            else:
                cur.execute("""
                    SELECT LOWER(predicted_class) AS predicted_class, COUNT(*) AS total
                    FROM detections
                    GROUP BY LOWER(predicted_class);
                """)
            rows = cur.fetchall()
            stats = {}
            for row in rows:
                stats[row[0]] = int(row[1] or 0)
            return stats
        except Exception as exc:
            print(f"[ERROR] Failed to fetch statistics: {exc}")
            return {}
        finally:
            cur.close()
            conn.close()

    @staticmethod
    def get_admin_summary():
        conn = get_db_connection()
        cur = conn.cursor()
        try:
            cur.execute("""
                SELECT
                    COUNT(*) AS total_detections,
                    COALESCE(SUM(CASE
                        WHEN LOWER(predicted_class) = 'no_chicken' THEN 0
                        ELSE COALESCE(chicken_count, 1)
                    END), 0) AS total_chickens_detected,
                    COALESCE(SUM(CASE
                        WHEN LOWER(predicted_class) IN ('healthy', 'chicken', 'no_chicken') THEN 0
                        ELSE 1
                    END), 0) AS total_disease_cases
                FROM detections;
            """)
            row = cur.fetchone()
            return {
                'total_detections': int(row[0] or 0),
                'total_chickens_detected': int(row[1] or 0),
                'total_disease_cases': int(row[2] or 0)
            }
        except Exception as exc:
            print(f"[ERROR] Failed to fetch admin summary: {exc}")
            return {
                'total_detections': 0,
                'total_chickens_detected': 0,
                'total_disease_cases': 0
            }
        finally:
            cur.close()
            conn.close()

    @staticmethod
    def delete_detection(detection_id):
        conn = get_db_connection()
        cur = conn.cursor()
        try:
            cur.execute("DELETE FROM detections WHERE id = %s;", (detection_id,))
            conn.commit()
            return cur.rowcount > 0
        except Exception as exc:
            conn.rollback()
            print(f"[ERROR] Failed to delete detection: {exc}")
            return False
        finally:
            cur.close()
            conn.close()
