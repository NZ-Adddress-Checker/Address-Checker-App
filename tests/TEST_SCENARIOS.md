# Test Scenarios - NZ Address Checker Application

## Overview
This document outlines all test scenarios for the NZ Address Checker application, organized by feature and user workflow.

---

## 1. Authentication Scenarios

### Scenario 1.1: User Login with Valid Credentials
**Description**: User logs in using valid Cognito credentials  
**Actor**: Unauthenticated User  
**Preconditions**:
- User is on the login page
- Valid Cognito test account exists
- Internet connection available

**Flow**:
1. User enters valid email
2. User enters valid password
3. User clicks "Sign In" button
4. Cognito authentication page appears
5. User completes Cognito login flow
6. Application receives authentication token
7. User is redirected to main application page

**Expected Result**: User successfully authenticated, redirected to home page, token stored locally

---

### Scenario 1.2: User Login with Invalid Credentials
**Description**: User attempts login with incorrect password  
**Actor**: Unauthenticated User  
**Preconditions**:
- User is on the login page
- Valid email but invalid password will be used

**Flow**:
1. User enters valid email
2. User enters incorrect password
3. User clicks "Sign In" button
4. Cognito authentication fails
5. Error message displayed

**Expected Result**: Login fails, error message shown, user remains on login page

---

### Scenario 1.3: User Logout
**Description**: Authenticated user logs out  
**Actor**: Authenticated User  
**Preconditions**:
- User is logged in
- User is on the main application page

**Flow**:
1. User clicks "Sign Out" button
2. Session is terminated
3. Token is removed from local storage
4. User is redirected to login page

**Expected Result**: User successfully logged out, token cleared, redirected to login page

---

### Scenario 1.4: Token Expiration Handling
**Description**: User's session token expires  
**Actor**: Authenticated User  
**Preconditions**:
- User is logged in
- Token will expire during test

**Flow**:
1. User is using the application
2. Token expires
3. User attempts to access protected resource
4. Backend returns 401 Unauthorized
5. Application detects token expiration
6. User is redirected to login page
7. Error message shown

**Expected Result**: User logged out due to token expiration, redirected to login, informed of session expiration

---

## 2. Address Suggestions Scenarios

### Scenario 2.1: Fetch Address Suggestions
**Description**: User gets address suggestions while typing  
**Actor**: Authenticated User  
**Preconditions**:
- User is logged in
- Backend API is available
- Test address data available

**Flow**:
1. User clicks on address input field
2. User types partial address "123 M"
3. Application calls address-suggestions API
4. API returns matching addresses
5. Suggestions dropdown appears below input

**Expected Result**: Dropdown shows relevant address suggestions, user can select one

---

### Scenario 2.2: Address Suggestions with No Results
**Description**: Search returns no matching addresses  
**Actor**: Authenticated User  
**Preconditions**:
- User is logged in
- Using non-existent address string

**Flow**:
1. User types invalid address string "ZZZZZZZ Invalid Street"
2. Application calls address-suggestions API
3. API returns empty result set
4. Dropdown appears empty or shows "No results" message

**Expected Result**: Empty suggestions, user can clear and try again

---

### Scenario 2.3: Address Suggestion Timeout
**Description**: API request times out  
**Actor**: Authenticated User  
**Preconditions**:
- Backend API is slow or unresponsive

**Flow**:
1. User types address in input field
2. API request is sent
3. Request timeout after configured wait time
4. Error message displayed to user

**Expected Result**: Graceful error handling, user notified of timeout, can retry

---

## 3. Address Validation Scenarios

### Scenario 3.1: Validate Valid Address
**Description**: User validates a correct NZ address  
**Actor**: Authenticated User  
**Preconditions**:
- User is logged in
- Valid NZ address available for testing

**Flow**:
1. User selects or enters valid address
2. User clicks "Validate Address" button
3. Application calls address-check API
4. API validates address against NZ Post database
5. Success response returned
6. Validation result displayed

**Expected Result**: Address validation succeeds, result shown (valid/invalid)

---

### Scenario 3.2: Validate Invalid Address
**Description**: User attempts to validate non-existent address  
**Actor**: Authenticated User  
**Preconditions**:
- User is logged in
- Invalid/non-existent address string available

**Flow**:
1. User enters invalid address
2. User clicks "Validate Address" button
3. Application calls address-check API
4. API returns invalid address response
5. Validation failed message displayed

**Expected Result**: Invalid address detected, appropriate error message shown

---

### Scenario 3.3: Empty Address Validation
**Description**: User attempts to validate empty address field  
**Actor**: Authenticated User  
**Preconditions**:
- User is logged in
- Address field is empty

**Flow**:
1. User leaves address field empty
2. User clicks "Validate Address" button
3. Client-side validation triggers
4. Error message: "Address cannot be empty"

**Expected Result**: Validation error shown, API not called

---

