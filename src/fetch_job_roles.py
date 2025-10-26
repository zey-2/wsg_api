"""
Skills Framework Job Roles Data Fetcher

This script fetches job roles data from the Singapore Skills Framework API
and saves the response as a JSON file for further processing.

Author: Generated for NTU Data Science & AI Capstone Project
Date: October 2025
"""

import requests
import json
import os
from datetime import datetime
from typing import Dict, Any, Optional


def fetch_job_roles_data(
    api_url: str = "https://api.ssg-wsg.sg/skillsFramework/jobRoles",
    cert_path: str = "cert.pem",
    key_path: str = "key.pem"
) -> Optional[Dict[str, Any]]:
    """
    Fetch job roles data from the Skills Framework API using certificate authentication.
    
    Parameters:
    api_url (str): The API endpoint URL for job roles data
    cert_path (str): Path to the certificate file
    key_path (str): Path to the private key file
    
    Returns:
    Optional[Dict[str, Any]]: The JSON response data if successful, None if failed
    
    Raises:
    requests.exceptions.RequestException: If the API request fails
    FileNotFoundError: If certificate or key files are not found
    """
    try:
        # Verify certificate files exist
        if not os.path.exists(cert_path):
            raise FileNotFoundError(f"Certificate file not found: {cert_path}")
        if not os.path.exists(key_path):
            raise FileNotFoundError(f"Key file not found: {key_path}")
        
        print("Fetching job roles data from Skills Framework API...")
        print(f"API URL: {api_url}")
        
        # Make the API request with certificate authentication
        response = requests.get(
            api_url,
            cert=(cert_path, key_path),
            timeout=30  # 30 second timeout
        )
        
        # Check if request was successful
        response.raise_for_status()
        
        print(f"Status Code: {response.status_code}")
        print("Data fetched successfully!")
        
        return response.json()
        
    except FileNotFoundError as e:
        print(f"Error: {e}")
        return None
    except requests.exceptions.Timeout:
        print("Error: Request timed out. Please try again.")
        return None
    except requests.exceptions.ConnectionError:
        print("Error: Failed to connect to the API. Please check your internet connection.")
        return None
    except requests.exceptions.HTTPError as e:
        print(f"Error: HTTP {response.status_code} - {e}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Error: Request failed - {e}")
        return None
    except json.JSONDecodeError:
        print("Error: Invalid JSON response from API")
        return None


def save_json_data(
    data: Dict[str, Any],
    filename: Optional[str] = None,
    output_dir: str = "data"
) -> bool:
    """
    Save the fetched data as a JSON file with proper formatting.
    
    Parameters:
    data (Dict[str, Any]): The data to save as JSON
    filename (Optional[str]): Custom filename, if None generates timestamp-based name
    output_dir (str): Directory to save the file in
    
    Returns:
    bool: True if successful, False otherwise
    """
    try:
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Generate filename if not provided
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"job_roles_data_{timestamp}.json"
        
        # Ensure filename has .json extension
        if not filename.endswith('.json'):
            filename += '.json'
        
        file_path = os.path.join(output_dir, filename)
        
        # Save data as formatted JSON
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(
                data,
                f,
                indent=2,
                ensure_ascii=False,
                separators=(',', ': ')
            )
        
        print(f"Data saved successfully to: {file_path}")
        
        # Print some basic statistics about the data
        if isinstance(data, dict):
            print(f"Number of top-level keys: {len(data.keys())}")
            if 'data' in data and isinstance(data['data'], list):
                print(f"Number of job roles: {len(data['data'])}")
        
        return True
        
    except OSError as e:
        print(f"Error: Failed to create directory or write file - {e}")
        return False
    except Exception as e:
        print(f"Error: Failed to save JSON data - {e}")
        return False


def main() -> None:
    """
    Main function to orchestrate the data fetching and saving process.
    """
    print("=" * 60)
    print("Skills Framework Job Roles Data Fetcher")
    print("=" * 60)
    
    # API endpoint for job roles
    api_url = "https://api.ssg-wsg.sg/skillsFramework/jobRoles"
    
    # Fetch the data
    job_roles_data = fetch_job_roles_data(api_url)
    
    if job_roles_data is None:
        print("Failed to fetch data. Please check your certificates and try again.")
        return
    
    # Save the data
    success = save_json_data(job_roles_data)
    
    if success:
        print("\nProcess completed successfully!")
        print("You can now use the saved JSON file for further processing.")
    else:
        print("\nFailed to save data to file.")


if __name__ == "__main__":
    main()