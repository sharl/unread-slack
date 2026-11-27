// ==UserScript==
// @name         Yahoo Radar Keep Fullscreen
// @namespace    https://github.com/sharl/unread-slack
// @version      0.3.0
// @description  Keep Yahoo! Weather rain radar in full-screen map mode. If the site layer drops back to normal mode, click the "全画面表示" button again.
// @match        https://weather.yahoo.co.jp/weather/zoomradar/*
// @icon         https://www.google.com/s2/favicons?sz=64&domain=yahoo.co.jp
// @grant        none
// @run-at       document-idle
// ==/UserScript==

(function() {
    'use strict';

    const ENTER_IMG = 'img[alt="全画面表示"]';
    const EXIT_IMG = 'img[alt="全画面地図を終了する"]';

    const pad = (n) => String(n).padStart(2, '0');

    const timestamp = () => {
        const d = new Date();
        return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())} ${pad(d.getHours())}:${pad(d.getMinutes())}:${pad(d.getSeconds())}`;
    };

    const log = (message) => console.log(`[RadarKeepFullscreen] ${timestamp()} ${message}`);

    const isVisible = (el) => !!(el && (el.offsetWidth || el.offsetHeight || el.getClientRects().length));

    const describe = (label) => {
        const enter = document.querySelector(ENTER_IMG);
        const exit = document.querySelector(EXIT_IMG);
        log(`${label}: enter found=${!!enter} visible=${isVisible(enter)}, exit found=${!!exit} visible=${isVisible(exit)}`);
    };

    let lastClickAt = 0;

    log('loaded');
    describe('initial state');

    const keepFullscreen = () => {
        // Judge by the enter button: only click when it is actually visible (normal mode).
        // The exit button may exist in the DOM even when hidden, so do not use its presence alone.
        const img = document.querySelector(ENTER_IMG);
        if (!isVisible(img)) return;

        // Cooldown: do not click again while the mode is switching.
        const now = Date.now();
        if (now - lastClickAt < 10000) return;
        lastClickAt = now;

        log('entering full-screen map mode');
        img.closest('a')?.click();
    };

    setInterval(keepFullscreen, 5000);
    keepFullscreen();
})();
