

function test(date){
    console.log("here" + "hj")
    console.log(date)
    fetch("/img.html", {
        method: 'POST',
        credentials: 'same-origin',
        headers:{
            'X-Requested-With': 'XMLHttpRequest', //Necessary to work with request.is_ajax()
            'X-CSRFToken': getCookie("csrftoken"),
    },
        body: JSON.stringify({'post_data':date}) //JavaScript object of data to POST
    })
    .then(response => {
      return response.json()
    })
    .then(data => {
      var a = 0
      console.log(Object.keys(data).length)
      var img = ""
      for(let i = 0; i < Object.keys(data).length;i = i + 1){
        var datee = data["p" + i.toString()]
        console.log(data["p"+ i.toString()])
        var text = "<img src='" + datee + "'>"
        img = img + text
        document.getElementById("put").innerHTML = img
      }
      alert(data["p0"])
      
      
      
    })
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
      const cookies = document.cookie.split(";");
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        // Does this cookie string begin with the name we want?
        if (cookie.substring(0, name.length + 1) === (name + "=")) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }