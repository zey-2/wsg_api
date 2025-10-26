"""
Quick test script to verify Courses API endpoints with certificate authentication.
This script tests basic connectivity and identifies which endpoints work.
"""

import requests
import json
import os
from typing import Dict, Any

# Configuration
BASE_URL = "https://api.ssg-wsg.sg"
CERT_PATH = os.path.join(os.path.dirname(__file__), "..", "certificates", "cert.pem")
KEY_PATH = os.path.join(os.path.dirname(__file__), "..", "certificates", "key.pem")

def test_endpoint(endpoint: str, method: str = "GET", params: Dict[str, Any] = None, 
                  headers: Dict[str, str] = None, description: str = "") -> bool:
    """Test a single endpoint and return whether it's working."""
    url = f"{BASE_URL}{endpoint}"
    
    if headers is None:
        headers = {}
    
    # Always add x-api-version header
    if 'x-api-version' not in headers:
        headers['x-api-version'] = 'v1'
    
    try:
        print(f"\n{'='*80}")
        print(f"Testing: {description}")
        print(f"Endpoint: {method} {endpoint}")
        print(f"Params: {params}")
        print(f"Headers: {headers}")
        
        response = requests.request(
            method=method,
            url=url,
            cert=(CERT_PATH, KEY_PATH),
            params=params,
            headers=headers,
            timeout=30
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print("✓ SUCCESS")
            data = response.json()
            # Print a sample of the response
            print(f"Response preview: {json.dumps(data, indent=2)[:500]}...")
            return True
        else:
            print(f"✗ FAILED - Status: {response.status_code}")
            print(f"Response: {response.text[:500]}")
            return False
            
    except Exception as e:
        print(f"✗ ERROR: {str(e)}")
        return False

def main():
    """Test all Courses API endpoints."""
    print("="*80)
    print("COURSES API - CERTIFICATE AUTHENTICATION TEST")
    print("="*80)
    
    results = {}
    
    # Test 1: Course Categories
    results['Course Categories'] = test_endpoint(
        endpoint="/courses/categories",
        params={'keyword': 'Training'},
        description="1. Course Categories - Retrieve browse categories by keyword"
    )
    
    # Test 2: Course Tags
    results['Course Tags'] = test_endpoint(
        endpoint="/courses/tags",
        params={'sortBy': '0'},  # 0=text, 1=count
        description="2. Course Tags - Retrieve course tags"
    )
    
    # Test 3: Course SubCategories
    results['Course SubCategories'] = test_endpoint(
        endpoint="/courses/subcategories",
        params={'categoryId': '34'},  # Using a category ID
        description="3. Course SubCategories - Retrieve subcategories by category ID"
    )
    
    # Test 4: Retrieve Courses by Keyword
    results['Retrieve Courses (Keyword)'] = test_endpoint(
        endpoint="/courses/directory",
        params={
            'pageSize': '10',
            'page': '0',
            'keyword': 'python'
        },
        headers={'x-api-version': 'v2.1'},
        description="4. Retrieve Courses - Search by keyword"
    )
    
    # Test 5: Retrieve Courses by Tagging Code
    results['Retrieve Courses (Tagging)'] = test_endpoint(
        endpoint="/courses/directory",
        params={
            'pageSize': '10',
            'page': '0',
            'taggingCodes': '1',  # SFC
            'courseSupportEndDate': '20250101',
            'retrieveType': 'FULL'
        },
        headers={'x-api-version': 'v2.1'},
        description="5. Retrieve Courses - Search by tagging code"
    )
    
    # Test 6: Course Autocomplete
    results['Course Autocomplete'] = test_endpoint(
        endpoint="/courses/autocomplete",
        params={'keyword': 'data'},
        description="6. Course Autocomplete - Get course title suggestions"
    )
    
    # Test 7: Popular Courses
    results['Popular Courses'] = test_endpoint(
        endpoint="/courses/popular",
        params={'taggingCodes': '1'},  # SFC
        description="7. Popular Courses - Get popular courses by tagging"
    )
    
    # Test 8: Featured Courses
    results['Featured Courses'] = test_endpoint(
        endpoint="/courses/featured",
        params={
            'pageSize': '10',
            'page': '0'
        },
        description="8. Featured Courses - Get featured courses"
    )
    
    # Test 9: Related Courses (Note: requires valid course reference number)
    # This one might fail if we don't have a valid course reference
    results['Related Courses'] = test_endpoint(
        endpoint="/courses/related/SCN-198202248E-01-CRS-N-0027685",
        description="9. Related Courses - Get courses related to a specific course"
    )
    
    # Test 10: Course Details (Note: requires valid course reference number)
    results['Course Details'] = test_endpoint(
        endpoint="/courses/directory/SCN-198202248E-01-CRS-N-0027685",
        params={'includeExpiredCourses': 'true'},
        headers={'x-api-version': 'v1.2'},
        description="10. Course Details - Get detailed course information"
    )
    
    # Print summary
    print("\n" + "="*80)
    print("TEST SUMMARY")
    print("="*80)
    
    working_count = sum(1 for result in results.values() if result)
    total_count = len(results)
    
    print(f"\nTotal Endpoints Tested: {total_count}")
    print(f"Working: {working_count}")
    print(f"Failed: {total_count - working_count}")
    print(f"Success Rate: {working_count/total_count*100:.1f}%\n")
    
    print("Detailed Results:")
    print("-" * 80)
    for name, result in results.items():
        status = "✓ WORKING" if result else "✗ FAILED"
        print(f"{name:.<50} {status}")
    
    print("\n" + "="*80)

if __name__ == "__main__":
    main()
