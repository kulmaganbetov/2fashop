#!/usr/bin/env python
"""
Script to run Telegram bot.
"""
import os
import sys
import django

# Setup Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smartshop.core.settings')
django.setup()

# Import and run bot
from smartshop.two_factor.telegram_bot import run_bot

if __name__ == '__main__':
    print("Starting Telegram bot...")
    print("Press Ctrl+C to stop")
    try:
        run_bot()
    except KeyboardInterrupt:
        print("\nBot stopped")
        sys.exit(0)
