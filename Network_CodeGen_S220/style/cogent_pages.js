/* Banner for the message / signal configuration pages: how many rows are new (no saved settings,
   highlighted green by the page's load()), "Next new" scrolls to the next one, "Only new" hides the rest. */
function cogentMarkNew(kind) {
  var rows = Array.prototype.slice.call(document.querySelectorAll("tr.cogent-new"));
  var single = kind.replace(/s$/, "");
  var bar = document.createElement("div");
  bar.id = "cogent-new-banner";
  bar.className = "cg-page-bar" + (rows.length ? "" : " none");
  if (!rows.length) {
    bar.textContent = "No new " + kind + ": every " + single + " of this DBC has saved settings.";
  } else {
    bar.innerHTML = "<strong>" + rows.length + " new " + (rows.length === 1 ? single : kind) + "</strong>" +
      " without saved settings (green rows). Check them, then press Save and Back." +
      ' <button type="button" id="cogent-next-new" class="cg-btn cg-btn-small">Next new</button>' +
      ' <button type="button" id="cogent-only-new" class="cg-btn cg-btn-small">Only new</button>';
  }
  // signal page: set the notification of every new row at once (e.g. the 130 signals of two new BMS messages)
  if (rows.length && document.querySelector('tr.cogent-new select[id$="_os_notify_no_of_events"]')) {
    var notify = document.createElement("span");
    notify.appendChild(document.createTextNode(" Notification for new rows: "));
    var choice = document.createElement("select");
    choice.id = "cogent-new-notify";
    ["No_Delay", "200ms_Delay_g1", "200ms_Delay_g2"].forEach(function (value) {
      var option = document.createElement("option");
      option.value = value;
      option.textContent = value;
      choice.appendChild(option);
    });
    var apply = document.createElement("button");
    apply.type = "button";
    apply.id = "cogent-apply-notify";
    apply.className = "cg-btn cg-btn-small";
    apply.textContent = "Apply to new rows";
    apply.onclick = function () {
      Array.prototype.forEach.call(document.querySelectorAll('tr.cogent-new select[id$="_os_notify_no_of_events"]'),
        function (select) { select.value = choice.value; });
    };
    notify.appendChild(choice);
    notify.appendChild(document.createTextNode(" "));
    notify.appendChild(apply);
    bar.appendChild(notify);
  }
  var save = document.createElement("button");
  save.type = "button";
  save.id = "cogent-save";
  save.className = "cg-btn cg-btn-small cg-btn-primary";
  save.textContent = "Save and Back";
  save.style.marginLeft = "auto";
  save.onclick = function () { document.getElementById("form_submit").click(); };
  bar.appendChild(save);
  var form = document.getElementById("form");
  form.parentNode.insertBefore(bar, form);
  if (!rows.length) { return; }
  var index = -1, only = false;
  document.getElementById("cogent-next-new").onclick = function () {
    rows.forEach(function (r) { r.classList.remove("cogent-current"); });
    index = (index + 1) % rows.length;
    rows[index].classList.add("cogent-current");
    rows[index].scrollIntoView({block: "center"});
  };
  document.getElementById("cogent-only-new").onclick = function () {
    only = !only;
    this.textContent = only ? "Show all" : "Only new";
    ["tx_table", "rx_table"].forEach(function (id) {
      var table = document.getElementById(id);
      if (!table) { return; }
      Array.prototype.forEach.call(table.getElementsByTagName("tr"), function (r) {
        if (r.id) { r.style.display = (only && !r.classList.contains("cogent-new")) ? "none" : ""; }
      });
    });
  };
}
