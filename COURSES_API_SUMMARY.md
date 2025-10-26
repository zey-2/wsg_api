# Courses API - Certificate Authentication Summary

## Overview

This document provides a comprehensive summary of the **SSG-WSG Courses API** endpoints that work with **Certificate Authentication** (mTLS).

**Base URL:** `https://api.ssg-wsg.sg`  
**Authentication Type:** Certificate-based (mutual TLS)  
**Certificate Files:** `cert.pem` and `key.pem`

---

## Working Endpoints Summary

| #   | Endpoint                          | Method | Description                         | Version |
| --- | --------------------------------- | ------ | ----------------------------------- | ------- |
| 1   | `/courses/categories`             | GET    | Retrieve course browse categories   | v1      |
| 2   | `/courses/tags`                   | GET    | Retrieve course tags                | v1      |
| 3   | `/courses/directory`              | GET    | Search courses by keyword           | v2.1    |
| 4   | `/courses/directory`              | GET    | Search courses by tagging code      | v2.1    |
| 5   | `/courses/directory/autocomplete` | GET    | Get course autocomplete suggestions | v1.2    |

**Total Working Endpoints:** 5  
**Success Rate:** 100% for GET (read) operations

---

## Detailed Endpoint Documentation

### 1. Course Categories

**Endpoint:** `GET /courses/categories`  
**API Version:** v1 (default)  
**Description:** Retrieve a list of course categories (e.g., Area of Training, Training Providers) by keyword

**Parameters:**
| Parameter | Type | Required | Location | Description |
|-----------|------|----------|----------|-------------|
| keyword | string | Yes | query | Keyword to search for (minimum 3 characters) |
| x-api-version | string | No | header | API version (default: v1) |

**Example Request:**

```python
api.get_course_categories(keyword='Training')
```

**Example Response:**

```json
{
  "data": {
    "categories": [
      {
        "id": 1,
        "name": "Area of Training",
        "display": true,
        "rolodex": {
          "display": false,
          "numberOfLetters": 1
        }
      },
      {
        "id": 4,
        "name": "Training Partners",
        "display": true,
        "rolodex": {
          "display": true,
          "numberOfLetters": 3
        }
      }
    ]
  },
  "meta": {
    "total": 2
  },
  "status": 200
}
```

**Notes:**

- Minimum 3 characters required for keyword search
- Returns category IDs that can be used in other API calls
- Case-insensitive search

---

### 2. Course Tags

**Endpoint:** `GET /courses/tags`  
**API Version:** v1 (default)  
**Description:** Retrieve a list of course tags with options to sort by text or count

**Parameters:**
| Parameter | Type | Required | Location | Description |
|-----------|------|----------|----------|-------------|
| sortBy | string | Yes | query | Sort order: '0' for text (default), '1' for count |
| x-api-version | string | No | header | API version (default: v1) |

**Example Request:**

```python
api.get_course_tags(sort_by='0')  # Sort by text
```

**Example Response:**

```json
{
  "data": {
    "tags": [
      {
        "text": "PSEA",
        "count": 20874
      },
      {
        "text": "Workfare_Absentee Payroll",
        "count": 20525
      }
    ]
  },
  "meta": {
    "total": 13
  },
  "status": 200
}
```

**Common Tags:**

- PSEA - Post-Secondary Education Account
- SF_Series_2023 - SkillsFuture Series 2023
- Workfare\_\* - Various Workfare schemes

**Notes:**

- sortBy '0' returns tags sorted alphabetically by text
- sortBy '1' returns tags sorted by course count (descending)
- Useful for building tag-based filtering interfaces

---

### 3. Search Courses by Keyword

**Endpoint:** `GET /courses/directory`  
**API Version:** v2.1  
**Description:** Retrieve course details using a keyword search (minimum 3 characters)

**Parameters:**
| Parameter | Type | Required | Location | Description |
|-----------|------|----------|----------|-------------|
| keyword | string | Yes | query | Search keyword (minimum 3 characters) |
| pageSize | integer | Yes | query | Number of items per page |
| page | integer | Yes | query | Page number (starting from 0) |
| x-api-version | string | No | header | API version (default: v2.1) |

**Example Request:**

```python
api.search_courses_by_keyword(
    keyword='python',
    page_size=10,
    page=0
)
```

**Example Response:**

```json
{
  "data": {
    "courses": [
      {
        "title": "Fundamentals of Python Programming (SF)",
        "referenceNumber": "TGS-2023019590",
        "areaOfTrainings": [
          {
            "code": "025",
            "description": "Information and Communications"
          }
        ],
        "url": "https://...",
        "content": "Course description...",
        "fees": [...],
        "runs": [...],
        "tags": [...],
        "trainingProvider": {...}
      }
    ],
    "meta": {
      "total": 150
    }
  },
  "status": 200
}
```

