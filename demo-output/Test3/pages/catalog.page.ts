// Extended from existing framework — see framework/pages/base.page.ts
import { BasePage } from '../../../../framework/pages/base.page';
import { Selectors } from '../../../../framework/selectors/app.selectors';
import { waitForElement } from '../../../../framework/helpers/wait.helper';

class CatalogPage extends BasePage {

  get productList()          { return $(Selectors.PRODUCT_LIST); }
  get sortDropdown()         { return $(Selectors.SORT_DROPDOWN); }
  get productTitles()        { return $$(Selectors.PRODUCT_TITLE); }
  get productItems()         { return $$(Selectors.PRODUCT_ITEM); }
  get cartBadge()            { return $(Selectors.CART_BADGE); }
  get cartLink()             { return $(Selectors.CART_LINK); }
  get backpackTitle()        { return $(`${Selectors.ITEM_DETAIL_NAME}=Sauce Labs Backpack`); }
  get backToproductsBtn()    { return $(Selectors.BACK_TO_PRODUCTS); }
  get itemDetailName()       { return $(Selectors.ITEM_DETAIL_NAME); }
  get itemDetailPrice()      { return $(Selectors.ITEM_DETAIL_PRICE); }

  async open(): Promise<void> {
    await super.open('/inventory.html');
    await waitForElement(this.productList);
  }

  async sortBy(option: 'az' | 'za' | 'lohi' | 'hilo'): Promise<void> {
    await this.sortDropdown.selectByAttribute('value', option);
  }

  async getProductCount(): Promise<number> {
    return (await this.productTitles).length;
  }

  async getProductNames(): Promise<string[]> {
    const titles = await this.productTitles;
    return Promise.all(titles.map(t => t.getText()));
  }

  async getFirstProductPrice(): Promise<number> {
    const prices = await $$(Selectors.PRODUCT_PRICE);
    const text = await prices[0].getText();
    return parseFloat(text.replace('$', ''));
  }

  async clickProductByName(name: string): Promise<void> {
    const link = await $(`[data-test="inventory-item-name"]*=${name}`);
    await waitForElement(link);
    await link.click();
  }

  async goBackToProducts(): Promise<void> {
    await waitForElement(this.backToproductsBtn);
    await this.backToproductsBtn.click();
    await waitForElement(this.productList);
  }
}

export default new CatalogPage();
