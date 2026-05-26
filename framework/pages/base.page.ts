// BasePage — parent class for all page objects in this framework
// Every page object must extend this class

export class BasePage {

  async open(path: string = '/'): Promise<void> {
    await browser.url(path);
  }

  async getTitle(): Promise<string> {
    return browser.getTitle();
  }

  async waitForDisplayed(element: WebdriverIO.Element, timeout: number = 8000): Promise<void> {
    await element.waitForDisplayed({ timeout });
  }

  async waitForEnabled(element: WebdriverIO.Element, timeout: number = 5000): Promise<void> {
    await element.waitForEnabled({ timeout });
  }

  async scrollToElement(element: WebdriverIO.Element): Promise<void> {
    await element.scrollIntoView();
  }

  async getUrl(): Promise<string> {
    return browser.getUrl();
  }
}