**Notes:**

- **Cannot be used together with tagging codes** in the same query
- Returns basic course information
- Supports pagination for large result sets
- Minimum 3 characters required for keyword

---

### 4. Search Courses by Tagging Code

**Endpoint:** `GET /courses/directory`  
**API Version:** v2.1  
**Description:** Retrieve detailed course information using course tagging codes and support end date

**Parameters:**
| Parameter | Type | Required | Location | Description |
|-----------|------|----------|----------|-------------|
| taggingCodes | string | Yes | query | Comma-separated tagging codes or 'FULL' |
| courseSupportEndDate | string (YYYYMMDD) | Yes | query | Support end date filter |
| retrieveType | string | Yes | query | 'FULL' or 'DELTA' |
| pageSize | integer | Yes | query | Number of items per page |
| page | integer | Yes | query | Page number (starting from 0) |
| lastUpdateDate | string (YYYYMMDD) | Conditional | query | Required if retrieveType='DELTA' |
| x-api-version | string | No | header | API version (default: v2.1) |

**Tagging Codes:**
| Code | Description |
|------|-------------|
| 1 | SFC (SkillsFuture Credit) |
| 2 | PET (Post-Employment Training) |
| 40 | SF Training Subsidy |
| 30011 | SF Series_Data Analytics_Basic |
| 30012 | SF Series_Data Analytics_Intermediate |
| 30013 | SF Series_Data Analytics_Advanced |
| 30021 | SF Series_Finance_Basic |
| 30022 | SF Series_Finance_Intermediate |
| 30031 | SF Series_Tech Enabled Services_Basic |
| 30032 | SF Series_Tech Enabled Services_Intermediate |
| 30033 | SF Series_Tech Enabled Services_Advanced |
| 30041 | SF Series_Digital Media_Basic |
| 30042 | SF Series_Digital Media_Intermediate |
| 30043 | SF Series_Digital Media_Advanced |
| 30051 | SF Series_Cyber Security_Basic |
| 30052 | SF Series_Cyber Security_Intermediate |
| 30053 | SF Series_Cyber Security_Advanced |
| 30061 | SF Series_Entrepreneurship_Basic |
| 30062 | SF Series_Entrepreneurship_Intermediate |
| 30063 | SF Series_Entrepreneurship_Advanced |
| 30071 | SF Series_Advanced Manufacturing_Basic |
| 30072 | SF Series_Advanced Manufacturing_Intermediate |
| 30073 | SF Series_Advanced Manufacturing_Advanced |
| 30081 | SF Series_Urban Solutions_Basic |
| 30082 | SF Series_Urban Solutions_Intermediate |
| 30083 | SF Series_Urban Solutions_Advanced |
| 9001 | Free Non-SFC Course |
| 9002 | Chargeable Non-SFC Course |
| FULL | All course tagging codes |

**Example Request:**

```python
api.search_courses_by_tagging(
    tagging_codes=['1'],  # SFC
    support_end_date='20250101',
    retrieve_type='FULL',
    page_size=10,
    page=0
)
```

**Example Response:**

```json
{
  "data": {
    "courses": [
      {
        "title": "Basics of Excel Analytics",
        "referenceNumber": "TGS-2022602278",
        "trainingProvider": {
          "name": "XALTIUS PTE. LTD.",
          "uen": "201725144R"
        },
        "areaOfTrainings": [{
          "code": "999",
          "description": "Others"
        }],
        "brochure": {...},
        "contactPerson": [...],
        "quality": {...},
        "outcome": {...},
        "skillsFrameworks": [...]
      }
    ],
    "meta": {
      "total": 5000
    }
  },
  "status": 200
}
```

**Notes:**

- **Cannot be used together with keyword** in the same query
- Returns comprehensive course details including:
  - Contact person information
  - Training provider details
  - Quality ratings and outcomes
  - Skills frameworks mapping
  - Course runs and schedules
- Multiple tagging codes can be specified (comma-separated)
- retrieveType 'DELTA' requires lastUpdateDate parameter
- courseSupportEndDate filters courses with support end date >= specified date

---

### 5. Course Autocomplete

**Endpoint:** `GET /courses/directory/autocomplete`  
**API Version:** v1.2  
**Description:** Retrieve course titles and search term suggestions matching the keyword

**Parameters:**
| Parameter | Type | Required | Location | Description |
|-----------|------|----------|----------|-------------|
| keyword | string | Yes | query | Search keyword (minimum 3 characters) |
| x-api-version | string | No | header | API version (default: v1.2) |

**Example Request:**

```python
api.get_course_autocomplete(keyword='data')
```

**Example Response:**

