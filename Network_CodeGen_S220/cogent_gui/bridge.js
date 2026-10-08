(function () {
  "use strict";
  var names = window.__cogentObjects || [];
  var ready = false, queue = [], objects = {};

  function callSlot(objName, method, args) {
    var target = objects[objName];
    if (!target || typeof target[method] !== "function") {
      console.error("cogent: unknown slot " + objName + "." + method);
      return;
    }
    target[method].apply(target, args);
  }

  names.forEach(function (objName) {
    window[objName] = new Proxy({}, {
      get: function (_t, method) {
        return function () {
          var args = Array.prototype.slice.call(arguments);
          if (ready) { callSlot(objName, method, args); } else { queue.push([objName, method, args]); }
        };
      }
    });
  });

  new QWebChannel(qt.webChannelTransport, function (channel) {
    objects = channel.objects;
    ready = true;
    var pending = queue; queue = [];
    pending.forEach(function (c) { callSlot(c[0], c[1], c[2]); });
    window.__cogentReady = true;
  });

  function resolveSlot(path) {
    var parts = String(path || "").split(".");
    if (parts.length !== 2 || names.indexOf(parts[0]) < 0) {
      console.error("cogent: not a bound slot: " + path);
      return null;
    }
    return function () { window[parts[0]][parts[1]].apply(null, arguments); };
  }

  function linkBind(e) {
    e.preventDefault();
    var anchor = e.currentTarget;
    if (anchor.getAttribute("data-bind") !== "true") { return true; }
    var slot = resolveSlot(anchor.getAttribute("href"));
    if (!slot) { return false; }
    var params = anchor.getAttribute("data-params");
    if (params !== null) { slot(params); } else { slot(); }
    return false;
  }

  // QtWebKit (Qt 4.8), which the legacy tool ran on, returned checked ? "on" : "" for a
  // checkbox/radio without a value attribute; Chromium always returns "on". The saved
  // .data files (and therefore which messages/signals are enabled) depend on the old rule.
  function legacyValue(input) {
    if ((input.type === "checkbox" || input.type === "radio") && !input.hasAttribute("value")) {
      return input.checked ? "on" : "";
    }
    return input.value;
  }

  function formBind(e) {
    e.preventDefault();
    var form = e.currentTarget;
    if (form.getAttribute("data-bind") !== "true") { return true; }
    var slot = resolveSlot(form.getAttribute("action"));
    if (!slot) { return false; }
    var formdata = {};
    for (var i = 0, ii = form.length; i < ii; ++i) {
      var input = form[i];
      if (input.name && input.type !== "file") { formdata[input.name] = legacyValue(input); }
    }
    var params = form.getAttribute("data-params");
    if (params !== null) { slot(JSON.stringify(formdata), params); } else { slot(JSON.stringify(formdata)); }
    return false;
  }

  function bindAll() {
    var anchors = document.getElementsByTagName("a");
    for (var i = anchors.length - 1; i >= 0; i--) {
      if (!anchors[i].classList.contains("htmlpy-activated")) {
        anchors[i].onclick = linkBind;
        anchors[i].classList.add("htmlpy-activated");
      }
    }
    var forms = document.getElementsByTagName("form");
    for (var f = forms.length - 1; f >= 0; f--) {
      if (!forms[f].classList.contains("htmlpy-activated")) {
        forms[f].onsubmit = formBind;
        forms[f].classList.add("htmlpy-activated");
      }
    }
  }

  document.addEventListener("DOMContentLoaded", function () {
    bindAll();
    new MutationObserver(bindAll).observe(document.body, { childList: true, subtree: true });
    document.body.classList.add("htmlPy-active");
  });
})();
