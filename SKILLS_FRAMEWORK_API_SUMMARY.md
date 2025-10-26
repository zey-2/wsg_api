# Skills Framework API - Certificate Authentication Summary

## Overview

This document summarizes the working endpoints for the Skills Framework API when using certificate authentication.

## Authentication

- **Base URL**: `https://api.ssg-wsg.sg/skillsFramework`
- **Auth Method**: Certificate-based authentication (mTLS)
- **Certificates**:
  - `certificates/cert.pem` (client certificate)
  - `certificates/key.pem` (private key)

## Working Endpoints

### 1. Job Roles Search

**Endpoint**: `/jobRoles`  
**Method**: GET  
**Description**: Search for job roles using keywords and filters

**Parameters**:

- `keyword` (optional): Search term
- `page` (optional): Page number (default: 0)
- `pageSize` (optional): Results per page (default: 10, max: 100)
- `qualification` (optional): Filter by qualification level
- `sectors` (optional): Comma-separated sector IDs

**Example**:

```python
api.get_job_roles(keyword="data", page_size=10, qualification="Degree")
```

### 2. Job Role Titles Autocomplete

**Endpoint**: `/jobRoles/titles`  
**Method**: GET  
**Description**: Get autocomplete suggestions for job role titles

**Parameters**:

- `keyword` (required): Search term for autocomplete

**Example**:

```python
api.get_job_role_titles(keyword="data")
```

### 3. Technical Skills (TSC) Autocomplete

**Endpoint**: `/codes/skillsAndCompetencies/technical/autocomplete`  
**Method**: GET  
**Description**: Search for technical skills and competencies by skill category

**Parameters**:

- `keyword` (required): Search term (minimum 3 characters, use single words)

**Example**:

```python
api.get_tsc_technical_skills(keyword="data")  # Returns "Data Analysis", "Data Management", etc.
api.get_tsc_technical_skills(keyword="prog")  # Returns "Programming and Coding", etc.
```

**Important Notes**:

- TSC codes represent **skill CATEGORIES** (e.g., "Data Analysis", "Programming and Coding", "Software Configuration")
- NOT specific technologies (e.g., "python", "java" will return 404 - no matching TSC codes)
- Keywords with spaces may cause 500 errors. Use single words or hyphens.
- Returns 404 when no matching TSC codes found (this is normal, not an error)

### 4. Critical Core Skills (CCS/GSC) Autocomplete

**Endpoint**: `/codes/skillsAndCompetencies/generic/autocomplete`  
**Method**: GET  
**Description**: Search for critical core/generic skills

**Parameters**:

- `keyword` (required): Search term (use single words, avoid spaces)

**Example**:

```python
api.get_ccs_generic_skills(keyword="communication")
```

**Note**: Keywords with spaces (e.g., "problem solving") may cause 500 errors. Use single words or hyphens.

### 5. TSC Code Autocomplete Details

**Endpoint**: `/codes/skillsAndCompetencies/technical/autocomplete/details`  
**Method**: GET  
**Description**: Get detailed technical skills competency information including titles, categories, and levels

**Parameters**:

- `keyword` (required): Search term (minimum 3 characters, use single words)

**Example**:

```python
api.get_tsc_autocomplete_details(keyword="data")
```

**Returns**: Detailed information in `data.technicalSkillCompetencies` array including:

- code, title, category, level, and more comprehensive skill information

**Note**: Provides more detail than the basic TSC autocomplete endpoint.

### 6. CCS Code Autocomplete Details

**Endpoint**: `/codes/skillsAndCompetencies/generic/autocomplete/details`  
**Method**: GET  
**Description**: Get detailed generic skills competency information including titles, categories, and levels

**Parameters**:

- `keyword` (required): Search term (minimum 3 characters, use single words)

**Example**:

```python
api.get_ccs_autocomplete_details(keyword="comm")
```

**Returns**: Detailed information in `data.genericSkillCompetencies` array including:

- code, title, category, level, and more comprehensive skill information

**Note**: Provides more detail than the basic CCS autocomplete endpoint.

## Non-Working Endpoints (403 Forbidden)

The following endpoints return 403 Forbidden errors with certificate authentication and have been removed:

- `/sectors` - Get all sectors
- `/sectors/{id}` - Get sector profile by ID
- `/sectors/{id}/subsectors` - Get subsectors for a sector
- `/jobRoles/{id}` - Get job role details by ID
- `/jobRoles/{id}/relatedJobRoles` - Get related job roles
- `/occupations` - Get occupations by sector
- `/fieldOfStudies` - Get field of studies classification
- `/ssic` - Get SSIC list

These endpoints likely require different authentication (OAuth2) or additional API permissions.

## Response Structure

All working endpoints return JSON responses with the following general structure:

```json
{
  "data": {
    // Response data varies by endpoint
    "jobRoles": [...],  // For job roles search
    "titles": [...],    // For title autocomplete
    "skills": [...]     // For skills autocomplete
  },
  "metadata": {
    "totalCount": 100,
    "page": 0,
    "pageSize": 10
  }
}
```

## Known Issues

1. **TSC Keywords - Skill Categories Only**: TSC autocomplete searches for skill **categories**, not specific technologies

   - ❌ Bad: `keyword="python"`, `keyword="java"` (will return 404 - no matching categories)
   - ✅ Good: `keyword="data"`, `keyword="prog"`, `keyword="soft"`, `keyword="comm"`
   - Returns: "Data Analysis-2", "Programming and Coding-3", "Software Configuration-3", etc.

2. **Keywords with Spaces**: Keywords containing spaces cause 500 Internal Server Error responses

   - ❌ Bad: `keyword="machine learning"`, `keyword="problem solving"`
   - ✅ Good: `keyword="machine"`, `keyword="learning"`, `keyword="problem"`

3. **Pagination Parameters**: Must use `page`/`pageSize` (not `offset`/`limit`)

4. **Certificate Authentication Limitations**: Many endpoints that work with OAuth2 return 403 with certificate auth

## Usage Examples

See `src/skills_framework_api_examples.py` for complete working examples:

1. **Search Job Roles by Keyword** - Basic search functionality
2. **Job Role Title Autocomplete** - Interactive search suggestions
3. **Search Technical Skills (TSC)** - Find relevant technical competencies
4. **Search Critical Core Skills (CCS)** - Find soft skills and core competencies
5. **Advanced Job Role Search** - Multi-criteria filtering
6. **TSC Autocomplete with Detailed Info** - Get comprehensive technical skill details
7. **CCS Autocomplete with Detailed Info** - Get comprehensive generic skill details

## Files Updated

- ✅ `src/skills_framework_api_examples.py` - Now includes 7 working certificate-auth examples
- ✅ `src/test_api_fixes.py` - Test script for endpoint verification
- ✅ `FIXES_APPLIED.md` - Documentation of changes made
- ✅ `README.md` - Updated with reference source
- ✅ `SKILLS_FRAMEWORK_API_SUMMARY.md` - Comprehensive endpoint documentation

## Testing

Run all examples:

```bash
python src/skills_framework_api_examples.py
```

Then select option `0` to run all examples, or choose individual examples 1-7.

All examples successfully tested and verified working on 2025-10-26.
