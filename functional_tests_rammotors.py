"""
Functional testing for Ram Motors
"""

from selenium import webdriver

BROWSER = webdriver.Firefox()
BROWSER.get('http://localhost:8000')

assert 'Django' in BROWSER.title
