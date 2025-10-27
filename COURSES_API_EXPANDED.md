# SSG-WSG Courses API - Expanded Implementation

## Overview

This document describes the expanded implementation of the SSG-WSG Courses API with **10 working endpoints** using certificate authentication (mTLS).

**Base URL:** `https://api.ssg-wsg.sg`  
**Authentication:** Certificate-based (mutual TLS)  
**Date:** October 2025

## New Endpoints Added (v1.2)

This expansion adds **5 new endpoints** to the existing implementation:

### 1. Course SubCategories

**Endpoint:** `GET /courses/categories/{browseCategoryID}/subCategories`  
**Version:** v1 (default)

Retrieve a list of course sub-categories within a main category by its ID.

**Parameters:**

- `browseCategoryID` (path, required): The category ID to retrieve sub-categories for

**Example:**

```python
api.get_course_subcategories(browse_category_id=34)
```

**Use Case:** Get detailed training areas within a specific category like "Area of Training" (ID: 34)

---

### 2. Course Details

**Endpoint:** `GET /courses/directory/{course reference number}`  
**Version:** v1.2 (default)

Retrieve comprehensive details of a course based on the course reference number.

**Parameters:**

- `course reference number` (path, required): Course reference number (e.g., 'SCN-198202248E-01-CRS-N-0027685')
- `includeExpiredCourses` (query, optional): Boolean to include expired courses (default: true)

**Response Includes:**

- Course information (title, objectives, content, URL)
- Training provider details (name, UEN, address, contact)
- Course runs (schedule, dates, venue, vacancy)
- Fees and subsidies
- Contact person details
- Course bundles and modules
- Job roles and sectors
- Quality indicators and statistics

**Example:**

```python
api.get_course_details(
    course_reference_number='SCN-198202248E-01-CRS-N-0027685',
    include_expired=True
)
```

**Use Case:** Get complete information about a specific course before registration

---

### 3. Related Courses

**Endpoint:** `GET /courses/directory/{course reference number}/related`  
**Version:** v1 (default)

Retrieve up to 10 courses related to a specified course based on its course reference number.

**Parameters:**

- `course reference number` (path, required): Course reference number

**Example:**

```python
api.get_related_courses(
    course_reference_number='SCN-198202248E-01-CRS-N-0027685'
)
```

**Use Case:** Help users discover similar courses or alternative options

---

### 4. Popular Courses

**Endpoint:** `GET /courses/directory/popular`  
**Version:** v1 (default)

Retrieve a list of popular/trending courses along with course provider information.

**Parameters:**

- `taggingCode` (query, optional): Course tagging code ('WSQ', 'CET', 'PET', 'SFC', 'PA')
- `pageSize` (query, optional): Number of items per page (default: 10)
- `page` (query, optional): Page number, starting from 0 (default: 0)

**Example:**

```python
# Get all popular courses
api.get_popular_courses(page_size=10)

# Get popular SkillsFuture Credit courses only
api.get_popular_courses(tagging_code='SFC', page_size=20)
```

**Use Case:** Discover trending courses and what others are taking

---

### 5. Featured Courses

**Endpoint:** `GET /courses/directory/featured`  
**Version:** v1 (default)

Retrieve a list of featured courses from the MySkillsFuture course directory.

**Parameters:**

- `taggingCode` (query, optional): Course tagging code ('WSQ', 'CET', 'PET', 'SFC', 'PA')
- `pageSize` (query, optional): Number of items per page (default: 10)
- `page` (query, optional): Page number, starting from 0 (default: 0)

**Example:**

```python
# Get all featured courses
api.get_featured_courses(page_size=10)

# Get featured WSQ courses only
api.get_featured_courses(tagging_code='WSQ', page_size=20)
```

**Use Case:** Browse curated/highlighted courses from MySkillsFuture

---

## Complete Endpoint List

### All 10 Courses API Endpoints

| #   | Endpoint                                               | Method | Version | Description                              |
| --- | ------------------------------------------------------ | ------ | ------- | ---------------------------------------- |
| 1   | `/courses/categories`                                  | GET    | v1      | Retrieve course categories by keyword    |
| 2   | `/courses/tags`                                        | GET    | v1      | Retrieve course tags with sort options   |
| 3   | `/courses/directory`                                   | GET    | v2.1    | Search courses by keyword                |
| 4   | `/courses/directory`                                   | GET    | v2.1    | Search courses by tagging codes          |
| 5   | `/courses/directory/autocomplete`                      | GET    | v1.2    | Autocomplete course titles               |
| 6   | `/courses/categories/{browseCategoryID}/subCategories` | GET    | v1      | **NEW:** Retrieve course subcategories   |
| 7   | `/courses/directory/{course reference number}`         | GET    | v1.2    | **NEW:** Get detailed course information |
| 8   | `/courses/directory/{course reference number}/related` | GET    | v1      | **NEW:** Get related courses             |
| 9   | `/courses/directory/popular`                           | GET    | v1      | **NEW:** Get popular/trending courses    |
| 10  | `/courses/directory/featured`                          | GET    | v1      | **NEW:** Get featured courses            |

