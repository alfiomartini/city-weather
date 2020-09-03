addEventListener('DOMContentLoaded', pipVideo);

function pipVideo(){
   let video = document.getElementById('whatchme-mini');
   let toggleBtn = document.getElementById('PiP');
   toggleBtn.addEventListener('click', togglePiPMode);
   async function togglePiPMode(event) {
      toggleBtn.disabled = true; //disable btn ,so that no multiple request are made
      try {
         if (video !== document.pictureInPictureElement) {
               await video.requestPictureInPicture();
               toggleBtn.textContent = "Mini Video (Open)";
         }
         // If already playing exit mide
         else {
               await document.exitPictureInPicture();
               toggleBtn.textContent = "Mini Video (Closed)";
         }
      } catch (error) {
         console.log(error);
      } finally {
         toggleBtn.disabled = false; //enable toggle at last
      }
   }
}
