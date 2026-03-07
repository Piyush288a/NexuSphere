"""
Test script for Phase 4 - Authentication System
Tests login, logout, and protected dashboard access
"""

import requests
from requests.exceptions import RequestException
import re

BASE_URL = "http://127.0.0.1:8000"

def test_authentication():
    print("\n" + "="*60)
    print("PHASE 4 - AUTHENTICATION SYSTEM TEST")
    print("="*60)
    
    session = requests.Session()
    
    # Test 1: Login page accessible
    print("\n[TEST 1] Testing login page accessibility...")
    try:
        response = session.get(f"{BASE_URL}/login/")
        if response.status_code == 200 and "NexuSphere Login" in response.text:
            print("✓ Login page is accessible and renders correctly")
        else:
            print("✗ Login page issue")
            return False
    except RequestException as e:
        print(f"✗ Error accessing login page: {e}")
        return False
    
    # Test 2: Dashboard redirects to login when not authenticated
    print("\n[TEST 2] Testing dashboard protection...")
    try:
        response = session.get(f"{BASE_URL}/dashboard/", allow_redirects=False)
        if response.status_code == 302:
            redirect_location = response.headers.get('Location', '')
            if '/login/' in redirect_location:
                print("✓ Dashboard correctly redirects unauthenticated users to login")
            else:
                print(f"✗ Dashboard redirects to wrong location: {redirect_location}")
                return False
        else:
            print(f"✗ Dashboard should redirect but returned: {response.status_code}")
            return False
    except RequestException as e:
        print(f"✗ Error testing dashboard: {e}")
        return False
    
    # Test 3: Login with credentials
    print("\n[TEST 3] Testing login functionality...")
    try:
        # Get CSRF token
        response = session.get(f"{BASE_URL}/login/")
        csrf_match = re.search(r'name=["\']csrfmiddlewaretoken["\']\s+value=["\']([^"\']+)["\']', response.text)
        if not csrf_match:
            csrf_match = re.search(r'value=["\']([^"\']+)["\']\s+name=["\']csrfmiddlewaretoken["\']', response.text)
        
        if not csrf_match:
            print("✗ Could not extract CSRF token")
            return False
        
        csrf_token = csrf_match.group(1)
        
        # Attempt login
        login_data = {
            'username': 'testuser',
            'password': 'testpass123',
            'csrfmiddlewaretoken': csrf_token
        }
        
        response = session.post(
            f"{BASE_URL}/login/",
            data=login_data,
            headers={'Referer': f"{BASE_URL}/login/"},
            allow_redirects=False
        )
        
        if response.status_code == 302:
            redirect_location = response.headers.get('Location', '')
            if '/dashboard/' in redirect_location:
                print("✓ Login successful, redirects to dashboard")
            else:
                print(f"✗ Login redirects to wrong location: {redirect_location}")
                return False
        else:
            print(f"✗ Login failed with status: {response.status_code}")
            return False
    except RequestException as e:
        print(f"✗ Error during login: {e}")
        return False
    
    # Test 4: Access dashboard after login
    print("\n[TEST 4] Testing authenticated dashboard access...")
    try:
        response = session.get(f"{BASE_URL}/dashboard/")
        if response.status_code == 200:
            if "Welcome to NexuSphere Dashboard" in response.text and "testuser" in response.text:
                print("✓ Dashboard accessible after login and displays username")
            else:
                print("✗ Dashboard content incorrect")
                return False
        else:
            print(f"✗ Dashboard returned status: {response.status_code}")
            return False
    except RequestException as e:
        print(f"✗ Error accessing dashboard: {e}")
        return False
    
    # Test 5: Logout functionality
    print("\n[TEST 5] Testing logout functionality...")
    try:
        # Get dashboard page with CSRF token
        response = session.get(f"{BASE_URL}/dashboard/")
        
        # Extract CSRF token from dashboard
        csrf_match = re.search(r'<input[^>]*name=["\']csrfmiddlewaretoken["\'][^>]*value=["\']([^"\']+)["\']', response.text)
        if not csrf_match:
            csrf_match = re.search(r'<input[^>]*value=["\']([^"\']+)["\'][^>]*name=["\']csrfmiddlewaretoken["\']', response.text)
        
        if not csrf_match:
            print("✗ Could not extract CSRF token for logout")
            print("  (Dashboard may not have logout form with CSRF token)")
            return False
        
        csrf_token = csrf_match.group(1)
        
        # Perform logout with POST
        response = session.post(
            f"{BASE_URL}/logout/",
            data={'csrfmiddlewaretoken': csrf_token},
            headers={'Referer': f"{BASE_URL}/dashboard/"},
            allow_redirects=False
        )
        
        if response.status_code == 302:
            redirect_location = response.headers.get('Location', '')
            if '/login/' in redirect_location:
                print("✓ Logout successful, redirects to login page")
            else:
                print(f"✗ Logout redirects to wrong location: {redirect_location}")
                return False
        else:
            print(f"✗ Logout returned status: {response.status_code}")
            return False
    except RequestException as e:
        print(f"✗ Error during logout: {e}")
        return False
    
    # Test 6: Dashboard inaccessible after logout
    print("\n[TEST 6] Testing dashboard protection after logout...")
    try:
        response = session.get(f"{BASE_URL}/dashboard/", allow_redirects=False)
        if response.status_code == 302:
            print("✓ Dashboard correctly redirects after logout")
        else:
            print(f"✗ Dashboard should redirect but returned: {response.status_code}")
            return False
    except RequestException as e:
        print(f"✗ Error testing dashboard after logout: {e}")
        return False
    
    # Test 7: Admin panel still accessible
    print("\n[TEST 7] Testing admin panel accessibility...")
    try:
        response = session.get(f"{BASE_URL}/admin/")
        if response.status_code == 200 or response.status_code == 302:
            print("✓ Admin panel is accessible")
        else:
            print(f"✗ Admin panel returned status: {response.status_code}")
            return False
    except RequestException as e:
        print(f"✗ Error accessing admin panel: {e}")
        return False
    
    return True

if __name__ == "__main__":
    try:
        success = test_authentication()
        
        print("\n" + "="*60)
        print("TEST SUMMARY")
        print("="*60)
        
        if success:
            print("✓ ALL AUTHENTICATION TESTS PASSED!")
            print("\nPhase 4 Implementation Status:")
            print("  ✓ Login page working")
            print("  ✓ Logout functionality working")
            print("  ✓ Dashboard protection working")
            print("  ✓ Authentication redirects working")
            print("  ✓ Session management working")
        else:
            print("✗ SOME TESTS FAILED")
        
        print("="*60 + "\n")
        
    except Exception as e:
        print(f"\n✗ Test suite error: {e}\n")
