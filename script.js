function send() {
  let input = document.getElementById("input");
  let msg = input.value.trim();
  input.value = "";
  let messages = document.getElementById("messages");
  messages.innerHTML += `<div class="user"><span>${msg}</span></div>`;

  let typing = document.createElement("div");
  typing.innerHTML = `<span class="bot typing">Typing...</span>`;
  messages.appendChild(typing);

  fetch("/chat", {
    method: "POST",
    headers: {"Content-Type":"application/json"},
    body: JSON.stringify({message:msg})
  })
  .then(res => res.json())
  .then(data => {
    typing.remove();
    messages.innerHTML += `<div class="bot"><span>${data.reply}</span></div>`;
    messages.scrollTop = messages.scrollHeight;
  });
}
