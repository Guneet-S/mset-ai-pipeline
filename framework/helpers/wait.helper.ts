// wait.helper.ts — shared wait utilities for element synchronisation
// Import these in page objects and specs instead of writing raw browser.waitUntil() calls

export async function waitForElement(
  element: WebdriverIO.Element,
  timeout: number = 8000
): Promise<void> {
  await element.waitForDisplayed({ timeout });
}

export async function waitForText(
  element: WebdriverIO.Element,
  text: string,
  timeout: number = 8000
): Promise<void> {
  await browser.waitUntil(
    async () => (await element.getText()).includes(text),
    { timeout, timeoutMsg: `Expected element to contain text: "${text}"` }
  );
}

export async function waitForUrl(
  urlFragment: string,
  timeout: number = 8000
): Promise<void> {
  await browser.waitUntil(
    async () => (await browser.getUrl()).includes(urlFragment),
    { timeout, timeoutMsg: `Expected URL to contain: "${urlFragment}"` }
  );
}

export async function waitForClickable(
  element: WebdriverIO.Element,
  timeout: number = 5000
): Promise<void> {
  await element.waitForClickable({ timeout });
}
