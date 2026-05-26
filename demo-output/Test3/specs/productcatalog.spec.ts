import LoginPage from '../pages/login.page';
import CatalogPage from '../pages/catalog.page';
import { waitForUrl } from '../../../../framework/helpers/wait.helper';

describe('Product Catalog', () => {

  beforeEach(async () => {
    await LoginPage.open();
    await LoginPage.login('standard_user', 'secret_sauce');
    await waitForUrl('/inventory.html');
  });

  // TC-010: Product catalog loads all items after login
  it('TC-010: Product catalog loads all items after login', async () => {
    await expect(CatalogPage.productList).toBeDisplayed();
    const count = await CatalogPage.getProductCount();
    expect(count).toBe(6);
  });

  // TC-011: Sort products by Name A to Z
  it('TC-011: Sort products by Name A to Z', async () => {
    await CatalogPage.sortBy('az');
    const names = await CatalogPage.getProductNames();
    expect(names[0]).toBe('Sauce Labs Backpack');
    expect(names[names.length - 1]).toBe('Test.allTheThings() T-Shirt (Red)');
    expect(names).toEqual([...names].sort());
  });

  // TC-012: Sort products by Name Z to A
  it('TC-012: Sort products by Name Z to A', async () => {
    await CatalogPage.sortBy('za');
    const names = await CatalogPage.getProductNames();
    expect(names[0]).toBe('Test.allTheThings() T-Shirt (Red)');
    expect(names[names.length - 1]).toBe('Sauce Labs Backpack');
    expect(names).toEqual([...names].sort().reverse());
  });

  // TC-013: Sort products by Price Low to High
  it('TC-013: Sort products by Price Low to High', async () => {
    await CatalogPage.sortBy('lohi');
    const firstPrice = await CatalogPage.getFirstProductPrice();
    expect(firstPrice).toBe(7.99);
  });

  // TC-014: Sort products by Price High to Low
  it('TC-014: Sort products by Price High to Low', async () => {
    await CatalogPage.sortBy('hilo');
    const firstPrice = await CatalogPage.getFirstProductPrice();
    expect(firstPrice).toBe(49.99);
  });

  // TC-015: Product detail page opens with correct information
  it('TC-015: Product detail page opens with correct information', async () => {
    await CatalogPage.clickProductByName('Sauce Labs Backpack');
    await expect(CatalogPage.itemDetailName).toBeDisplayed();
    await expect(CatalogPage.itemDetailName).toHaveText('Sauce Labs Backpack');
    await expect(CatalogPage.itemDetailPrice).toHaveText('$29.99');
  });

  // TC-016: Back button on product detail returns to catalog
  it('TC-016: Back button on product detail returns to catalog', async () => {
    await CatalogPage.clickProductByName('Sauce Labs Backpack');
    await expect(CatalogPage.itemDetailName).toBeDisplayed();
    await CatalogPage.goBackToProducts();
    await expect(CatalogPage.productList).toBeDisplayed();
    const count = await CatalogPage.getProductCount();
    expect(count).toBe(6);
  });

});
