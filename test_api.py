import requests
import json
import os
import sys

# Ensure UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')

BASE_URL = "http://127.0.0.1:5000"

def test_api():
    print("--- Testing API Flow ---")
    
    # 1. Test Login
    print("\n1. Testing Login...")
    login_payload = {
        "code": "2023001",
        "password": "123",  # Assuming 123 is the default pass based on common test data
        "device_id": "TEST_TEST_TEST"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/login", json=login_payload, timeout=5)
        print(f"Login Status: {response.status_code}")
        
        if response.status_code != 200:
            print(f"Login Error: {response.text}")
            return
            
        auth_data = response.json()
        print(f"Login Response: {json.dumps(auth_data, ensure_ascii=False, indent=2)}")
        token = auth_data.get('token')
        
    except Exception as e:
        print(f"Login Exception: {e}")
        return

    headers = {"Authorization": f"Bearer {token}"}
    
    # 2. Test Fetching Courses
    print("\n2. Testing Fetch Courses...")
    try:
        # Note: we need a session cookie normally, but wait, the API uses login_user under the hood in routes.py
        # Let's use a session object to hold the cookie from the login
        session = requests.Session()
        session.post(f"{BASE_URL}/api/login", json=login_payload)
        
        resp_courses = session.get(f"{BASE_URL}/api/courses", timeout=5)
        print(f"Courses Status: {resp_courses.status_code}")
        print(f"Courses Data: {json.dumps(resp_courses.json(), ensure_ascii=False, indent=2)}")
        
        courses = resp_courses.json()
        if not courses:
            print("No courses returned, cannot test lessons.")
            return
            
        course_id = courses[0]['id']
        
    except Exception as e:
        print(f"Courses Exception: {e}")
        return

    # 3. Test Fetching Lessons
    print(f"\n3. Testing Fetch Lessons for Course {course_id}...")
    try:
        resp_lessons = session.get(f"{BASE_URL}/api/lessons/{course_id}", timeout=5)
        print(f"Lessons Status: {resp_lessons.status_code}")
        print(f"Lessons Data: {json.dumps(resp_lessons.json(), ensure_ascii=False, indent=2)}")
        
        lessons = resp_lessons.json()
        if not lessons:
            print("No lessons returned, cannot test download.")
            return
            
        lesson_id = lessons[0]['id']
        
    except Exception as e:
        print(f"Lessons Exception: {e}")
        return

    # 4. Test Secure Download
    print(f"\n4. Testing Secure Download for Lesson {lesson_id}...")
    try:
        resp_dl = session.get(f"{BASE_URL}/api/secure_content/lesson/{lesson_id}", timeout=5)
        print(f"Download Status: {resp_dl.status_code}")
        print(f"Download Content-Type: {resp_dl.headers.get('Content-Type')}")
        print(f"Download X-File-Name: {resp_dl.headers.get('X-File-Name')}")
        if resp_dl.status_code == 200:
            print(f"Downloaded Size: {len(resp_dl.content)} bytes")
    except Exception as e:
        print(f"Download Exception: {e}")

if __name__ == "__main__":
    test_api()
