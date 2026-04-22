# CI/CD Status Badges

Once you push your code to GitHub/GitLab and the pipelines run, you can add live status badges to your README.

## GitHub Actions

### Test Status Badge

Replace `YOUR_USERNAME` and `YOUR_REPO_NAME` with your actual values:

```markdown
[![Test Automation](https://github.com/YOUR_USERNAME/YOUR_REPO_NAME/actions/workflows/test.yml/badge.svg)](https://github.com/YOUR_USERNAME/YOUR_REPO_NAME/actions/workflows/test.yml)
```

### Example for Different Branches

**Main branch:**
```markdown
[![Tests - Main](https://github.com/YOUR_USERNAME/YOUR_REPO_NAME/actions/workflows/test.yml/badge.svg?branch=main)](https://github.com/YOUR_USERNAME/YOUR_REPO_NAME/actions/workflows/test.yml)
```

**Develop branch:**
```markdown
[![Tests - Develop](https://github.com/YOUR_USERNAME/YOUR_REPO_NAME/actions/workflows/test.yml/badge.svg?branch=develop)](https://github.com/YOUR_USERNAME/YOUR_REPO_NAME/actions/workflows/test.yml)
```

---

## GitLab CI

### Pipeline Status Badge

Go to: **Settings → CI/CD → General pipelines → Pipeline status**

Copy the badge markdown and add to README:

```markdown
[![Pipeline Status](https://gitlab.com/YOUR_USERNAME/YOUR_PROJECT/badges/main/pipeline.svg)](https://gitlab.com/YOUR_USERNAME/YOUR_PROJECT/-/commits/main)
```

### Coverage Badge (if configured)

```markdown
[![Coverage](https://gitlab.com/YOUR_USERNAME/YOUR_PROJECT/badges/main/coverage.svg)](https://gitlab.com/YOUR_USERNAME/YOUR_PROJECT/-/commits/main)
```

---

## Custom Badges (shields.io)

### Tests Badge
```markdown
![Tests](https://img.shields.io/badge/tests-16%20passed-brightgreen)
```

### Coverage Badge
```markdown
![Coverage](https://img.shields.io/badge/coverage-100%25-brightgreen)
```

### CI/CD Badge
```markdown
![CI/CD](https://img.shields.io/badge/CI%2FCD-ready-blue)
```

### Framework Badge
```markdown
![Framework](https://img.shields.io/badge/framework-Playwright%20%2B%20Pytest-orange)
```

---

## Adding to README

Add these badges at the top of your README.md:

```markdown
# NZ Address Checker - Test Automation

[![Test Automation](https://github.com/YOUR_USERNAME/YOUR_REPO_NAME/actions/workflows/test.yml/badge.svg)](https://github.com/YOUR_USERNAME/YOUR_REPO_NAME/actions/workflows/test.yml)
[![Coverage](https://img.shields.io/badge/coverage-100%25-brightgreen)](Documents/TEST_STRATEGY.md)
[![Tests](https://img.shields.io/badge/tests-16%20passed-brightgreen)](Documents/TEST_CASES.md)

Professional test automation framework...
```

---

## Dynamic Badges

### Test Count from pytest
Use GitHub Actions to update badge dynamically:

```yaml
- name: Extract test count
  run: |
    PASSED=$(grep -oP '\d+(?= passed)' pytest-output.txt)
    echo "PASSED_TESTS=$PASSED" >> $GITHUB_ENV

- name: Create badge
  uses: schneegans/dynamic-badges-action@v1.6.0
  with:
    auth: ${{ secrets.GIST_SECRET }}
    gistID: your-gist-id
    filename: tests.json
    label: Tests
    message: ${{ env.PASSED_TESTS }} passed
    color: brightgreen
```

---

## Status Check Requirements

### GitHub Branch Protection

Enable in **Settings → Branches → Add rule:**

Required status checks before merging:
- ✅ Code Quality Checks
- ✅ Security Scan
- ✅ Functional Tests
- ✅ Security Tests
- ✅ Full Regression Suite

---

**For more information, see [CI/CD Integration Guide](CICD_GUIDE.md)**
