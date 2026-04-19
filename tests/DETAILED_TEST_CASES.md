# Detailed Test Cases - NZ Address Checker Application

## Test Case Format

Each test case follows this structure:

```
TEST ID: TC-XXX-YYY
TITLE: [Test Title]
CATEGORY: [Authentication/Address/Error/Journey/Visual]
PRIORITY: [Critical/High/Medium/Low]
TYPE: [Functional/Integration/Visual/Regression]

PRECONDITIONS:
- Item 1
- Item 2

TEST DATA:
- Field: Value

STEPS:
1. Step description
2. Step description
...

EXPECTED RESULT:
- Assertion 1
- Assertion 2

NOTES:
- Additional notes
```

---

## Authentication Test Cases

### TEST CASE: TC-AUTH-001
**TITLE**: User successfully logs in with valid credentials  
**CATEGORY**: Authentication  
**PRIORITY**: Critical  
**TYPE**: Functional/Integration  

**PRECONDITIONS**:
- User is on login page (http://localhost:8080)
- Valid Cognito test account exists
- Backend is running and healthy
- Internet connection available

**TEST DATA**:
- Email: test-user@example.com
- Password: ValidPassword123!
- Expected JWT token issuer: https://cognito-idp.ap-southeast-2.amazonaws.com/ap-southeast-2_2oQQDAKa4

**STEPS**:
1. Navigate to http://localhost:8080
2. Verify login page loads with form
3. Enter valid email address
4. Enter valid password
5. Click "Sign In" button
6. Wait for Cognito redirect (2-3 seconds)
7. Complete Cognito authentication
8. Wait for redirect back to application
9. Verify user is on main dashboard page
10. Check browser local storage for JWT token

**EXPECTED RESULT**:
- Login page displays correctly
- Cognito auth page loads on sign in
- User successfully authenticated with AWS Cognito
- JWT token present in localStorage
- User redirected to main application page
- No error messages displayed

**NOTES**:
- This is the critical path for authentication
- Must use actual Cognito test account
- Token expiration: 1 hour

---

### TEST CASE: TC-AUTH-002
**TITLE**: User login fails with invalid password  
**CATEGORY**: Authentication  
**PRIORITY**: High  
**TYPE**: Functional  

**PRECONDITIONS**:
- User is on login page
- Valid email exists in Cognito
- Network available

**TEST DATA**:
- Email: test-user@example.com
- Password: WrongPassword123!
- Expected error: Authentication failed

**STEPS**:
1. Navigate to http://localhost:8080
2. Enter valid email
3. Enter invalid password
4. Click "Sign In" button
5. Wait for Cognito response (3-5 seconds)
6. Observe Cognito error message

**EXPECTED RESULT**:
- Cognito displays "Incorrect username or password" error
- User remains on Cognito login page
- No JWT token created
- User cannot access main application

**NOTES**:
- Test negative scenario for authentication

---

### TEST CASE: TC-AUTH-003
**TITLE**: User successfully logs out  
**CATEGORY**: Authentication  
**PRIORITY**: Critical  
**TYPE**: Functional  

**PRECONDITIONS**:
- User is already logged in (JWT token in localStorage)
- User is on main application page

**TEST DATA**:
- JWT token: Valid token from login

**STEPS**:
1. Verify user is logged in (token exists)
2. Locate "Sign Out" button on page
3. Click "Sign Out" button
4. Wait for redirect (1-2 seconds)
5. Verify redirect to login page
6. Check browser localStorage for JWT token

**EXPECTED RESULT**:
- Sign Out button click successful
- JWT token removed from localStorage
- User redirected to login page (http://localhost:8080)
- Subsequent API calls return 401 if attempted

**NOTES**:
- Session termination must be immediate

---

### TEST CASE: TC-AUTH-004
**TITLE**: Protected endpoints reject requests without valid JWT  
**CATEGORY**: Authentication/Integration  
**PRIORITY**: Critical  
**TYPE**: Integration  

**PRECONDITIONS**:
- User is logged out (no JWT token)
- Backend is running

**TEST DATA**:
- Endpoint: /address-suggestions
- Method: GET
- Expected error: 401 Unauthorized

**STEPS**:
1. Ensure user is logged out
2. Clear localStorage (remove JWT)
3. Attempt to access protected endpoint via API call
4. Observe API response
5. Check response status code and error message

**EXPECTED RESULT**:
- API returns 401 Unauthorized status
- Response includes error message: "Missing bearer token"
- No sensitive data returned
- Request fails gracefully

**NOTES**:
- Security critical test case

---

## Address Suggestions Test Cases

### TEST CASE: TC-ADDR-001
**TITLE**: Address suggestions displayed for partial address input  
**CATEGORY**: Address/Functional  
**PRIORITY**: Critical  
**TYPE**: Functional/Integration  

**PRECONDITIONS**:
- User is logged in (JWT token exists)
- Backend address-suggestions API is available
- Test address data is loaded

**TEST DATA**:
- Input: "123 Main"
- Expected suggestions count: 5-10
- Sample expected address: "123 Main Street, Auckland"

**STEPS**:
1. Click on address input field
2. Type "123 Main"
3. Wait for API response (2-3 seconds)
4. Observe dropdown with suggestions
5. Count displayed suggestions
6. Verify address format

**EXPECTED RESULT**:
- Dropdown appears below input field
- Displays 5+ relevant address suggestions
- Each suggestion shows full address format
- Suggestions are clickable
- No error messages displayed
- API call completes within 3 seconds

**NOTES**:
- Core functionality for address input
- Requires real address database

---

### TEST CASE: TC-ADDR-002
**TITLE**: No suggestions displayed for invalid address string  
**CATEGORY**: Address/Functional  
**PRIORITY**: High  
**TYPE**: Functional  

**PRECONDITIONS**:
- User is logged in

**TEST DATA**:
- Input: "ZZZZZZZ Invalid Address 999"
- Expected suggestions count: 0

**STEPS**:
1. Click on address input field
2. Type invalid address string
3. Wait for API response (2-3 seconds)
4. Observe dropdown behavior

**EXPECTED RESULT**:
- Dropdown appears but is empty
- Message shows "No results found" (or similar)
- User can clear field and retry
- No error messages displayed

**NOTES**:
- Graceful handling of no-match scenario

---

### TEST CASE: TC-ADDR-003
**TITLE**: User can select address from suggestions  
**CATEGORY**: Address/Functional  
**PRIORITY**: Critical  
**TYPE**: Functional  

**PRECONDITIONS**:
- User is logged in
- Address suggestions are displayed

**TEST DATA**:
- Input: "123 Main"
- Select: First suggestion in dropdown
- Expected: Address input filled with selection

**STEPS**:
1. Type "123 Main" in address field
2. Wait for suggestions to appear
3. Click on first suggestion
4. Wait 1 second for field to update
5. Verify selected address appears in input field

**EXPECTED RESULT**:
- Selected address populates input field
- Dropdown closes after selection
- Full address displayed in input
- Ready for validation

**NOTES**:
- Critical for user workflow

---

## Address Validation Test Cases

### TEST CASE: TC-VAL-001
**TITLE**: Valid address passes validation  
**CATEGORY**: Validation/Functional  
**PRIORITY**: Critical  
**TYPE**: Functional/Integration  

**PRECONDITIONS**:
- User is logged in
- Address is selected or entered
- Backend address-check API is available

**TEST DATA**:
- Address: "1 Queen Street, Auckland, 1010"
- Expected result: Valid (true)
- API expected response: 200 OK

**STEPS**:
1. Enter or select valid address
2. Click "Validate Address" button
3. Wait for API response (3-5 seconds)
4. Observe validation result

**EXPECTED RESULT**:
- API returns 200 OK
- Validation result displayed: "Address is valid"
- Success message shown (green checkmark)
- No error messages
- API response time < 5 seconds

**NOTES**:
- Core validation functionality
- Address must exist in NZ Post database

---

### TEST CASE: TC-VAL-002
**TITLE**: Invalid address fails validation  
**CATEGORY**: Validation/Functional  
**PRIORITY**: High  
**TYPE**: Functional/Integration  

**PRECONDITIONS**:
- User is logged in
- Valid non-existent address will be tested

**TEST DATA**:
- Address: "999 Fake Street, Nowhere, 9999"
- Expected result: Invalid (false)

**STEPS**:
1. Enter invalid address
2. Click "Validate Address" button
3. Wait for API response (3-5 seconds)
4. Observe validation result

**EXPECTED RESULT**:
- API returns 200 OK with invalid result
- Validation result displayed: "Address is invalid"
- Error/warning message shown (red color)
- No exception/error in API response

**NOTES**:
- Tests negative validation path

---

### TEST CASE: TC-VAL-003
**TITLE**: Empty address field shows validation error  
**CATEGORY**: Validation/Functional  
**PRIORITY**: High  
**TYPE**: Functional  

**PRECONDITIONS**:
- User is logged in
- Address field is empty

**TEST DATA**:
- Input: (empty)
- Expected error: "Address cannot be empty"

**STEPS**:
1. Leave address field empty
2. Click "Validate Address" button
3. Observe client-side validation

**EXPECTED RESULT**:
- Client-side validation triggers immediately
- Error message displayed: "Address cannot be empty"
- No API request sent
- Button remains enabled for retry

**NOTES**:
- Client-side validation should prevent API call

---

### TEST CASE: TC-VAL-004
**TITLE**: API timeout handled gracefully  
**CATEGORY**: Validation/Error Handling  
**PRIORITY**: High  
**TYPE**: Functional  

**PRECONDITIONS**:
- User is logged in
- Address entered
- Backend API is slow or unresponsive

**TEST DATA**:
- Address: Any valid address
- Expected timeout: 10 seconds

**STEPS**:
1. Enter valid address
2. Click "Validate Address" button
3. Wait 10+ seconds for timeout
4. Observe error handling

**EXPECTED RESULT**:
- After timeout, error message displayed
- Message: "Request timeout, please try again"
- User can retry validation
- Loading indicator disappears
- No application crash

**NOTES**:
- Tests API resilience

---

## Error Handling Test Cases

### TEST CASE: TC-ERR-001
**TITLE**: Network error during API call shows error message  
**CATEGORY**: Error Handling  
**PRIORITY**: High  
**TYPE**: Functional  

**PRECONDITIONS**:
- User is logged in
- Network will be simulated as unavailable

**TEST DATA**:
- Scenario: Network disconnect
- Expected error: Network error message

**STEPS**:
1. Enter address
2. Simulate network failure (browser DevTools)
3. Click "Validate Address" button
4. Observe error handling

**EXPECTED RESULT**:
- Error message displayed to user
- User can retry when network restored
- Application remains stable
- No blank screens or crashes

**NOTES**:
- Tests error resilience

---

### TEST CASE: TC-ERR-002
**TITLE**: JWT token validation error handled  
**CATEGORY**: Error Handling/Integration  
**PRIORITY**: Critical  
**TYPE**: Integration  

**PRECONDITIONS**:
- User is logged in with valid token
- Token will be corrupted/invalid

**TEST DATA**:
- Token: Valid → Corrupted
- Expected error: 401 Unauthorized

**STEPS**:
1. User has valid session
2. Manually corrupt JWT token in localStorage
3. Attempt API call (validate address)
4. Observe error handling

**EXPECTED RESULT**:
- Backend returns 401 Unauthorized
- Frontend detects invalid token
- User is logged out automatically
- Redirect to login page
- Clear error message shown

**NOTES**:
- Security critical test

---

## User Journey Test Cases

### TEST CASE: TC-JRN-001
**TITLE**: Complete login → validate address → logout workflow  
**CATEGORY**: User Journey  
**PRIORITY**: Critical  
**TYPE**: Integration/E2E  

**PRECONDITIONS**:
- Application running on http://localhost:8080
- Valid test user credentials available
- Valid test address available

**TEST DATA**:
- Email: test-user@example.com
- Password: ValidPassword123!
- Address: "1 Queen Street, Auckland"

**STEPS**:
1. Navigate to http://localhost:8080
2. Login with valid credentials (see TC-AUTH-001 for details)
3. Wait for redirect to main page
4. Enter address "1 Queen" in search field
5. Select suggestion from dropdown
6. Click "Validate Address" button
7. Observe validation result
8. Click "Sign Out" button
9. Verify redirect to login page

**EXPECTED RESULT**:
- All steps complete successfully
- User successfully logs in
- Address suggestions work
- Validation completes
- User successfully logs out
- No errors or exceptions during workflow

**NOTES**:
- This is the primary user workflow
- All steps must succeed

---

### TEST CASE: TC-JRN-002
**TITLE**: Session recovery after token expiration  
**CATEGORY**: User Journey  
**PRIORITY**: High  
**TYPE**: Integration  

**PRECONDITIONS**:
- User is logged in
- Enough time passes for token to expire (1 hour)

**TEST DATA**:
- Token expiration time: 1 hour
- Test duration: Requires wait or token manipulation

**STEPS**:
1. User logs in and receives JWT token
2. Wait for token to approach expiration (or manually expire)
3. User attempts to validate an address
4. API returns 401 due to expired token
5. Application detects expiration
6. User is presented with "Session expired" message
7. User is logged out automatically
8. User can log back in

**EXPECTED RESULT**:
- Token expiration detected
- User informed of session expiration
- Graceful logout and redirect
- User can log back in to continue

**NOTES**:
- Token can be manually expired for testing

---

## Summary Table

| Test ID | Title | Category | Priority | Type | Status |
|---------|-------|----------|----------|------|--------|
| TC-AUTH-001 | Valid login | Auth | Critical | Functional | Pending |
| TC-AUTH-002 | Invalid login | Auth | High | Functional | Pending |
| TC-AUTH-003 | Logout | Auth | Critical | Functional | Pending |
| TC-AUTH-004 | Protected endpoints | Auth | Critical | Integration | Pending |
| TC-ADDR-001 | Suggestions display | Address | Critical | Functional | Pending |
| TC-ADDR-002 | No suggestions | Address | High | Functional | Pending |
| TC-ADDR-003 | Select suggestion | Address | Critical | Functional | Pending |
| TC-VAL-001 | Valid address | Validation | Critical | Integration | Pending |
| TC-VAL-002 | Invalid address | Validation | High | Integration | Pending |
| TC-VAL-003 | Empty address | Validation | High | Functional | Pending |
| TC-VAL-004 | API timeout | Validation | High | Functional | Pending |
| TC-ERR-001 | Network error | Error | High | Functional | Pending |
| TC-ERR-002 | JWT error | Error | Critical | Integration | Pending |
| TC-JRN-001 | Complete workflow | Journey | Critical | E2E | Pending |
| TC-JRN-002 | Session recovery | Journey | High | Integration | Pending |

**Total Test Cases**: 15  
**Critical Priority**: 7  
**High Priority**: 5  
**Medium Priority**: 3  

---

**Document Version**: 1.0  
**Last Updated**: 2026-04-19