---

## Usage Examples

### Complete Workflow Example

```python
from courses_api_examples import CoursesAPI

# Initialize client
api = CoursesAPI(
    cert_path='certificates/cert.pem',
    key_path='certificates/key.pem'
)

# 1. Browse course categories
categories = api.get_course_categories(keyword='Training')
print(f"Found {len(categories['data']['categories'])} categories")

# 2. Get subcategories for "Area of Training" (ID: 34)
subcategories = api.get_course_subcategories(browse_category_id=34)
for subcat in subcategories['data']['subCategories']:
    print(f"- {subcat['description']}")

# 3. Search for Python courses
courses = api.search_courses_by_keyword(keyword='python', page_size=5)
course_ref = courses['data']['courses'][0]['referenceNumber']
print(f"First course: {course_ref}")

# 4. Get detailed course information
details = api.get_course_details(course_reference_number=course_ref)
course = details['data']['courses'][0]
print(f"Title: {course['title']}")
print(f"Duration: {course['totalTrainingDurationHour']} hours")
print(f"Cost: ${course['totalCostOfTrainingPerTrainee']}")

# 5. Find related courses
related = api.get_related_courses(course_reference_number=course_ref)
print(f"Found {len(related['data']['courses'])} related courses")

# 6. Browse popular courses
popular = api.get_popular_courses(page_size=5)
print("Popular courses:")
for course in popular['data']['courses']:
    print(f"- {course['title']}")

# 7. Check featured courses
featured = api.get_featured_courses(tagging_code='SFC', page_size=5)
print("Featured SkillsFuture Credit courses:")
for course in featured['data']['courses']:
    print(f"- {course['title']}")
```

---

## Interactive Menu

Run the script to access an interactive menu:

```bash
python src/courses_api_examples.py
```

Menu options:

```
1.  Course Categories         - Browse course category types
2.  Course Tags               - List available course tags
3.  Search by Keyword         - Search courses by keyword
4.  Search by Tagging         - Filter by tagging codes (SFC, WSQ, etc.)
5.  Autocomplete              - Course title suggestions
6.  Course SubCategories      - List subcategories within a category
7.  Course Details            - Complete information about a course
8.  Related Courses           - Find similar courses
9.  Popular Courses           - Trending/most viewed courses
10. Featured Courses          - Curated courses from MySkillsFuture
0.  Run all examples
q.  Quit
```

---

## Common Use Cases

### 1. Course Discovery Flow

```python
# Browse categories → subcategories → search → details
categories = api.get_course_categories(keyword='Tech')
subcats = api.get_course_subcategories(browse_category_id=34)
courses = api.search_courses_by_keyword(keyword='data analytics')
details = api.get_course_details(course_ref)
```

### 2. Course Comparison

```python
# Get course details and compare with related courses
course1 = api.get_course_details(course_ref_1)
related = api.get_related_courses(course_ref_1)
course2 = api.get_course_details(related['data']['courses'][0]['referenceNumber'])
```

### 3. Trending Analysis

```python
# Analyze popular vs featured courses
popular = api.get_popular_courses(page_size=20)
featured = api.get_featured_courses(page_size=20)
# Compare course types, providers, areas of training
```

### 4. SkillsFuture Credit Shopping

```python
# Find SFC-eligible courses
sfc_popular = api.get_popular_courses(tagging_code='SFC', page_size=50)
sfc_featured = api.get_featured_courses(tagging_code='SFC', page_size=50)
# Filter by area of interest, cost, duration
```

---

## Response Examples

### Course Details Response Structure

```json
{
  "status": "200",
  "data": {
    "courses": [{
      "referenceNumber": "SCN-198202248E-01-CRS-N-0027685",
      "title": "Certificate of Competency in Earth Control Measures",
      "objective": "Upon completion...",
      "totalTrainingDurationHour": 16,
      "totalCostOfTrainingPerTrainee": 643.21,
      "trainingProvider": {
        "uen": "10000000K",
        "name": "SINGAPORE ABC PTE. LTD.",
        "address": [...]
      },
      "runs": [{
        "courseStartDate": 20191101,
        "courseEndDate": 20191105,
        "intakeSize": 70
      }],
      "support": [{
        "period": {
          "from": 20190529,
          "to": 20190530,
          "taggingCode": "1",
          "taggingDescription": "SFC"
        }
      }],
      "bundles": [...],
      "modules": [...]
    }]
  }
}
```

