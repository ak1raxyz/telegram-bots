# HAL 9000 Nex Generation Bot

https://t.me/hal9000ng_bot

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

## Ref

1. [實戰篇－打造人性化 Telegram Bot](https://medium.com/@zaoldyeck9970/%E5%AF%A6%E6%88%B0%E7%AF%87-%E6%89%93%E9%80%A0%E4%BA%BA%E6%80%A7%E5%8C%96-telegram-bot-ed9bb5b8a6d9)
