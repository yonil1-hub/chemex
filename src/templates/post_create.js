$("#upload").submit(function (event) {
  event.preventDefault(); // prevent the form from submitting

  let title = $("#tutorial-title").val(); // get the title from the input element
  let description = $("#tutorial-description").val(); // get the description from the input element
  let file = $("#tutorial-file")[0].files[0]; // get the file from the input element
  var selectedOption = $("#course option:selected").val();
  let formData = new FormData(); // create a new FormData object
  formData.append("title", title); // append the title to the FormData object
  formData.append("description", description); // append the description to the FormData object
  formData.append("file", file); // append the file to the FormData object
  formData.append("category", selectedOption); //append selected option

  $.ajax({
    url: "http://127.0.0.1:5000/api/v1/create", // the URL of the server-side script
    type: "POST", // use the POST method to send the data
    data: formData, // send the FormData object as the request data
    processData: false, // do not process the data before sending it
    contentType: false, // do not set the content type of the request
    success: function (response) {
      // called when the request succeeds
      console.log(response);
    },
    error: function (xhr, status, error) {
      // called when the request fails
      console.error(error);
    },
  });
});
