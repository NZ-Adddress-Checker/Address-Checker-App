# AWS Cognito Setup Guide

This guide explains how to configure AWS Cognito for the NZ Address Checker application.

## Prerequisites

- AWS Account with access to Cognito
- Application deployed or running locally
- Domain for callback URLs (localhost for local development)

## Quick Start

### 1. Create User Pool

1. Go to [AWS Cognito Console](https://console.aws.amazon.com/cognito)
2. Click **Create user pool**
3. Choose **Cognito user pool** (recommended for this app)
4. Configure sign-in:
   - Select **Email** as sign-in method
   - Click **Next**

### 2. Configure Multi-Factor Authentication (MFA)

- Skip or select **No MFA** for development
- For production, select **Optional** and choose authenticator apps
- Click **Next**

### 3. Configure User Attributes

Required attributes:
- ✅ Email (required)
- Optional: Phone number, name

Additional attributes:
- Select **Preferred username** if you want usernames
- Click **Next**

### 4. Set Message Delivery

- Choose **Send email with Cognito** (default)
- Configure sender email if needed
- Click **Next**

### 5. Review and Create

- Review all settings
- Click **Create user pool**
- Note the **User Pool ID** (you'll need this)

## Configure App Client

### 1. Create App Client

1. In your User Pool, go to **App Integration** → **App Clients and analytics**
2. Click **Create app client**
3. Configure:
   - **App client name**: `nz-address-checker-app`
   - **Client type**: **Public client**
   - Click **Create**

### 2. Configure OAuth Settings

1. Go to **App Integration** → **App clients**
2. Click your app client
3. Scroll to **Authentication flows configuration**:
   - ✅ Check **ALLOW_USER_PASSWORD_AUTH**
   - ✅ Check **ALLOW_REFRESH_TOKEN_AUTH**
   - ✅ Check **ALLOW_CUSTOM_AUTH**
   - Click **Save**

### 3. Configure Callback URLs

**Still in the same app client, scroll to "Allowed callback URLs":**

Add both (for local development):
```
http://localhost:5173/callback
http://localhost:8080/callback
```

For production, add your domain:
```
https://yourdomain.com/callback
```

### 4. Configure Sign Out URLs

Add both:
```
http://localhost:5173/
http://localhost:8080/
```

For production:
```
https://yourdomain.com/
```

### 5. Configure Allowed OAuth Scopes

In the **OAuth 2.0 settings** section:
- ✅ Check **openid**
- ✅ Check **email**
- ✅ Check **profile**
- ✅ Check **phone** (optional)
- Click **Save**

## Enable Hosted UI

1. Go to **App Integration** → **Domain name**
2. Create a domain (must be unique globally):
   - Example: `yourdomain-prod` → `https://yourdomain-prod.auth.ap-southeast-2.amazoncognito.com`
3. Click **Create domain**
4. Wait for creation to complete (~1 minute)

## Get Configuration Values

Once setup is complete, collect these values:

1. Go to **App Integration** → **App clients** → Your app
2. Note:
   - **Client ID**: Copy this → `VITE_COGNITO_CLIENT_ID`
   - **Client secret**: (Not needed for public client)

3. Go to **App Integration** → **Domain name**
4. Note the domain → `VITE_COGNITO_DOMAIN`
   - Example: `https://yourdomain-prod.auth.ap-southeast-2.amazoncognito.com`

## Environment Configuration

Update your environment files:

**For local development** (`frontend/.env`):
```env
VITE_API_BASE_URL=http://localhost:8000
VITE_COGNITO_DOMAIN=https://yourdomain-prod.auth.ap-southeast-2.amazoncognito.com
VITE_COGNITO_CLIENT_ID=your-client-id-here
VITE_COGNITO_REDIRECT_URI=http://localhost:5173/callback
VITE_COGNITO_SCOPE=email+openid+phone+profile
```

**For Docker** (`docker/.env`):
```env
VITE_COGNITO_DOMAIN=https://yourdomain-prod.auth.ap-southeast-2.amazoncognito.com
VITE_COGNITO_CLIENT_ID=your-client-id-here
VITE_COGNITO_REDIRECT_URI=http://localhost:8080/callback
VITE_COGNITO_SCOPE=email+openid+phone+profile
```

**Backend** (`backend/.env`):
```env
COGNITO_REGION=ap-southeast-2
JWT_ISSUER=https://cognito-idp.ap-southeast-2.amazonaws.com/your-user-pool-id
JWT_AUDIENCE=your-client-id
JWKS_URL=https://cognito-idp.ap-southeast-2.amazonaws.com/your-user-pool-id/.well-known/jwks.json
```

## Testing Login Flow

1. Start the application:
   ```bash
   docker compose -f docker/docker-compose.yml up -d
   ```

2. Navigate to `http://localhost:8080`

3. Click **Login**

4. You'll be redirected to Cognito Hosted UI

5. Create test account or sign in

6. Upon successful authentication, you'll be redirected back to the app

## Troubleshooting

### "Invalid redirect URI"
- **Cause**: Callback URL doesn't match Cognito configuration
- **Fix**: Verify callback URLs in App Client settings match your environment

### "Unauthorized client"
- **Cause**: OAuth scopes not enabled
- **Fix**: Check "Allowed OAuth scopes" in app client, enable at least: openid, email

### "User not confirmed"
- **Cause**: User account exists but is not in CONFIRMED state
- **Fix**: 
  - Manual confirmation via AWS console: Go to Users → Select user → Admin actions → Confirm user
  - Or enable auto-confirmation in Cognito settings

### "JWKS endpoint unreachable"
- **Cause**: Backend can't reach Cognito's public key endpoint (network/firewall issue)
- **Fix**: Check internet connectivity, verify JWT_ISSUER URL format

## Production Deployment

### Security Considerations

1. **Enable MFA**: Go to User Pool settings → MFA configuration → Optional or Required
2. **Enable Email Verification**: Users must verify email before account is confirmed
3. **Use HTTPS**: All callback URLs must use HTTPS
4. **Set Strong Password Policy**: User Pool → Policies → Password policy
5. **Enable CloudTrail**: Track all Cognito operations for compliance

### Environment Variables

For production, use AWS Secrets Manager:

```bash
aws secretsmanager create-secret \
  --name address-checker/cognito \
  --secret-string '{"clientId":"...", "domain":"..."}'
```

### Scaling Considerations

Cognito automatically scales, but review:
- **Rate limiting**: Default limits are usually sufficient
- **Data retention**: Configure access token expiration (default 1 hour)
- **Sign-up restrictions**: Optional email domain whitelist

## References

- [AWS Cognito Documentation](https://docs.aws.amazon.com/cognito/)
- [OAuth 2.0 Authorization Code Grant](https://tools.ietf.org/html/rfc6749#section-1.3.1)
- [PKCE (RFC 7636)](https://tools.ietf.org/html/rfc7636)
