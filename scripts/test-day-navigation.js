#!/usr/bin/env node

const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');

const source = fs.readFileSync('assets/js/course.js', 'utf8');
const css = fs.readFileSync('assets/css/course.css', 'utf8');
const match = source.match(/function goDay\(n\) \{[\s\S]*?\n\}\n\nfunction jumpTo/);

assert.ok(match, 'goDay function should exist');
assert.match(css, /\.day-section\.active\s*\{\s*display:\s*block;/, 'active days must be visible by CSS');

function element(id, classNames, display = '') {
  const classes = new Set(classNames);
  return {
    id,
    classList: {
      add: value => classes.add(value),
      remove: value => classes.delete(value),
      contains: value => classes.has(value),
    },
    style: {
      display,
      removeProperty(property) { if (property === 'display') this.display = ''; },
    },
    setAttribute() {},
  };
}

const day118 = element('day-118', ['day-section', 'active']);
const day119 = element('day-119', ['day-section'], 'none');
const pills = [element('pill-118', ['day-pill', 'active']), element('pill-119', ['day-pill'])];
const sidebar = [element('sb-118', ['sb-item', 'active']), element('sb-119', ['sb-item'])];
const byId = Object.fromEntries([day118, day119, ...pills, ...sidebar].map(item => [item.id, item]));

const document = {
  querySelectorAll(selector) {
    if (selector === '.day-section') return [day118, day119];
    if (selector === '.day-pill') return pills;
    if (selector === '.sb-item') return sidebar;
    return [];
  },
  getElementById: id => byId[id] || null,
  documentElement: { scrollTop: 0 },
  body: { scrollTop: 0 },
};

// Run in the same context so goDay uses the mocked DOM.
const context = { document, window: { scrollTo() {} }, renderMermaid() {} };
vm.runInNewContext(`${match[0].replace(/\nfunction jumpTo$/, '')}\ngoDay(119);`, context);

assert.equal(day119.style.display, '', 'switching to a day must clear its inline display:none');
assert.ok(day119.classList.contains('active'), 'selected day must become active');
assert.ok(!day118.classList.contains('active'), 'previous day must become inactive');

const affectedWeeks = fs.readdirSync('pages/weeks')
  .filter(file => /^week\d+\.html$/.test(file))
  .filter(file => /class="day-section" id="day-\d+" style="display:none;"/.test(fs.readFileSync(`pages/weeks/${file}`, 'utf8')));
assert.ok(affectedWeeks.length > 0, 'fixture should cover week pages with inline-hidden days');
affectedWeeks.forEach(file => {
  const page = fs.readFileSync(`pages/weeks/${file}`, 'utf8');
  assert.match(page, /src="\.\.\/\.\.\/assets\/js\/course\.js"/, `${file} must use the shared navigation fix`);
});
console.log('Day navigation regression check passed.');
