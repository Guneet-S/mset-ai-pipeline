# Test Plan — Login and Product Catalog (Sauce Labs Demo App)

## 1. Scope
Testing covers: username/password login (valid, invalid, locked-out credentials), product catalog listing (sort by name A-Z/Z-A, price low-high/high-low), and the add-to-cart flow (add single item, add multiple items, verify cart badge count). Out of scope: checkout/payment flow, user profile management, and backend API internals.

## 2. Objectives
Validate that authenticated users can log in successfully, that the product catalog renders and sorts correctly under all four sort options, and that items can be added to (and reflected in) the cart — covering all core functional paths for these three features.

## 3. Test Types
- **Functional testing** — all login states, all sort options, add-to-cart across multiple products
- **Negative / boundary testing** — invalid credentials, locked-out user, empty cart state, adding the same item twice
- **Regression testing** — re-run all functional flows after any change to login or catalog logic
- **Accessibility** — verify login form labels, button roles, and keyboard navigation are correct

## 4. Test Approach
- **Manual:** exploratory testing of UX edge cases (e.g. error message copy, visual sort feedback), one-time login-state scenarios (session expiry), and accessibility spot-checks
- **Automated:** data-driven login tests (credential matrix), sort verification (assert DOM order matches expected), add-to-cart regression suite
- **Tools:** WebDriverIO + Appium (web driver for https://www.saucedemo.com), Sauce Labs My Demo App as the reference implementation for expected behaviours

## 5. Entry Criteria
- https://www.saucedemo.com is reachable and returning HTTP 200
- All test credentials (standard_user, locked_out_user, problem_user) are confirmed active
- Automated test framework is configured and able to open the target URL

## 6. Exit Criteria
- All functional test cases pass for login, sort, and add-to-cart flows
- Zero P1 defects open; all P2 defects have an accepted mitigation or scheduled fix
- Automated suite runs clean (no flaky failures) on two consecutive runs

## 7. Risks
- **Sauce Labs demo site instability** — mitigate by retrying on transient failures and pinning test runs to off-peak hours
- **problem_user rendering bugs** — these are intentional; document but do not block on them unless they affect scope features
- **Browser compatibility variance** — mitigate by running suite on Chrome and Firefox as minimum baseline

## 8. Timeline
| Test Type | Estimated Effort |
|---|---|
| Functional (manual pass) | 2 hours |
| Negative / boundary (manual) | 1 hour |
| Automated suite setup + scripting | 3 hours |
| Regression run + triage | 1 hour |
| Accessibility spot-check | 0.5 hours |
| **Total** | **7.5 hours** |
