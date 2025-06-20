#!/usr/bin/env python 
# -*- coding: utf-8 -*-
#!/usr/bin/env python 
# -*- coding: utf-8 -*-

import os
from typing import Optional, Union
import redis
import sqlite3
import pickle
from contextlib import contextmanager

class SaveIt:
    """
    A helper library for storing and retrieving Python primitive types in Redis or SQLite.
    """
    
    database_systems = [
        REDIS := 'redis',
        SQLITE := 'sqlite'
    ]
    
    def __init__(self, backend: str = 'redis', redis_config: dict = None, sqlite_db_name: Optional[str] = None):
        """
        Initialize SaveIt with Redis or SQLite.
        Args:
            backend (str): Storage backend ('redis' or 'sqlite').
            redis_config (dict): Redis connection details (host, port, db).
            sqlite_db_name (str): SQLite database file name.
        """
        
        # Check if backend is valid
        self.backend = backend.lower()
        if self.backend not in ['redis', 'sqlite']:
            raise ValueError("Backend must be either 'redis' or 'sqlite'")
        
        # Redis configuration
        if self.backend == 'redis':
            
            # Check if redis_config is provided
            if not redis_config:
                redis_config = {'host': 'localhost', 'port': 6379, 'db': 0}
            
            self._init_redis(**redis_config)
        
        # SQLite configuration
        if self.backend == 'sqlite':
            
            # Check if sqlite3 is installed on the system
            try:
                sqlite3.connect(':memory:')
            except sqlite3.Error:
                raise ValueError("SQLite is not installed on your system.")
            
            self._init_sqlite(sqlite_db_name)
        
    def _init_redis(self, host: str = 'localhost', port: int = 6379, db: int = 0) -> None:
        """
        Initialize Redis connection.
        Args:
            host (str): Redis host.
            port (int): Redis port.
            db (int): Redis database number
        """
        
        # Check if redis database is installed on the system
        try:
            redis.Redis()
        except redis.ConnectionError:
            raise ValueError("Redis is not installed on your system.")
        
        # Check if the connection details are valid
        if not isinstance(port, int) or not isinstance(db, int):
            raise ValueError("Port and database number must be integers.")
        if port < 0 or port > 65535:
            raise ValueError("Port number must be between 0 and 65535.")
        if db < 0 or db > 15:
            raise ValueError("Database number must be between 0 and 15.")
        if not isinstance(host, str):
            raise ValueError("Host must be a string.")
            
        # Connect to Redis
        self.redis_client = redis.Redis(
            host=host,
            port=port,
            db=db,
            decode_responses=False
        )
        # Test connection
        try:
            self.redis_client.ping()  
        except Exception as e:
            raise RuntimeError(f"Failed to connect to Redis on {host}:{port}: {e}")

    def _init_sqlite(self, sqlite_db_name: Optional[str] = None) -> None:
        """
        Initialize SQLite connection.
        Args:
            sqlite_db_name (str): SQLite database name.
        """
        
        # SaveIt sqlite databases directory
        directory = '__saveit__'
        if not os.path.exists(directory):
            os.makedirs(directory)
            
        # Database file
        if sqlite_db_name is None:
            # Get package name as database name
            sqlite_db_name = os.path.basename(os.path.dirname(__file__))
        
        # Initialize SQLite
        self.sqlite_db_name = sqlite_db_name
        self.sqlite_db = f"{directory}/{sqlite_db_name}.db"
        
        # Test connection
        try:
            self._initialize_sqlite()
        except Exception as e:
            raise ValueError(f"Failed to initialize SQLite: {e}")

    @contextmanager
    def _sqlite_connection(self):
        """Context manager for SQLite connection."""
        conn = sqlite3.connect(self.sqlite_db)
        cursor = conn.cursor()
        try:
            yield cursor
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    def _initialize_sqlite(self):
        """Create the SQLite table if it doesn't exist."""
        with self._sqlite_connection() as cursor:
            cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS {self.sqlite_db_name} (
                    key TEXT PRIMARY KEY,
                    value BLOB,
                    expiry INTEGER
                )
            """)

    def set(self, key: str, value: Union[int, str, float, list, dict, set, tuple], expiry_seconds: int = None) -> None:
        """
        Store a Python object in the selected backend with an optional expiry time.
        Args:
            key (str): Key for the object.
            value: Python object to store (int, str, float, list, dict, set, tuple).
            expiry_seconds (int): Expiry time in seconds (ignored in SQLite).
        """
        serialized_value = pickle.dumps(value)

        if self.backend == 'redis':
            if expiry_seconds is None:
                self.redis_client.set(key, serialized_value)
            else:
                self.redis_client.setex(key, expiry_seconds, serialized_value)
        elif self.backend == 'sqlite':
            expiry = None
            if expiry_seconds:
                expiry = int(sqlite3.time.time() + expiry_seconds)
            with self._sqlite_connection() as cursor:
                cursor.execute(f"""
                    INSERT OR REPLACE INTO {self.sqlite_db_name} (key, value, expiry) 
                    VALUES (?, ?, ?)
                """, (key, serialized_value, expiry))

    def get(self, key: str) -> Union[int, str, float, list, dict, set, tuple, None]:
        """
        Retrieve a Python object from the selected backend.
        Args:
            key (str): Key for the object.
        Returns:
            The deserialized Python object or None if the key does not exist.
        """
        if self.backend == 'redis':
            serialized_value = self.redis_client.get(key)
            return pickle.loads(serialized_value) if serialized_value else None
        elif self.backend == 'sqlite':
            with self._sqlite_connection() as cursor:
                cursor.execute(f"SELECT value, expiry FROM {self.sqlite_db_name} WHERE key = ?", (key,))
                row = cursor.fetchone()
                if not row:
                    return None
                serialized_value, expiry = row
                if expiry and expiry < int(sqlite3.time.time()):
                    self.delete(key)  # Delete expired key
                    return None
                return pickle.loads(serialized_value)
            
    def get_all_keys(self):
        """
        Retrieve all keys from the storage backend.
        Returns:
            List of keys.
        """
        if self.backend == 'redis':
            keys = self.redis_client.keys('*')
            return [key.decode('utf-8') if isinstance(key, bytes) else key for key in keys]
        elif self.backend == 'sqlite':
            with self._sqlite_connection() as cursor:
                cursor.execute(f"SELECT key FROM {self.sqlite_db_name}")
                return [row[0] for row in cursor.fetchall()]

    def delete(self, key: str) -> None:
        """
        Delete a key from the selected backend.
        Args:
            key (str): Key to delete.
        """
        if self.backend == 'redis':
            self.redis_client.delete(key)
        elif self.backend == 'sqlite':
            with self._sqlite_connection() as cursor:
                cursor.execute(f"DELETE FROM {self.sqlite_db_name} WHERE key = ?", (key,))

    def exists(self, key: str) -> bool:
        """
        Check if a key exists in the selected backend.
        Args:
            key (str): Key to check.
        Returns:
            bool: True if the key exists, False otherwise.
        """
        if self.backend == 'redis':
            return self.redis_client.exists(key) == 1
        elif self.backend == 'sqlite':
            with self._sqlite_connection() as cursor:
                cursor.execute(f"SELECT 1 FROM {self.sqlite_db_name} WHERE key = ?", (key,))
                return cursor.fetchone() is not None

    def flush_all(self) -> None:
        """
        Flush all data from the selected backend.
        WARNING: This deletes all data!
        """
        if self.backend == 'redis':
            self.redis_client.flushdb()
        elif self.backend == 'sqlite':
            with self._sqlite_connection() as cursor:
                cursor.execute(f"DELETE FROM {self.sqlite_db_name}")

# Main function to test the class
if __name__ == '__main__':
    
    # Test with Redis
    print(f"\n{'='*10} REDIS EXAMPLE {'='*10}")
    saveit_redis = SaveIt(backend='redis', redis_config={'host': 'localhost', 'port': 6379})
    saveit_redis.set('example_key_1', {'name': 'Alice', 'age': 30}, expiry_seconds=3600)
    data = saveit_redis.get('example_key_1')
    print(data)  # Output: {'name': 'Alice', 'age': 30}
    saveit_redis.delete('example_key_1')
    print(saveit_redis.exists('example_key_1'))  # Output: False
    saveit_redis.flush_all()
    
    # Test with SQLite
    print(f"\n{'='*10} SQLITE EXAMPLE {'='*10}")
    saveit_sqlite = SaveIt(backend='sqlite')
    saveit_sqlite.set('example_key_2', [1, 2, 3])
    data = saveit_sqlite.get('example_key_2')
    print(data)  # Output: [1, 2, 3]
    saveit_sqlite.delete('example_key_2')
    print(saveit_sqlite.exists('example_key_2'))  # Output: False
    saveit_sqlite.flush_all()
