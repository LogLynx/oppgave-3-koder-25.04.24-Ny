var button = document.getElementById("enter");
var input = document.getElementById("userinput");
var ul = document.querySelector("ul");
var items = ul.getElementsByTagName("li");

function inputLength() {
    return input.value.length;
}

function createListElement() {
    var li = document.createElement("li");
    var button = document.createElement("button");
    li.appendChild(document.createTextNode(input.value));
    ul.appendChild(li);
    li.appendChild(button);
    button.innerHTML = "Delete";
    input.value = "";

    liToggle();
    buttonDelete();
    saveToLocalStorage(); // Save to local storage after creating new item
}

function addListAfterClick() {
    if (inputLength() > 0) {
        createListElement();
    }
}

function addListAfterKeypress(event) {
    if (inputLength() > 0 && event.keyCode === 13) {
        createListElement();
    }
}

function liToggle() {
    for (i = 0; i < items.length; i++) {
        items[i].addEventListener("click", toggleClass);
    }
}

function toggleClass() {
    this.classList.toggle("done");
}

function buttonDelete() {
    var buttons = document.querySelectorAll("li button");
    for (i = 0; i < buttons.length; i++) {
        buttons[i].addEventListener("click", clearElement);
    }
}

function clearElement() {
    this.parentNode.remove();
    saveToLocalStorage(); // Save to local storage after deleting item
}

function saveToLocalStorage() {
    localStorage.setItem("items", ul.innerHTML);
}

button.addEventListener("click", addListAfterClick);
input.addEventListener("keypress", addListAfterKeypress);

// Load items from local storage when the page loads
window.onload = function() {
    var savedItems = localStorage.getItem("items");
    if (savedItems) {
        ul.innerHTML = savedItems;
        // Reassign the items variable after loading from local storage
        items = ul.getElementsByTagName("li");
        liToggle();
        buttonDelete();
    }
};