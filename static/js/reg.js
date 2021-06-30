// const sign_up_btn = document.querySelector("#sign-up-btn");
// const sign_in_btn = document.querySelector("#sign-in-btn");
// const container = document.querySelector(".container.sign-up-mode");

// sign_in_btn.addEventListener("click", () => {
//   container.classList.remove("sign-up-mode");
// });

// sign_up_btn.addEventListener("click", () => {
//   container.classList.add("sign-up-mode");
// });

var sing_in = document.querySelector("#sign-in-btn");
var container = document.getElementById("1");
var up = document.querySelector("#sign-up-btn");

sing_in.addEventListener("click", () => {
  container.classList.remove("sign-up-mode");
});
up.addEventListener("click", () => {
  container.classList.add("sign-up-mode");
});

//for password validation//
var password = document.getElementById("password"),
  confirm_password = document.getElementById("confirm_password");

function validatePassword() {
  if (password.value != confirm_password.value) {
    confirm_password.setCustomValidity("Passwords Don't Match");
  } else {
    confirm_password.setCustomValidity("");
  }
}
password.onchange = validatePassword;
confirm_password.onkeyup = validatePassword;
