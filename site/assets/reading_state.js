/* 已读状态管理：localStorage 持久化 + 列表标记 + 顶栏阅读统计 */

(function () {
  'use strict';

  var STORAGE_KEY = 'amc.reading.v1';
  var MAX_ENTRIES = 500;

  function ready(fn) {
    if (document.readyState !== 'loading') fn();
    else document.addEventListener('DOMContentLoaded', fn);
  }

  function loadAll() {
    try {
      var raw = localStorage.getItem(STORAGE_KEY);
      if (!raw) return {};
      var data = JSON.parse(raw);
      return (data && typeof data === 'object') ? data : {};
    } catch (e) { return {}; }
  }

  function saveAll(data) {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(data));
    } catch (e) { /* quota or disabled */ }
  }

  function markRead(file) {
    if (!file) return;
    var data = loadAll();
    if (data[file]) return;
    data[file] = Date.now();
    // 限制条目数（保留最新的 500 条）
    var keys = Object.keys(data);
    if (keys.length > MAX_ENTRIES) {
      keys.sort(function (a, b) { return data[a] - data[b]; });
      var remove = keys.slice(0, keys.length - MAX_ENTRIES);
      remove.forEach(function (k) { delete data[k]; });
    }
    saveAll(data);
  }

  function isRead(file) {
    var data = loadAll();
    return Boolean(data[file]);
  }

  function countRead() {
    return Object.keys(loadAll()).length;
  }

  function getRecent(n) {
    var data = loadAll();
    var keys = Object.keys(data);
    keys.sort(function (a, b) { return data[b] - data[a]; });
    return keys.slice(0, n || 5);
  }

  // 标记当前文章为已读
  ready(function () {
    var params = new URLSearchParams(window.location.search);
    var file = params.get('file');
    if (file) {
      // 等待正文加载后标记
      setTimeout(function () { markRead(file); }, 200);
    }
    // 给列表页的链接加"已读"视觉标记
    decorateLists();
    // 更新顶栏"已读 / 总数"统计
    updateStat();
  });

  function decorateLists() {
    var links = document.querySelectorAll('a[href*="article.html?file="]');
    links.forEach(function (a) {
      try {
        var u = new URL(a.href, window.location.href);
        var f = u.searchParams.get('file');
        if (f && isRead(f)) {
          a.classList.add('is-read');
          a.setAttribute('aria-label', a.getAttribute('aria-label') || a.textContent);
        }
      } catch (e) { /* invalid href */ }
    });
  }

  function updateStat() {
    var els = document.querySelectorAll('[data-read-stat]');
    if (!els.length) return;
    var read = countRead();
    var total = (window.ARTICLE_META || window.ARTICLES) ? Object.keys(window.ARTICLE_META || window.ARTICLES).length : 0;
    var text = read + ' / ' + total;
    els.forEach(function (el) { el.textContent = text; });
  }

  // 暴露 API 给 article.html 用于"标记已读"按钮
  window.AMCReading = {
    markRead: markRead,
    isRead: isRead,
    countRead: countRead,
    getRecent: getRecent,
  };
})();