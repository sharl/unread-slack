// ==UserScript==
// @name         Discord Unread Title Notifier
// @namespace    https://github.com/sharl/unread-slack
// @version      1.0.0
// @description  Unread items in the title will be detected
// @author       sharl
// @match        https://discord.com/channels/*
// @icon         https://cdn.prod.website-files.com/6257adef93867e50d84d30e2/6266bc493fb42d4e27bb8393_847541504914fd33810e70a0ea73177e.ico
// @grant        none
// ==/UserScript==

(function() {
    'use strict';

    const updateTitle = () => {
        if (document.title.startsWith('\u2022')) {
            if ('setAppBadge' in navigator) {
                navigator.setAppBadge();
            }
        } else {
            if ('setAppBadge' in navigator) {
                navigator.setAppBadge(0);
            }
        }
    };

    updateTitle();
    const targetTitle = document.querySelector('title');
    
    if (targetTitle) {
        const observer = new MutationObserver(updateTitle);
        observer.observe(targetTitle, { childList: true });
    }
})();
