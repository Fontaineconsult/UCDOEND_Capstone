
let mouseOverPopup = false;
let popUpActive = false;


function queryLocalDb(isbn) {

    function queryCallback(data) {
        console.log("SUCCESS ", data);
        activeIndexViewModel.insertHolding(data)
    }
    $.ajax({
        url:"http://127.0.0.1:5000/api/booksearch/getdata",
        data: {'q': isbn[0].value},
        callback: 'queryCallback',
        headers: {'Api-User-Agent': 'Example/1.0'},
        type: 'GET',
        success: function (data) {
            queryCallback(data)
        }
    });
}
function queryTextbookList(searchInput, type) {

    function queryCallback(data) {
        activeIndexViewModel.textbookCallback(data)
        console.log('DAATAAA', data)
    }
    if (type === "isbn") {
        searchInput = searchInput.replace(/\D|\s/g, "")
        if (searchInput.length > 3) {
            $.ajax({
                url:"http://127.0.0.1:5000/api/booksearch/textbook-json",
                data: {'isbn': searchInput},
                callback: 'queryCallback',
                headers: {'Api-User-Agent': 'Example/1.0'},
                type: 'GET',
                success: function (data) {
                    queryCallback(data)
                }
            });
        }
        console.log(searchInput)


    } else if (type === "course") {
        searchInput = searchInput.replace(/ /g, "_");
        $.ajax({
            url:"http://127.0.0.1:5000/api/booksearch/textbook-json",
            data: {'course': searchInput},
            callback: 'queryCallback',
            headers: {'Api-User-Agent': 'Example/1.0'},
            type: 'GET',
            success: function (data) {
                queryCallback(data)
            }
        });
    }

}
function accessibleTextSearch(isbn) {

    function queryCallback(data) {
        console.log('RETURNED FROM SERVER', data)
        let expireDate = new Date();
        expireDate.setMonth(expireDate.getMonth() + 1);

        if (data['status']['aimhub']['available'] === true || data['status']['local']['available'] === true || data['status']['atn']['available'] === true || data['status']['bookshare']['available'] === true) {

            saveToLocalStorage({'isbn': data['isbn'], 'results': {'status': true, 'results': data, 'expiration': expireDate} });
            console.log(data)
            let localIds = {'atn': data['status']['atn']['id'], 'bookshare': data['status']['bookshare']['id']}
            activeIndexViewModel.accessibleCallback({'isbn': data['isbn'], 'status': true, 'results':data['status'], 'localIds': localIds})
        } else {

            saveToLocalStorage( {'isbn': data['isbn'], 'results': {'status': false, 'results': data, 'expiration': expireDate} } );
            console.log("TisFALSE")
            activeIndexViewModel.accessibleCallback({'isbn': data['isbn'], 'status': false, 'results': data['status']})
        }

    }

    $.ajax({
        async: true,
        url:"http://127.0.0.1:5000/api/booksearch/textbook-json",
        data: {'isbn': isbn, 'check': true},
        callback: 'queryCallback',
        headers: {'Api-User-Agent': 'Example/1.0'},
        type: 'GET',
        success: function (data) {
            queryCallback(data)
        }
    });

}
function saveToLocalStorage(accessibleResult) {
    let isbn = accessibleResult['isbn'];
    let status = JSON.stringify(accessibleResult['results']);
    if (localStorage.getItem(isbn) === null) {
        localStorage.setItem(isbn, status)}
}

function checkLocalStorage(isbn) {
    let status = localStorage.getItem(isbn)

    status = JSON.parse(status)
    if (status){
        if (status['status'] === false) {
            return false
        } else {
            return status
        }
    }

}

function buildPopup(searchStatus, itemIds) {
    console.log("SEARCH STATUS ", searchStatus)
    if (searchStatus['results']['aimhub']['available'] === true) {
        aimhub = "<a href='https://aimhub.org/search?q=" + searchStatus['isbn'] + "' target='_blank'>Available</a>"
    } else {
        aimhub = "Unavailable"
    }
    if (searchStatus['results']['atn']['available'] === true) {
        atn = "<a href='https://accesstext.gatech.edu/atn/requests/add/" + searchStatus['results']['atn']['id'] + "' target='_blank'>Available</a>"
    } else {
        atn = "Unavailable"
    }
    if (searchStatus['results']['bookshare']['available'] === true) {
        bookshare = "<a href='https://www.bookshare.org/browse/book/" + searchStatus['results']['bookshare']['id'] + "' target='_blank'>Available</a>"
    } else {
        bookshare = "Unavailable"
    }
    if (searchStatus['results']['local']['available'] === true) {
        local = "Available"
    } else {
        local = "Unavailable"
    }
    let resultsTable = $("<table/>").addClass("popUpTable");

    let aimHubRow = $("<tr><td>" + "AimHub" + "</td><td>" + aimhub + "</td></tr>");
    let atnRow = $("<tr><td>" + "Access Text" + "</td><td>" + atn + "</td></tr>")
    let bookShareRow = $("<tr><td>" + "Bookshare" + "</td><td>" + bookshare + "</td></tr>")
    let localRow = $("<tr><td>" + "SF State" + "</td><td>" + local + "</td></tr>")

    let tableBody = $("<tbody/>")

    tableBody.append(aimHubRow).append(atnRow).append(localRow).append(bookShareRow)
    resultsTable.append(tableBody)

    let currentPopup = $( "<div id = 'currentPopup' class='popUp'></div>")
    currentPopup.append(resultsTable).mouseenter(mouseOver).mouseleave(mouseOut);
    return currentPopup

}

function applySearchStatusPopUp(searchStatus, divId, itemIds) {

    let currentPopup = buildPopup(searchStatus, itemIds)
    if ($( "#currentPopup" ).length === 0) {

        $( "#" + divId ).prepend(currentPopup)
        popUpActive = true
    } else {
    }

}

function hideSearchStatusPopup() {
    setTimeout(function () {
        if (mouseOverPopup === false) {

            $( "#currentPopup" ).remove()
            popUpActive = false
        }
    },1)
}

function mouseOver() {
    mouseOverPopup = ((mouseOverPopup === false) ? true : false)
}
function mouseOut() {
    $( "#currentPopup" ).remove();
    mouseOverPopup = false;
}
