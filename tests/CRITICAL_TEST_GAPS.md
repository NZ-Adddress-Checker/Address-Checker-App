# Critical Test Gaps - P0 & P1 Scenarios

## Overview
This document outlines critical (P0) and high-priority (P1) test scenarios that are missing from the current test suite. These are essential for production readiness.

---

## P0 (Critical) - Must Have Before Production

### P0-1: Session Persistence on Page Refresh
**Description**: User's session should persist when page is refreshed  
**Priority**: Critical (P0)  
**Type**: Integration  

**Preconditions**:
- User is logged in with valid JWT token
- Token stored in localStorage

**Steps**:
1. User logs in successfully
2. Verify JWT token in localStorage
3. User refreshes page (F5 or Ctrl+R)
4. Verify user is still logged in
5. Verify token is still valid
6. Attempt API call to validate address
7. Verify API accepts request (not 401)

**Expected Result**:
- Page refresh does not log user out
- JWT token persists in localStorage
- API calls work immediately after refresh
- No redirect to login page

**Test Data**:
- Same as TC-AUTH-001

---

### P0-2: Multiple Browser Tabs Session Synchronization
**Description**: Logout in one tab should affect other tabs  
**Priority**: Critical (P0)  
**Type**: Integration  

**Preconditions**:
- User is logged in
- User has 2 browser tabs open with application

**Steps**:
1. User has application open in Tab A (logged in)
2. User opens application in Tab B (also logged in)
3. User clicks logout in Tab A
4. Wait 1 second
5. Switch to Tab B
6. Attempt to validate address in Tab B
7. Observe response

**Expected Result**:
- Logout in Tab A clears localStorage
- Tab B detects missing token on API call
- Tab B redirects user to login page
- User cannot access protected resources from Tab B

**Test Data**:
- Cognito credentials

---

### P0-3: API Handling Null/Undefined Response
**Description**: API returning null/undefined data should be handled gracefully  
**Priority**: Critical (P0)  
**Type**: Integration  

**Preconditions**:
- User is logged in
- Backend configured to return null for address-check

**Steps**:
1. Enter valid address
2. Backend returns null response (200 OK, but null data)
3. Observe frontend handling

**Expected Result**:
- Application displays error message
- No JavaScript console errors
- No blank/undefined UI elements
- User can retry

**Notes**:
- Tests robustness against malformed API responses

---

### P0-4: Form State Persistence During Error
**Description**: Address input should not be cleared when validation fails  
**Priority**: Critical (P0)  
**Type**: Functional  

**Preconditions**:
- User is logged in
- User has entered address

**Steps**:
1. Enter address "999 Fake Street"
2. Click "Validate Address"
3. Address validation fails (invalid address)
4. Observe address field

**Expected Result**:
- Error message displayed
- Address remains in input field
- User can edit address and retry
- User does not need to re-type entire address

---

### P0-5: XSS Prevention in Address Input
**Description**: Special/malicious characters in address field should be safely handled  
**Priority**: Critical (P0)  
**Type**: Security/Functional  

**Preconditions**:
- User is logged in

**Steps**:
1. Enter malicious input: `<script>alert('xss')</script>`
2. Click validate
3. Observe application behavior
4. Check browser console for errors

**Expected Result**:
- Input is safely escaped/sanitized
- No JavaScript alert appears
- Input is treated as literal string
- API receives properly encoded data
- No console errors
- No page crash

---

### P0-6: API Error with Malformed JSON Response
**Description**: Backend returning malformed JSON should be handled  
**Priority**: Critical (P0)  
**Type**: Integration  

**Preconditions**:
- User is logged in
- Backend configured to return invalid JSON

**Steps**:
1. Enter address
2. Backend returns invalid JSON response (e.g., `{invalid json}`)
3. Observe frontend error handling

**Expected Result**:
- Application catches JSON parse error
- User sees "Server error, please try again" message
- Application remains stable
- No blank screens
- User can retry

---

### P0-7: Keyboard Navigation in Suggestions Dropdown
**Description**: User should navigate suggestions using arrow keys  
**Priority**: Critical (P0)  
**Type**: Functional  

**Preconditions**:
- User is logged in
- Address suggestions are displayed in dropdown

**Steps**:
1. Type "123 Main" to show suggestions
2. Press arrow down key
3. Verify first suggestion is highlighted
4. Press arrow down again
5. Verify second suggestion is highlighted
6. Press Enter
7. Verify selected suggestion fills input

