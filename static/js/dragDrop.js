// Get elements
let fileInput = document.getElementById('file');
const dragDropZone = document.querySelector('.drag-drop-zone');

// Prevent default behaviors for drag events
['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
    dragDropZone.addEventListener(eventName, preventDefaults, false);
    document.body.addEventListener(eventName, preventDefaults, false);
});

// Highlight drop area when a file is being dragged over it
['dragenter', 'dragover'].forEach(eventName => {
    dragDropZone.addEventListener(eventName, highlight, false);
});
['dragleave', 'drop'].forEach(eventName => {
    dragDropZone.addEventListener(eventName, unhighlight, false);
});

// Handle dropped files
dragDropZone.addEventListener('drop', handleDrop, false);

function preventDefaults(e) {
    e.preventDefault();
    e.stopPropagation();
}

function highlight() {
    dragDropZone.classList.add('highlight');
}

function unhighlight() {
    dragDropZone.classList.remove('highlight');
}

function handleDrop(e) {
    const dt = e.dataTransfer;
    const files = dt.files;

    // Update file input with dropped files
    fileInput.files = files;
    fileInput.dispatchEvent(new Event("change", { "bubbles": true }));
}

// change placeholder to upload filename
const fileNamePlaceholder = document.getElementById('filename-placeholder');
fileInput.addEventListener('change', (event) => {
    const selectedFile = event.target.files[0];

    if (selectedFile) {
        fileNamePlaceholder.textContent = selectedFile.name;
    } else {
        fileNamePlaceholder.textContent = "点击或者拖拽上传";
    }
});
