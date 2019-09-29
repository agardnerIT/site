---
layout: page
title: Contact Me
permalink: /contact
---


<div class="field">
  <label class="label">Name*</label>
  <div class="control">
    <input id="name" class="input" type="text" required value="adam">
  </div>
</div>

<div class="field">
  <label class="label">Email*</label>
  <div class="control">
    <input id="email" class="input" type="email" required value="bob@mysite.com">
  </div>
</div>

<div class="field">
  <label class="label">Message</label>
  <div class="control">
    <textarea id="message" class="textarea">My Message...</textarea>
  </div>
</div>

<div class="field">
  <div class="control">
    <button id="submit" class="button is-link">Submit Message</button>
  </div>
</div>

<!-- Hidden by default. Form submit unhides. Close button re-hides -->
<div class="notification is-success hidden" id="submit-notification">
  <button class="delete" id="submit-delete"></button>
  Thanks. Your message has been sent. I'll be in touch soon.
</div>

<script>
  // Form submit clicked...
  document.getElementById('submit').addEventListener('click', function(event) {

    // Prevent form submission default, disable the submit button and show the notification.
    event.preventDefault();
    document.getElementById('submit').disabled = true;
    document.getElementById('submit-notification').classList.remove("hidden");

    name = document.getElementById('name').value;
    email = document.getElementById('email').value;
    message = document.getElementById('message').value;

    // Submit data to AWS API
    var xmlhttp = new XMLHttpRequest();
    var theUrl = "https://pkhlhwjn33.execute-api.ap-southeast-2.amazonaws.com/default/submitAGardnerNetContactForm";
    xmlhttp.open("POST", theUrl);
    xmlhttp.send(JSON.stringify({ "name": name, "email": email, "message": message}));

  });

  // When notification delete button is clicked, hide notifiction.
  document.getElementById('submit-delete').addEventListener('click', function(event) {
    document.getElementById('submit-notification').classList.add("hidden");
  });
</script>
<style>
.hidden {
  visibility: hidden;
}
</script>
