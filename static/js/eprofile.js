const inputs = document.querySelectorAll(".input");

function addcl() {
  let parent = this.parentNode.parentNode;
  parent.classList.add("focus");
}

function remcl() {
  let parent = this.parentNode.parentNode;
  if (this.value == "") {
    parent.classList.remove("focus");
  }
}

inputs.forEach((input) => {
  input.addEventListener("focus", addcl);
  input.addEventListener("blur", remcl);
});

const succ = document.getElementById("succ");
const div = document.getElementById("data");
const inp = document.getElementById("selectfile");

inp.addEventListener("change", function () {
  console.log("hello");
  var filename = inp.value;
  let regexp = /^s*$/;
  if (filename.match(regexp)) {
    div.textContent = "No File Chosen..";
    succ.setAttribute("hidden", false);
  } else {
    var name = filename.replace(/^.*?([^\\\/]*)$/, "$1");
    div.textContent = name;
    succ.removeAttribute("hidden");
  }
});
