// Funktion för att förhandsgranska bilden när den laddas upp
document.getElementById('fileInput').addEventListener('change', function(event) {
    const file = event.target.files[0];
    const previewImage = document.getElementById('previewImage');
    
    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            previewImage.src = e.target.result;
            previewImage.style.display = 'block';
        };
        reader.readAsDataURL(file);
    }
});

// Funktion för att visa laddningsmeddelande och dölja formulär
document.getElementById('imageForm').addEventListener('submit', function() {
    const form = document.getElementById('imageForm');
    const loadingMessage = document.getElementById('loadingMessage');
    const spinner = document.getElementById('loading-spinner');
    
    form.style.display = 'none';
    spinner.style.display = 'block';
    loadingMessage.style.display = 'block';
});