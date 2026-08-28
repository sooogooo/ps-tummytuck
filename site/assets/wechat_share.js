/* ============================================================
   微信公众号分享（JS-SDK 增强 + og:image 兜底）
   ------------------------------------------------------------
   两层策略：
   1) og:image 兜底（无需后端，默认生效）：
      所有页面 <head> 已带 Open Graph 标签，og:image 指向 logo。
      无论用户把链接发到聊天还是朋友圈，微信抓取网页即自动带出
      标题、描述与 logo 小图。这是"默认分享带图、logo 做小图标"
      最可靠、零后端的路径。
   2) JS-SDK 增强（微信内打开时精确控制分享卡片，需后端签名）：
      加载微信 jweixin-1.6.0.js，调用 wx.updateAppMessageShareData
      （发好友）与 wx.updateTimelineShareData（朋友圈）。
      签名数据由后端注入 window.WECHAT_SIGN = { appId, timestamp,
      nonceStr, signature }。缺省时本脚本记录提示并静默降级，
      网页仍可正常使用，分享走 og 兜底。
   ------------------------------------------------------------
   签名由后端生成（以当前 URL 计算 jsapi_ticket 签名），
   前端无法单独算出有效签名。本脚本只做前端接入与优雅降级。
   ============================================================ */

(function () {
  'use strict';

  var SDK_URL = 'https://res.wx.qq.com/open/js/jweixin-1.6.0.js';
  var SIGN_KEY = '__WECHAT_SIGN__';
  var LOG_PREFIX = '[wechat-share]';

  // 默认分享图：logo（圆形）。可用 window.WECHAT_SHARE_IMG 覆盖。
  function defaultImg() {
    return (window.WECHAT_SHARE_IMG || 'assets/img/share-card.png');
  }

  // 默认分享链接：当前页 URL（不带 hash）。
  function currentUrl() {
    return window.location.href.split('#')[0];
  }

  // 把相对路径转成绝对 URL（JS-SDK 需要绝对地址）
  function absolute(url) {
    if (!url) return url;
    if (/^(https?:)?\/\//i.test(url) || url.indexOf('data:') === 0) return url;
    try { return new URL(url, window.location.href).href; }
    catch (e) { return url; }
  }

  // 从 og 标签读取默认分享标题/描述。
  function fromOG(prop) {
    var el = document.querySelector('meta[property="' + prop + '"]');
    return el ? el.getAttribute('content') : '';
  }

  function title() {
    return fromOG('og:title') || document.title;
  }

  function desc() {
    return fromOG('og:description') || fromOG('description') || '';
  }

  function img() {
    // 优先 JS-SDK 分享图，其次 og:image，最后 logo；统一转绝对 URL
    var ogImg = fromOG('og:image');
    return absolute(window.WECHAT_SHARE_IMG || ogImg || defaultImg());
  }

  function sign() {
    try {
      var raw = window[window.WECHAT_SIGN_KEY || SIGN_KEY];
      if (!raw) return null;
      return (typeof raw === 'string') ? JSON.parse(raw) : raw;
    } catch (e) {
      return null;
    }
  }

  function loadSDK(cb) {
    if (window.wx && window.wx.config) { cb(); return; }
    var s = document.createElement('script');
    s.src = SDK_URL;
    s.onload = cb;
    s.onerror = function () { warn('JS-SDK 加载失败，使用 og:image 兜底。'); };
    document.head.appendChild(s);
  }

  function warn(msg) {
    try { console.warn(LOG_PREFIX, msg); } catch (e) {}
  }

  function init() {
    var cfg = sign();
    if (!cfg) {
      // 未注入后端签名：静默降级，出错误信息帮助调试，但不打扰用户。
      warn('未检测到后端签名 window.WECHAT_SIGN，分享将走 og:image 兜底。');
      return;
    }
    // 避免 SDK 校验失败导致 JS 报错：配置失败也静默。
    try {
      window.wx.config({
        debug: false,
        appId: cfg.appId,
        timestamp: cfg.timestamp,
        nonceStr: cfg.nonceStr,
        signature: cfg.signature,
        jsApiList: [
          'updateAppMessageShareData',
          'updateTimelineShareData',
          'onMenuShareAppMessage',
          'onMenuShareTimeline'
        ]
      });

      var shareData = {
        title: title(),
        desc: desc(),
        link: currentUrl(),
        imgUrl: img()
      };

      window.wx.ready(function () {
        // 发送给朋友
        if (window.wx.updateAppMessageShareData) {
          window.wx.updateAppMessageShareData(shareData);
        }
        // 分享到朋友圈
        if (window.wx.updateTimelineShareData) {
          window.wx.updateTimelineShareData({
            title: title(),
            link: currentUrl(),
            imgUrl: img()
          });
        }
        // 兼容旧基础库
        if (window.wx.onMenuShareAppMessage) {
          window.wx.onMenuShareAppMessage(shareData);
          window.wx.onMenuShareTimeline({
            title: title(),
            link: currentUrl(),
            imgUrl: img()
          });
        }
      });
    } catch (e) {
      warn('wx.config 配置异常：' + (e && e.message));
    }
  }

  // 暴露 refresh()：文章页动态更新 og:title 后调用，重新入参
  window.AMCWechatShare = {
    refresh: function () {
      var cfg = sign();
      if (!cfg || !window.wx || !window.wx.ready) return;
      try {
        window.wx.ready(function () {
          window.wx.updateAppMessageShareData({
            title: title(),
            desc: desc(),
            link: currentUrl(),
            imgUrl: img()
          });
          if (window.wx.updateTimelineShareData) {
            window.wx.updateTimelineShareData({
              title: title(),
              link: currentUrl(),
              imgUrl: img()
            });
          }
        });
      } catch (e) { warn('refresh 异常：' + (e && e.message)); }
    }
  };

  // 只在微信内置浏览器里才真正初始化 SDK；其他环境不加载 SDK，
  // 分享内容交给微信抓取 og:image。
  function isWeChat() {
    var ua = navigator.userAgent || '';
    return /MicroMessenger/i.test(ua);
  }

  if (!isWeChat()) {
    // 非微信环境：完全不加载 SDK，降低多余请求。og:image 由微信抓取。
    return;
  }

  loadSDK(init);
})();