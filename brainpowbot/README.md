# Brain Power Bot

https://t.me/brainpowbot

## How to setWebhook?

Replace the `$bot_token` and `$webhook_url`. [#setWebhook](https://core.telegram.org/bots/api#setwebhook)

```
https://api.telegram.org/bot${bot_token}/setWebhook?url=${webhook_url}
```

## Environment variables

Add `ACCESS_TOKEN` and `VOICE_BASE_URL` in using `heroku` cli command.

```
heroku config:set ACCESS_TOKEN=$bot_token
heroku config:set VOICE_BASE_URL=$voice_base_url
```

The `$voice_base_url` is where you store the static files, for example: `https://example.com/telegram/assets/voice/`.

---

You can use git `http.proxy` and `https.proxy`.

```
git config --global http.proxy http://127.0.0.1:1082
git config --global https.proxy http://127.0.0.1:1082
```
