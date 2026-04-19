# Enhanced Security Scanning

## Overview
This document describes the enhanced security scanning capabilities added to the CI/CD pipeline.

## 🔒 Security Workflows

### 1. CodeQL Analysis (`codeql.yml`)
**Purpose:** GitHub's advanced code scanning for security vulnerabilities

**Coverage:**
- Python code analysis
- JavaScript code analysis
- Runs on push and scheduled weekly

**Features:**
- Detects security anti-patterns
- Finds code quality issues
- Uploads to GitHub Security tab

**Setup:** No additional setup needed (free for public repos)

---

### 2. Secret Scanning (`secret-scanning.yml`)
**Purpose:** Detect hardcoded secrets, credentials, and API keys

**Tools Used:**
- **TruffleHog** - Scans git history
- **GitGuardian** - Commercial secret detection (optional)
- **detect-secrets** - Python secret patterns
- **Custom Regex** - AWS keys, private keys, database URLs

**Detects:**
- API keys and tokens
- Private keys (RSA, OpenSSH)
- AWS credentials (AKIA patterns)
- Database connection strings with credentials
- Stripe keys, JWT tokens, etc.

**Setup:** 
To enable GitGuardian:
1. Sign up at https://www.gitguardian.com/
2. Add to **Settings → Secrets**: `GITGUARDIAN_API_KEY`

---

### 3. Container Security (`container-security.yml`)
**Purpose:** Scan Docker images and Dockerfiles for vulnerabilities

**Tools:**
- **Hadolint** - Dockerfile linting and best practices
- **Trivy** - Container image vulnerability scanning

**Hadolint Checks:**
- Base image recommendations
- Layer caching best practices
- Security vulnerabilities in Docker config
- Performance optimizations

**Trivy Checks:**
- OS package vulnerabilities
- Application dependency vulnerabilities
- Secrets in images
- Configurable severity levels

**Configuration:** `.hadolintignore`

---

### 4. SBOM Generation (`sbom.yml`)
**Purpose:** Generate Software Bill of Materials (supply chain security)

**Generates:**
- Backend SBOM (CycloneDX format)
- Frontend SBOM (CycloneDX format)
- Dependency audit reports
- npm audit results

**Artifacts Generated:**
- `sbom/backend-sbom.xml` - Python dependencies in CycloneDX format
- `sbom/frontend-sbom.xml` - Node.js dependencies in CycloneDX format
- `sbom/SBOM_REPORT.md` - Detailed report

**Standards:**
- CycloneDX - Open standard for SBOM
- Can be integrated with supply chain tools
- Tracks all dependencies and versions

---

## 📊 Security Summary in CI Pipeline

All security checks are orchestrated in `ci.yml`:

```
CI Pipeline Checks:
├── Backend Lint & Type Check
├── Frontend Lint & Build
├── CodeQL Security Analysis
├── Secret & Credential Scanning
├── Container Security (Hadolint + Trivy)
├── SBOM & Dependency Report
└── Integration Tests
```

---

## 🔑 Required Secrets (Optional)

### GitGuardian (Optional)
- **Secret Name:** `GITGUARDIAN_API_KEY`
- **Get from:** https://dashboard.gitguardian.com/api/
- **Adds:** Commercial-grade secret detection

### Future Additions
- SonarCloud: `SONAR_TOKEN`
- Snyk: `SNYK_TOKEN`

---

## 📈 Viewing Results

### CodeQL Results
1. Go to **Security** tab → **Code scanning**
2. View alerts by severity
3. Review recommended fixes

### Trivy Results
1. Go to **Actions** → Run name
2. Click **Container Security Scanning** job
3. View SARIF uploads in Security tab

### SBOM Artifacts
1. Go to **Actions** → Run name
2. Download **sbom-artifacts**
3. View CycloneDX XMLs and reports

### Secret Scanning
1. Go to **Actions** → **Secret Scanning** run
2. Check logs for TruffleHog and detect-secrets output

---

## 🎯 Best Practices

### 1. Secret Prevention
- Never commit credentials to git
- Use environment variables
- Rotate compromised secrets immediately
- Use GitHub Secrets for sensitive data

### 2. Container Security
- Update base images regularly
- Use minimal base images
- Scan images before deployment
- Follow Hadolint recommendations

### 3. Dependency Management
- Review SBOM regularly
- Keep dependencies updated
- Monitor security advisories
- Use lock files (package-lock.json)

### 4. Code Quality
- Fix high/critical CodeQL alerts
- Review secret scanning logs
- Keep Dockerfile optimized
- Regular dependency audits

---

## 🚀 Customization

### Adjust Trivy Severity
Edit `container-security.yml`:
```yaml
severity: 'CRITICAL,HIGH,MEDIUM'  # Include medium severity
```

### Skip Specific Hadolint Rules
Edit `.hadolintignore`:
```
ignored:
  - DL3008
  - DL3013
  - DL3009
```

### Schedule Frequency
Edit any workflow's `schedule`:
```yaml
schedule:
  - cron: '0 0 * * 0'  # Weekly Sunday
  - cron: '0 2 * * *'  # Daily at 2 AM
```

---

## 📚 Resources

- **CodeQL**: https://codeql.github.com/
- **GitGuardian**: https://www.gitguardian.com/
- **Hadolint**: https://github.com/hadolint/hadolint
- **Trivy**: https://github.com/aquasecurity/trivy
- **CycloneDX**: https://cyclonedx.org/
- **SBOM**: https://www.cisa.gov/sbom

---

## 🆘 Troubleshooting

### GitGuardian API Key Not Working
- Verify key in **Settings → Secrets**
- Check GitGuardian dashboard for key validity
- Regenerate key if needed

### Trivy Scan Failing
- Check Docker daemon is running
- Verify image builds successfully
- Review Trivy documentation for your OS

### CodeQL Timeouts
- Reduce language matrix (analyze one language at a time)
- Check GitHub Actions quota
- Request Actions increase if needed

---

## Next Steps

1. ✅ Workflows created and running
2. Review first scan results
3. Address critical findings
4. Set up branch protection rules
5. Monitor security dashboard weekly
