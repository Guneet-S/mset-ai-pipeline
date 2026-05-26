import LoginPage from '../pages/login.page';
import CartPage from '../pages/cart.page';
import { waitForUrl } from '../../../../framework/helpers/wait.helper';

describe('Cart', () => {

  beforeEach(async () => {
    await LoginPage.open();
    await LoginPage.login('standard_user', 'secret_sauce');
    await waitForUrl('/inventory.html');
  });

  // TC-018: Add a single item to the cart from catalog
  it('TC-018: Add a single item to the cart from catalog', async () => {
    await CartPage.addToCartBySlug('sauce-labs-backpack');
    const badge = await CartPage.getBadgeCount();
    expect(badge).toBe('1');
    await expect(CartPage.removeBackpackBtn).toBeDisplayed();
  });

  // TC-019: Add multiple items to the cart and verify badge count
  it('TC-019: Add multiple items to the cart and verify badge count', async () => {
    await CartPage.addToCartBySlug('sauce-labs-backpack');
    await CartPage.addToCartBySlug('sauce-labs-bike-light');
    await CartPage.addToCartBySlug('sauce-labs-bolt-t-shirt');
    const badge = await CartPage.getBadgeCount();
    expect(badge).toBe('3');
  });

  // TC-020: Cart badge increments correctly with each added item
  it('TC-020: Cart badge increments correctly with each added item', async () => {
    await CartPage.addToCartBySlug('sauce-labs-backpack');
    expect(await CartPage.getBadgeCount()).toBe('1');

    await CartPage.addToCartBySlug('sauce-labs-bike-light');
    expect(await CartPage.getBadgeCount()).toBe('2');

    await CartPage.addToCartBySlug('sauce-labs-bolt-t-shirt');
    expect(await CartPage.getBadgeCount()).toBe('3');
  });

  // TC-021: Remove an item from the catalog page updates badge
  it('TC-021: Remove an item from the catalog page updates badge', async () => {
    await CartPage.addToCartBySlug('sauce-labs-backpack');
    expect(await CartPage.getBadgeCount()).toBe('1');

    await CartPage.removeFromCartBySlug('sauce-labs-backpack');
    await expect(CartPage.cartBadge).not.toBeDisplayed();
    await expect(CartPage.addBackpackBtn).toBeDisplayed();
  });

  // TC-022: Cart page shows correct items and totals
  it('TC-022: Cart page shows correct items and totals', async () => {
    await CartPage.addToCartBySlug('sauce-labs-backpack');
    await CartPage.addToCartBySlug('sauce-labs-bike-light');
    expect(await CartPage.getBadgeCount()).toBe('2');

    await CartPage.openCart();
    const names = await CartPage.getCartItemNames();
    expect(names).toContain('Sauce Labs Backpack');
    expect(names).toContain('Sauce Labs Bike Light');
    expect(names).toHaveLength(2);
  });

  // TC-024: Add to cart from product detail page updates catalog button state
  it('TC-024: Add to cart from product detail page updates catalog button state', async () => {
    await CartPage.clickProductByName('Sauce Labs Backpack');
    await CartPage.addToCartFromDetail();
    expect(await CartPage.getBadgeCount()).toBe('1');

    await CartPage.goBackToProducts();
    await expect(CartPage.removeBackpackBtn).toBeDisplayed();
    expect(await CartPage.getBadgeCount()).toBe('1');
  });

});
