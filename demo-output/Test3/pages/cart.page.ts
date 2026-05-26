// Extended from existing framework — see framework/pages/base.page.ts
import { BasePage } from '../../../../framework/pages/base.page';
import { Selectors } from '../../../../framework/selectors/app.selectors';
import { waitForElement, waitForUrl } from '../../../../framework/helpers/wait.helper';

class CartPage extends BasePage {

  get cartBadge()             { return $(Selectors.CART_BADGE); }
  get cartLink()              { return $(Selectors.CART_LINK); }
  get cartItems()             { return $$(Selectors.CART_ITEM); }
  get cartItemNames()         { return $$(Selectors.CART_ITEM_NAME); }
  get cartItemPrices()        { return $$(Selectors.CART_ITEM_PRICE); }
  get addBackpackBtn()        { return $(Selectors.ADD_TO_CART_BACKPACK); }
  get addBikeLightBtn()       { return $(Selectors.ADD_TO_CART_BIKE_LIGHT); }
  get addBoltTshirtBtn()      { return $(Selectors.ADD_TO_CART_BOLT_TSHIRT); }
  get removeBackpackBtn()     { return $(Selectors.REMOVE_BACKPACK); }
  get removeBikeLightBtn()    { return $(Selectors.REMOVE_BIKE_LIGHT); }
  get continueShoppingBtn()   { return $(Selectors.CONTINUE_SHOPPING); }
  get backpackDetailTitle()   { return $(`[data-test="inventory-item-name"]*=Sauce Labs Backpack`); }
  get addToCartDetailBtn()    { return $(Selectors.ADD_TO_CART_DETAIL); }
  get backToProductsBtn()     { return $(Selectors.BACK_TO_PRODUCTS); }
  get productList()           { return $(Selectors.PRODUCT_LIST); }

  async addToCartBySlug(slug: string): Promise<void> {
    const btn = await $(`[data-test="add-to-cart-${slug}"]`);
    await waitForElement(btn);
    await btn.click();
  }

  async removeFromCartBySlug(slug: string): Promise<void> {
    const btn = await $(`[data-test="remove-${slug}"]`);
    await waitForElement(btn);
    await btn.click();
  }

  async getBadgeCount(): Promise<string> {
    await waitForElement(this.cartBadge);
    return this.cartBadge.getText();
  }

  async openCart(): Promise<void> {
    await this.cartLink.click();
    await waitForUrl('/cart.html');
  }

  async getCartItemNames(): Promise<string[]> {
    const names = await this.cartItemNames;
    return Promise.all(names.map(n => n.getText()));
  }

  async clickProductByName(name: string): Promise<void> {
    const link = await $(`[data-test="inventory-item-name"]*=${name}`);
    await waitForElement(link);
    await link.click();
  }

  async addToCartFromDetail(): Promise<void> {
    await waitForElement(this.addToCartDetailBtn);
    await this.addToCartDetailBtn.click();
  }

  async goBackToProducts(): Promise<void> {
    await waitForElement(this.backToProductsBtn);
    await this.backToProductsBtn.click();
    await waitForElement(this.productList);
  }
}

export default new CartPage();
