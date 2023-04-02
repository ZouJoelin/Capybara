
var total_fee = 0;

function count_fee() {
    var pages = document.getElementById("pages").value;
    var copies = document.getElementById("copies").value;


    total_fee = pages * 0.01 * copies;
    //    document.getElementById("total_fee").innerHTML = total_fee//.toFixed(2);
    document.getElementById("total_fee").value = total_fee//.toFixed(2);

    //    alert(total_fee);
    return total_fee;

}

function count_pdf() {
    file = document.getElementById("files").files[0];
    url = URL.createObjectURL(file)

    var pdfjsLib = window['pdfjs-dist/build/pdf'];
    pdfjsLib.GlobalWorkerOptions.workerSrc = '//mozilla.github.io/pdf.js/build/pdf.worker.js';
    //    pdfjsLib.GlobalWorkerOptions.workerSrc = './pdf.worker.js';

    pdf = pdfjsLib.getDocument(url);
    pdf.promise.then(function (doc) {
        document.getElementById('pages').value = doc.numPages;
        count_fee();            // 这里pdf.promise.then是异步编程，此函数块会被放到最后执行，
        return doc.numPages;    // 所以只能把count_fee()放在块里面，保证先改变pages再count_fee().

    });


}

document.getElementById("files").addEventListener("change", count_pdf);

document.getElementById("copies").addEventListener("change", count_fee);





