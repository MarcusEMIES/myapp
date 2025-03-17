document.addEventListener('DOMContentLoaded', function() {
  // Obtener el modal y la imagen dentro del modal
  var modalImage = document.getElementById('modalImage');
  var imageElements = document.querySelectorAll('img[data-bs-image]');

  imageElements.forEach(function(imageElement) {
     imageElement.addEventListener('click', function() {
        var imageUrl = imageElement.getAttribute('data-bs-image');
        if (imageUrl) {
           modalImage.setAttribute('src', imageUrl);
        } else {
           console.error("No se encontró la URL de la imagen");
        }
     });
  });
});
