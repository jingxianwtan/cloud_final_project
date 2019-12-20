function handleSearch() {
    const request = document.getElementById("searchRequest").value;
    var searchFlag = "full";

    console.log("user session in handle search: " + JSON.stringify(UserSession));
    var userID = UserSession.token;
    sessionStorage.setItem("text", request);
    const apigClient = apigClientFactory.newClient();
        apigClient.rootPost(null, {"content": request, "flag": searchFlag, "userId": userID})
            .then((response) => {
              // alert("searchSuccess!");
              const body = response.data;

              document.getElementById("event").value = body.Event;
              document.getElementById("place").value = body.Location;
              document.getElementById("time").value = body.Time;
              const lati = body.Latitude;
              const long = body.Longitude;
              sessionStorage.setItem("Address", body.Address);
              sessionStorage.setItem("Latitude", body.Latitude);
              sessionStorage.setItem("Longitude", body.Longitude);

              var uluru = {lat: lati, lng: long};
              map = new google.maps.Map(document.getElementById('map'), {
                center: uluru,
                zoom: 16
              });
              var marker = new google.maps.Marker({position: uluru, map: map});
            })
            .catch(error => {
              console.log("search failed with error: " + JSON.stringify(error));
            });

    document.getElementById("searchRequest").value = "";
}

function handleEvent() {
    const newEvent = document.getElementById("event").value;
    const newPlace = document.getElementById("place").value;
    const newTime = document.getElementById("time").value;
    const obj = document.getElementById("category");
    var index = obj.selectedIndex;
    var newCategory = obj.options[index].value;
    var searchFlag = "final";
    console.log(sessionStorage.getItem("ID"));

    console.log("user session in handle event: " + JSON.stringify(UserSession));
    // console.log(localStorage.getItem("ID"));
    const apigClient = apigClientFactory.newClient();
        apigClient.rootPost(null, {"userId": UserSession.token, "Category": newCategory, "Text": sessionStorage.getItem("text"), "Address": sessionStorage.getItem("Address"),"Lat": sessionStorage.getItem("Latitude"), "Lng": sessionStorage.getItem("Longitude"), "Event": newEvent, "Place": newPlace, "Time": newTime, "flag": searchFlag})
            .then(response => {
              console.log(response);
              // alert("Note Added!");
            })
            .catch(error => {
              console.log("event creation failed with error: " + JSON.stringify(error));
            });
    alert("Note Added!");
    document.getElementById("event").value = "";
    document.getElementById("place").value = "";
    document.getElementById("time").value = "";
}

function verifyPlace() {
    const newPlace = document.getElementById("place").value;
    var searchFlag = "place";
    const apigClient = apigClientFactory.newClient();
        apigClient.rootPost(null, {"content": newPlace, "flag": searchFlag})
            .then(response => {
              // alert("placeSuccess!");
              const body = response.data;
              document.getElementById("place").value = body.Location;
              const lati = body.Latitude;
              const long = body.Longitude;
              sessionStorage.setItem("Address", body.Address);
              sessionStorage.setItem("Latitude", body.Latitude);
              sessionStorage.setItem("Longitude", body.Longitude);
              var uluru = {lat: lati, lng: long};
              map = new google.maps.Map(document.getElementById('map'), {
                center: uluru,
                zoom: 16
              });
              var marker = new google.maps.Marker({position: uluru, map: map});
            })
            .catch(error => {
              console.log("place verification failed with error: " + JSON.stringify(error));
            });

    // document.getElementById("place").value = "";
}