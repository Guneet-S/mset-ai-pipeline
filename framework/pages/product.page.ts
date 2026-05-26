// ProductPage — existing page object for the product catalog screen
// Written by QA team. AutomationAgent must follow this pattern when generating new pages.

import { BasePage } from './base.page';
import { Selectors } from '../selectors/app.selectors';
import { waitForElement, waitForUrl } from '../helpers/wait.helper';

class ProductPage extends BasePage {

  get productList()    { return $(Selectors.PRODUCT_LIST); }
  get sortDropdown()   { return $(Selectors.SORT_DROPDOWN); }
  get productTitles()  { return $$(Selectors.PRODUCT_TITLE); }
  get addToCartBtn()   { return $(Selectors.ADD_TO_CART); }
  get cartBadge()      { return $(Selectors.CART_BADGE); }
  get cartLink()       { return $(Selectors.CART_LINK); }

  async open(): Promise<void> {
    await super.open('/inventory.html');
    await waitForElement(this.productList);
  }

  async sortBy(option: 'az' | 'za' | 'lohi' | 'hilo'): Promise<void> {
    await this.sortDropdown.selectByAttribute('value', option);
  }

  async addFirstProductToCart(): Promise<void> {
    await waitForElement(this.addToCartBtn);
    await this.addToCartBtn.click();
  }

  async goToCart(): Promise<void> {
    await this.cartLink.click();
    await waitForUrl('/cart.html');
  }

  async getProductCount(): Promise<number> {
    return (await this.productTitles).length;
  }
}

export default new ProductPage();