```json
{
  "data": {
    "courses": [
      {
        "title": "<b>Data</b> Driven Organisational Development"
      },
      {
        "title": "WSQ <b>Data</b> Visualization Techniques using Power BI"
      }
    ],
    "terms": [
      {
        "value": "data"
      },
      {
        "value": "5423"
      },
      {
        "value": "data analytics"
      },
      {
        "value": "1006"
      }
    ],
    "areaOfTrainings": [],
    "jobRoles": [],
    "trainingProviders": []
  },
  "status": 200
}
```

**Notes:**

- Returns course titles with keyword highlighted in `<b>` tags
- Returns search term suggestions with course counts
- Terms array contains pairs: [term, count, term, count, ...]
- Useful for implementing type-ahead search functionality
- Minimum 3 characters required for keyword

---

## Implementation Examples

### Python Client Class

```python
from typing import Dict, Any, Optional, List
import requests

class CoursesAPI:
    def __init__(self, cert_path: str, key_path: str):
        self.base_url = "https://api.ssg-wsg.sg"
        self.session = requests.Session()
        self.session.cert = (cert_path, key_path)

    def _make_request(self, endpoint: str, params: Optional[Dict] = None,
                     headers: Optional[Dict] = None) -> Dict[str, Any]:
        url = f"{self.base_url}{endpoint}"
        if headers is None:
            headers = {}
        if 'x-api-version' not in headers:
            headers['x-api-version'] = 'v1'

        response = self.session.get(url, params=params, headers=headers, timeout=30)
        response.raise_for_status()
        return response.json()
```

### Basic Usage

```python
# Initialize API client
api = CoursesAPI(cert_path='cert.pem', key_path='key.pem')

# Example 1: Get course categories
categories = api.get_course_categories(keyword='Training')

# Example 2: Get course tags
tags = api.get_course_tags(sort_by='1')  # Sort by count

# Example 3: Search courses by keyword
courses = api.search_courses_by_keyword(
    keyword='python',
    page_size=20,
    page=0
)

# Example 4: Search courses by tagging
sfc_courses = api.search_courses_by_tagging(
    tagging_codes=['1'],  # SkillsFuture Credit
    support_end_date='20250101',
    page_size=50
)

# Example 5: Get autocomplete suggestions
suggestions = api.get_course_autocomplete(keyword='data')
```

---

## Common Error Responses

### 400 Bad Request

```json
{
  "status": 400,
  "data": {},
  "meta": "string",
  "error": {
    "code": 400,
    "message": "Bad Request",
    "details": [],
    "errorId": ""
  }
}
```

**Causes:**

- Missing required parameters
- Invalid parameter values
- Keyword less than 3 characters
- Using keyword and tagging codes together

### 403 Forbidden

```json
{
  "status": 403,
  "message": "Forbidden. Authorization information is missing or invalid."
}
```

**Causes:**

- Invalid or expired certificates
- Certificate not properly configured
- Attempting to access non-certificate endpoints

### 404 Not Found

```json
{
  "status": 404,
  "data": {},
  "error": {
    "code": 404,
    "message": "Not Found",
    "details": [
      {
        "field": "",
        "message": "Course is not found."
      }
    ]
  }
}
```

**Causes:**

- Invalid course reference number
- Endpoint path incorrect
- Resource does not exist

---

## Best Practices

1. **Certificate Management**

   - Store certificates securely
   - Never commit certificates to version control
   - Regularly renew certificates before expiration
   - Use environment variables for certificate paths

2. **Parameter Validation**

   - Always validate keyword length (minimum 3 characters)
   - Check date format (YYYYMMDD) before making requests
   - Validate tagging codes against the supported list
   - Never mix keyword and tagging codes in the same request

3. **Pagination**

   - Use reasonable page sizes (10-50 items)
   - Implement proper pagination handling for large datasets
   - Cache results when appropriate to reduce API calls

4. **Error Handling**

   - Implement retry logic for transient errors
   - Log errors with context for debugging
   - Handle timeout scenarios gracefully
   - Provide user-friendly error messages

5. **Performance**
   - Reuse session objects to maintain connection pooling
   - Implement request rate limiting if making bulk requests
   - Use appropriate timeout values (30 seconds recommended)
   - Cache frequently accessed data (categories, tags)

---

## Version History

| Date     | Version | Changes               |
| -------- | ------- | --------------------- |
| Oct 2025 | v1.0    | Initial documentation |

---

## Related Documentation

- [Skills Framework API Documentation](SKILLS_FRAMEWORK_API_SUMMARY.md)
- [Quick Reference Guide](API_QUICK_REFERENCE.md)
- SSG-WSG Developer Portal: https://developer.ssg-wsg.gov.sg/
- API Status Monitoring: https://status.api.ssg-wsg.sg/

---

## Support

For API access issues or technical support:

- Visit: https://developer.ssg-wsg.gov.sg/webapp/help
- Community Forum: https://stackoverflow.com/search?q=%22ssg-wsg%22
