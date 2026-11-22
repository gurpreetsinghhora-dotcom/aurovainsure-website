/* Aurova Insure — small, dependency-free script. No cookies, no tracking. */
(function () {
  "use strict";

  // Mobile menu
  var toggle = document.querySelector(".menu-toggle");
  var nav = document.getElementById("site-nav");
  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      var open = nav.classList.toggle("open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
      toggle.textContent = open ? "Close" : "Menu";
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && nav.classList.contains("open")) {
        nav.classList.remove("open");
        toggle.setAttribute("aria-expanded", "false");
        toggle.textContent = "Menu";
        toggle.focus();
      }
    });
  }

  // Year in footer
  var y = document.querySelector("[data-year]");
  if (y) y.textContent = String(new Date().getFullYear());

  // Enquiry form
  var form = document.getElementById("enquiry-form");
  if (!form) return;

  // Preselect the enquiry type from the link the visitor clicked (?topic=...)
  var params = new URLSearchParams(window.location.search);
  var topic = params.get("topic");
  var topicSelect = form.querySelector("#enquiry_type");
  var topics = { discovery: "Book a discovery call", backlog: "Discuss a backlog", quote: "Request a quote", general: "General enquiry" };
  if (topic && topicSelect && topics[topic]) topicSelect.value = topics[topic];

  var statusBox = document.getElementById("form-status");
  function show(kind, msg) {
    statusBox.className = "form-status " + kind;
    statusBox.textContent = msg;
    statusBox.setAttribute("role", kind === "err" ? "alert" : "status");
    statusBox.focus();
  }

  form.addEventListener("submit", function (e) {
    e.preventDefault();

    if (!form.checkValidity()) {
      form.reportValidity();
      return;
    }
    // Honeypot: real people never fill this in
    if (form.querySelector('[name="botcheck"]').checked) return;

    var data = new FormData(form);
    var accessKey = form.getAttribute("data-access-key") || "";
    var button = form.querySelector('button[type="submit"]');

    var summary =
      "Name: " + data.get("name") + "\n" +
      "Business: " + data.get("business") + "\n" +
      "Email: " + data.get("email") + "\n" +
      "Telephone: " + (data.get("phone") || "-") + "\n" +
      "Type of business: " + data.get("business_type") + "\n" +
      "Enquiry: " + data.get("enquiry_type") + "\n" +
      "Support needed: " + data.get("support") + "\n\n" +
      data.get("message");

    // Without a form-delivery key, open the visitor's own email app with the enquiry ready to send.
    if (!accessKey) {
      var to = form.getAttribute("data-email");
      var subject = "Website enquiry: " + data.get("enquiry_type") + " - " + data.get("business");
      window.location.href = "mailto:" + to + "?subject=" + encodeURIComponent(subject) + "&body=" + encodeURIComponent(summary);
      show("ok", "Your email app should now open with your enquiry ready to send. If it doesn't, email us at " + to + " or call 07884 691080.");
      return;
    }

    button.disabled = true;
    button.textContent = "Sending...";
    var payload = {
      access_key: accessKey,
      subject: "Website enquiry: " + data.get("enquiry_type") + " - " + data.get("business"),
      from_name: "Aurova Insure website",
      name: data.get("name"),
      email: data.get("email"),
      business: data.get("business"),
      phone: data.get("phone") || "",
      business_type: data.get("business_type"),
      enquiry_type: data.get("enquiry_type"),
      support: data.get("support"),
      message: data.get("message"),
      botcheck: false
    };
    fetch("https://api.web3forms.com/submit", {
      method: "POST",
      headers: { "Content-Type": "application/json", Accept: "application/json" },
      body: JSON.stringify(payload)
    })
      .then(function (r) { return r.json().then(function (j) { return { ok: r.ok, j: j }; }); })
      .then(function (res) {
        if (res.ok && res.j.success) {
          form.reset();
          show("ok", "Thank you. Your enquiry has been sent and we'll reply within one working day.");
        } else {
          throw new Error("send failed");
        }
      })
      .catch(function () {
        show("err", "Sorry, your enquiry couldn't be sent. Please email us at " + form.getAttribute("data-email") + " or call 07884 691080.");
      })
      .finally(function () {
        button.disabled = false;
        button.textContent = "Send enquiry";
      });
  });
})();
