---
layout: page
title: Contact Me
permalink: /contact
---



<label class="label">Name*</label>
<input id="name" class="input" type="text" required value="adam">

<label class="label">Email*</label>
<input id="email" class="input" type="email" required value="bob@mysite.com">

<label class="label">Message</label>
<textarea id="message" class="textarea" rows="5">My Message...</textarea>

<button id="submit" class="button is-link">Submit Message</button>

<!-- Hidden by default. Form submit unhides. Close button re-hides -->
<div class="notification is-success hidden" id="submit-notification">
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
  .input, .textarea {
box-shadow: inset 0 1px 2px rgba(10, 10, 10, 0.1);
max-width: 100%;
width: 100%;
}
.input, .textarea, .select select {
  background-color: white;
  border-color: #dbdbdb;
  border-radius: 4px;
  color: #363636;
}
.button, .input, .textarea, select{
  align-items: center;
  border: 1px solid #ccc;
  border-radius: 4px;
  padding: 1em;
}

.notification.is-success {
  background-color: #23d160;
  color: #fff;
}

.hidden {
  visibility: hidden;
}
</script>
