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

  // Clicks and submits are handled at document level from the moment the document is created: a large
  // page (the signal page is several MB) is shown and clickable long before it has loaded, and a click
  // that reached the browser's default action would navigate to "BackEnd.<slot>" (ERR_FILE_NOT_FOUND).
  var pendingForms = [];

  function pageLoaded() {
    return document.readyState === "complete";
  }

  window.addEventListener("load", function () {
    // after every load handler (the pages fill their forms in onload), send what was submitted early
    setTimeout(function () {
      var forms = pendingForms; pendingForms = [];
      forms.forEach(sendForm);
    }, 0);
  });

  document.addEventListener("click", function (e) {
    var anchor = e.target && e.target.closest ? e.target.closest("a") : null;
    if (!anchor) { return; }
    e.preventDefault();
    e.stopPropagation();
    if (anchor.getAttribute("data-bind") !== "true") { return; }
    var slot = resolveSlot(anchor.getAttribute("href"));
    if (!slot) { return; }
    var params = anchor.getAttribute("data-params");
    if (params !== null) { slot(params); } else { slot(); }
  }, true);

  document.addEventListener("submit", function (e) {
    var form = e.target;
    e.preventDefault();
    e.stopPropagation();
    if (!form || form.getAttribute("data-bind") !== "true") { return; }
    if (pageLoaded()) {
      sendForm(form);
    } else if (pendingForms.indexOf(form) < 0) {
      pendingForms.push(form);          // sent once, after the page has filled in its values
    }
  }, true);

  // QtWebKit (Qt 4.8), which the legacy tool ran on, returned checked ? "on" : "" for a
  // checkbox/radio without a value attribute; Chromium always returns "on". The saved
  // .data files (and therefore which messages/signals are enabled) depend on the old rule.
  function legacyValue(input) {
    if ((input.type === "checkbox" || input.type === "radio") && !input.hasAttribute("value")) {
      return input.checked ? "on" : "";
    }
    return input.value;
  }

  function sendForm(form) {
    var slot = resolveSlot(form.getAttribute("action"));
    if (!slot) { return; }
    var formdata = {};
    for (var i = 0, ii = form.length; i < ii; ++i) {
      var input = form[i];
      if (input.name && input.type !== "file") { formdata[input.name] = legacyValue(input); }
    }
    var params = form.getAttribute("data-params");
    if (params !== null) { slot(JSON.stringify(formdata), params); } else { slot(JSON.stringify(formdata)); }
  }

  document.addEventListener("DOMContentLoaded", function () {
    document.body.classList.add("htmlPy-active");
  });
})();
