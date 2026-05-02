# unread-slack

When viewing Slack in a browser, a notification will appear in the task tray indicating that there are unread messages other than mentions

ブラウザで Slack を表示しているときにタスクトレイにメンション以外の「未読」メッセージがあることを示す通知を表示します


## Prerequisites

- Web browser
- [Tampermonkey](https://www.tampermonkey.net/) or [Greasemonkey](https://addons.mozilla.org/ja/firefox/addon/greasemonkey/)

Install "Slack Unread Title Notifier.user.js" to extension

## Run

```powershell
git clone https://github.com/sharl/unread-slack.git
cd unread-slack
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
python unread-slack.py
```