**Expected Result**:
- Arrow keys navigate suggestions
- Current selection is visually highlighted
- Enter key selects highlighted suggestion
- Suggestion populates address field
- Dropdown closes

---

### P0-8: Escape Key Closes Suggestions Dropdown
**Description**: Escape key should close open suggestions dropdown  
**Priority**: Critical (P0)  
**Type**: Functional  

**Preconditions**:
- User is logged in
- Address suggestions dropdown is open

**Steps**:
1. Type "123" to show suggestions
2. Dropdown appears
3. Press Escape key
4. Observe dropdown

**Expected Result**:
- Dropdown closes immediately
- Address input retains typed value
- Input field remains focused
- User can continue typing or validate

---

### P0-9: Token Refresh/Rotation Mechanism
**Description**: Expired token should be refreshed before API call fails  
**Priority**: Critical (P0)  
**Type**: Integration/Security  

**Preconditions**:
- User is logged in
- Refresh token available
- Access token approaching expiration

**Steps**:
1. User logs in (get access + refresh token)
2. Wait until access token expires (within last minute)
3. User attempts to validate address
4. Application detects token expiration
5. Application uses refresh token to get new access token
6. API call retries with new token
7. Validation succeeds

**Expected Result**:
- User does not experience interruption
- Token refreshed silently
- API call succeeds with new token
- No redirect to login
- User continues workflow seamlessly

---

### P0-10: Click Outside Dropdown Closes It
**Description**: Clicking outside dropdown should close suggestions  
**Priority**: Critical (P0)  
**Type**: Functional  

**Preconditions**:
- Suggestions dropdown is open

**Steps**:
1. Type "123 Main" to show suggestions
2. Dropdown displays suggestions
3. Click on empty area of page (not dropdown)
4. Observe dropdown

**Expected Result**:
- Dropdown closes
- Address input value preserved
- Click does not trigger validation

---

## P1 (High) - Important for Quality

### P1-1: Debounce Address Suggestions API Calls
**Description**: Rapid typing should debounce API calls (prevent 5+ calls for 5 keystrokes)  
**Priority**: High (P1)  
**Type**: Performance/Functional  

**Preconditions**:
- User is logged in

**Steps**:
1. Type "1 2 3 4 5" rapidly (one char per 100ms)
2. Open browser DevTools Network tab
3. Count API calls to address-suggestions
4. Wait for all typing to complete

**Expected Result**:
- Only 1-2 API calls made (not 5)
- Debounce delay approximately 300-500ms
- Last keystroke triggers final API call
- Reduces server load significantly

---

### P1-2: Copy/Paste Address Input Handling
**Description**: User should be able to copy/paste address  
**Priority**: High (P1)  
**Type**: Functional  

**Preconditions**:
- User is logged in
- Address text available to copy

**Steps**:
1. Copy address text from external source
2. Click address input field
3. Paste address (Ctrl+V)
4. Verify address appears correctly
5. Wait for suggestions
6. Click validate

**Expected Result**:
- Pasted text appears in input
- Suggestions API triggered normally
- Validation works with pasted address
- No formatting issues

---

### P1-3: Multiple Form Submissions Prevention
**Description**: Clicking validate button rapidly should only process once  
**Priority**: High (P1)  
**Type**: Functional  

**Preconditions**:
- User is logged in
- Address entered

**Steps**:
1. Enter valid address
2. Click "Validate Address" button 3 times rapidly
3. Observe button and API calls

**Expected Result**:
- Button is disabled during processing
- Only 1 API call made (not 3)
- Loading spinner shows
- Button re-enabled when response received
- User sees single result (not duplicated)

---

### P1-4: Browser Back Button Behavior
**Description**: Back button should not break application  
**Priority**: High (P1)  
**Type**: Functional  

**Preconditions**:
- User is logged in
- User has validated an address

**Steps**:
1. User validates an address (result shown)
2. User clicks browser back button
3. Observe application state

**Expected Result**:
- Application remains functional
- User stays logged in
- Navigation works correctly
- No 404 errors or redirects to login
- State is preserved appropriately

---

### P1-5: Special Characters in Address Input
**Description**: Addresses with special characters should work  
**Priority**: High (P1)  
**Type**: Functional  

**Preconditions**:
- User is logged in
- Test addresses with special characters available

**Steps**:
1. Enter address with apostrophe: "O'Connell Street"
2. Verify suggestions appear
3. Enter address with dash: "North-East"
4. Verify suggestions work
5. Enter address with numbers: "123A Main Street"
6. Validate address

