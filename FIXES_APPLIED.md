# API Examples - Fixes Applied

## Summary of Changes

Based on the official Skills Framework API documentation at:
https://developer.ssg-wsg.gov.sg/webapp/docs/product/6Gl44K5M46EuDgn7LCsAs2/group/5uyNzClV5UJk6Uo0wDg7Mt

The following corrections have been made to `src/api_examples.py`:

## 1. Corrected API Endpoints

### Job Role Titles (Example 2)

- **Old:** `jobRoleTitles`
- **New:** `jobRoles/titles`
- **Endpoint:** `GET /skillsFramework/jobRoles/titles`

### Skills & Competencies - Generic/CCS (Examples 7, 14)

- **Old:** `skills/generic` and `skills/ccs/autocomplete`
- **New:** `codes/skillsAndCompetencies/generic/autocomplete`
- **Endpoint:** `GET /skillsFramework/codes/skillsAndCompetencies/generic/autocomplete`
- **Note:** CCS (Critical Core Skills) is also called GSC (Generic Skills Competency)

### Skills & Competencies - Technical/TSC (Examples 6, 13)

- **Old:** `skills/technical` and `skills/tsc/autocomplete`
- **New:** `codes/skillsAndCompetencies/technical/autocomplete`
- **Endpoint:** `GET /skillsFramework/codes/skillsAndCompetencies/technical/autocomplete`

## 2. Fixed Pagination Parameters

### Job Roles Search (Examples 1, 3, 11, 12)

- **Old Parameters:** `offset`, `limit`
- **New Parameters:** `page`, `pageSize`
- **API Documentation:** Uses `page` (starting from 0) and `pageSize` (default 20)

**Before:**

```python
api.get_job_roles(keyword="data", offset=0, limit=20)
```

**After:**

```python
api.get_job_roles(keyword="data", page=0, page_size=20)
```

## 3. Fixed Response Structure Access

### Job Roles Response

The API returns job roles in a nested structure:

```json
{
  "data": {
    "jobRoles": [{ "id": "...", "title": "..." }]
  }
}
```

**Before:**

```python
job_role_id = search_result['data'][0].get('id')
```

**After:**

```python
job_roles = search_result['data']['jobRoles']
job_role_id = job_roles[0].get('id')
```

### Sectors Response

The API returns sectors as a direct array:

```json
{
  "data": [{ "id": "...", "title": "..." }]
}
```

**Fixed field access:**

- Changed from `sectors['data'][0].get('sectorId')`
- To: `sectors['data'][0].get('id')`

## 4. Clarified Duplicate Endpoints

The following methods use the same API endpoints and are now documented as aliases:

- `get_ccs_generic_skills()` and `get_ccs_autocomplete_details()` → Same endpoint
- `get_tsc_technical_skills()` and `get_tsc_autocomplete_details()` → Same endpoint

## 5. Updated Documentation

### API Parameters

- Clarified that `keyword` parameters require minimum 3 characters
- Updated parameter descriptions for `sector`, `qualification`, `fieldOfStudy` to indicate they accept IDs, not names
- Added note that multiple values can be separated by comma delimiter

### Authentication

- **Open Authentication:** `public-api.ssg-wsg.sg` (no certificate required)
- **Certificate Authentication:** `api.ssg-wsg.sg` (requires cert.pem and key.pem)

The current implementation uses Certificate Authentication.

## 6. Examples Fixed

All 15 examples have been updated:

1. ✅ Search Job Roles by Keyword - Fixed pagination
2. ✅ Job Role Title Autocomplete - Fixed endpoint
3. ✅ Get Job Role Details by ID - Fixed response structure access
4. ✅ Get All Sectors - No changes needed
5. ✅ Get Sector Profile - Fixed field access
6. ✅ Search Technical Skills (TSC) - Fixed endpoint
7. ✅ Search Critical Core Skills (CCS) - Fixed endpoint
8. ✅ Get Field of Studies - No changes needed
9. ✅ Get SSIC List - No changes needed
10. ✅ Get Occupations by Sector - Fixed field access
11. ✅ Get Related Job Roles - Fixed response structure access
12. ✅ Advanced Job Role Search - Fixed pagination
13. ✅ TSC Autocomplete Details - Fixed endpoint
14. ✅ CCS Autocomplete Details - Fixed endpoint
15. ✅ Get Subsectors - Fixed field access

## Testing Recommendations

1. Run Example 2 first to test the corrected job role titles endpoint
2. Run Example 6 to verify TSC autocomplete endpoint
3. Run Example 7 to verify CCS/GSC autocomplete endpoint
4. Run Example 1 to verify pagination parameters
5. Run Example 3 to verify response structure parsing

## API Version

All endpoints use API version **v1** or **v1.1** (default) as specified in the `x-api-version` header.

## Common Response Format

Most endpoints return data in this format:

```json
{
  "data": { ... },
  "status": "200",
  "meta": { ... }
}
```

Some endpoints (like sectors) return data as an array:

```json
{
  "data": [ ... ],
  "status": "200"
}
```

## Next Steps

1. Test all examples with your certificates
2. Verify the response structures match the updated code
3. Check if any additional endpoints need to be added based on your requirements
4. Consider adding error handling for specific HTTP status codes

## References

- Official API Documentation: https://developer.ssg-wsg.gov.sg/webapp/docs/product/6Gl44K5M46EuDgn7LCsAs2/group/5uyNzClV5UJk6Uo0wDg7Mt
- Sample Code Repository: https://github.com/ssg-wsg/Sample-Codes/tree/master/API%20Basic%20Access/Certificate%20Authentication/Python
