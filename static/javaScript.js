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


// Script parta el control de inicio de sesion 
// Verificar si el usuario está autenticado y si hay una fecha de expiración
if (isAuthenticated && sessionExpiration instanceof Date && !isNaN(sessionExpiration)) {

   const warningTime = 30 * 1000; // Alerta 30 segundos antes de que expire la sesión (2 minutos de inactividad)
 
   // Función para actualizar la expiración de la sesión cada vez que hay actividad
   function resetSessionExpiration() {
     fetch("/update-session"); // Llamada al backend para actualizar la expiración
     sessionExpiration = new Date(new Date().getTime() + 2 * 60 * 1000); // Restablecer la expiración a 2 minutos desde la última actividad
   }
 
   // Detectar la inactividad del usuario
   let activityEvents = ["mousemove", "keydown", "click"];
   activityEvents.forEach(function (event) {
     window.addEventListener(event, resetSessionExpiration);
   });
 
   // Mostrar el modal si el tiempo restante es menor que el tiempo para mostrar la alerta
   setInterval(function () {
     const currentTime = new Date();
     const timeRemaining = sessionExpiration - currentTime;
 
     // Si el tiempo restante es menor que el tiempo para mostrar la alerta
     if (timeRemaining <= warningTime && timeRemaining > 0) {
       // Mostrar el modal de expiración de sesión
       const sessionModal = new bootstrap.Modal(document.getElementById('sessionModal'));
       sessionModal.show();
     }
 
     // Si la sesión ya ha expirado, redirigir al usuario con un desvanecimiento
     if (timeRemaining <= 0) {
       // Aplicar el efecto de desvanecimiento en el body
       document.body.classList.add('fade-out-hidden');
 
       // Esperar a que se complete el efecto de desvanecimiento (2 segundos)
       setTimeout(function () {
         window.location.href = "/logout"; // Redirige a la página de cierre de sesión
       }, 2000); // Espera 2 segundos antes de redirigir
     }
   }, 1000); // Comprobar cada segundo
 
   // Si el usuario decide continuar la sesión
   document.getElementById("extendSessionBtn").addEventListener("click", function() {
     // Restablecer la expiración de la sesión
     resetSessionExpiration();
     
     // Cerrar el modal
     const sessionModal = new bootstrap.Modal(document.getElementById('sessionModal'));
     sessionModal.hide();
   });
 
   // Aquí puedes agregar más listeners para cerrar el modal al hacer clic en cualquier botón
   const closeSessionBtn = document.getElementById("closeSessionBtn");
   if (closeSessionBtn) {
     closeSessionBtn.addEventListener("click", function() {
       // Si el usuario elige cerrar la sesión, redirigir
       window.location.href = "/logout"; // Redirige a la página de cierre de sesión
     });
   }
 
   // Si el usuario elige una opción alternativa, cerramos el modal sin hacer nada
   const otherOptionBtn = document.getElementById("otherOptionBtn");
   if (otherOptionBtn) {
     otherOptionBtn.addEventListener("click", function() {
       // Cerrar el modal sin hacer nada
       const sessionModal = new bootstrap.Modal(document.getElementById('sessionModal'));
       sessionModal.hide();
     });
   }
 
 }
 
 