const fs = require('fs');
const code = fs.readFileSync('js/i18n.js', 'utf8');
const html = fs.readFileSync('index.html', 'utf8');

// Simple DOM element store
const elements = {};
const idRegex = /id=["']([^"']+)["']/g;
let m;
while ((m = idRegex.exec(html)) !== null) {
  const id = m[1];
  elements[id] = { id, textContent: '', innerHTML: '', classList: { add: () => {}, remove: () => {}, toggle: () => {} }, setAttribute: () => {}, addEventListener: () => {} };
}

const vm = require('vm');
const windowObj = { dispatchEvent: () => {} };
const documentObj = {
  querySelectorAll: (sel) => [],
  querySelector: (sel) => ({ setAttribute: () => {}, classList: { remove: () => {} }, addEventListener: () => {} }),
  getElementById: (id) => elements[id] || null,
  documentElement: { lang: 'en' },
  title: '',
  readyState: 'complete',
  addEventListener: () => {}
};
const context = {
  window: windowObj,
  document: documentObj,
  localStorage: { getItem: () => 'en', setItem: () => {} },
  setTimeout: (fn) => fn(),
  requestIdleCallback: (fn) => fn(),
  CustomEvent: class {},
  fetch: () => Promise.resolve({ ok: false })
};
vm.createContext(context);
vm.runInContext(code, context);

console.log('=== TEST GERMAN (DE) SWITCH ===');
context.switchLanguage('de');
console.log('heroBadge:', elements.heroBadge?.textContent);
console.log('homeProductsHeading:', elements.homeProductsHeading?.textContent);
console.log('prodGeoTitle:', elements.prodGeoTitle?.textContent);
console.log('faqHeading:', elements.faqHeading?.textContent);
console.log('faq1q:', elements.faq1q?.textContent);
console.log('heroCta:', elements.heroCta?.textContent);
console.log('heroContact:', elements.heroContact?.textContent);

console.log('\n=== TEST POLISH (PL) SWITCH ===');
context.switchLanguage('pl');
console.log('heroBadge:', elements.heroBadge?.textContent);
console.log('homeProductsHeading:', elements.homeProductsHeading?.textContent);
console.log('prodGeoTitle:', elements.prodGeoTitle?.textContent);
console.log('faqHeading:', elements.faqHeading?.textContent);
console.log('faq1q:', elements.faq1q?.textContent);
console.log('heroCta:', elements.heroCta?.textContent);
console.log('heroContact:', elements.heroContact?.textContent);

console.log('\n=== TEST SLOVAK (SK) SWITCH ===');
context.switchLanguage('sk');
console.log('heroBadge:', elements.heroBadge?.textContent);
console.log('homeProductsHeading:', elements.homeProductsHeading?.textContent);
console.log('prodGeoTitle:', elements.prodGeoTitle?.textContent);
console.log('faqHeading:', elements.faqHeading?.textContent);
console.log('faq1q:', elements.faq1q?.textContent);
console.log('heroCta:', elements.heroCta?.textContent);
console.log('heroContact:', elements.heroContact?.textContent);
