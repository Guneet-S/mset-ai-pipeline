# Test Plan — Basic User Login Scenario

## 1. Scope
Testing the critical login flow on https://www.saucedemo.com — entering a valid username and password and successfully reaching the products page. Out of scope: password reset, account creation, session persistence, and all post-login functionality.

## 2. Objectives
Validate that a registered user can authenticate with correct credentials, that invalid credentials are rejected with an appropriate error message, and that the application loads the authenticated state reliably on the web platform.

## 3. Test Types
- Functional testing: happy path login with valid credentials
- Negative testing: invalid username, invalid password, empty fields
- Boundary testing: locked-out user account (provided by Sauce Labs demo data)

## 4. Test Approach
- Manual: one-time exploratory pass to verify UX, error message wording, and field behaviour
- Automated: regression-safe smoke suite using WebDriverIO targeting the login form on https://www.saucedemo.com; leverages Sauce Labs My Demo App credential fixtures (standard_user, locked_out_user, problem_user)

## 5. Entry Criteria
The application at https://www.saucedemo.com is reachable, the test environment has network access, and valid test credentials (standard_user / secret_sauce) are confirmed working.

## 6. Exit Criteria
All smoke test cases pass with zero critical defects open; login with valid credentials consistently reaches the products page; invalid-credential error messages display correctly.

## 7. Risks
The demo site is a third-party public URL — availability is not guaranteed; mitigation is to retry on transient failures and alert if the site is down. Sauce Labs demo credentials are publicly known and could change without notice.

## 8. Timeline
Automated smoke suite: 2 hours to author and validate. Manual exploratory pass: 30 minutes. Total estimated effort: 2.5 hours.
