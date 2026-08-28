/* 首页"继续阅读"区块：展示用户最近 3 篇已读 */

(function () {
  'use strict';

  function ready(fn) {
    if (document.readyState !== 'loading') fn();
    else document.addEventListener('DOMContentLoaded', fn);
  }

  function titleOf(file) {
    var meta = (window.ARTICLE_META || window.ARTICLES || {})[file];
    if (meta && meta.title) return meta.title;
    // 退化：从文件名推导
    var name = file.replace(/\.md$/, '');
    for (var i = 0; i < 5; i++) {
      if (name.indexOf('A' + (i + 1) + '-') === 0) {
        return name.split('-').slice(1).join(' ').slice(0, 24);
      }
    }
    return name;
  }

  ready(function () {
    var section = document.getElementById('resume-section');
    var list = document.getElementById('resume-list');
    var clearBtn = document.getElementById('clear-read-btn');
    if (!section || !list || !window.AMCReading) return;

    function render() {
      var recent = window.AMCReading.getRecent(3);
      section.hidden = false;
      if (!recent.length) {
        if (clearBtn) clearBtn.hidden = true;
        list.innerHTML =
          '<li class="resume__empty">' +
          '  <p class="resume__empty-title">尚无阅读记录</p>' +
          '  <p class="resume__empty-hint">从一篇 A 档主题开始，例如 ' +
          '  <a href="article.html?file=A1-新生儿耳朵像花生米.md">A1 新生儿耳朵像花生米</a>' +
          '  </p>' +
          '</li>';
        return;
      }
      if (clearBtn) clearBtn.hidden = false;
      list.innerHTML = '';
      recent.forEach(function (file) {
        var li = document.createElement('li');
        var a = document.createElement('a');
        a.href = 'article.html?file=' + encodeURIComponent(file);
        a.innerHTML =
          '<span class="resume__title">' + titleOf(file) + '</span>' +
          '<span class="resume__hint">继续阅读</span>';
        li.appendChild(a);
        list.appendChild(li);
      });
    }

    if (clearBtn) {
      clearBtn.addEventListener('click', function () {
        if (!confirm('确定要清除本机所有已读记录吗？此操作不可撤销。')) return;
        try {
          localStorage.removeItem('amc.reading.v1');
        } catch (e) { /* noop */ }
        render();
        // 触发一次 updateStat 重读
        var statEl = document.querySelector('[data-read-stat]');
        if (statEl) statEl.textContent = '0 / ' + Object.keys(window.ARTICLE_META || window.ARTICLES || {}).length;
        // 通知所有列表页装饰函数重读
        document.querySelectorAll('.is-read').forEach(function (a) { a.classList.remove('is-read'); });
      });
    }

    render();
  });
})();