### Scenario 3.4: Address Validation API Timeout
**Description**: Address validation API request times out  
**Actor**: Authenticated User  
**Preconditions**:
- Backend API is slow or unresponsive

**Flow**:
1. User enters address
2. User clicks "Validate Address" button
3. API request sent
4. Request times out (504 error)
5. Timeout error message displayed

**Expected Result**: Timeout error shown, user can retry

---

## 4. Error Handling Scenarios

### Scenario 4.1: Network Error During Login
**Description**: Network disconnects during login attempt  
**Actor**: Unauthenticated User  
**Preconditions**:
- Network is unavailable
- User is on login page

**Flow**:
1. User enters credentials
2. User clicks "Sign In"
3. Network request fails
4. Error message shown: "Network error, please retry"

**Expected Result**: Graceful error handling, user can retry

---

### Scenario 4.2: Invalid JWT Token Response
**Description**: Backend returns JWT validation error  
**Actor**: Authenticated User  
**Preconditions**:
- User is logged in
- JWT token is corrupted or invalid

**Flow**:
1. User attempts API call
2. Backend validates JWT
3. JWT validation fails (401)
4. Error response: "Unable to validate token"

**Expected Result**: Error shown, user may need to re-login

---

### Scenario 4.3: API Rate Limiting
**Description**: User exceeds API rate limit  
**Actor**: Authenticated User  
**Preconditions**:
- User makes many rapid requests

**Flow**:
1. User rapidly validates multiple addresses
2. Rate limit exceeded on backend
3. 429 error returned
4. Rate limit message displayed

**Expected Result**: Rate limit error shown, user advised to wait

---

## 5. User Journey Scenarios

### Scenario 5.1: Complete Address Validation Workflow
**Description**: User logs in, searches for address, validates it, and logs out  
**Actor**: User  
**Preconditions**:
- Application is running
- Valid test user and address data available

**Flow**:
1. User lands on login page
2. User logs in with valid credentials
3. User is redirected to main page
4. User enters address in search field
5. User sees address suggestions
6. User selects suggestion
7. User clicks "Validate Address" button
8. Validation result is displayed
9. User clicks "Sign Out" button
10. User is logged out and redirected to login page

**Expected Result**: Complete workflow succeeds, user can perform all actions

---

### Scenario 5.2: Session Timeout During Usage
**Description**: User's session expires while using the application  
**Actor**: Authenticated User  
**Preconditions**:
- User is logged in and using the application
- Enough time passes for token to expire

**Flow**:
1. User is actively using the application
2. Token expires in background
3. User attempts to validate an address
4. API returns 401 Unauthorized
5. Application detects session timeout
6. User is automatically logged out
7. Redirect to login page with timeout message

**Expected Result**: Graceful session timeout, user informed, can log back in

---

### Scenario 5.3: Multiple Address Validations
**Description**: User validates multiple addresses in one session  
**Actor**: Authenticated User  
**Preconditions**:
- User is logged in

**Flow**:
1. User validates address #1
2. Result displayed
3. User clears form
4. User validates address #2
5. Result displayed
6. User validates address #3
7. Result displayed
8. Repeat for multiple addresses

**Expected Result**: All validations succeed, results displayed correctly

---

## 6. Visual & UI Scenarios

### Scenario 6.1: Form Input Validation Messages
**Description**: User sees appropriate validation messages  
**Actor**: User  
**Preconditions**:
- User is on the application

**Flow**:
1. User sees login form with empty fields
2. User tries to submit empty form
3. Validation message appears
4. User sees helpful error text
5. User fills in fields
6. Error messages clear

**Expected Result**: Clear, helpful validation messages displayed

---

### Scenario 6.2: Loading State During API Calls
**Description**: User sees loading indicator during API requests  
**Actor**: Authenticated User  
**Preconditions**:
- User is on the application
- API call is in progress

**Flow**:
1. User clicks "Validate Address"
2. Loading spinner appears
3. Button is disabled
4. Request completes
5. Loading spinner disappears
6. Result displayed

**Expected Result**: Loading state clearly shown, user knows request is processing

---

### Scenario 6.3: Responsive Design on Mobile
**Description**: Application displays correctly on mobile devices  
**Actor**: User on Mobile Device  
**Preconditions**:
- Application accessed on mobile browser (320px width)

**Flow**:
1. User opens application on mobile
2. Layout adapts to small screen
3. Form elements are properly sized
4. Text is readable
5. Buttons are clickable
6. All functionality works

**Expected Result**: Application fully functional and visually correct on mobile

---

## Summary

| Category | Count | Status |
|----------|-------|--------|
| Authentication | 4 | Planned |
| Address Suggestions | 3 | Planned |
| Address Validation | 4 | Planned |
| Error Handling | 3 | Planned |
| User Journeys | 3 | Planned |
| Visual & UI | 3 | Planned |
| **Total** | **20** | **Planned** |

---

**Document Version**: 1.0  
**Last Updated**: 2026-04-19
