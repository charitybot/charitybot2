import os
from pathlib import Path

# Databases
production_logs_db_path = os.path.join(os.path.dirname(__file__), 'db', 'logs.db')
production_donations_db_path = os.path.join(os.path.dirname(__file__), 'db', 'donations.db')

# Services
mocksite_path = os.path.join(os.path.dirname(__file__), 'sources', 'mocks', 'mocksite.py')
