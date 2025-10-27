"""
Courses API Examples with Certificate Authentication
=====================================================

This script demonstrates working examples for the SSG-WSG Courses API
using certificate authentication (mTLS).

All examples use certificate authentication to api.ssg-wsg.sg

Author: Generated for SSG-WSG API Integration
Date: October 2025
"""

import requests
import json
import os
from datetime import datetime
from typing import Dict, Any, Optional, List

class CoursesAPI:
    """
    Client for SSG-WSG Courses API with certificate authentication.
    
    Base URL: https://api.ssg-wsg.sg
    Authentication: Certificate-based (mTLS)
    """
    
    def __init__(self, cert_path: str, key_path: str):
        """
        Initialize the Courses API client.
        
        Args:
            cert_path: Path to the certificate file (.pem)
            key_path: Path to the private key file (.pem)
        """
        self.base_url = "https://api.ssg-wsg.sg"
        self.cert_path = cert_path
        self.key_path = key_path
        self.session = requests.Session()
        self.session.cert = (cert_path, key_path)
    
    def _make_request(self, endpoint: str, params: Optional[Dict[str, Any]] = None,
                     headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """
        Make an authenticated API request.
        
        Args:
            endpoint: API endpoint path
            params: Query parameters
            headers: Request headers
            
        Returns:
            JSON response as dictionary
        """
        url = f"{self.base_url}{endpoint}"
        
        if headers is None:
            headers = {}
        
        # Add default API version if not specified
        if 'x-api-version' not in headers:
            headers['x-api-version'] = 'v1'
        
        try:
            response = self.session.get(
                url,
                params=params,
                headers=headers,
                timeout=30
            )
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            print(f"Error making request to {endpoint}: {str(e)}")
            # Safely log server response if available
            resp = getattr(e, 'response', None)
            if resp is not None:
                try:
                    # Prefer JSON error bodies if provided
                    err_json = resp.json()
                    print(f"Response JSON: {json.dumps(err_json, indent=2, ensure_ascii=False)}")
                except Exception:
                    # Fallback to raw text
                    try:
                        print(f"Response: {resp.text}")
                    except Exception:
                        pass
            raise
    
    def get_course_categories(self, keyword: str) -> Dict[str, Any]:
        """
        Example 1: Get Course Categories by Keyword
        
        Retrieve a list of course categories (e.g., Area of Training, Training Providers)
        by keyword. Minimum 3 characters required.
        
        Args:
            keyword: Keyword to search for (minimum 3 characters)
            
        Returns:
            Dictionary containing course categories
            
        API Endpoint: GET /courses/categories
        API Version: v1 (default)
        """
        return self._make_request(
            endpoint="/courses/categories",
            params={'keyword': keyword}
        )
    
    def get_course_tags(self, sort_by: str = '0') -> Dict[str, Any]:
        """
        Example 2: Get Course Tags
        
        Retrieve a list of course tags with options to sort by text or count.
        Course tags ease searching based on suggestions like Popular, New, PSEA, etc.
        
        Args:
            sort_by: '0' for text (default), '1' for count
            
        Returns:
            Dictionary containing course tags
            
        API Endpoint: GET /courses/tags  
        API Version: v1 (default)
        """
        return self._make_request(
            endpoint="/courses/tags",
            params={'sortBy': sort_by}
        )
    
    def search_courses_by_keyword(self, keyword: str, page_size: int = 10, 
                                  page: int = 0) -> Dict[str, Any]:
        """
        Example 3: Search Courses by Keyword
        
        Retrieve course details using a keyword search (minimum 3 characters).
        Returns basic course information.
        
        Note: Keyword and tagging codes cannot be used together in the same query.
        
        Args:
            keyword: Search keyword (minimum 3 characters)
            page_size: Number of items per page (default: 10)
            page: Page number, starting from 0 (default: 0)
            
        Returns:
            Dictionary containing course search results
            
        API Endpoint: GET /courses/directory
        API Version: v2.1
        """
        return self._make_request(
            endpoint="/courses/directory",
            params={
                'keyword': keyword,
                'pageSize': str(page_size),
                'page': str(page)
            },
            headers={'x-api-version': 'v2.1'}
        )
    
    def search_courses_by_tagging(self, tagging_codes: List[str], 
                                  support_end_date: str,
                                  retrieve_type: str = 'FULL',
                                  page_size: int = 10,
                                  page: int = 0,
                                  last_update_date: Optional[str] = None) -> Dict[str, Any]:
        """
        Example 4: Search Courses by Tagging Code
        
        Retrieve detailed course information using course tagging codes and support end date.
        Returns comprehensive details including contact person, training provider, quality, 
        outcome, and skills frameworks information.
        
        Note: Keyword and tagging codes cannot be used together in the same query.
        
        Tagging Codes:
        - 1: SFC (SkillsFuture Credit)
        - 2: PET
        - 40: SF Training Subsidy
        - 30011-30083: SkillsFuture Series (various categories and levels)
        - 9001: Free Non-SFC Course
        - 9002: Chargeable Non-SFC Course
        - FULL: All course tagging codes
        
        Args:
            tagging_codes: List of tagging codes (e.g., ['1', '2'] or ['FULL'])
            support_end_date: Format YYYYMMDD (e.g., '20250101')
            retrieve_type: 'FULL' or 'DELTA' (default: 'FULL')
            page_size: Number of items per page (default: 10)
            page: Page number, starting from 0 (default: 0)
            last_update_date: Required if retrieve_type='DELTA', format YYYYMMDD
            
        Returns:
            Dictionary containing detailed course information
            
        API Endpoint: GET /courses/directory
        API Version: v2.1
        """
        params = {
            'taggingCodes': ','.join(tagging_codes),
            'courseSupportEndDate': support_end_date,
            'retrieveType': retrieve_type,
            'pageSize': str(page_size),
            'page': str(page)
        }
        
        if retrieve_type == 'DELTA' and last_update_date:
            params['lastUpdateDate'] = last_update_date
        
        return self._make_request(
            endpoint="/courses/directory",
            params=params,
            headers={'x-api-version': 'v2.1'}
        )
    
    def get_course_autocomplete(self, keyword: str) -> Dict[str, Any]:
        """
        Example 5: Get Course Autocomplete Suggestions
        
        Retrieve course titles that match the keyword (minimum 3 characters).
        Use this to implement an autocomplete feature for course search.
        
        Args:
            keyword: Search keyword (minimum 3 characters)
            
        Returns:
            Dictionary containing course title suggestions
            
        API Endpoint: GET /courses/directory/autocomplete
        API Version: v1.2
        """
        return self._make_request(
            endpoint="/courses/directory/autocomplete",
            params={'keyword': keyword},
            headers={'x-api-version': 'v1.2'}
        )
    
    def get_course_subcategories(self, browse_category_id: int) -> Dict[str, Any]:
        """
        Example 6: Get Course SubCategories
        
        Retrieve a list of course sub-categories within a main category by its ID.
        The keyword search functionality is not available in this API.
        
        Args:
            browse_category_id: The category ID to retrieve sub-categories for
            
        Returns:
            Dictionary containing sub-categories
            
        API Endpoint: GET /courses/categories/{browseCategoryID}/subCategories
        API Version: v1 (default)
        """
        return self._make_request(
            endpoint=f"/courses/categories/{browse_category_id}/subCategories"
        )
    
    def get_course_details(self, course_reference_number: str, 
                          include_expired: bool = True) -> Dict[str, Any]:
        """
        Example 7: Get Course Details
        
        Retrieve comprehensive details of a course based on the course reference number.
        These details include course information such as course runs, fees, objectives,
        contents, course contact person, community feedback, and training provider information.
        
        Args:
            course_reference_number: Course reference number (e.g., 'SCN-198202248E-01-CRS-N-0027685')
            include_expired: Whether to retrieve expired courses (default: True)
            
        Returns:
            Dictionary containing comprehensive course details
            
        API Endpoint: GET /courses/directory/{course reference number}
        API Version: v1.2 (default)
        """
        return self._make_request(
            endpoint=f"/courses/directory/{course_reference_number}",
            params={'includeExpiredCourses': str(include_expired).lower()},
            headers={'x-api-version': 'v1.2'}
        )
    
    def get_related_courses(self, course_reference_number: str) -> Dict[str, Any]:
        """
        Example 8: Get Related Courses
        
        Retrieve up to 10 courses related to a specified course based on its 
        course reference number. This helps users discover similar courses.
        
        Args:
            course_reference_number: Course reference number
            
        Returns:
            Dictionary containing related courses
            
        API Endpoint: GET /courses/directory/{course reference number}/related
        API Version: v1 (default)
        """
        return self._make_request(
            endpoint=f"/courses/directory/{course_reference_number}/related"
        )
    
    def get_popular_courses(self, tagging_code: Optional[str] = None,
                           page_size: int = 10, page: int = 0) -> Dict[str, Any]:
        """
        Example 9: Get Popular Courses
        
        Retrieve a list of popular courses along with course provider information.
        Courses can be filtered based on course tagging code (WSQ, CET, PET, SFC, and PA).
        Use this API to find out what the trending courses are.
        
        Args:
            tagging_code: Course tagging code (optional). Examples: 'WSQ', 'CET', 'PET', 'SFC', 'PA'
            page_size: Number of items per page (default: 10)
            page: Page number, starting from 0 (default: 0)
            
        Returns:
            Dictionary containing popular courses
            
        API Endpoint: GET /courses/directory/popular
        API Version: v1.2 (Certificate)
        """
        params = {
            'pageSize': str(page_size),
            'page': str(page)
        }
        
        if tagging_code:
            params['taggingCode'] = tagging_code
        
        return self._make_request(
            endpoint="/courses/directory/popular",
            params=params,
            headers={'x-api-version': 'v1.2'}
        )
    
    def get_featured_courses(self, tagging_code: Optional[str] = None,
                            page_size: int = 10, page: int = 0) -> Dict[str, Any]:
        """
        Example 10: Get Featured Courses
        
        Retrieve a list of featured courses along with course provider information
        from the MySkillsFuture course directory. Courses can be filtered based on
        course tagging code (WSQ, CET, PET, SFC, and PA).
        
        Args:
            tagging_code: Course tagging code (optional). Examples: 'WSQ', 'CET', 'PET', 'SFC', 'PA'
            page_size: Number of items per page (default: 10)
            page: Page number, starting from 0 (default: 0)
            
        Returns:
            Dictionary containing featured courses
            
        API Endpoint: GET /courses/directory/featured
        API Version: v1.2 (Certificate)
        """
        params = {
            'pageSize': str(page_size),
            'page': str(page)
        }
        
        if tagging_code:
            params['taggingCode'] = tagging_code
        
        return self._make_request(
            endpoint="/courses/directory/featured",
            params=params,
            headers={'x-api-version': 'v1.2'}
        )

# Example usage functions
def save_response(data: Dict[str, Any], filename: str):
    """Save API response to JSON file."""
    output_dir = os.path.join(os.path.dirname(__file__), "..", "data", "courses_examples")
    os.makedirs(output_dir, exist_ok=True)
    
    filepath = os.path.join(output_dir, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"✓ Saved to: {filepath}")

def example_1_course_categories():
    """Example 1: Retrieve course categories by keyword."""
    print("\n" + "="*80)
    print("Example 1: Get Course Categories")
    print("="*80)
    print("\nSearching for categories containing 'Training'...")
    
    cert_path = os.path.join(os.path.dirname(__file__), "..", "certificates", "cert.pem")
    key_path = os.path.join(os.path.dirname(__file__), "..", "certificates", "key.pem")
    
    api = CoursesAPI(cert_path, key_path)
    result = api.get_course_categories(keyword='Training')
    
    print(f"\nFound {result.get('meta', {}).get('total', 0)} categories:")
    for category in result.get('data', {}).get('categories', []):
        print(f"  - ID: {category.get('id')}, Name: {category.get('name')}")
    
    save_response(result, "example_1_course_categories.json")
    return result

def example_2_course_tags():
    """Example 2: Retrieve course tags sorted by text."""
    print("\n" + "="*80)
    print("Example 2: Get Course Tags")
    print("="*80)
    print("\nRetrieving course tags sorted by text...")
    
    cert_path = os.path.join(os.path.dirname(__file__), "..", "certificates", "cert.pem")
    key_path = os.path.join(os.path.dirname(__file__), "..", "certificates", "key.pem")
    
    api = CoursesAPI(cert_path, key_path)
    result = api.get_course_tags(sort_by='0')
    
    print(f"\nFound {result.get('meta', {}).get('total', 0)} tags:")
    tags = result.get('data', {}).get('tags', [])
    for tag in tags[:10]:  # Show first 10 tags
        print(f"  - {tag.get('text')}: {tag.get('count')} courses")
    if len(tags) > 10:
        print(f"  ... and {len(tags) - 10} more tags")
    
    save_response(result, "example_2_course_tags.json")
    return result

def example_3_search_by_keyword():
    """Example 3: Search courses by keyword."""
    print("\n" + "="*80)
    print("Example 3: Search Courses by Keyword")
    print("="*80)
    print("\nSearching for 'python' courses...")
    
    cert_path = os.path.join(os.path.dirname(__file__), "..", "certificates", "cert.pem")
    key_path = os.path.join(os.path.dirname(__file__), "..", "certificates", "key.pem")
    
    api = CoursesAPI(cert_path, key_path)
    result = api.search_courses_by_keyword(keyword='python', page_size=5)
    
    courses = result.get('data', {}).get('courses', [])
    total = result.get('data', {}).get('meta', {}).get('total', 0)
    
    print(f"\nFound {total} courses (showing first {len(courses)}):")
    for course in courses:
        print(f"\n  Title: {course.get('title')}")
        print(f"  Reference: {course.get('referenceNumber')}")
        areas = course.get('areaOfTrainings', [])
        if areas:
            print(f"  Area: {areas[0].get('description')}")
    
    save_response(result, "example_3_search_by_keyword.json")
    return result

def example_4_search_by_tagging():
    """Example 4: Search courses by tagging code."""
    print("\n" + "="*80)
    print("Example 4: Search Courses by Tagging Code (SkillsFuture Credit)")
    print("="*80)
    print("\nSearching for SkillsFuture Credit (SFC) supported courses...")
    
    cert_path = os.path.join(os.path.dirname(__file__), "..", "certificates", "cert.pem")
    key_path = os.path.join(os.path.dirname(__file__), "..", "certificates", "key.pem")
    
    api = CoursesAPI(cert_path, key_path)
    result = api.search_courses_by_tagging(
        tagging_codes=['1'],  # SFC
        support_end_date='20250101',
        page_size=5
    )
    
    courses = result.get('data', {}).get('courses', [])
    total = result.get('data', {}).get('meta', {}).get('total', 0)
    
    print(f"\nFound {total} SFC courses (showing first {len(courses)}):")
    for course in courses:
        print(f"\n  Title: {course.get('title')}")
        print(f"  Reference: {course.get('referenceNumber')}")
        provider = course.get('trainingProvider', {})
        if provider:
            print(f"  Provider: {provider.get('name')}")
        areas = course.get('areaOfTrainings', [])
        if areas:
            print(f"  Area: {areas[0].get('description')}")
    
    save_response(result, "example_4_search_by_tagging.json")
    return result

def example_5_autocomplete():
    """Example 5: Get course title autocomplete suggestions."""
    print("\n" + "="*80)
    print("Example 5: Get Course Autocomplete Suggestions")
    print("="*80)
    print("\nGetting autocomplete suggestions for 'data'...")
    
    cert_path = os.path.join(os.path.dirname(__file__), "..", "certificates", "cert.pem")
    key_path = os.path.join(os.path.dirname(__file__), "..", "certificates", "key.pem")
    
    api = CoursesAPI(cert_path, key_path)
    result = api.get_course_autocomplete(keyword='data')
    
    # Extract course titles from the response
    courses = result.get('data', {}).get('courses', [])
    terms = result.get('data', {}).get('terms', [])
    
    print(f"\nFound {len(courses)} course title suggestions:")
    for i, course in enumerate(courses[:10], 1):  # Show first 10
        # Remove HTML tags for cleaner display
        title = course.get('title', '').replace('<b>', '').replace('</b>', '')
        print(f"  {i}. {title}")
    if len(courses) > 10:
        print(f"  ... and {len(courses) - 10} more course titles")
    
    if terms:
        print(f"\nFound {len(terms)} search term suggestions:")
        for i in range(0, len(terms), 2):  # Terms come in pairs (term, count)
            if i < len(terms):
                term = terms[i].get('value', '')
                count = terms[i+1].get('value', '0') if i+1 < len(terms) else '0'
                print(f"  - {term} ({count} courses)")
                if i >= 8:  # Show first 5 term pairs
                    break
    
    save_response(result, "example_5_autocomplete.json")
    return result

def example_6_subcategories():
    """Example 6: Retrieve course sub-categories."""
    print("\n" + "="*80)
    print("Example 6: Get Course SubCategories")
    print("="*80)
    print("\nRetrieving sub-categories for category ID 34 (Area of Training)...")
    
    cert_path = os.path.join(os.path.dirname(__file__), "..", "certificates", "cert.pem")
    key_path = os.path.join(os.path.dirname(__file__), "..", "certificates", "key.pem")
    
    api = CoursesAPI(cert_path, key_path)
    result = api.get_course_subcategories(browse_category_id=34)
    
    subcategories = result.get('data', {}).get('subCategories', [])
    total = result.get('meta', {}).get('total', 0)
    
    print(f"\nFound {total} sub-categories:")
    for i, subcat in enumerate(subcategories[:15], 1):  # Show first 15
        print(f"  {i}. {subcat.get('description')} (ID: {subcat.get('id')})")
    if len(subcategories) > 15:
        print(f"  ... and {len(subcategories) - 15} more sub-categories")
    
    save_response(result, "example_6_subcategories.json")
    return result

def example_7_course_details():
    """Example 7: Retrieve detailed course information."""
    print("\n" + "="*80)
    print("Example 7: Get Course Details")
    print("="*80)
    
    # Using an example course reference number
    course_ref = "SCN-198202248E-01-CRS-N-0027685"
    print(f"\nRetrieving details for course: {course_ref}...")
    
    cert_path = os.path.join(os.path.dirname(__file__), "..", "certificates", "cert.pem")
    key_path = os.path.join(os.path.dirname(__file__), "..", "certificates", "key.pem")
    
    api = CoursesAPI(cert_path, key_path)
    result = api.get_course_details(course_reference_number=course_ref)
    
    courses = result.get('data', {}).get('courses', [])
    if courses:
        course = courses[0]
        print(f"\n  Title: {course.get('title')}")
        print(f"  Reference: {course.get('referenceNumber')}")
        
        provider = course.get('trainingProvider', {})
        if provider:
            print(f"  Provider: {provider.get('name')}")
        
        print(f"  Duration: {course.get('totalTrainingDurationHour', 0)} hours")
        print(f"  Cost: ${course.get('totalCostOfTrainingPerTrainee', 0):.2f}")
        
        areas = course.get('areaOfTrainings', [])
        if areas:
            print(f"  Area: {areas[0].get('description')}")
        
        runs = course.get('runs', [])
        print(f"  Available runs: {len(runs)}")
    else:
        print("\n  No course details found")
    
    save_response(result, "example_7_course_details.json")
    return result

def example_8_related_courses():
    """Example 8: Retrieve courses related to a specific course."""
    print("\n" + "="*80)
    print("Example 8: Get Related Courses")
    print("="*80)
    
    # Using an example course reference number
    course_ref = "SCN-198202248E-01-CRS-N-0027685"
    print(f"\nRetrieving courses related to: {course_ref}...")
    
    cert_path = os.path.join(os.path.dirname(__file__), "..", "certificates", "cert.pem")
    key_path = os.path.join(os.path.dirname(__file__), "..", "certificates", "key.pem")
    
    api = CoursesAPI(cert_path, key_path)
    result = api.get_related_courses(course_reference_number=course_ref)
    
    courses = result.get('data', {}).get('courses', [])
    
    print(f"\nFound {len(courses)} related courses:")
    for i, course in enumerate(courses, 1):
        print(f"\n  {i}. {course.get('title')}")
        print(f"     Reference: {course.get('referenceNumber')}")
        provider = course.get('trainingProvider', {})
        if provider:
            print(f"     Provider: {provider.get('name')}")
    
    save_response(result, "example_8_related_courses.json")
    return result

def example_9_popular_courses():
    """Example 9: Retrieve popular/trending courses."""
    print("\n" + "="*80)
    print("Example 9: Get Popular Courses")
    print("="*80)
    print("\nRetrieving popular courses...")
    
    cert_path = os.path.join(os.path.dirname(__file__), "..", "certificates", "cert.pem")
    key_path = os.path.join(os.path.dirname(__file__), "..", "certificates", "key.pem")
    
    api = CoursesAPI(cert_path, key_path)
    result = api.get_popular_courses(page_size=5)
    
    courses = result.get('data', {}).get('courses', [])
    total = result.get('data', {}).get('meta', {}).get('total', 0)
    
    print(f"\nFound {total} popular courses (showing first {len(courses)}):")
    for i, course in enumerate(courses, 1):
        print(f"\n  {i}. {course.get('title')}")
        print(f"     Reference: {course.get('referenceNumber')}")
        provider = course.get('trainingProvider', {})
        if provider:
            print(f"     Provider: {provider.get('name')}")
        areas = course.get('areaOfTrainings', [])
        if areas:
            print(f"     Area: {areas[0].get('description')}")
    
    save_response(result, "example_9_popular_courses.json")
    return result

def example_10_featured_courses():
    """Example 10: Retrieve featured courses from MySkillsFuture."""
    print("\n" + "="*80)
    print("Example 10: Get Featured Courses")
    print("="*80)
    print("\nRetrieving featured courses from MySkillsFuture...")
    
    cert_path = os.path.join(os.path.dirname(__file__), "..", "certificates", "cert.pem")
    key_path = os.path.join(os.path.dirname(__file__), "..", "certificates", "key.pem")
    
    api = CoursesAPI(cert_path, key_path)
    result = api.get_featured_courses(page_size=5)
    
    courses = result.get('data', {}).get('courses', [])
    total = result.get('data', {}).get('meta', {}).get('total', 0)
    
    print(f"\nFound {total} featured courses (showing first {len(courses)}):")
    for i, course in enumerate(courses, 1):
        print(f"\n  {i}. {course.get('title')}")
        print(f"     Reference: {course.get('referenceNumber')}")
        provider = course.get('trainingProvider', {})
        if provider:
            print(f"     Provider: {provider.get('name')}")
        areas = course.get('areaOfTrainings', [])
        if areas:
            print(f"     Area: {areas[0].get('description')}")
    
    save_response(result, "example_10_featured_courses.json")
    return result

def run_all_examples():
    """Run all Courses API examples."""
    print("\n" + "="*80)
    print("SSG-WSG COURSES API - CERTIFICATE AUTHENTICATION EXAMPLES")
    print("="*80)
    print("\nBase URL: https://api.ssg-wsg.sg")
    print("Authentication: Certificate-based (mTLS)")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    examples = [
        ("1", "Course Categories", example_1_course_categories),
        ("2", "Course Tags", example_2_course_tags),
        ("3", "Search by Keyword", example_3_search_by_keyword),
        ("4", "Search by Tagging", example_4_search_by_tagging),
        ("5", "Autocomplete", example_5_autocomplete),
        ("6", "Course SubCategories", example_6_subcategories),
        ("7", "Course Details", example_7_course_details),
        ("8", "Related Courses", example_8_related_courses),
        ("9", "Popular Courses", example_9_popular_courses),
        ("10", "Featured Courses", example_10_featured_courses),
    ]
    
    while True:
        print("\n" + "="*80)
        print("Available Examples:")
        print("="*80)
        for num, name, _ in examples:
            print(f"  {num}. {name}")
        print("  0. Run all examples")
        print("  q. Quit")
        
        choice = input("\nSelect an example (0-10, or q to quit): ").strip().lower()
        
        if choice == 'q':
            print("\nExiting...")
            break
        elif choice == '0':
            for _, _, func in examples:
                try:
                    func()
                except Exception as e:
                    print(f"\n✗ Error: {str(e)}")
            print("\n" + "="*80)
            print("All examples completed!")
            print("="*80)
        elif choice in [num for num, _, _ in examples]:
            for num, _, func in examples:
                if num == choice:
                    try:
                        func()
                    except Exception as e:
                        print(f"\n✗ Error: {str(e)}")
                    break
        else:
            print("\n✗ Invalid choice. Please try again.")

if __name__ == "__main__":
    run_all_examples()
