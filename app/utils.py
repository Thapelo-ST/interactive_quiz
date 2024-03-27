import random
import string
from datetime import datetime

def generate_random_string(length=10):
    """Generate a random string of alphanumeric characters."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def format_datetime(dt):
    """Format datetime object to string."""
    return dt.strftime('%Y-%m-%d %H:%M:%S')