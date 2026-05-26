// app.selectors.ts — centralised selector constants for Sauce Labs Demo App
// All page objects must import selectors from here — never hardcode selectors inline

export const Selectors = {
  // Authentication
  USERNAME:         '[data-test="username"]',
  PASSWORD:         '[data-test="password"]',
  LOGIN_BTN:        '[data-test="login-button"]',
  ERROR_MSG:        '[data-test="error"]',

  // Product catalog
  PRODUCT_LIST:     '[data-test="inventory-container"]',
  PRODUCT_TITLE:    '[data-test="inventory-item-name"]',
  SORT_DROPDOWN:    '[data-test="product-sort-container"]',
  ADD_TO_CART:      '[data-test="add-to-cart-sauce-labs-backpack"]',

  // Cart
  CART_BADGE:       '[data-test="shopping-cart-badge"]',
  CART_LINK:        '[data-test="shopping-cart-link"]',
  CART_ITEM:        '[data-test="cart-item"]',
  REMOVE_BTN:       '[data-test="remove-sauce-labs-backpack"]',

  // Checkout
  CHECKOUT_BTN:     '[data-test="checkout"]',
  FIRST_NAME:       '[data-test="firstName"]',
  LAST_NAME:        '[data-test="lastName"]',
  POSTAL_CODE:      '[data-test="postalCode"]',
  CONTINUE_BTN:     '[data-test="continue"]',
  FINISH_BTN:       '[data-test="finish"]',
  ORDER_CONFIRM:    '[data-test="checkout-complete-container"]',
} as const;
