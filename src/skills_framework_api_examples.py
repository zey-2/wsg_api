"""
Skills Framework API - Certificate Authentication Examples

This module provides working examples for Skills Framework API endpoints
that are accessible with CERTIFICATE AUTHENTICATION.

API Documentation: https://developer.ssg-wsg.gov.sg/webapp/docs/product/6Gl44K5M46EuDgn7LCsAs2/group/5uyNzClV5UJk6Uo0wDg7Mt

WORKING Certificate-Authenticated Endpoints:
1. Job Roles - Search and retrieve job roles
2. Job Role Titles - Autocomplete for job role titles (up to 5 results)
3. Skills & Competencies Generic (CCS/GSC) - Critical Core Skills autocomplete
4. Skills & Competencies Technical (TSC) - Technical Skills autocomplete
5. TSC Code Autocomplete Details - Detailed technical skills information
6. CCS Code Autocomplete Details - Detailed generic skills information

NOTE: The following endpoints return 403 Forbidden with certificate authentication
and are NOT included in this implementation:
- Sectors, Sector Profile, Subsectors, Videos By Sector
- Field of Studies, SSIC List
- Occupations, Job Roles By Occupation
- Job Role Details By ID, Job Role Profile By ID, Related Job Roles By ID
- Get CCS Details, Get TSC Details (require Corppass subscription approval)

These endpoints may require different authentication or additional API permissions.

Author: Generated for NTU Data Science & AI Capstone Project
Date: October 2025
"""

import requests
import json
import os
from typing import Dict, Any, Optional, List
from datetime import datetime


