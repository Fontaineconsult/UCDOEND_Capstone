// ##! Seems to be double accessibility checking for some entries
// ##! Disallow checking for NA isbn



const textbookItem = function (data) {
    let self = this;
    self.isbn = ko.observable(data.isbn);
    self.title = ko.observable(data.title);
    self.course = ko.observable(data.course);
    self.instructor = ko.observable(data.instructor)
    self.accessible = ko.observable('Ready To Check');
    self.validISBN = ko.observable(data.validIsbn);
    self.incompleteISBN = ko.observable(false)
    self.mouseOn = ko.observable(false);
    self.statusCSS = ko.computed(function () {
        switch (self.accessible()) {
            case "Ready To Check":
                return "isReadyToCheck";
            case "Available":
                return "isAccessible";
            case "Need to scan":
                return "isNeedToScan";
            case "Can't Check":
                return "isCantCheck";
            case "Standby":
                return "isStandby";
            case "Checking":
                return "loadPulse"
        }
        
    });
    self.searchStatus = undefined;
    self.checkAccessible = function(){
        self.accessible("Checking")
        if (self.isbn().length === 13) {
            accessibleTextSearch(self.isbn())
        } else {
            self.accessible("Invalid ISBN")
        }

    };
    self.showSearchStatus = function(id, event){
        if (self.searchStatus !== undefined){
            if (self.accessible() === 'Available') {
                console.log(self.searchStatus)
                applySearchStatusPopUp(self.searchStatus, event.currentTarget.id)
            }
        }
    }
    self.hideSearchStatus = function(){
        if (self.searchStatus !== undefined){
            if (self.accessible() === 'Available'){
                hideSearchStatusPopup(self.searchStatus, event.currentTarget.id)
            }
        }
    }
    self.setInitialState = function () {
        let localStorageCheck = checkLocalStorage(self.isbn());
        if (localStorageCheck !== undefined) {
            if (localStorageCheck === false) {
                self.searchStatus = false
                self.accessible('Need to scan')
            } else {
                self.searchStatus = {'isbn': localStorageCheck['results']['isbn'], 'results': localStorageCheck['results']['status']}
                self.accessible('Available')
            }
        }

        if (self.validISBN() === false) {
            self.accessible("Can't Check")
            self.title("Unassigned ISBN (Could not find a match)")
        }
        if (data.title === null && data.isbn.length < 13) {
            self.incompleteISBN(true)
            self.title("Incomplete ISBN (please enter 13 digits)")
        }
        if (self.isbn().length !== 13) {
            self.accessible("Can't Check")
        }

    };
    self.setInitialState()
};

