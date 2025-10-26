# SSG-WSG Courses API - Certificate Authentication Examples

## Overview

This package provides complete working examples of the **SSG-WSG Courses API** using **certificate authentication** (mTLS). All examples have been tested and verified to work with the production API.

**Base URL:** `https://api.ssg-wsg.sg`  
**Authentication:** Certificate-based (mutual TLS)

## 📁 Project Structure

```
skills_framework/
├── certificates/
│   ├── cert.pem              # Client certificate
│   └── key.pem               # Private key
├── data/
│   ├── courses_examples/     # Courses API example outputs (5 files)
│   └── skills_framework_examples/             # Skills Framework API outputs (7 files)
├── src/
│   ├── courses_api_examples.py         # Courses API client & examples
│   ├── skills_framework_api_examples.py                  # Skills Framework API client
│   ├── test_courses_api.py             # Courses API test script
│   └── test_api_fixes.py               # Skills Framework test script
├── COURSES_API_SUMMARY.md    # Comprehensive Courses API documentation
├── SKILLS_FRAMEWORK_API_SUMMARY.md  # Skills Framework API documentation
└── README.md                 # This file
```

## 🚀 Quick Start

### Installation

```bash
# Install required package
pip install requests
```

### Running Courses API Examples

```bash
# Run interactive examples menu
python src/courses_api_examples.py

# The script will present a menu:
# 1. Course Categories
# 2. Course Tags
# 3. Search by Keyword
# 4. Search by Tagging
# 5. Autocomplete
# 0. Run all examples
# q. Quit
```

### Running Tests

```bash
# Test all Courses API endpoints
python src/test_courses_api.py

# Test Skills Framework API endpoints
python src/test_api_fixes.py
```

## 📚 Available APIs

### Courses API (5 Working Endpoints)

| Endpoint                          | Description           | Example                                              |
| --------------------------------- | --------------------- | ---------------------------------------------------- |
| `/courses/categories`             | Get course categories | `api.get_course_categories(keyword='Training')`      |
| `/courses/tags`                   | Get course tags       | `api.get_course_tags(sort_by='0')`                   |
| `/courses/directory`              | Search by keyword     | `api.search_courses_by_keyword(keyword='python')`    |
| `/courses/directory`              | Search by tagging     | `api.search_courses_by_tagging(tagging_codes=['1'])` |
| `/courses/directory/autocomplete` | Get autocomplete      | `api.get_course_autocomplete(keyword='data')`        |

### Skills Framework API (6 Working Endpoints)

| Endpoint                                                  | Description      | Example                                            |
| --------------------------------------------------------- | ---------------- | -------------------------------------------------- |
| `/skills-framework/job-roles/search`                      | Search job roles | `api.get_job_roles(keyword='data')`                |
| `/skills-framework/job-role-titles`                       | Get job titles   | `api.get_job_role_titles(keyword='analyst')`       |
| `/skills-framework/tsc/technical-skills-and-competencies` | TSC basic        | `api.get_tsc_technical_skills()`                   |
| `/skills-framework/ccs/generic-skills-and-competencies`   | CCS basic        | `api.get_ccs_generic_skills()`                     |
| `/skills-framework/tsc/details`                           | TSC details      | `api.get_tsc_autocomplete_details(keyword='data')` |
| `/skills-framework/ccs/details`                           | CCS details      | `api.get_ccs_autocomplete_details(keyword='comm')` |

**Total Working Endpoints: 11** (5 Courses + 6 Skills Framework)

## 💡 Usage Examples

### Courses API - Python Client

```python
from src.courses_api_examples import CoursesAPI

# Initialize API client
api = CoursesAPI(
    cert_path='certificates/cert.pem',
    key_path='certificates/key.pem'
)

# Example 1: Get course categories
categories = api.get_course_categories(keyword='Training')
print(f"Found {len(categories['data']['categories'])} categories")

# Example 2: Search courses by keyword
courses = api.search_courses_by_keyword(
    keyword='python',
    page_size=10,
    page=0
)
for course in courses['data']['courses']:
    print(f"- {course['title']}")

# Example 3: Search SkillsFuture Credit courses
sfc_courses = api.search_courses_by_tagging(
    tagging_codes=['1'],  # SFC
    support_end_date='20250101',
    page_size=20
)
print(f"Found {len(sfc_courses['data']['courses'])} SFC courses")

# Example 4: Get autocomplete suggestions
suggestions = api.get_course_autocomplete(keyword='data')
for course in suggestions['data']['courses']:
    title = course['title'].replace('<b>', '').replace('</b>', '')
    print(f"- {title}")
```

### Skills Framework API - Python Client

```python
from src.skills_framework_api_examples import SkillsFrameworkAPI

# Initialize API client
api = SkillsFrameworkAPI(
    cert_path='certificates/cert.pem',
    key_path='certificates/key.pem'
)

# Search for data-related job roles
job_roles = api.get_job_roles(keyword='data')
for role in job_roles['jobRoles']:
    print(f"- {role['jobRoleTitle']}")

# Get technical skills (TSC)
tsc_skills = api.get_tsc_autocomplete_details(keyword='data')
for skill in tsc_skills:
    print(f"- {skill['title']}")
```