class SkillsFrameworkAPI:
    """
    A client for the Singapore Skills Framework API (Certificate Authentication).
    
    This class provides methods to interact with certificate-authenticated endpoints.
    Only includes endpoints that are confirmed to work with certificate authentication.
    """
    
    BASE_URL = "https://api.ssg-wsg.sg/skillsFramework"
    
    def __init__(self, cert_path: str = "certificates/cert.pem", key_path: str = "certificates/key.pem"):
        """
        Initialize the API client with certificate paths.
        
        Parameters:
        cert_path (str): Path to the certificate file
        key_path (str): Path to the private key file
        """
        self.cert_path = cert_path
        self.key_path = key_path
        self.cert = (cert_path, key_path)
        
        # Verify certificate files exist
        if not os.path.exists(cert_path):
            raise FileNotFoundError(f"Certificate file not found: {cert_path}")
        if not os.path.exists(key_path):
            raise FileNotFoundError(f"Key file not found: {key_path}")
    
    def _make_request(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
        """
        Make an authenticated API request.
        
        Parameters:
        endpoint (str): API endpoint path
        params (Optional[Dict[str, Any]]): Query parameters
        
        Returns:
        Optional[Dict[str, Any]]: JSON response or None if failed
        """
        url = f"{self.BASE_URL}/{endpoint}"
        
        try:
            print(f"Requesting: {url}")
            if params:
                print(f"Parameters: {params}")
            
            response = requests.get(
                url,
                cert=self.cert,
                params=params,
                timeout=30
            )
            
            response.raise_for_status()
            print(f"✓ Status: {response.status_code}")
            return response.json()
            
        except requests.exceptions.RequestException as e:
            print(f"✗ Error: {e}")
            return None
    
    # ========== Job Roles APIs (Certificate Auth - WORKING) ==========
    
    def get_job_roles(
        self,
        keyword: Optional[str] = None,
        sector: Optional[str] = None,
        qualification: Optional[str] = None,
        field_of_study: Optional[str] = None,
        page: int = 0,
        page_size: int = 20
    ) -> Optional[Dict[str, Any]]:
        """
        Search job roles based on various criteria.
        
        Parameters:
        keyword (str): Search keyword for job roles
        sector (str): Filter by sector ID (use comma delimiter for multiple)
        qualification (str): Filter by qualification ID (use comma delimiter for multiple)
        field_of_study (str): Filter by field of study ID (use comma delimiter for multiple)
        page (int): Page number starting from 0
        page_size (int): Number of results per page (default 20, max 100)
        
        Returns:
        Job roles with details including code, description, qualifications, sectors, etc.
        """
        params: Dict[str, Any] = {
            "page": page,
            "pageSize": page_size
        }
        if keyword:
            params["keyword"] = keyword
        if sector:
            params["sector"] = sector
        if qualification:
            params["qualification"] = qualification
        if field_of_study:
            params["fieldOfStudy"] = field_of_study
        
        return self._make_request("jobRoles", params)
    
    def get_job_role_titles(self, keyword: str) -> Optional[Dict[str, Any]]:
        """
        Get job role titles for autocomplete functionality.
        Retrieves up to 5 job role titles matching the keyword.
        
        Parameters:
        keyword (str): Search keyword (partial job role title, minimum 3 characters)
        
        Returns:
        Up to 5 matching job role titles with score, title, alternative title, etc.
        """
        params: Dict[str, Any] = {"keyword": keyword}
        return self._make_request("jobRoles/titles", params)
    
    # ========== Skills & Competencies APIs (Certificate Auth - WORKING) ==========
    
    def get_ccs_generic_skills(self, keyword: str) -> Optional[Dict[str, Any]]:
        """
        Get Generic Skills Competency (GSC) / Critical Core Skills (CCS) codes for autocomplete.
        Search for generic/critical core skills.
        
        Parameters:
        keyword (str): Search keyword (minimum 3 characters, avoid spaces)
        
        Returns:
        GSC/CCS codes with code and description
        
        Note: Keywords with spaces may cause 500 errors. Use single words or hyphens.
        """
        params: Dict[str, Any] = {"keyword": keyword}
        return self._make_request("codes/skillsAndCompetencies/generic/autocomplete", params)
    
    def get_tsc_technical_skills(self, keyword: str) -> Optional[Dict[str, Any]]:
        """
        Get Technical Skill Competency (TSC) codes for autocomplete.
        Search for technical skills by skill category.
        
        Parameters:
        keyword (str): Search keyword (minimum 3 characters, avoid spaces)
                      Examples: "data", "prog", "soft", "comm"
        
        Returns:
        TSC codes with code and description (e.g., "Data Analysis-2", "Programming and Coding-3")
        
        Note: 
        - TSC codes represent skill CATEGORIES (e.g., "Data Analysis", "Programming and Coding"),
          not specific technologies (e.g., "python", "java" will return 404).
        - Keywords with spaces may cause 500 errors. Use single words or hyphens.
        - May return 404 if no matching TSC codes found for the keyword.
        """
        params: Dict[str, Any] = {"keyword": keyword}
        return self._make_request("codes/skillsAndCompetencies/technical/autocomplete", params)
    
    def get_tsc_autocomplete_details(self, keyword: str) -> Optional[Dict[str, Any]]:
        """
        Get detailed Technical Skill Competency (TSC) information for autocomplete.
        Returns more detailed information including titles, categories, and level info.
        
        Parameters:
        keyword (str): Search keyword (minimum 3 characters, avoid spaces)
                      Examples: "data", "prog", "soft", "comm"
        
        Returns:
        Detailed TSC information including:
        - technicalSkillCompetencies: Array of skills with code, title, category, level, etc.
        
        Note: 
        - Returns more details than get_tsc_technical_skills()
        - Keywords with spaces may cause 500 errors. Use single words or hyphens.
        - May return 404 if no matching TSC codes found for the keyword.
        """
        params: Dict[str, Any] = {"keyword": keyword}
        return self._make_request("codes/skillsAndCompetencies/technical/autocomplete/details", params)
    
    def get_ccs_autocomplete_details(self, keyword: str) -> Optional[Dict[str, Any]]:
        """
        Get detailed Generic/Critical Core Skills (GSC/CCS) information for autocomplete.
        Returns more detailed information including titles, categories, and level info.
        
        Parameters:
        keyword (str): Search keyword (minimum 3 characters, avoid spaces)
                      Examples: "comm", "problem", "leader"
        
        Returns:
        Detailed GSC/CCS information including:
        - genericSkillCompetencies: Array of skills with code, title, category, level, etc.
        
        Note: 
        - Returns more details than get_ccs_generic_skills()
        - Keywords with spaces may cause 500 errors. Use single words or hyphens.
        - May return 404 if no matching codes found for the keyword.
        """
        params: Dict[str, Any] = {"keyword": keyword}
        return self._make_request("codes/skillsAndCompetencies/generic/autocomplete/details", params)


# ========== Example Usage Functions ==========

def example_1_search_job_roles():
    """Example 1: Search for job roles with keyword."""
    print("\n" + "=" * 80)
    print("EXAMPLE 1: Search Job Roles by Keyword")
    print("=" * 80)
    
    api = SkillsFrameworkAPI()
    
    # Search for data-related job roles
    result = api.get_job_roles(keyword="data", page_size=5)
    
    if result:
        print("\nFound job roles related to 'data':")
        save_example_output("example_1_job_roles_search.json", result)


def example_2_autocomplete_job_titles():
    """Example 2: Use job role title autocomplete."""
    print("\n" + "=" * 80)
    print("EXAMPLE 2: Job Role Title Autocomplete")
    print("=" * 80)
    
    api = SkillsFrameworkAPI()
    
    # Autocomplete for "data"
    result = api.get_job_role_titles(keyword="data")
    
    if result:
        print("\nAutocomplete suggestions for 'data':")
        save_example_output("example_2_job_title_autocomplete.json", result)


def example_3_search_technical_skills():
    """Example 3: Search for technical skills (TSC)."""
    print("\n" + "=" * 80)
    print("EXAMPLE 3: Search Technical Skills")
    print("=" * 80)
    
    api = SkillsFrameworkAPI()
    
    # Search for data-related technical skills
    # Note: TSC codes are skill categories (e.g., "Data Analysis", "Programming")
    # not specific technologies (e.g., "python", "java")
    result = api.get_tsc_technical_skills(keyword="data")
    
    if result:
        print("\nTechnical skills related to 'data':")
        print(f"Found {result.get('meta', {}).get('total', 0)} TSC codes")
        save_example_output("example_3_technical_skills.json", result)


def example_4_search_core_skills():
    """Example 4: Search for critical core skills (CCS)."""
    print("\n" + "=" * 80)
    print("EXAMPLE 4: Search Critical Core Skills")
    print("=" * 80)
    
    api = SkillsFrameworkAPI()
    
    # Search for communication skills
    result = api.get_ccs_generic_skills(keyword="communication")
    
    if result:
        print("\nCritical core skills related to 'communication':")
        save_example_output("example_4_core_skills.json", result)


def example_5_advanced_job_search():
    """Example 5: Advanced job role search with multiple filters."""
    print("\n" + "=" * 80)
    print("EXAMPLE 5: Advanced Job Role Search")
    print("=" * 80)
    
    api = SkillsFrameworkAPI()
    
    # Search with multiple criteria
    result = api.get_job_roles(
        keyword="engineer",
        qualification="Degree",
        page_size=10
    )
    
    if result:
        print("\nJob roles matching criteria:")
        print("- Keyword: engineer")
        print("- Qualification: Degree")
        save_example_output("example_5_advanced_search.json", result)


def example_6_tsc_autocomplete_details():
    """Example 6: Get detailed TSC skill information."""
    print("\n" + "=" * 80)
    print("EXAMPLE 6: TSC Autocomplete with Detailed Information")
    print("=" * 80)
    
    api = SkillsFrameworkAPI()
    
    # Get detailed information about technical skills
    result = api.get_tsc_autocomplete_details(keyword="data")
    
    if result:
        print("\nDetailed technical skill information for 'data':")
        if result.get('data') and result['data'].get('technicalSkillCompetencies'):
            skills = result['data']['technicalSkillCompetencies']
            print(f"Found {len(skills)} detailed TSC entries")
        save_example_output("example_6_tsc_details.json", result)


def example_7_ccs_autocomplete_details():
    """Example 7: Get detailed CCS/GSC skill information."""
    print("\n" + "=" * 80)
    print("EXAMPLE 7: CCS Autocomplete with Detailed Information")
    print("=" * 80)
    
    api = SkillsFrameworkAPI()
    
    # Get detailed information about generic/core skills
    result = api.get_ccs_autocomplete_details(keyword="comm")
    
    if result:
        print("\nDetailed generic skill information for 'comm':")
        if result.get('data') and result['data'].get('genericSkillCompetencies'):
            skills = result['data']['genericSkillCompetencies']
            print(f"Found {len(skills)} detailed CCS entries")
        save_example_output("example_7_ccs_details.json", result)


def save_example_output(filename: str, data: Dict[str, Any]) -> None:
    """Save example output to a JSON file."""
    output_dir = "data/skills_framework_examples"
    os.makedirs(output_dir, exist_ok=True)
    
    file_path = os.path.join(output_dir, filename)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"✓ Saved to: {file_path}")


