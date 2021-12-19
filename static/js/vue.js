/**
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

/* jshint esversion: 8 */
/* jshint node: true */
/* jshint browser: true */
'use strict';

const details = new Vue({
    el: "#deeets",
    data: {
        title: book_data["title"],
        author: book_data["author"],
        page_count: book_data["page_count"],
        pub_year: book_data["pub_year"],
        description: book_data["description"]
    }
});