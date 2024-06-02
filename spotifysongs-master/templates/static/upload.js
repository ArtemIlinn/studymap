document.addEventListener('DOMContentLoaded', function() {
    const fileInputButton = document.getElementById('file-input-button');
    const fileInput = document.getElementById('file-input');
    const selectedFilesDiv = document.getElementById('selected-files');

    fileInputButton.addEventListener('click', function() {
        fileInput.click();
    });

    fileInput.addEventListener('change', function() {
        const selectedFiles = fileInput.files;
        selectedFilesDiv.innerHTML = '';

        for (let i = 0; i < selectedFiles.length; i++) {
            const fileName = selectedFiles[i].name;
            const fileElement = document.createElement('p');
            fileElement.textContent = fileName;
            selectedFilesDiv.appendChild(fileElement);
        }
    });
});