const isbnSearchViewModel = function (type) {
    let self = this;
    self.type = type;
    self.isbn_check_list = [];
    self.course_check_list = [];
    self.availableBookList = ko.observableArray([]);
    self.searchReturnCount = ko.observableArray([]);
    self.textbookList = ko.observableArray([]);
    self.isNan = ko.observable(true);
    self.searchInput = ko.observable("");
    self.searchOutput = ko.computed(function () {
        if (self.isNan() === false){
            let scrubbedInput = self.searchInput().replace(/\D|\s/g, "")
            return scrubbedInput
        } else {
            return self.searchInput()
        }
    });
    self.incompleteISBN = ko.computed(function () {
        if (self.textbookList().length > 0){
            if (self.textbookList()[0].incompleteISBN() === true) {
                return true
            } else {
                return false
            }
        } else {
            return false
        }
    })
    self.validISBN = ko.computed(function () {

        if (self.textbookList().length > 0){
            if (self.textbookList()[0].validISBN() === false) {
                return false
            } else {
                return true
            }
        } else {
            return true
        }


    });
    self.isNanCheck = ko.computed(function () {
        if (isNaN(self.searchInput().charAt(0))) {
            self.isNan(true)
        } else {
            self.isNan(false)
        }
    });
    self.courseColumnVisible = ko.computed(function () {

        if (self.textbookList().length > 0) {
            if (self.textbookList()[0].course()) {
                return true
            } else {
                return false
            }
        } else {
            return false
        }
    }).extend({notify: 'always'});
    self.requestTextbookdata = ko.computed(function () {
        if (self.searchOutput().length > 0 && self.searchOutput().length < 14) {
            if (self.isNan() === false) {
                if (self.searchOutput().length <= 3) {
                    self.textbookList([])
                }
                if (self.searchOutput().length > 3) {
                    queryTextbookList(self.searchOutput(), 'isbn');
                }

            } else {
                if (self.searchOutput().length === 0) {
                    self.textbookList([])
                }
                queryTextbookList(self.searchOutput(), 'course');
            }
        }
        if (self.searchOutput().length === 0){
            self.textbookList([])
            self.searchReturnCount([])
        }


    }, self);
    self.accessible_check = ko.computed(function () {
        self.searchReturnCount([])
        self.textbookList().forEach(function (textbookItem, index) {
            if (self.isbn_check_list.indexOf(textbookItem.isbn()) === -1){
                self.isbn_check_list.push(textbookItem.isbn());
                if (self.isNan() === false){
                    self.searchReturnCount.push(textbookItem.isbn())
                }
            }
            if (self.course_check_list.indexOf(textbookItem.course()) === -1){
                self.course_check_list.push(textbookItem.course());
                if (self.isNan() === true){
                    self.searchReturnCount.push(textbookItem.isbn())
                }

            }
            self.tableAutoRead(false)
        });

        if (self.isNan() === false) {

            if (self.isbn_check_list.length === 1) {

                if (self.isbn_check_list[0].length === 13) {
                    let alreadyChecked = checkLocalStorage(self.isbn_check_list[0]);
                    if (alreadyChecked) {
                        self.accessibleCallback(alreadyChecked)
                    } else {
                        if (self.textbookList()[0].validISBN() === true) {
                            accessibleTextSearch(self.isbn_check_list[0]);
                            self.tableAutoRead(true)
                            self.textbookList().forEach(function (textbookItem) {
                                textbookItem.accessible('Checking')
                            })
                        } else {
                            self.textbookList()[0].accessible("Can't Check")
                        }
                    }
                } else {
                    self.textbookList()[0].accessible('Standby')
                }
            } // procedure for checking isbn
        }

        if (self.isNan() === true) {

            if (self.course_check_list.length === 1) {
                self.isbn_check_list.forEach(function (isbn) {
                    if (isbn.length === 13) {
                        let alreadyChecked = checkLocalStorage(isbn);
                        if (alreadyChecked){
                            self.accessibleCallback(alreadyChecked)
                        } else {
                            accessibleTextSearch(isbn)
                            self.tableAutoRead(true)
                            self.textbookList().forEach(function (textbookItem) {
                                if (textbookItem.isbn() === isbn) {
                                    textbookItem.accessible('Checking')
                                }
                            })
                        }
                    } else {
                        console.log("SOMETHING AINT RIGHT")
                    }
                })
            } // procedure for checking courses
        }


        self.isbn_check_list = [];
        self.course_check_list = []
    },self);
    self.tableAutoRead = ko.observable(false)

    self.ariaReadTable = ko.computed(function () {
        if (self.tableAutoRead() === true) {
            console.log("ASSERTIVE")
            return 'polite'
        } else {
            return 'off'
        }


    },self);
    self.textbookCallback = function(textBookQuery){
        console.log("Textbook Q", textBookQuery)
        if (textBookQuery.length > 0){
            self.textbookList([]);
            textBookQuery.forEach(function (textBookQueryItem) {
                self.textbookList.push(new textbookItem(textBookQueryItem))
            })
        }


    };
    self.accessibleCallback = function(data){
        if (data['status'] === false || data['status'] === 'false'){
            console.log(data)
            self.textbookList().forEach(function (textbookItem) {
                if (textbookItem.isbn() === data.isbn) {
                    textbookItem.searchStatus = {isbn: data.isbn, results: data["results"]}
                    textbookItem.accessible('Need to scan')
                }
            })
        } else {
            self.textbookList().forEach(function (textbookItem) {
                if (textbookItem.isbn() === data.isbn) {
                    textbookItem.searchStatus = {isbn: data.isbn, results: data["results"]}
                    console.log(data["results"])
                    textbookItem.accessible('Available')
                }
            })
        }

    };
};
ko.options.deferUpdates = true;
const activeIndexViewModel = new isbnSearchViewModel('deferred');
ko.applyBindings(activeIndexViewModel);