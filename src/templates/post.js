const buttons = document.querySelectorAll("button");
textFeild.document.designMode = "On";
let show = false;
for (let i = 0; i < buttons.length; i++) {
  buttons[i].addEventListener("click", () => {
    let cmd = buttons[i].getAttribute("data-cmd");
    if (buttons[i].name === "active") {
      buttons[i].classList.toggle("active");
    }

    if (cmd === "createLink") {
      let url = prompt("Enter the link here", "");
      textFeild.document.execCommand(cmd, false, url);
      const links = textFeild.document.querySelectorAll("a");
      links.forEach((item) => {
        item.target = "_black";
        item.addEventListener("mouseover", () => {
          textFeild.document.designMode = "Off";
        });
        item.addEventListener("mouseout", () => {
          textFeild.document.designMode = "On";
        });
      });
    } else {
      textFeild.document.execCommand(cmd, false, null);
    }

    if (cmd === "showCode") {
      const textBody = textFeild.document.querySelector("body");
      if (show) {
        textBody.innerHTML = textBody.textContent;
        show = false;
      } else {
        textBody.textContent = textBody.innerHTML;
        show = true;
      }
    }
  });
}
$("#submit").click(function () {
  let body = $("#output").contents().find("body").html();
  let title = $("#title").val();
  let desc = $("#description").val();
  let element = document.getElementById("options");
  let cat = element.options[element.selectedIndex].text;

  let postData = {
    title: title,
    description: desc,
    body: body,
    category: cat,
  };

  let header = {
    "Content-Type": "application/json",
    Authorization: localStorage.getItem("Authorization"),
  };

  const subjectsDictionary = {
    "Reaction Engineering": "reaction/post",
    Thermodynamics: "thermodynamics/post",
    "Fluid Mechanics": "fluid/post",
    "Material Engineering": "material/post",
    Chemistry: "chem/post",
    Biotechnology: "biotech/post",
  };

  const baseUrl = "http://localhost:5000/api/v1/";
  let appendant = subjectsDictionary[cat];

  $.ajax({
    type: "POST",
    url: baseUrl + appendant,
    headers: header,
    data: JSON.stringify(postData),
    success: function (data) {
      //
    },
    error: function (xhr) {
      let msg = xhr.responseJSON.msg;
      alert(msg);
    },
  });
});
