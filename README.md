# Skills Framework API - Examples Guide

This guide demonstrates how to use the comprehensive API examples for the Singapore Skills Framework API.

## Reference Materials

The information in the `reference` folder is obtained from:
https://github.com/ssg-wsg/Sample-Codes/tree/master/API%20Basic%20Access/Certificate%20Authentication/Python

## Overview

The `skills_framework_api_examples.py` file provides a complete implementation of all available Skills Framework API endpoints with working examples.

## Prerequisites

1. Valid SSL certificates (`cert.pem` and `key.pem`) in the `certificates/` directory
2. Python 3.7 or higher
3. Required packages: `requests`

## Installation

```bash
pip install requests
```

## Available API Endpoints

### Job Roles APIs

1. **Job Roles Search** - Search job roles with filters (keyword, sector, qualification, field of study)
2. **Job Role Titles Autocomplete** - Get up to 5 matching job role titles
3. **Job Role Details By ID** - Get comprehensive details for a specific job role
4. **Job Role Profile By ID** - Get job role profile with RIASEC compatibility
5. **Related Job Roles** - Find related job roles by ID
6. **Job Roles By Occupation** - Get job roles for a specific occupation

### Sectors APIs

7. **Sectors List** - Get all sectors in the taxonomy
8. **Sector Profile** - Get detailed sector profile
9. **Subsectors** - Get subsectors by sector ID
10. **Videos By Sector** - Get sector-related videos

### Classifications APIs

11. **Occupations** - Get occupations by sector
12. **SSIC List** - Singapore Standard Industrial Classification
13. **Field of Studies** - Educational classification (SSEC-FOS)

### Skills & Competencies APIs

14. **CCS Generic Skills** - Search Critical Core Skills
15. **TSC Technical Skills** - Search Technical Skill Competencies
16. **CCS Autocomplete Details** - Detailed CCS search
17. **TSC Autocomplete Details** - Detailed TSC search
18. **Get CCS Details** - Full CCS details by retrieval type
19. **Get TSC Details** - Full TSC details by retrieval type

## Usage

### Quick Start - Interactive Menu

Run the script to access an interactive menu:

```bash
python src/skills_framework_api_examples.py
```

This will display:

```
SKILLS FRAMEWORK API - EXAMPLES MENU
================================================================================

Available Examples:
1.  Search Job Roles by Keyword
2.  Job Role Title Autocomplete
3.  Get Job Role Details by ID
...
0.  Run ALL Examples

Enter 'q' to quit

Select an example (0-15, or 'q' to quit):
```

### Using the SkillsFrameworkAPI Class

```python
from skills_framework_api_examples import SkillsFrameworkAPI

# Initialize the API client
api = SkillsFrameworkAPI(
    cert_path="certificates/cert.pem",
    key_path="certificates/key.pem"
)

# Search for job roles
result = api.get_job_roles(keyword="data scientist", limit=10)
print(result)

# Get job role titles for autocomplete
titles = api.get_job_role_titles(keyword="engineer")
print(titles)

# Get all sectors
sectors = api.get_sectors()
print(sectors)

# Search for technical skills
tech_skills = api.get_tsc_technical_skills(keyword="python")
print(tech_skills)

# Search for core skills
core_skills = api.get_ccs_generic_skills(keyword="communication")
print(core_skills)
```

## Example Scenarios

### Scenario 1: Building a Job Search Portal

```python
api = SkillsFrameworkAPI()

# User types "data" in search box
autocomplete_results = api.get_job_role_titles(keyword="data")

# User selects "Data Scientist" and searches
search_results = api.get_job_roles(
    keyword="data scientist",
    qualification="Degree",
    limit=20
)

# User clicks on a specific job role
job_role_id = search_results['data'][0]['jobRoleId']
job_details = api.get_job_role_details_by_id(job_role_id)
job_profile = api.get_job_role_profile_by_id(job_role_id)
related_jobs = api.get_related_job_roles(job_role_id)
```

### Scenario 2: Skills Analysis

```python
api = SkillsFrameworkAPI()

# Get all technical skills related to Python
python_skills = api.get_tsc_technical_skills(keyword="python")

# Get detailed TSC information
detailed_tsc = api.get_tsc_autocomplete_details(keyword="machine learning")

# Get all CCS details
all_ccs = api.get_ccs_details(retrieval_type="full")

# Search for specific core skills
problem_solving = api.get_ccs_generic_skills(keyword="problem solving")
```

### Scenario 3: Sector and Occupation Analysis

```python
api = SkillsFrameworkAPI()

# Get all sectors
sectors = api.get_sectors()

# Get detailed profile for first sector
sector_id = sectors['data'][0]['sectorId']
sector_profile = api.get_sector_profile(sector_id)

# Get occupations in this sector
occupations = api.get_occupations(sector_id)

# Get subsectors
subsectors = api.get_subsectors(sector_id=sector_id)

# Get sector videos
videos = api.get_videos_by_sector(sector_id)

# For each occupation, get job roles
occupation_id = occupations['data'][0]['id']
job_roles = api.get_job_roles_by_occupation(occupation_id)
```

