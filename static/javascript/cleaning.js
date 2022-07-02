let polltext = document.querySelectorAll(".pollText");
polltext.forEach((e) => {
    if (e.innerText.length > 100) {
        e.innerText = e.innerText.slice(0, 100) + " ...";
    }
});

let questiontext = document.querySelectorAll(".questionText");
questiontext.forEach((e) => {
    if (e.innerText.length > 75) {
        e.innerText = e.innerText.slice(0, 75) + " ...";
    }
});
