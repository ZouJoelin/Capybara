


let file = document.getElementById("file");
file.addEventListener('change', async function (event) {
    let uploadFile = event.target.files[0];

    let formData = new FormData();
    formData.append('file', uploadFile);
    console.log(formData.get("file"));

    let response = await fetch('/auto_count', {
        method: 'POST',
        body: formData
    });

    alert("response:" + response);
    let parsedJSON = await response.json();
    alert("parsedJSON:" + parsedJSON);
    let pages = parsedJSON.pages;
    alert("pages:" + +pages);

    document.getElementById('pages').value = pages;
    alert(document.getElementById('pages').value);

    let pagesChangeEvent = new Event("change", { "bubbles": true });
    document.getElementById("information-form").dispatchEvent(pagesChangeEvent);
});


let form = document.getElementById("information-form");

form.addEventListener('change', async function (event) {
    console.log(event)
    console.log(event.target)
    console.log(form)
    console.log(form.form)
    let uploadForm = form;

    let formData = new FormData(uploadForm);
    // below line WOULDN'T work! must add it in Constructor!!!
    // FUCK javascript!!!!
    // formData.append('form', uploadForm);
    // console.log(formData.get("form"));

    let response = await fetch('/auto_count', {
        method: 'POST',
        body: formData
    });

    alert("response:" + response);
    let parsedJSON = await response.json();
    alert("parsedJSON:" + parsedJSON);
    let fee = parsedJSON.fee;
    alert("fee:" + fee);

    document.getElementById('fee').innerHTML = fee.toFixed(2);
    alert(document.getElementById('fee').innerHTML);
});