## 📊 Example Output Files

All API responses are automatically saved to JSON files:

### Courses API Examples (`data/courses_examples/`)

- `example_1_course_categories.json` - Course categories (Area of Training, etc.)
- `example_2_course_tags.json` - Course tags (PSEA, Workfare, etc.)
- `example_3_search_by_keyword.json` - Keyword search results
- `example_4_search_by_tagging.json` - Tagging code search results
- `example_5_autocomplete.json` - Autocomplete suggestions

### Skills Framework API Examples (`data/skills_framework_examples/`)

- `example_1_job_roles_search.json` - Job roles search results
- `example_2_job_role_titles.json` - Job title listings
- `example_3_tsc_technical_skills.json` - Technical skills (TSC)
- `example_4_ccs_generic_skills.json` - Generic skills (CCS)
- `example_5_tsc_details.json` - Detailed TSC information
- `example_6_ccs_details.json` - Detailed CCS information
- `example_7_ccs_details.json` - Additional CCS details

## 🔍 Courses Tagging Codes Reference

Common tagging codes for filtering courses:

| Code          | Description                                                |
| ------------- | ---------------------------------------------------------- |
| `1`           | SkillsFuture Credit (SFC)                                  |
| `2`           | Post-Employment Training (PET)                             |
| `40`          | SkillsFuture Training Subsidy                              |
| `30011-30013` | SF Series - Data Analytics (Basic, Intermediate, Advanced) |
| `30021-30022` | SF Series - Finance (Basic, Intermediate)                  |
| `30031-30033` | SF Series - Tech Enabled Services                          |
| `30041-30043` | SF Series - Digital Media                                  |
| `30051-30053` | SF Series - Cyber Security                                 |
| `30061-30063` | SF Series - Entrepreneurship                               |
| `30071-30073` | SF Series - Advanced Manufacturing                         |
| `30081-30083` | SF Series - Urban Solutions                                |
| `9001`        | Free Non-SFC Course                                        |
| `9002`        | Chargeable Non-SFC Course                                  |
| `FULL`        | All course tagging codes                                   |

## 📖 Documentation

- **[COURSES_API_SUMMARY.md](COURSES_API_SUMMARY.md)** - Comprehensive Courses API documentation with all parameters, examples, and error codes
- **[SKILLS_FRAMEWORK_API_SUMMARY.md](SKILLS_FRAMEWORK_API_SUMMARY.md)** - Skills Framework API documentation
- **[API_QUICK_REFERENCE.md](API_QUICK_REFERENCE.md)** - Quick reference tables for both APIs

## ⚠️ Important Notes

### Certificate Authentication

- Both APIs require valid certificate files (`cert.pem` and `key.pem`)
- Certificates must be stored securely and never committed to version control
- Certificate authentication only works with `api.ssg-wsg.sg` (not `public-api.ssg-wsg.sg`)

### API Limitations

- **Minimum keyword length:** 3 characters
- **Cannot mix parameters:** Keyword and tagging codes cannot be used together
- **Read-only:** Certificate authentication only supports GET requests (no POST/PUT/DELETE)
- **Pagination:** Use reasonable page sizes (10-50) to avoid timeouts
- **Rate limiting:** Be mindful of API call frequency

### Common Errors

- **403 Forbidden:** Invalid or expired certificates
- **404 Not Found:** Incorrect endpoint path or resource doesn't exist
- **400 Bad Request:** Missing/invalid parameters or keyword < 3 characters

## 🛠️ Troubleshooting

### Certificate Issues

```python
# Verify certificates exist
import os
assert os.path.exists('certificates/cert.pem'), "Certificate not found"
assert os.path.exists('certificates/key.pem'), "Private key not found"
```

### Connection Timeout

```python
# Increase timeout value
response = session.get(url, timeout=60)  # 60 seconds
```

### Invalid Response

```python
# Add error handling
try:
    response = api.get_course_categories(keyword='Training')
except requests.exceptions.RequestException as e:
    print(f"Error: {e}")
    if hasattr(e.response, 'text'):
        print(f"Response: {e.response.text}")
```

## 📞 Support

- **Developer Portal:** https://developer.ssg-wsg.gov.sg/
- **API Status:** https://status.api.ssg-wsg.sg/
- **Help Center:** https://developer.ssg-wsg.gov.sg/webapp/help
- **Community:** https://stackoverflow.com/search?q=%22ssg-wsg%22

## 📝 Version History

| Date     | Version | Changes                                              |
| -------- | ------- | ---------------------------------------------------- |
| Oct 2025 | 1.0     | Initial release with 5 working Courses API endpoints |
| Oct 2025 | 1.1     | Added 6 Skills Framework API endpoints               |

## 📄 License

This project is for educational and integration purposes with the SSG-WSG API.

---

**Note:** Always refer to the official [SSG-WSG Developer Portal](https://developer.ssg-wsg.gov.sg/) for the latest API specifications and updates.
