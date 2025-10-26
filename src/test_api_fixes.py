"""
Certificate Authentication Endpoints Verification

This script verifies all certificate-authenticated endpoints are working correctly.
Runs quick tests on all 6 working endpoints to ensure connectivity and proper responses.

Usage: python src/test_api_fixes.py
"""

from api_examples import SkillsFrameworkAPI
import json


def test_endpoint(name, func, *args, **kwargs):
    """Test a single endpoint and display results."""
    print(f"\n{'='*70}")
    print(f"Testing: {name}")
    print(f"{'='*70}")
    
    try:
        result = func(*args, **kwargs)
        
        if result and result.get('status') in [200, '200']:
            print(f"✓ SUCCESS - Status: {result.get('status')}")
            
            # Display data summary
            if 'data' in result:
                data = result['data']
                if isinstance(data, dict):
                    if 'jobRoles' in data:
                        print(f"  - Job Roles Count: {len(data['jobRoles'])}")
                    elif 'codes' in data:
                        print(f"  - Codes Count: {len(data['codes'])}")
                    elif 'technicalSkillCompetencies' in data:
                        print(f"  - TSC Details Count: {len(data['technicalSkillCompetencies'])}")
                    elif 'genericSkillCompetencies' in data:
                        print(f"  - GSC Details Count: {len(data['genericSkillCompetencies'])}")
                    else:
                        print(f"  - Data Keys: {list(data.keys())}")
                elif isinstance(data, list):
                    print(f"  - Items Count: {len(data)}")
            
            return True
        else:
            status = result.get('status') if result else 'No response'
            print(f"✗ FAILED - Status: {status}")
            return False
            
    except Exception as e:
        print(f"✗ ERROR: {str(e)}")
        return False


def main():
    print("\n" + "="*70)
    print("CERTIFICATE AUTHENTICATION ENDPOINTS VERIFICATION")
    print("="*70)
    print("\nTesting all 6 working certificate-authenticated endpoints...")
    print("Base URL: https://api.ssg-wsg.sg/skillsFramework")
    
    try:
        api = SkillsFrameworkAPI()
        print("\n✓ API Client initialized successfully")
        print(f"  Base URL: {api.BASE_URL}")
        print(f"  Certificate: {api.cert_path}")
    except Exception as e:
        print(f"\n✗ Failed to initialize API client: {e}")
        return
    
    # Test results tracking
    results = {}
    
    # Test 1: Job Roles Search
    results['Job Roles Search'] = test_endpoint(
        "Job Roles Search - /jobRoles",
        api.get_job_roles,
        keyword="data",
        page=0,
        page_size=5
    )
    
    # Test 2: Job Role Titles Autocomplete
    results['Job Role Titles'] = test_endpoint(
        "Job Role Titles Autocomplete - /jobRoles/titles",
        api.get_job_role_titles,
        keyword="data"
    )
    
    # Test 3: TSC Technical Skills (Basic)
    results['TSC Basic'] = test_endpoint(
        "TSC Basic - /codes/skillsAndCompetencies/technical/autocomplete",
        api.get_tsc_technical_skills,
        keyword="data"
    )
    
    # Test 4: CCS Generic Skills (Basic)
    results['CCS Basic'] = test_endpoint(
        "CCS Basic - /codes/skillsAndCompetencies/generic/autocomplete",
        api.get_ccs_generic_skills,
        keyword="communication"
    )
    
    # Test 5: TSC Autocomplete Details
    results['TSC Details'] = test_endpoint(
        "TSC Details - /codes/skillsAndCompetencies/technical/autocomplete/details",
        api.get_tsc_autocomplete_details,
        keyword="data"
    )
    
    # Test 6: CCS Autocomplete Details
    results['CCS Details'] = test_endpoint(
        "CCS Details - /codes/skillsAndCompetencies/generic/autocomplete/details",
        api.get_ccs_autocomplete_details,
        keyword="comm"
    )
    
    # Summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for name, success in results.items():
        status = "✓ PASS" if success else "✗ FAIL"
        print(f"{status} - {name}")
    
    print(f"\nResults: {passed}/{total} tests passed ({passed/total*100:.0f}%)")
    
    if passed == total:
        print("\n✓ All certificate-authenticated endpoints are working correctly!")
    else:
        print(f"\n⚠ Warning: {total - passed} endpoint(s) failed. Check error messages above.")
    
    print("\nNote: All tested endpoints use certificate authentication.")
    print("For full examples with output saving, run: python src/api_examples.py")


if __name__ == "__main__":
    main()