**Expected Result**:
- Special characters preserved
- Suggestions work correctly
- Validation handles special characters
- API receives proper encoding (UTF-8)
- No data corruption

---

### P1-6: API Timeout with Loading Indicator
**Description**: Long API calls should show loading state  
**Priority**: High (P1)  
**Type**: Functional/UX  

**Preconditions**:
- User is logged in
- Backend configured to respond slowly (5+ seconds)

**Steps**:
1. Enter address
2. Click "Validate Address"
3. Observe UI during wait
4. API responds after 5+ seconds

**Expected Result**:
- Loading spinner/indicator appears immediately
- Button is disabled
- User cannot click validate again
- After timeout (10s), error message shows
- User can retry

---

### P1-7: Invalid Token Error Message Clarity
**Description**: 401 errors should show clear message prompting re-login  
**Priority**: High (P1)  
**Type**: Error Handling/UX  

**Preconditions**:
- User has invalid/corrupted JWT token

**Steps**:
1. Manually corrupt JWT in localStorage
2. Attempt to validate address
3. Observe error message
4. Check if user is logged out

**Expected Result**:
- Clear error message: "Your session has expired. Please log in again."
- User is logged out automatically
- Redirect to login page
- Message is actionable (not technical)

---

### P1-8: Network Error Handling
**Description**: Network errors should be caught and displayed  
**Priority**: High (P1)  
**Type**: Error Handling  

**Preconditions**:
- User is logged in

**Steps**:
1. Open DevTools Network tab
2. Check "Offline" checkbox (offline mode)
3. Try to validate address
4. Observe error handling

**Expected Result**:
- Network error caught (not a page crash)
- User sees error message: "Network error. Check connection."
- User can retry when network restored
- Application remains stable

---

### P1-9: Maximum Input Length Handling
**Description**: Very long address input should be handled  
**Priority**: High (P1)  
**Type**: Functional/Boundary  

**Preconditions**:
- User is logged in

**Steps**:
1. Enter address string of 500 characters
2. Verify input accepts it (or truncates)
3. Attempt validation
4. Observe behavior

**Expected Result**:
- Input field has max length limit (or enforced)
- Does not crash
- API handles long strings gracefully
- Error message if too long

---

### P1-10: Suggestions with Same Name Different Suburbs
**Description**: Duplicate street names in different areas handled correctly  
**Priority**: High (P1)  
**Type**: Functional  

**Preconditions**:
- NZ has multiple "Main Streets" in different suburbs

**Steps**:
1. Search for common street name: "Main Street"
2. Verify suggestions show multiple results
3. Verify each result shows suburb/area
4. User can select specific one
5. Validation succeeds

**Expected Result**:
- All matching streets displayed
- Area/suburb shown for each
- User can distinguish between results
- Selection is specific
- Validation uses correct address

---

## Summary Table

| ID | Test Name | Category | Priority | Type |
|----|-----------|-----------|-----------|----|
| P0-1 | Session persistence | Auth | P0 | Integration |
| P0-2 | Multi-tab sync | Auth | P0 | Integration |
| P0-3 | Null API response | Error | P0 | Integration |
| P0-4 | Form state on error | UX | P0 | Functional |
| P0-5 | XSS prevention | Security | P0 | Security |
| P0-6 | Malformed JSON | Error | P0 | Integration |
| P0-7 | Keyboard navigation | UX | P0 | Functional |
| P0-8 | Escape key | UX | P0 | Functional |
| P0-9 | Token refresh | Auth | P0 | Integration |
| P0-10 | Click outside close | UX | P0 | Functional |
| P1-1 | Debounce calls | Performance | P1 | Functional |
| P1-2 | Copy/paste | UX | P1 | Functional |
| P1-3 | Multi-submit prevention | UX | P1 | Functional |
| P1-4 | Back button | Navigation | P1 | Functional |
| P1-5 | Special characters | Data | P1 | Functional |
| P1-6 | Slow API | UX | P1 | Functional |
| P1-7 | 401 error message | Error | P1 | UX |
| P1-8 | Network error | Error | P1 | Error |
| P1-9 | Max input length | Boundary | P1 | Functional |
| P1-10 | Duplicate streets | Data | P1 | Functional |

**Total**: 20 critical tests (10 P0 + 10 P1)

---

**Document Version**: 1.0  
**Last Updated**: 2026-04-19  
**Status**: Ready for Implementation
