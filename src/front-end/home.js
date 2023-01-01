$(document).ready(function () {
  // make ajax call to server
  $.ajax({
    type: "GET",
    url: "http://127.0.0.1:5000/api/v1/recent",
    success: function (response) {
      let serverResponse = response.msg;
      let array = Object.values(serverResponse);
      let counter = 0;

      // fill the title
      $(".tutorial")
        .find("h3")
        .each(function () {
          $(this).text(array[counter].title);
          counter = counter + 1;
        });
    },
  });
});
