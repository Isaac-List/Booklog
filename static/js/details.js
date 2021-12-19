/**
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

/* jshint esversion: 8 */
/* jshint node: true */
/* jshint browser: true */
'use strict';

async function getBooksInfo() {
    let url = "/api/v1/books";
    return fetch(url)
    .then(response => response.json())
    .catch(error => console.log(error));
}

async function loadTitles(menuID) {
    let titleOptions = await getBooksInfo();

    let menu = document.querySelector(menuID);

    for (const title in titleOptions) {
        let newOption = document.createElement("option");
        newOption.setAttribute("value", titleOptions[title]);
        newOption.innerHTML = title;
        menu.appendChild(newOption);
    }
}

window.onload = function() {
    this.loadTitles("#sel_book");
};
