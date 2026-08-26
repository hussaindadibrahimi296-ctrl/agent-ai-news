import psycopg2
from config import DATABASE_URL


def get_connection():
    if not DATABASE_URL:
        raise RuntimeError("DATABASE_URL is not configured")

    return psycopg2.connect(DATABASE_URL)


def init_database():
    conn = get_connection()

    try:
        with conn.cursor() as cursor:

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS sources (
                    id SERIAL PRIMARY KEY,
                    name TEXT NOT NULL,
                    url TEXT NOT NULL UNIQUE,
                    enabled BOOLEAN DEFAULT TRUE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS articles (
                    id SERIAL PRIMARY KEY,
                    source_id INTEGER REFERENCES sources(id),
                    title TEXT NOT NULL,
                    url TEXT NOT NULL UNIQUE,
                    content TEXT,
                    published_at TIMESTAMP,
                    score INTEGER DEFAULT 0,
                    category TEXT,
                    status TEXT DEFAULT 'new',
                    content_hash TEXT UNIQUE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS posts (
                    id SERIAL PRIMARY KEY,
                    article_id INTEGER REFERENCES articles(id),
                    telegram_message_id BIGINT,
                    status TEXT DEFAULT 'queued',
                    scheduled_at TIMESTAMP,
                    published_at TIMESTAMP,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS settings (
                    key TEXT PRIMARY KEY,
                    value TEXT NOT NULL,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS admins (
                    telegram_id BIGINT PRIMARY KEY,
                    role TEXT NOT NULL DEFAULT 'editor',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS errors (
                    id SERIAL PRIMARY KEY,
                    component TEXT,
                    message TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)

        conn.commit()

    finally:
        conn.close()


def test_database():
    conn = get_connection()

    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT 1")
            result = cursor.fetchone()

        return result == (1,)

    finally:
        conn.close()