### Scenario 4: Educational Pathway Planning

```python
api = SkillsFrameworkAPI()

# Get field of studies classification
field_of_studies = api.get_field_of_studies()

# Search for job roles by qualification
degree_jobs = api.get_job_roles(qualification="Degree", limit=50)
diploma_jobs = api.get_job_roles(qualification="Diploma", limit=50)

# Get job roles in a specific field
engineering_jobs = api.get_job_roles(
    field_of_study="Engineering",
    qualification="Degree"
)
```

## Output

All examples save their results to `data/skills_framework_examples/` directory as JSON files:

- `example_1_job_roles_search.json`
- `example_2_job_title_autocomplete.json`
- `example_3_job_role_details.json`
- ... and more

## API Response Structure

### Typical Response Format

```json
{
  "status": "success",
  "data": [
    {
      "jobRoleId": "12345",
      "title": "Data Scientist",
      "description": "...",
      "sector": {...},
      "skills": [...],
      ...
    }
  ],
  "meta": {
    "total": 100,
    "offset": 0,
    "limit": 20
  }
}
```

## Error Handling

The API client includes comprehensive error handling:

- **FileNotFoundError**: Certificate files not found
- **Timeout**: Request timeout (30 seconds)
- **ConnectionError**: Network connectivity issues
- **HTTPError**: HTTP error responses
- **JSONDecodeError**: Invalid JSON response

Example:

```python
api = SkillsFrameworkAPI()
result = api.get_job_roles(keyword="engineer")

if result is None:
    print("API request failed - check logs for details")
else:
    print(f"Found {len(result.get('data', []))} results")
```

## Pagination

For endpoints that support pagination:

```python
api = SkillsFrameworkAPI()

# Get first page
page1 = api.get_job_roles(keyword="engineer", offset=0, limit=20)

# Get second page
page2 = api.get_job_roles(keyword="engineer", offset=20, limit=20)

# Get third page
page3 = api.get_job_roles(keyword="engineer", offset=40, limit=20)
```

## Best Practices

1. **Use autocomplete endpoints** for search-as-you-type features
2. **Cache sector and classification data** as they change infrequently
3. **Implement pagination** for large result sets
4. **Handle errors gracefully** with appropriate user feedback
5. **Use specific IDs** when fetching detailed information
6. **Combine multiple endpoints** for comprehensive data

## Common Use Cases

### Building an Autocomplete Search

```python
def autocomplete_job_search(user_input: str):
    api = SkillsFrameworkAPI()

    if len(user_input) < 3:
        return []

    results = api.get_job_role_titles(keyword=user_input)

    if results and results.get('data'):
        return [item['title'] for item in results['data']]

    return []
```

### Finding Skills Gap

```python
def analyze_skills_gap(current_role_id: str, target_role_id: str):
    api = SkillsFrameworkAPI()

    current_role = api.get_job_role_details_by_id(current_role_id)
    target_role = api.get_job_role_details_by_id(target_role_id)

    current_skills = set(s['code'] for s in current_role['data']['skills'])
    target_skills = set(s['code'] for s in target_role['data']['skills'])

    skills_gap = target_skills - current_skills

    return skills_gap
```

### Career Path Recommendation

```python
def recommend_career_paths(job_role_id: str):
    api = SkillsFrameworkAPI()

    # Get current job details
    current_job = api.get_job_role_details_by_id(job_role_id)

    # Get related jobs
    related_jobs = api.get_related_job_roles(job_role_id)

    # Get jobs in same occupation
    occupation_id = current_job['data']['occupationId']
    occupation_jobs = api.get_job_roles_by_occupation(occupation_id)

    return {
        'current': current_job,
        'related': related_jobs,
        'same_occupation': occupation_jobs
    }
```

## Testing

To verify your setup:

```bash
# Run a single example
python src/skills_framework_api_examples.py
# Select option 1

# Run all examples
python src/skills_framework_api_examples.py
# Select option 0
```

## Troubleshooting

### Certificate Issues

- Ensure `cert.pem` and `key.pem` are in the `certificates/` directory
- Verify certificates are valid and not expired
- Check file permissions

### Connection Issues

- Verify internet connectivity
- Check if API endpoint is accessible
- Ensure firewall allows outbound HTTPS connections

### Empty Results

- Verify search keywords are valid
- Check if filters are too restrictive
- Try broader search terms

## Additional Resources

- [Official API Documentation](https://developer.ssg-wsg.gov.sg/webapp/docs/product/6Gl44K5M46EuDgn7LCsAs2/group/5uyNzClV5UJk6Uo0wDg7Mt)
- [SSG-WSG Developer Portal](https://developer.ssg-wsg.gov.sg/)
- [API Status Monitoring](https://status.api.ssg-wsg.sg/)

## Support

For API-related issues:

- [Community Forum](https://stackoverflow.com/search?q=%22ssg-wsg%22)
- [FAQs](https://developer.ssg-wsg.gov.sg/webapp/faq)

## License

This code is provided for educational purposes as part of the NTU Data Science & AI Capstone Project.
