"""
users: create table
"""

from yoyo import step

__depends__ = {}

steps = [
    step(
        """
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username VARCHAR(100) NOT NULL UNIQUE,
            email VARCHAR(255) NOT NULL UNIQUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        
        CREATE INDEX idx_users_username ON users(username);
        CREATE INDEX idx_users_email ON users(email);
        """,
        """
        DROP INDEX IF EXISTS idx_users_email;
        DROP INDEX IF EXISTS idx_users_username;
        DROP TABLE IF EXISTS users;
        """
    )
]
