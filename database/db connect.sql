import mysql.connector
from datetime import datetime

# MYSQL CONFIG

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "your_password",
    "database": "drug_rag"
}

# DATABASE MANAGER

class DatabaseManager:

    def __init__(self):

        self.create_tables()

    def get_connection(self):

        return mysql.connector.connect(
            **DB_CONFIG
        )

    # CREATE TABLES

    def create_tables(self):

        conn = self.get_connection()

        cursor = conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS query_logs(

            id INT AUTO_INCREMENT PRIMARY KEY,

            question TEXT,

            answer LONGTEXT,

            route VARCHAR(50),

            response_time FLOAT,

            timestamp DATETIME
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS search_stats(

            id INT AUTO_INCREMENT PRIMARY KEY,

            search_term VARCHAR(255),

            search_count INT DEFAULT 1
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS feedback(

            id INT AUTO_INCREMENT PRIMARY KEY,

            question TEXT,

            rating INT,

            comments TEXT,

            timestamp DATETIME
        )
        """)

        conn.commit()

        cursor.close()
        conn.close()

    # LOG QUERY

    def log_query(
        self,
        question,
        answer,
        route,
        response_time
    ):

        conn = self.get_connection()

        cursor = conn.cursor()

        sql = """
        INSERT INTO query_logs
        (
            question,
            answer,
            route,
            response_time,
            timestamp
        )
        VALUES (%s,%s,%s,%s,%s)
        """

        values = (
            question,
            answer,
            route,
            response_time,
            datetime.now()
        )

        cursor.execute(
            sql,
            values
        )

        conn.commit()

        cursor.close()
        conn.close()

    # SEARCH STATS

    def update_search_stats(
        self,
        search_term
    ):

        conn = self.get_connection()

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT id,search_count
            FROM search_stats
            WHERE search_term=%s
            """,
            (search_term,)
        )

        result = cursor.fetchone()

        if result:

            cursor.execute(
                """
                UPDATE search_stats
                SET search_count=search_count+1
                WHERE search_term=%s
                """,
                (search_term,)
            )

        else:

            cursor.execute(
                """
                INSERT INTO search_stats
                (
                    search_term,
                    search_count
                )
                VALUES (%s,%s)
                """,
                (
                    search_term,
                    1
                )
            )

        conn.commit()

        cursor.close()
        conn.close()

    # FEEDBACK

    def save_feedback(
        self,
        question,
        rating,
        comments=""
    ):

        conn = self.get_connection()

        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO feedback
            (
                question,
                rating,
                comments,
                timestamp
            )
            VALUES (%s,%s,%s,%s)
            """,
            (
                question,
                rating,
                comments,
                datetime.now()
            )
        )

        conn.commit()

        cursor.close()
        conn.close()

    # RECENT QUERIES

    def get_recent_queries(
        self,
        limit=20
    ):

        conn = self.get_connection()

        cursor = conn.cursor()

        cursor.execute(
            f"""
            SELECT
            question,
            route,
            response_time,
            timestamp
            FROM query_logs
            ORDER BY id DESC
            LIMIT {limit}
            """
        )

        data = cursor.fetchall()

        cursor.close()
        conn.close()

        return data

    # TOP SEARCHES

    def get_top_searches(
        self,
        limit=10
    ):

        conn = self.get_connection()

        cursor = conn.cursor()

        cursor.execute(
            f"""
            SELECT
            search_term,
            search_count
            FROM search_stats
            ORDER BY search_count DESC
            LIMIT {limit}
            """
        )

        data = cursor.fetchall()

        cursor.close()
        conn.close()

        return data

    # METRICS

    def total_queries(self):

        conn = self.get_connection()

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM query_logs
            """
        )

        count = cursor.fetchone()[0]

        cursor.close()
        conn.close()

        return count

    def average_response_time(self):

        conn = self.get_connection()

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT AVG(response_time)
            FROM query_logs
            """
        )

        result = cursor.fetchone()[0]

        cursor.close()
        conn.close()

        return round(
            result or 0,
            2
        )

    def average_rating(self):

        conn = self.get_connection()

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT AVG(rating)
            FROM feedback
            """
        )

        result = cursor.fetchone()[0]

        cursor.close()
        conn.close()

        return round(
            result or 0,
            2
        )


    # DASHBOARD

    def dashboard_metrics(self):

        return {

            "total_queries":
                self.total_queries(),

            "avg_response_time":
                self.average_response_time(),

            "avg_rating":
                self.average_rating(),

            "top_searches":
                self.get_top_searches()
        }


db = DatabaseManager()

if __name__ == "__main__":

    print(
        "MySQL Connected Successfully"
    )
