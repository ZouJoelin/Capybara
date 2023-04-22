

const MAX_SIZE = 50 * 1024 * 1024; // x * 1MB

let file = document.getElementById("file");
file.addEventListener('change', async function (event) {
    try {
        let uploadFile = event.target.files[0];

        // constrain file size
        // Max~50MB; nomarl-max~30MB;
        if (uploadFile.size > MAX_SIZE) {
            alert('文件大小不能超过 50MB');
            // event.preventDefault();
            return;
        }

        let formData = new FormData();
        formData.append('file', uploadFile);
        // console.log(formData.get("file"));
        let response = await fetch('/auto_count', {
            method: 'POST',
            body: formData
        });
        if (!response.ok) {
            let errorJSON = await response.json();
            throw errorJSON;
        }
        let parsedJSON = await response.json();
        let pages = parsedJSON.pages;
        document.getElementById('pages').value = pages;

        let pagesChangeEvent = new Event("change", { "bubbles": true });
        document.getElementById("information-form").dispatchEvent(pagesChangeEvent);

    } catch (errorJSON) {
        let error_message = errorJSON.error_message;
        alert(error_message);
    }
});


let form = document.getElementById("information-form");
form.addEventListener('change', async function (event) {
    try {
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
        if (!response.ok) {
            let errorJSON = await response.json();
            throw errorJSON;
        }
        let parsedJSON = await response.json();
        let fee = parsedJSON.fee;
        document.getElementById('fee').innerHTML = fee.toFixed(2);

    } catch (errorJSON) {
        let error_message = errorJSON.error_message;
        alert(error_message);
    }
});