def run_all_examples():
    """Run all example functions."""
    print("\n" + "=" * 80)
    print("SKILLS FRAMEWORK API - CERTIFICATE AUTHENTICATION EXAMPLES")
    print("=" * 80)
    print("\nRunning all working examples...")
    
    examples = [
        example_1_search_job_roles,
        example_2_autocomplete_job_titles,
        example_3_search_technical_skills,
        example_4_search_core_skills,
        example_5_advanced_job_search,
        example_6_tsc_autocomplete_details,
        example_7_ccs_autocomplete_details,
    ]
    
    for i, example_func in enumerate(examples, 1):
        try:
            example_func()
        except Exception as e:
            print(f"\n✗ Error in example {i}: {e}")
    
    print("\n" + "=" * 80)
    print("ALL EXAMPLES COMPLETED")
    print("=" * 80)


def main():
    """Main function with menu for running examples."""
    print("\n" + "=" * 80)
    print("SKILLS FRAMEWORK API - CERTIFICATE AUTHENTICATION EXAMPLES")
    print("=" * 80)
    print("\nAvailable Working Examples (Certificate Auth Only):")
    print("1. Search Job Roles by Keyword")
    print("2. Job Role Title Autocomplete")
    print("3. Search Technical Skills (TSC)")
    print("4. Search Critical Core Skills (CCS)")
    print("5. Advanced Job Role Search")
    print("6. TSC Autocomplete with Detailed Info")
    print("7. CCS Autocomplete with Detailed Info")
    print("0. Run ALL Examples")
    print("\nEnter 'q' to quit")
    
    while True:
        choice = input("\nSelect an example (0-7, or 'q' to quit): ").strip()
        
        if choice.lower() == 'q':
            print("Exiting...")
            break
        
        if choice == '0':
            run_all_examples()
        elif choice == '1':
            example_1_search_job_roles()
        elif choice == '2':
            example_2_autocomplete_job_titles()
        elif choice == '3':
            example_3_search_technical_skills()
        elif choice == '4':
            example_4_search_core_skills()
        elif choice == '5':
            example_5_advanced_job_search()
        elif choice == '6':
            example_6_tsc_autocomplete_details()
        elif choice == '7':
            example_7_ccs_autocomplete_details()
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
