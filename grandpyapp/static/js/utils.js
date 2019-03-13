// Make an AJAX POST call
// Takes into parameters the target URL, the data to be sent and the callback function called on success
// The isJson parameter is used to indicate whether the send is for JSON data
function ajaxPost(url, data, successCallback, errorCallback, generalCallback, progressCallback) {
    let req = new XMLHttpRequest();
    req.open("POST", url, true);
    req.addEventListener("load", function () {
        if (req.status >= 200 && req.status < 400) {
            // Appelle la fonction callback en lui passant la réponse de la requête
            successCallback(req.responseText);
        } else {
            errorCallback(req);
        }
        generalCallback();
    });
    req.addEventListener("progress", progressCallback);

    req.send(data);
}

let submit_button = document.createElement("button");
submit_button.type = "submit";
submit_button.classList.add("btn", "btn-primary");
submit_button.appendChild(document.createTextNode("Envoyer"));

let loader_img = document.createElement("div");
loader_img.classList.add("loader");

let block_from_form = document.getElementById("submit_form");
block_from_form.appendChild(submit_button);

let ask_input = document.getElementById("ask");
let countries_input = document.getElementById('countries');

// create messaging ul
let messagerie = document.createElement("ul");
messagerie.classList.add("list-unstyled");
messagerie.classList.add("mb-0");

// add media function
function addMedia(title, message, src_media, nofirst) {
    let media = document.createElement("li");
    media.classList.add("media");
    if (nofirst) {
        media.classList.add("mt-4")
    }

    let image = document.createElement("img");
    image.src = src_media;
    image.classList.add("mr-3");
    image.width = "50";
    image.height = "50";

    let media_body = document.createElement("div");
    media_body.classList.add("media-body");
    media_body.classList.add("px-1", "py-1");

    let _title = document.createElement("h5");
    _title.classList.add("mt-0");
    _title.classList.add("mb-1");
    _title.appendChild(document.createTextNode(title));

    let div_media_body = document.createElement("div");

    let span_media_body = document.createElement("span");
    span_media_body.innerHTML = message;

    media_body.appendChild(_title);
    media_body.appendChild(span_media_body);
    media_body.appendChild(div_media_body);

    media.appendChild(image);
    media.appendChild(media_body);

    messagerie.appendChild(media);

    return media_body
}

let div_messagerie = document.getElementById("messagerie");
div_messagerie.appendChild(messagerie);

let span_messagerie = div_messagerie.getElementsByTagName("span")[0];

// add media
addMedia("GrandPy Bot",
    "Je suis un as de l'exploration. Questionne mon savoir.",
    span_messagerie.getAttribute("data-image-papi")
);

let form = document.querySelector("form");

// Form submission management
form.addEventListener("submit", function (e) {
    e.preventDefault();

    // Récupération des champs du formulaire dans l'objet FormData
    let data = new FormData(form);

    if (data.get("ask").trim() === "") {
        return
    }

    submit_button.style.display = 'none';
    block_from_form.appendChild(loader_img);
    ask_input.readOnly = "true";

    addMedia("Moi", data.get('ask'),
        span_messagerie.getAttribute("data-image-user"),
        true);

    div_messagerie.scrollTop = div_messagerie.scrollHeight - div_messagerie.clientHeight;

    ajaxPost(form.action, data,
        function (responseText) {
            let obj = JSON.parse(responseText);

            try {
                let _location = new google.maps.LatLng(obj.google_maps_parsed.location.lat,
                    obj.google_maps_parsed.location.lng);

                let _location_northeast = new google.maps.LatLng(obj.google_maps_parsed.bounds.northeast.lat,
                    obj.google_maps_parsed.bounds.northeast.lng);

                let _location_southwest = new google.maps.LatLng(obj.google_maps_parsed.bounds.southwest.lat,
                    obj.google_maps_parsed.bounds.southwest.lng);

                let media_body = addMedia("GrandPy Bot",
                    "Hum.. Je vois où celà se trouve !<br>" +
                    "Adresse: " + obj.google_maps_parsed.formatted_address,
                    span_messagerie.getAttribute("data-image-papi"),
                    true);

                let div_media_body = media_body.getElementsByTagName('div')[0];
                div_media_body.classList.add("map_canvas");

                let map = new google.maps.Map(div_media_body, {
                    mapTypeId: google.maps.MapTypeId.ROADMAP,
                });

                let marker = new google.maps.Marker({
                    position: _location,
                    map: map
                });

                let bounds = new google.maps.LatLngBounds();
                bounds.extend(_location_northeast);
                bounds.extend(_location_southwest);
                map.fitBounds(bounds);

                addMedia("GrandPy Bot",
                    "Tiens, ça me rappelle quelque chose: <br>" +
                    obj.wikipedia_parsed._summary +
                    "<br><a href='" + obj.wikipedia_parsed.url + "' target='_blank'>[En savoir plus]</a>",
                    span_messagerie.getAttribute("data-image-papi"),
                    true);
            } catch (error) {
                addMedia("GrandPy Bot",
                    "Je suis vieux tu sais, formule moi ta question un peu plus simplement...",
                    span_messagerie.getAttribute("data-image-papi"),
                    true);
            }
            div_messagerie.scrollTop = div_messagerie.scrollHeight - div_messagerie.clientHeight;
        },
        function (req) {
            console.error(req.status + " " + req.statusText + " " + form.action);
        },
        function () {
            setTimeout(function () {
                submit_button.style.display = "block";
                ask_input.removeAttribute('readonly');
                ask_input.value = "";
                loader_img.parentNode.removeChild(loader_img);
                loader_img.removeAttribute("style");
            }, 1000);
        },
        function () {
            loader_img.style.borderBottom = "10px solid red";
            loader_img.style.borderTop = "10px solid red";
        }
    );
});

let question_list = [
    ["Salut papi, j'aimerai avoir l'adresse de sète stp.", "FR"],
    ["coucou grand père, tu ne saurais pas où est situé Paris par hasard ?", "FR"],
    ["yo papi, j'veux bien l'adresse du groenland.", "GP"],
    ["hey, tu n'aurais pas une idée d'où se situe la rue des rosiers par hasard ?", "FR"],
    ["je veux aller en angleterre", "GB"],
    ["Salut GrandPy ! Est-ce que tu connais l'adresse d'OpenClassrooms ?", "FR"]
];
let eraser_button = form.querySelector('#eraser');
let random_button = form.querySelector('#random');

eraser_button.addEventListener("click", function (e) {
    e.preventDefault();
    ask_input.value = "";
    countries_input.value = "";
});

random_button.addEventListener("click", function (e) {
    e.preventDefault();
    let random_list = question_list[Math.floor(Math.random() * question_list.length)];
    ask_input.value = random_list[0];
    countries_input.value = random_list[1];
});