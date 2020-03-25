const artistDelete = document.querySelectorAll(".artist-btn-delete");
for (let i = 0; i < artistDelete.length; i++) {
  const btnDelete = artistDelete[i];
  btnDelete.onclick = function(e) {
    const artistId = btnDelete.getAttribute("artist-id");
    fetch("/artists/" + artistId, {
      method: "DELETE"
    })
      .then(function() {
        window.location.href = "/";
      })
      .catch(function(e) {
        console.log("error", e);
      });
  };
}