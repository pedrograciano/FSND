const venueDelete = document.querySelectorAll(".btn-delete");
  for (let i = 0; i < venueDelete.length; i++) {
    const vdelete = venueDelete[i];
    vdelete.onclick = function(e) {
      const venueId = vdelete.getAttribute("venue-id");
      fetch("/venues/" + venueId, {
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
/**
const venueEdit = document.querySelectorAll(".btn-edit");
  for (let i = 0; i < venueEdit.length; i++) {
    const vedit = venueEdit[i];
    vedit.onclick = function(e) {
      const venueId = vedit.getAttribute("venue-id");
      fetch("/venues/" + venueId + "/edit" , {
        method: "GET"
      })
      .then(function() {
        window.location.href = "/venues/"+venueId+"/edit";
      });
    };
  }
*/
