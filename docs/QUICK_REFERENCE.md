name: Quick Reference Guide

## GitHub Actions CI/CD Quick Reference

### View Workflow Results

1. **GitHub Web UI**
   - Go to your repository
   - Click "Actions" tab
   - View workflow run history and logs

2. **Using GitHub CLI**
   ```bash
   # List recent workflow runs
   gh run list
   
   # View specific run logs
   gh run view <RUN_ID>
   
   # Watch workflow live
   gh run watch <RUN_ID>
   ```

### Trigger Workflows Manually

From GitHub UI:
- Go to Actions → Select workflow → "Run workflow" button

From CLI:
```bash
gh workflow run deploy.yml -r main
```

### Local Testing with Act

```bash
# Install act
brew install act  # macOS
choco install act-cli  # Windows

# Run specific job
act -j lint-and-test

# Run specific workflow
act -W .github/workflows/backend.yml

# View available jobs
act -l

# Run with specific event
act pull_request
```

### Common Commands

```bash
# Format backend code with Black
black backend/

# Sort imports with isort
isort backend/

# Check with pylint
pylint backend/

# Format frontend code
cd frontend && npx prettier --write .

# Build frontend
cd frontend && npm run build

# Run integration tests locally
cd backend
python -m pytest tests/ -v

# Check docker build locally
docker build -f docker/Dockerfile .
docker build -f docker/frontend.Dockerfile .
```

### Environment Variables

Set these in GitHub Actions Secrets for deployment:
- `DOCKER_USERNAME` - Docker Hub username
- `DOCKER_PASSWORD` - Docker Hub access token

### Branch Protection Rules

Recommended settings for `main` branch:
- ✅ Require status checks to pass before merging
- ✅ Require branches to be up to date before merging
- ✅ Require reviews before merging (optional)
- ✅ Dismiss stale pull request approvals

### Troubleshooting Workflows

**Workflow not running:**
- Verify path matches in `on.push.paths`
- Check branch name (case-sensitive)
- Ensure `.github/workflows/` directory exists
- Enable Actions in repository settings

**Jobs not running in parallel:**
- Add `concurrency` section to prevent cancellation
- Ensure no `needs:` dependencies unless required

**Slow builds:**
- Check cache hit/miss in logs
- Consider splitting into smaller jobs
- Use workflow concurrency to cancel old runs

**Secret not available:**
- Verify secret added in Settings → Secrets
- Check secret name is correct (case-sensitive)
- Use `if: secrets.DOCKER_USERNAME != ''` to make optional

### Monitoring and Alerts

1. **GitHub Notifications** - Get email alerts on failures
2. **Status Badge** - Add to README.md
3. **Slack Integration** - Optional via GitHub App
4. **Email Digest** - Configure in settings

### Performance Optimization

- Cache dependencies (automatically done)
- Use `matrix` strategy for parallel testing
- Skip workflows for documentation-only changes
- Use `concurrency` to cancel old runs

### Debugging Workflow Issues

1. **View raw logs** - Click job name in workflow run
2. **Add debug logging** - Use `run: echo "::debug::message"`
3. **Re-run failed jobs** - "Re-run" button in workflow
4. **SSH into runner** - GitHub supports debugging via SSH

### Cost Optimization

- Use `paths` to skip unnecessary workflow runs
- Set `concurrency` to cancel redundant runs
- Use Ubuntu runners (included in free tier)
- Consider timeouts to prevent stuck jobs

### Next Steps

1. Customize workflows for your needs
2. Set up branch protection rules
3. Configure deployment secrets
4. Monitor first few runs
5. Adjust thresholds and timeouts as needed

---
For detailed documentation, see [CI/CD Guide](CI_CD_GUIDE.md)