### Related Courses Response

```json
{
  "status": "200",
  "data": {
    "courses": [
      {
        "referenceNumber": "...",
        "title": "Similar Course Title",
        "trainingProvider": {...}
      }
    ]
  }
}
```

---

## Key Features

### Certificate Authentication

- Uses mTLS (mutual TLS) for secure API access
- Requires valid `cert.pem` and `key.pem` files
- Works with `api.ssg-wsg.sg` endpoint

### Comprehensive Coverage

- 10 endpoints covering search, browse, and discovery
- Supports keyword search, filtering, and autocomplete
- Provides detailed course information and relationships

### Production Ready

- Error handling for common scenarios
- Response validation and parsing
- JSON output files for all examples
- Interactive menu for testing

### Well Documented

- Inline code documentation
- Example usage for each endpoint
- Response structure examples
- Common use case patterns

---

## API Versions Summary

| Endpoint          | API Version | Notes                            |
| ----------------- | ----------- | -------------------------------- |
| Course Categories | v1          | Default, stable                  |
| Course Tags       | v1          | Default, stable                  |
| Search by Keyword | v2.1        | Enhanced search                  |
| Search by Tagging | v2.1        | Enhanced search                  |
| Autocomplete      | v1.2        | Latest version                   |
| SubCategories     | v1          | Default, stable                  |
| Course Details    | v1.2        | Latest, includes bundles/modules |
| Related Courses   | v1          | Default, stable                  |
| Popular Courses   | v1          | Default, stable                  |
| Featured Courses  | v1          | Default, stable                  |

---

## Testing

All endpoints have been verified with the production API:

```bash
# Test individual endpoint
python -c "from src.courses_api_examples import CoursesAPI; \
api = CoursesAPI('certificates/cert.pem', 'certificates/key.pem'); \
print(api.get_popular_courses())"

# Run all examples
python src/courses_api_examples.py
# Select option 0 (Run all examples)
```

---

## File Structure

```
wsg_api/
├── src/
│   └── courses_api_examples.py       # Main implementation (10 endpoints)
├── data/
│   └── courses_examples/
│       ├── example_1_course_categories.json
│       ├── example_2_course_tags.json
│       ├── example_3_search_by_keyword.json
│       ├── example_4_search_by_tagging.json
│       ├── example_5_autocomplete.json
│       ├── example_6_subcategories.json       # NEW
│       ├── example_7_course_details.json      # NEW
│       ├── example_8_related_courses.json     # NEW
│       ├── example_9_popular_courses.json     # NEW
│       └── example_10_featured_courses.json   # NEW
├── certificates/
│   ├── cert.pem
│   └── key.pem
├── COURSES_README.md                  # Updated documentation
├── COURSES_API_EXPANDED.md            # This file
└── API_QUICK_REFERENCE.md
```

---

## Benefits of Expansion

### For Developers

- **Complete API coverage** for course discovery and information
- **Relationship mapping** between courses (related courses)
- **Trend analysis** capabilities (popular/featured courses)
- **Hierarchical navigation** (categories → subcategories → courses)

### For End Users

- **Better course discovery** through multiple entry points
- **Informed decisions** with comprehensive course details
- **Course comparison** using related courses feature
- **Trust signals** from popular and featured listings

### For Training Providers

- **Market insights** from popular courses data
- **Competitive analysis** using related courses
- **Visibility** through featured courses
- **Detailed analytics** from comprehensive course data

---

## Next Steps

### Potential Enhancements

1. Add course quality and outcome endpoints
2. Implement course feedback/reviews endpoints
3. Add course brochure management
4. Include course enquiry functionality
5. Add webhook subscriptions for course updates

### Integration Opportunities

- Build recommendation engines using related courses
- Create comparison tools using course details
- Develop trend analysis dashboards with popular courses
- Implement intelligent search with autocomplete + details

---

## Support & References

- **Developer Portal:** https://developer.ssg-wsg.gov.sg/
- **API Documentation:** https://developer.ssg-wsg.gov.sg/webapp/docs/product/6kYpfJEWVb7NyYVVHvUmHi
- **Article:** https://developer.ssg-wsg.gov.sg/webapp/articles/eGSGMc97oNlUjSJZTGafV
- **API Status:** https://status.api.ssg-wsg.sg/

---

**Last Updated:** October 27, 2025  
**Version:** 1.2  
**Status:** Production Ready ✓
