document.addEventListener('DOMContentLoaded', function() {
  // Obtener el modal y la imagen dentro del modal
  var modalImage = document.getElementById('modalImage');

  // Obtener todas las imágenes dentro de las tarjetas
  var imageElements = document.querySelectorAll('img[data-bs-image]');

  // Agregar el evento de clic a cada imagen
  imageElements.forEach(function(imageElement) {
    imageElement.addEventListener('click', function() {
      // Actualizar la imagen en el modal con la fuente de la imagen clickeada
      var imageUrl = imageElement.getAttribute('data-bs-image');
      modalImage.setAttribute('src', imageUrl);
    });
  });
});
