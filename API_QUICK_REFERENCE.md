# Skills Framework API - Certificate Authentication Quick Reference

## Working Endpoints Summary

| #   | Endpoint                                                      | Description             | Example Keyword  | Returns                                                   |
| --- | ------------------------------------------------------------- | ----------------------- | ---------------- | --------------------------------------------------------- |
| 1   | `/jobRoles`                                                   | Search job roles        | `keyword="data"` | Job roles with titles, descriptions, sectors              |
| 2   | `/jobRoles/titles`                                            | Autocomplete job titles | `keyword="data"` | Up to 5 matching job role titles                          |
| 3   | `/codes/skillsAndCompetencies/technical/autocomplete`         | TSC skill codes         | `keyword="data"` | TSC codes like "Data Analysis-2" (250 results)            |
| 4   | `/codes/skillsAndCompetencies/generic/autocomplete`           | CCS skill codes         | `keyword="comm"` | CCS codes like "Communication-2"                          |
| 5   | `/codes/skillsAndCompetencies/technical/autocomplete/details` | TSC detailed info       | `keyword="data"` | Detailed TSC with titles, categories, levels (44 results) |
| 6   | `/codes/skillsAndCompetencies/generic/autocomplete/details`   | CCS detailed info       | `keyword="comm"` | Detailed CCS with titles, categories, levels              |

## Python API Methods

```python
from skills_framework_api_examples import SkillsFrameworkAPI

api = SkillsFrameworkAPI()

# 1. Search job roles
api.get_job_roles(keyword="data", page_size=10, qualification="Degree")

# 2. Autocomplete job titles
api.get_job_role_titles(keyword="data")

# 3. TSC technical skills (basic)
api.get_tsc_technical_skills(keyword="data")

# 4. CCS generic skills (basic)
api.get_ccs_generic_skills(keyword="communication")

# 5. TSC technical skills (detailed)
api.get_tsc_autocomplete_details(keyword="data")

# 6. CCS generic skills (detailed)
api.get_ccs_autocomplete_details(keyword="comm")
```

## Key Differences: Basic vs Detailed Autocomplete

### Basic Autocomplete

- **TSC**: Returns simple array of `{code, description}` pairs (e.g., 250 results for "data")
- **CCS**: Returns simple array of `{code, description}` pairs
- **Use case**: Quick lookups, dropdown lists, simple searches

### Detailed Autocomplete

- **TSC**: Returns comprehensive `technicalSkillCompetencies` array with titles, categories, levels (e.g., 44 results for "data")
- **CCS**: Returns comprehensive `genericSkillCompetencies` array with titles, categories, levels
- **Use case**: Detailed information display, skill profiling, competency mapping

## Important Notes

1. **TSC Keywords**: Use skill CATEGORIES ("data", "prog", "soft"), not technologies ("python", "java")
2. **Keyword Length**: Minimum 3 characters
3. **Spaces**: Avoid spaces in keywords (use "problem" not "problem solving")
4. **404 Responses**: Normal when no matching skills found
5. **Pagination**: Use `page`/`pageSize` parameters (not `offset`/`limit`)

## Non-Working Endpoints (403 Forbidden)

These require OAuth2 or additional permissions:

- Sectors, Subsectors, Sector Profiles
- Field of Studies, SSIC List
- Occupations, Job Roles by Occupation
- Job Role Details by ID, Job Role Profile by ID
- Related Job Roles
- Get TSC/CCS Details (require Corppass subscription)

## Testing

```bash
# Run all 7 examples
python src/skills_framework_api_examples.py

# Test individual endpoints
python -c "import sys; sys.path.insert(0, 'src'); from skills_framework_api_examples import example_1_search_job_roles; example_1_search_job_roles()"
```

All endpoints tested and verified: **2025-10-26**
