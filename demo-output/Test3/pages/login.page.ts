// Extended from existing framework — see framework/pages/base.page.ts
import { BasePage } from '../../../../framework/pages/base.page';
import { Selectors } from '../../../../framework/selectors/app.selectors';
import { waitForElement, waitForUrl } from '../../../../framework/helpers/wait.helper';

class LoginPage extends BasePage {

  get usernameField()  { return $(Selectors.USERNAME); }
  get passwordField()  { return $(Selectors.PASSWORD); }
  get loginButton()    { return $(Selectors.LOGIN_BTN); }
  get errorMessage()   { return $(Selectors.ERROR_MSG); }
  get errorCloseBtn()  { return $(Selectors.ERROR_CLOSE); }
  get burgerMenu()     { return $(Selectors.BURGER_MENU); }
  get logoutLink()     { return $(Selectors.LOGOUT_LINK); }

  async open(): Promise<void> {
    await super.open('/');
    await waitForElement(this.loginButton);
  }

  async login(username: string, password: string): Promise<void> {
    if (username) {
      await this.usernameField.setValue(username);
    }
    if (password) {
      await this.passwordField.setValue(password);
    }
    await this.loginButton.click();
  }

  async dismissError(): Promise<void> {
    await waitForElement(this.errorCloseBtn);
    await this.errorCloseBtn.click();
  }

  async logout(): Promise<void> {
    await this.burgerMenu.click();
    await waitForElement(this.logoutLink);
    await this.logoutLink.click();
    await waitForUrl('/');
  }
}

export default new LoginPage();
