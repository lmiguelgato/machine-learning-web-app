"""Configuration file for a basic Celery set-up.
"""

# Broker settings.
broker_url = 'redis://localhost:6379/0'

# Using the database to store task state and results.
result_backend = 'redis://localhost:6379/0'
