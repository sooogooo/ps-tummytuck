/* 全局搜索：顶栏按钮触发，键盘可达，按分类分组展示 */

(function () {
  'use strict';

  function ready(fn) {
    if (document.readyState !== 'loading') fn();
    else document.addEventListener('DOMContentLoaded', fn);
  }

  function escapeHtml(s) {
    return String(s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }

  function highlight(text, q) {
    if (!q) return escapeHtml(text);
    var t = escapeHtml(text);
    var pat = q.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    return t.replace(new RegExp('(' + pat + ')', 'gi'), '<mark>$1</mark>');
  }

  // 抽取首个匹配位置的片段（前后各 50 字符）
  function snippet(text, q) {
    if (!q) return '';
    var lower = text.toLowerCase();
    var ql = q.toLowerCase();
    var idx = lower.indexOf(ql);
    if (idx < 0) return '';
    var start = Math.max(0, idx - 50);
    var end = Math.min(text.length, idx + ql.length + 50);
    var prefix = start > 0 ? '…' : '';
    var suffix = end < text.length ? '…' : '';
    return prefix + text.substring(start, end) + suffix;
  }

  function back(c) {
    return ({ A: 'a-popular.html', B: 'b-training.html', C: 'c-review.html' })[c] || 'index.html';
  }

  function categoryLabel(c) {
    return ({ A: '大众科普', B: '业务培训', C: '专业综述' })[c] || '其他';
  }

  ready(function () {
    // 找到顶栏并加入搜索按钮 + 版本徽章
    var headers = document.querySelectorAll('.site-header');
    headers.forEach(function (header) {
      if (header.querySelector('.search-btn')) return;
      // 版本徽章
      if (!header.querySelector('.version-badge')) {
        var badge = document.createElement('span');
        badge.className = 'version-badge';
        badge.setAttribute('aria-label', '版本 v1.3');
        badge.title = '版本 v1.3 · 内容更新截至 2026 春季';
        badge.textContent = 'v1.3';
        header.appendChild(badge);
      }
      var btn = document.createElement('button');
      btn.className = 'search-btn';
      btn.type = 'button';
      btn.setAttribute('aria-label', '搜索本站');
      btn.setAttribute('aria-haspopup', 'dialog');
      btn.innerHTML = '<span aria-hidden="true"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="6.5"></circle><line x1="16" y1="16" x2="20.5" y2="20.5"></line></svg></span><span class="search-btn__label">搜索</span><kbd class="search-btn__kbd" aria-hidden="true">Ctrl+K</kbd>';
      header.appendChild(btn);

      btn.addEventListener('click', function () { openOverlay(); });
    });

    if (!document.getElementById('global-search-overlay')) {
      buildOverlay();
    }

    // 全局快捷键：Ctrl/Cmd + K 切换搜索开关；/ 打开搜索
    document.addEventListener('keydown', function (e) {
      if ((e.metaKey || e.ctrlKey) && (e.key === 'k' || e.key === 'K')) {
        e.preventDefault();
        var overlay = document.getElementById('global-search-overlay');
        if (overlay && !overlay.hidden) closeOverlay();
        else openOverlay();
      } else if (e.key === '/' && !['INPUT', 'TEXTAREA'].includes(document.activeElement.tagName)) {
        e.preventDefault();
        openOverlay();
      }
    });
  });

  function buildOverlay() {
    var overlay = document.createElement('div');
    overlay.className = 'search-overlay';
    overlay.id = 'global-search-overlay';
    overlay.setAttribute('role', 'dialog');
    overlay.setAttribute('aria-modal', 'true');
    overlay.setAttribute('aria-label', '全局搜索');
    overlay.hidden = true;
    overlay.innerHTML =
      '<div class="search-overlay__backdrop" data-close></div>' +
      '<div class="search-overlay__panel" role="document" aria-labelledby="global-search-title">' +
      '  <h2 id="global-search-title" class="sr-only">全局搜索</h2>' +
      '  <div class="search-overlay__head">' +
      '    <label for="global-search-input" class="sr-only">关键词搜索本站内容</label>' +
      '    <span class="search-overlay__icon" aria-hidden="true"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="6.5"></circle><line x1="16" y1="16" x2="20.5" y2="20.5"></line></svg></span>' +
      '    <input id="global-search-input" class="search-overlay__input" type="search" placeholder="输入关键词，按 Esc 关闭" autocomplete="off" enterkeyhint="search" />' +
      '    <kbd class="search-overlay__kbd">Esc</kbd>' +
      '    <button type="button" class="search-overlay__close" data-close aria-label="关闭搜索">' +
      '      <span aria-hidden="true">×</span>' +
      '    </button>' +
      '  </div>' +
      '  <div class="search-overlay__body" id="global-search-results" aria-live="polite">' +
      '    <p class="search-overlay__hint">输入关键词搜索 89 篇文章</p>' +
      '  </div>' +
      '</div>';
    document.body.appendChild(overlay);

    overlay.addEventListener('click', function (e) {
      if (e.target.matches('[data-close]') || e.target.classList.contains('search-overlay__backdrop')) {
        closeOverlay();
      }
    });

    var input = overlay.querySelector('#global-search-input');
    input.addEventListener('input', function () { renderResults(input.value); });
    input.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') { closeOverlay(); }
      if (e.key === 'ArrowDown') { e.preventDefault(); focusNext(); }
      if (e.key === 'ArrowUp') { e.preventDefault(); focusPrev(); }
      if (e.key === 'Enter') {
        var active = overlay.querySelector('.search-result.is-focused');
        if (active) {
          window.location.href = active.href;
        }
      }
    });
  }

  function openOverlay() {
    var overlay = document.getElementById('global-search-overlay');
    if (!overlay) return;
    overlay.hidden = false;
    document.body.classList.add('search-open');
    var input = overlay.querySelector('#global-search-input');
    setTimeout(function () { input.focus(); input.select(); }, 30);
  }

  function closeOverlay() {
    var overlay = document.getElementById('global-search-overlay');
    if (!overlay) return;
    overlay.hidden = true;
    document.body.classList.remove('search-open');
    var btn = document.querySelector('.search-btn');
    if (btn) btn.focus();
  }

  function focusNext() {
    var overlay = document.getElementById('global-search-overlay');
    var list = overlay.querySelectorAll('.search-result');
    if (!list.length) return;
    var idx = Array.from(list).findIndex(function (x) { return x.classList.contains('is-focused'); });
    var next = list[Math.min(idx + 1, list.length - 1)];
    list.forEach(function (x) { x.classList.remove('is-focused'); });
    next.classList.add('is-focused');
    next.focus();
  }
  function focusPrev() {
    var overlay = document.getElementById('global-search-overlay');
    var list = overlay.querySelectorAll('.search-result');
    if (!list.length) return;
    var idx = Array.from(list).findIndex(function (x) { return x.classList.contains('is-focused'); });
    var prev = list[Math.max(idx - 1, 0)];
    list.forEach(function (x) { x.classList.remove('is-focused'); });
    prev.classList.add('is-focused');
    prev.focus();
  }

  function renderResults(q) {
    var body = document.getElementById('global-search-results');
    q = q.trim();
    if (!q) {
      body.innerHTML =
        '<p class="search-overlay__hint">输入关键词搜索 89 篇文章</p>' +
        '<p class="search-overlay__suggest">试试：' +
        '<button type="button" class="search-suggest" data-q="花生米">花生米</button>' +
        '<button type="button" class="search-suggest" data-q="助听">助听</button>' +
        '<button type="button" class="search-suggest" data-q="肋软骨">肋软骨</button>' +
        '<button type="button" class="search-suggest" data-q="红旗">红旗</button>' +
        '<button type="button" class="search-suggest" data-q="烧伤">烧伤</button>' +
        '</p>';
      body.querySelectorAll('.search-suggest').forEach(function (b) {
        b.addEventListener('click', function () {
          var input = document.getElementById('global-search-input');
          input.value = b.dataset.q;
          renderResults(b.dataset.q);
        });
      });
      return;
    }
    var ql = q.toLowerCase();
    var scored = (window.GLOBAL_INDEX || []).map(function (e) {
      var score = 0;
      var title = e.title.toLowerCase();
      var text = e.text.toLowerCase();
      var file = e.file.toLowerCase();
      if (title.indexOf(ql) >= 0) score += 10;
      if (file.indexOf(ql) >= 0) score += 5;
      if (text.indexOf(ql) >= 0) score += 1;
      // 模糊匹配：字符重叠
      var hits = 0;
      for (var i = 0; i < ql.length; i++) {
        if (text.indexOf(ql[i]) >= 0) hits++;
      }
      score += hits * 0.1;
      return { e: e, score: score };
    }).filter(function (x) { return x.score > 0; })
      .sort(function (a, b) { return b.score - a.score; })
      .slice(0, 30);

    if (!scored.length) {
      body.innerHTML = '<p class="search-overlay__hint">未找到匹配文章。试试"花生米"、"助听"、"肋软骨"。</p>';
      return;
    }

    var groups = { A: [], B: [], C: [] };
    scored.forEach(function (s) {
      var c = s.e.cat;
      if (groups[c]) groups[c].push(s);
      else groups.A.push(s);  // 顶层配套归入 A
    });

    var html = '<p class="search-overlay__count">匹配到 ' + scored.length + ' 篇</p>';
    ['A', 'B', 'C'].forEach(function (c) {
      if (!groups[c].length) return;
      html += '<div class="search-group"><p class="search-group__label">' + categoryLabel(c) + '</p><ul class="search-group__list">';
      groups[c].forEach(function (s) {
        var snip = snippet(s.e.text || '', q);
        var snipHtml = snip ? '<span class="search-result__snip">' + highlight(snip, q) + '</span>' : '';
        html += '<li><a class="search-result" href="article.html?file=' + encodeURIComponent(s.e.file) + '&q=' + encodeURIComponent(q) + '">' +
                '<span class="search-result__title">' + highlight(s.e.title, q) + '</span>' +
                snipHtml +
                '<span class="search-result__cat">' + categoryLabel(s.e.cat) + '</span></a></li>';
      });
      html += '</ul></div>';
    });

    body.innerHTML = html;
  }
})();