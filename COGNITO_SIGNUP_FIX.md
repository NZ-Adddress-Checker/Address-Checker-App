# Cognito Sign Up Fix: Invalid Challenge Transition Error

## Problem

When users click "Sign Up" and complete the registration through the Cognito Hosted UI, they may encounter this error:

```
Invalid input: Invalid challenge transition while signing up new user
```

This error occurs because the user's account is created but left in a state that requires additional action (e.g., `FORCE_CHANGE_PASSWORD`), which conflicts with the OAuth PKCE flow.

## Root Cause

1. User signs up via Cognito Hosted UI (using `prompt=signup`)
2. Cognito creates the user account but places them in a state like `FORCE_CHANGE_PASSWORD`
3. During the OAuth callback, Cognito attempts to verify the PKCE challenge, but the challenge state is invalid because the user needs to complete additional steps
4. The app fails to exchange the authorization code for tokens

## Solution: Configure Cognito for Self-Service Sign Up

### Step 1: Enable Self-Service Sign Up

1. Go to **AWS Cognito Console** → Select your User Pool
2. Navigate to **Sign-up experience** (in the left sidebar)
3. Under "Self-service sign-up", select **Enable self-registration**
4. Configure the following:
   - **Attribute verification or confirmation**: Choose one:
     - **Send email message** (Recommended for production)
     - **Automatic confirmation** (Immediate account activation, useful for testing)
   - **Allowed attributes for sign-up**: Select attributes users can set during signup
   - **Required attributes**: Mark required fields (email, phone, etc.)

### Step 2: Configure Cognito to Auto-Confirm New Users (Optional - Testing Only)

For development/testing, auto-confirm new users:

1. Go to **App Integration** → **App Clients** → Select your app client
2. Scroll down to **Additional settings**
3. Under **Email settings** or **MFA settings**, ensure:
   - **Email required for sign-up**: Check if you want email verification
   - **Phone number required for sign-up**: Uncheck unless you need it

### Step 3: Alternatively, Manually Confirm Users in AWS Console

If you cannot auto-confirm, you must manually confirm new users:

1. Go to **User management** → **Users**
2. Find the user who signed up
3. Click the user
4. Scroll to **Account status**
5. Click **Set permanent password** or **Confirm user account**
6. Set a permanent password
7. User should now be able to log in

### Step 4: Set User Password Using Backend (Recommended for Production)

Instead of manual confirmation, use your backend to auto-confirm users:

**Add this to your FastAPI backend** (`backend/services/cognito_management.py`):

```python
import boto3
from botocore.exceptions import ClientError

cognito_client = boto3.client('cognito-idp', region_name='ap-southeast-2')

def confirm_user_signup(user_pool_id: str, username: str):
    """Auto-confirm a user after signup"""
    try:
        cognito_client.admin_confirm_sign_up(
            UserPoolId=user_pool_id,
            Username=username
        )
        return True
    except ClientError as e:
        print(f"Error confirming user: {e}")
        return False

def set_user_permanent_password(user_pool_id: str, username: str, password: str):
    """Set a permanent password for a user"""
    try:
        cognito_client.admin_set_user_password(
            UserPoolId=user_pool_id,
            Username=username,
            Password=password,
            Permanent=True
        )
        return True
    except ClientError as e:
        print(f"Error setting permanent password: {e}")
        return False
```

Then hook this into a post-signup Lambda trigger in Cognito.

## Changes Made to Frontend

The frontend now supports both login and signup flows:

1. **Added `isSignUp` parameter** to `buildPkceAuthorizeUrl()` in `src/auth/pkce.js`
   - Uses `prompt=signup` for new user registration
   - Uses `prompt=login` for existing users

2. **Added "Sign Up" button** in `src/components/LoginPage.jsx`
   - Users can now choose between Login and Sign Up
   - Both flows use the same PKCE security flow

3. **Updated styling** in `src/styles.css`
   - Login and Sign Up buttons display side-by-side

## Testing the Fix

1. Start the application
2. Click "Sign Up"
3. Complete the registration form
4. **If auto-confirm is enabled**: You should be redirected to the address checker
5. **If manual confirmation required**: 
   - Confirm the user in AWS Cognito Console
   - Try logging in again

## Environment Configuration

Ensure your Cognito configuration in `docker/.env` or `frontend/.env` is correct:

```env
VITE_COGNITO_DOMAIN=https://your-domain.auth.region.amazoncognito.com
VITE_COGNITO_CLIENT_ID=your-client-id
VITE_COGNITO_REDIRECT_URI=http://localhost:8080/callback  # or http://localhost:5173/callback for local dev
VITE_COGNITO_SCOPE=email+openid+phone+profile
```

## Common Issues and Troubleshooting

### Issue: "Invalid challenge transition" still appears

**Solution**: 
- Manually confirm the user in AWS Cognito Console (User management → Users → Select user → Set permanent password)
- OR enable auto-confirmation in Cognito settings

### Issue: Sign Up button does nothing

**Solution**: 
- Check browser console for errors (F12)
- Verify `VITE_COGNITO_*` environment variables are set correctly
- Ensure Cognito self-service sign-up is enabled

### Issue: Error after successful signup redirect

**Solution**: 
- Check that the redirect URI in your Cognito app client matches `VITE_COGNITO_REDIRECT_URI`
- Ensure callback URL is added to Cognito: **App Integration** → **App Clients** → **Allowed callback URLs**

## Recommended Production Setup

For production:

1. **Enable email verification**: Users receive an email with a confirmation link
2. **Set user password via Lambda**: Use a post-signup Lambda to auto-confirm users
3. **Require email**: Make email a required attribute
4. **Enable MFA**: Consider enabling MFA for enhanced security

For development/testing:

1. Enable auto-confirmation
2. Skip email verification
3. Manually confirm test users as needed
