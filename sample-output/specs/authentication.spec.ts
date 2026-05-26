import LoginPage from '../pages/login.page';

describe('Authentication', () => {

  beforeEach(async () => {
    await LoginPage.open();
  });

  it('TC-001: Valid login with correct credentials', async () => {
    await LoginPage.login('standard_user', 'secret_sauce');
    await expect(LoginPage.inventoryContainer).toBeDisplayed();
    await expect(browser).toHaveUrl(expect.stringContaining('/inventory.html'));
  });

  it('TC-002: Login rejected with invalid username', async () => {
    await LoginPage.login('wrong_user', 'secret_sauce');
    await expect(LoginPage.errorMessage).toBeDisplayed();
    await expect(LoginPage.errorMessage).toHaveText(
      expect.stringContaining('Username and password do not match any user in this service')
    );
  });

  it('TC-003: Login rejected with invalid password', async () => {
    await LoginPage.login('standard_user', 'wrong_password');
    await expect(LoginPage.errorMessage).toBeDisplayed();
    await expect(LoginPage.errorMessage).toHaveText(
      expect.stringContaining('Username and password do not match any user in this service')
    );
  });

  it('TC-004: Locked-out user cannot log in', async () => {
    await LoginPage.login('locked_out_user', 'secret_sauce');
    await expect(LoginPage.errorMessage).toBeDisplayed();
    await expect(LoginPage.errorMessage).toHaveText(
      expect.stringContaining('Sorry, this user has been locked out')
    );
  });

  it('TC-005: Login rejected when both fields are empty', async () => {
    await LoginPage.loginButton.click();
    await expect(LoginPage.errorMessage).toBeDisplayed();
    await expect(LoginPage.errorMessage).toHaveText(
      expect.stringContaining('Username is required')
    );
  });

  it('TC-006: Login rejected when only username is provided', async () => {
    await LoginPage.usernameField.setValue('standard_user');
    await LoginPage.loginButton.click();
    await expect(LoginPage.errorMessage).toBeDisplayed();
    await expect(LoginPage.errorMessage).toHaveText(
      expect.stringContaining('Password is required')
    );
  });

  it('TC-007: Login page loads correctly on navigation', async () => {
    await expect(browser).toHaveTitle('Swag Labs');
    await expect(LoginPage.usernameField).toBeDisplayed();
    await expect(LoginPage.passwordField).toBeDisplayed();
    await expect(LoginPage.loginButton).toBeDisplayed();
    await expect(LoginPage.loginButton).toBeEnabled();
    await expect(browser).toHaveUrl('https://www.saucedemo.com/');
  });

});
