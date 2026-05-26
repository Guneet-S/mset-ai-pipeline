import LoginPage from '../pages/login.page';
import { waitForUrl } from '../../../../framework/helpers/wait.helper';

describe('Authentication', () => {

  beforeEach(async () => {
    await LoginPage.open();
  });

  // TC-001: Valid login with standard_user credentials
  it('TC-001: Valid login with standard_user credentials', async () => {
    await LoginPage.login('standard_user', 'secret_sauce');
    await waitForUrl('/inventory.html');
    expect(await browser.getUrl()).toContain('/inventory.html');
  });

  // TC-002: Login fails with incorrect password
  it('TC-002: Login fails with incorrect password', async () => {
    await LoginPage.login('standard_user', 'wrong_password');
    await expect(LoginPage.errorMessage).toBeDisplayed();
    await expect(LoginPage.errorMessage).toHaveText(
      expect.stringContaining('Username and password do not match')
    );
    expect(await browser.getUrl()).not.toContain('/inventory.html');
  });

  // TC-003: Login fails with completely invalid credentials
  it('TC-003: Login fails with completely invalid credentials', async () => {
    await LoginPage.login('invalid_user', 'invalid_pass');
    await expect(LoginPage.errorMessage).toBeDisplayed();
    expect(await browser.getUrl()).not.toContain('/inventory.html');
  });

  // TC-004: Locked-out user cannot log in
  it('TC-004: Locked-out user cannot log in', async () => {
    await LoginPage.login('locked_out_user', 'secret_sauce');
    await expect(LoginPage.errorMessage).toBeDisplayed();
    await expect(LoginPage.errorMessage).toHaveText(
      expect.stringContaining('Sorry, this user has been locked out')
    );
    expect(await browser.getUrl()).not.toContain('/inventory.html');
  });

  // TC-005: Login fails when Username field is empty
  it('TC-005: Login fails when Username field is empty', async () => {
    await LoginPage.passwordField.setValue('secret_sauce');
    await LoginPage.loginButton.click();
    await expect(LoginPage.errorMessage).toBeDisplayed();
    await expect(LoginPage.errorMessage).toHaveText(
      expect.stringContaining('Username is required')
    );
  });

  // TC-006: Login fails when Password field is empty
  it('TC-006: Login fails when Password field is empty', async () => {
    await LoginPage.usernameField.setValue('standard_user');
    await LoginPage.loginButton.click();
    await expect(LoginPage.errorMessage).toBeDisplayed();
    await expect(LoginPage.errorMessage).toHaveText(
      expect.stringContaining('Password is required')
    );
  });

  // TC-007: Login fails when both fields are empty
  it('TC-007: Login fails when both fields are empty', async () => {
    await LoginPage.loginButton.click();
    await expect(LoginPage.errorMessage).toBeDisplayed();
    await expect(LoginPage.errorMessage).toHaveText(
      expect.stringContaining('Username is required')
    );
  });

  // TC-008: Error message can be dismissed after failed login
  it('TC-008: Error message can be dismissed after failed login', async () => {
    await LoginPage.login('bad_user', 'bad_pass');
    await expect(LoginPage.errorMessage).toBeDisplayed();
    await LoginPage.dismissError();
    await expect(LoginPage.errorMessage).not.toBeDisplayed();
    await expect(LoginPage.usernameField).toBeDisplayed();
  });

  // TC-009: Successful logout returns user to login page
  it('TC-009: Successful logout returns user to login page', async () => {
    await LoginPage.login('standard_user', 'secret_sauce');
    await waitForUrl('/inventory.html');
    await LoginPage.logout();
    expect(await browser.getUrl()).not.toContain('/inventory.html');
    await expect(LoginPage.loginButton).toBeDisplayed();
  });

});
