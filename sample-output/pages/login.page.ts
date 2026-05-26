class LoginPage {
  get usernameField()       { return $('[data-test="username"]'); }
  get passwordField()       { return $('[data-test="password"]'); }
  get loginButton()         { return $('[data-test="login-button"]'); }
  get errorMessage()        { return $('[data-test="error"]'); }
  get inventoryContainer()  { return $('[data-test="inventory-container"]'); }

  async open() {
    await browser.url('https://www.saucedemo.com');
  }

  async login(username: string, password: string) {
    await this.usernameField.setValue(username);
    await this.passwordField.setValue(password);
    await this.loginButton.click();
  }
}

export default new LoginPage();
