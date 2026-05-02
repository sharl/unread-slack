// ==UserScript==
// @name         Slack Unread Title Notifier
// @namespace    https://github.com/sharl/unread-slack
// @version      1.0.0
// @description  Unread items in the sidebar will be detected and an asterisk (*) will be added to their titles
// @author       sharl
// @match        https://app.slack.com/*
// @icon         https://www.google.com/s2/favicons?sz=64&domain=slack.com
// @grant        none
// ==/UserScript==

(function() {
    'use strict';

    const updateTitle = () => {
        // Find a class name that indicates "just an unread message" other than a mention.
        // This may change due to updates to Slack's specifications, but this is just one example at the moment.
        const hasUnread = document.querySelector('.p-unread_dot');

        if (hasUnread && !document.title.startsWith('(*)')) {
            document.title = '(*) ' + document.title;
        } else if (!hasUnread && document.title.startsWith('(*)')) {
            document.title = document.title.replace('(*) ', '');
        }
    };

    const observer = new MutationObserver(updateTitle);
    observer.observe(document.body, { childList: true, subtree: true });
})();
