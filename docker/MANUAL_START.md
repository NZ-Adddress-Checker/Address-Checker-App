# How to Start the App - Manual Steps

The automated startup is timing out. Let me give you manual steps to start the app.

## Quick Start (Copy & Paste These Commands)

### Step 1: Open Terminal or Command Prompt

Press: `Win + R`, type `cmd`, press Enter

Or use PowerShell:
Press: `Win + X`, then select "Windows PowerShell" or "Terminal"

### Step 2: Navigate to Docker Directory

```bash
cd C:\Users\jeffr\OneDrive\Desktop\Jeff\Python\Python Projects\Address-Checker-App\docker
```

### Step 3: Start Services

```bash
docker-compose up -d
```

This starts the containers in background mode.

### Step 4: Wait 30-45 Seconds

Services need time to start and initialize.

### Step 5: Check Status

```bash
docker-compose ps
```

You should see 2-3 containers running:
- address-checker-api (backend)
- address-checker-frontend (frontend)
- (optionally: address-checker-automation for tests)

### Step 6: Open Browser

Go to: **http://localhost:8080**

## If It Still Doesn't Work

### Check logs in real-time:

```bash
docker-compose logs -f
```

Press `Ctrl + C` to stop viewing logs.

### Check specific service logs:

```bash
docker-compose logs frontend
docker-compose logs backend
docker-compose logs automation
```

### Troubleshooting Commands

```bash
# See all containers (running and stopped)
docker-compose ps -a

# Stop all containers
docker-compose down

# Remove stopped containers
docker-compose down -v

# Rebuild without cache (if you changed docker/.env)
docker-compose build --no-cache

# Start fresh
docker-compose down
docker-compose build --no-cache
docker-compose up -d

# Check if ports are in use
netstat -ano | findstr 8080
netstat -ano | findstr 8000

# Kill process using port 8080 (if needed)
taskkill /PID <PID> /F
```

## Expected Success

After running `docker-compose up -d` and waiting 30-45 seconds:

1. **http://localhost:8080** shows:
   - "NZ Address Checker" title
   - Enabled blue "Login" button
   - No error messages

2. **http://localhost:8000/health** returns:
   ```json
   {"status": "healthy"}
   ```

## If Port 8080 Shows "Refused Connection"

The container might not be responding yet. Try:

```bash
# View container status
docker-compose ps

# View logs
docker-compose logs frontend

# If status shows "Exit" or "Exited", containers crashed
# Check backend logs:
docker-compose logs backend
```

## Common Issues

### Issue 1: "ERROR: docker-compose command not found"
**Solution**: Update Docker Desktop to latest version, or use `docker compose` (without hyphen) instead.

### Issue 2: Containers starting but can't access app
**Solution**: Wait longer (60 seconds), or check logs for errors.

### Issue 3: Port 8080 already in use
**Solution**:
```bash
# Find what's using port 8080
netstat -ano | findstr 8080

# Kill that process (replace PID with actual PID)
taskkill /PID [PID] /F

# Then start docker-compose again
```

### Issue 4: Backend won't start
**Solution**:
```bash
# Check if port 8000 is in use
netstat -ano | findstr 8000

# Free port if needed
taskkill /PID [PID] /F

# Restart services
docker-compose down
docker-compose up -d
```

## Next Steps After App Starts

1. **Test login**: Click the "Login" button on the app
2. **Run tests**: `docker-compose run --rm automation`
3. **Check results**: See `test-results/report.html`

## Commands Summary

```bash
# Start services
docker-compose up -d

# View status
docker-compose ps

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Rebuild
docker-compose build --no-cache

# Run tests
docker-compose run --rm automation

# Clean everything
docker-compose down -v
docker system prune -a
```

## Still Having Issues?

1. Check that Docker Desktop is running (look for Docker icon in system tray)
2. Ensure ports 8000 and 8080 are not blocked by firewall
3. Try: `docker-compose restart` to restart existing containers
4. If all else fails: `docker-compose down -v` then `docker-compose up -d` from scratch
