from app import get_db_connection


class VetReview:
    REVIEW_STATUSES = {'pending', 'approved', 'needs_more_checks', 'confirmed'}
    RISK_LEVELS = {'low', 'medium', 'high', 'critical'}

    @staticmethod
    def create_table():
        conn = get_db_connection()
        cur = conn.cursor()
        try:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS vet_reviews (
                    id SERIAL PRIMARY KEY,
                    detection_id INTEGER NOT NULL REFERENCES detections(id) ON DELETE CASCADE,
                    vet_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                    status VARCHAR(30) NOT NULL DEFAULT 'pending',
                    risk_level VARCHAR(20) DEFAULT 'medium',
                    diagnosis_notes TEXT,
                    recommended_action TEXT,
                    needs_lab_test BOOLEAN DEFAULT FALSE,
                    needs_farm_visit BOOLEAN DEFAULT FALSE,
                    needs_medication_change BOOLEAN DEFAULT FALSE,
                    reviewed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(detection_id, vet_id)
                );
            """)
            conn.commit()
            print("[INFO] vet_reviews table created or already exists.")
        except Exception as exc:
            conn.rollback()
            print(f"[ERROR] Failed to create vet_reviews table: {exc}")
            raise
        finally:
            cur.close()
            conn.close()

    @staticmethod
    def upsert_review(detection_id, vet_id, status, risk_level,
                      diagnosis_notes, recommended_action,
                      needs_lab_test=False, needs_farm_visit=False,
                      needs_medication_change=False):
        conn = get_db_connection()
        cur = conn.cursor()
        try:
            cur.execute("""
                INSERT INTO vet_reviews
                    (detection_id, vet_id, status, risk_level,
                     diagnosis_notes, recommended_action,
                     needs_lab_test, needs_farm_visit, needs_medication_change,
                     reviewed_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP)
                ON CONFLICT (detection_id, vet_id)
                DO UPDATE SET
                    status = EXCLUDED.status,
                    risk_level = EXCLUDED.risk_level,
                    diagnosis_notes = EXCLUDED.diagnosis_notes,
                    recommended_action = EXCLUDED.recommended_action,
                    needs_lab_test = EXCLUDED.needs_lab_test,
                    needs_farm_visit = EXCLUDED.needs_farm_visit,
                    needs_medication_change = EXCLUDED.needs_medication_change,
                    reviewed_at = CURRENT_TIMESTAMP
                RETURNING id;
            """, (
                detection_id, vet_id, status, risk_level,
                diagnosis_notes, recommended_action,
                needs_lab_test, needs_farm_visit, needs_medication_change
            ))
            review_id = cur.fetchone()[0]
            conn.commit()
            return review_id
        except Exception as exc:
            conn.rollback()
            print(f"[ERROR] Failed to save vet review: {exc}")
            return None
        finally:
            cur.close()
            conn.close()

    @staticmethod
    def get_reviews_for_detection(detection_id):
        conn = get_db_connection()
        cur = conn.cursor()
        try:
            cur.execute("""
                SELECT r.id, r.detection_id, r.vet_id,
                       u.username AS vet_username,
                       r.status, r.risk_level,
                       r.diagnosis_notes, r.recommended_action,
                       r.needs_lab_test, r.needs_farm_visit,
                       r.needs_medication_change, r.reviewed_at
                FROM vet_reviews r
                JOIN users u ON u.id = r.vet_id
                WHERE r.detection_id = %s
                ORDER BY r.reviewed_at DESC;
            """, (detection_id,))
            rows = cur.fetchall()
            return [{
                'id': row[0],
                'detection_id': row[1],
                'vet_id': row[2],
                'vet_username': row[3],
                'status': row[4],
                'risk_level': row[5],
                'diagnosis_notes': row[6],
                'recommended_action': row[7],
                'needs_lab_test': bool(row[8]),
                'needs_farm_visit': bool(row[9]),
                'needs_medication_change': bool(row[10]),
                'reviewed_at': row[11]
            } for row in rows]
        except Exception as exc:
            print(f"[ERROR] Failed to fetch vet reviews: {exc}")
            return []
        finally:
            cur.close()
            conn.close()

    @staticmethod
    def get_all_reviews(vet_id=None, status=None):
        conn = get_db_connection()
        cur = conn.cursor()
        conditions = []
        params = []

        if vet_id:
            conditions.append("r.vet_id = %s")
            params.append(vet_id)
        if status:
            conditions.append("r.status = %s")
            params.append(status)

        where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else ''

        try:
            cur.execute(f"""
                SELECT r.id, r.detection_id, r.vet_id,
                       u.username AS vet_username,
                       d.image_name, d.predicted_class, d.confidence,
                       d.username AS farmer_username,
                       r.status, r.risk_level,
                       r.diagnosis_notes, r.recommended_action,
                       r.needs_lab_test, r.needs_farm_visit,
                       r.needs_medication_change, r.reviewed_at
                FROM vet_reviews r
                JOIN users u ON u.id = r.vet_id
                JOIN detections d ON d.id = r.detection_id
                {where_clause}
                ORDER BY r.reviewed_at DESC;
            """, params)
            rows = cur.fetchall()
            return [{
                'id': row[0],
                'detection_id': row[1],
                'vet_id': row[2],
                'vet_username': row[3],
                'image_name': row[4],
                'predicted_class': row[5],
                'confidence': float(row[6] or 0),
                'farmer_username': row[7],
                'status': row[8],
                'risk_level': row[9],
                'diagnosis_notes': row[10],
                'recommended_action': row[11],
                'needs_lab_test': bool(row[12]),
                'needs_farm_visit': bool(row[13]),
                'needs_medication_change': bool(row[14]),
                'reviewed_at': row[15]
            } for row in rows]
        except Exception as exc:
            print(f"[ERROR] Failed to fetch all vet reviews: {exc}")
            return []
        finally:
            cur.close()
            conn.close()

    @staticmethod
    def get_vet_summary(vet_id):
        conn = get_db_connection()
        cur = conn.cursor()
        try:
            cur.execute("""
                SELECT
                    COUNT(*) AS total_reviews,
                    COUNT(*) FILTER (WHERE status = 'needs_more_checks') AS needs_more,
                    COUNT(*) FILTER (WHERE status = 'confirmed') AS confirmed,
                    COUNT(*) FILTER (WHERE needs_lab_test = TRUE) AS lab_tests,
                    COUNT(*) FILTER (WHERE needs_farm_visit = TRUE) AS farm_visits
                FROM vet_reviews
                WHERE vet_id = %s;
            """, (vet_id,))
            row = cur.fetchone()
            return {
                'total_reviews': int(row[0] or 0),
                'needs_more_checks': int(row[1] or 0),
                'confirmed': int(row[2] or 0),
                'lab_tests_requested': int(row[3] or 0),
                'farm_visits_requested': int(row[4] or 0)
            }
        except Exception as exc:
            print(f"[ERROR] Failed to fetch vet summary: {exc}")
            return {}
        finally:
            cur.close()
            conn.close()