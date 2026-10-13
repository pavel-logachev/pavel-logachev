<a href="https://logachev.net/"><picture><source media="(max-width: 767px)" srcset="assets/profile-banner-mobile.png"><img src="assets/profile-banner.png" alt="Павел Логачев. Разбираю задачу. Лично довожу до запуска. Сайты, веб-сервисы, приложения, Telegram-боты и автоматизация — с ИИ или без него."></picture></a>

[Сайт](https://logachev.net/) · [Журнал](https://logachev.net/journal/) · [Telegram-канал](https://t.me/neirogazeta) · [Обсудить задачу](mailto:pavel@logachev.net)

В ИТ 20 лет. Первые 10 занимался сетями, серверами, рабочими местами и информационной безопасностью. Следующие 10 руководил проектами системной интеграции для госсектора и крупных международных компаний: бюджеты от 200 млн ₽, команды 5–10 человек.

Сейчас сам проектирую, разрабатываю и запускаю [сайты](https://logachev.net/sites/), [веб-сервисы](https://logachev.net/services/), [Telegram-боты](https://logachev.net/bots/), [приложения](https://logachev.net/apps/) и [автоматизацию](https://logachev.net/ai/) для бизнеса и частных клиентов. ИИ использую там, где он нужен, — не как обязательную часть каждого проекта.

Здесь — код, релизы и ограничения моих проектов. У каждого открытого проекта написано, что он делает, до какой стадии доведен и с чего начать читать код.

## Приложения

<a href="https://github.com/pavel-logachev/voice-input"><picture><source media="(max-width: 767px)" srcset="assets/card-voice-input-mobile.png"><img src="assets/card-voice-input.png" alt="Voice Input: оверлей диктовки в трех состояниях — «Слушаю», «Распознаю», «Готово»."></picture></a>

**[Voice Input](https://github.com/pavel-logachev/voice-input)** — диктовка в поля ввода Windows: зажать горячую клавишу, говорить, отпустить — текст появится у курсора. Разработал интерфейс и настройки, запись звука, подключение к распознаванию OpenAI, вставку текста и установщик. Для распознавания нужны интернет и API-ключ OpenAI; запросы оплачиваются с аккаунта пользователя.

[![Последний релиз](https://img.shields.io/github/v/release/pavel-logachev/voice-input?style=flat-square&label=%D1%80%D0%B5%D0%BB%D0%B8%D0%B7&labelColor=0b0f14&color=c3f451)](https://github.com/pavel-logachev/voice-input/releases/latest) [![Проверки в CI](https://img.shields.io/github/actions/workflow/status/pavel-logachev/voice-input/ci.yml?branch=main&style=flat-square&label=CI&labelColor=0b0f14)](https://github.com/pavel-logachev/voice-input/actions/workflows/ci.yml) [![Лицензия](https://img.shields.io/github/license/pavel-logachev/voice-input?style=flat-square&label=%D0%BB%D0%B8%D1%86%D0%B5%D0%BD%D0%B7%D0%B8%D1%8F&labelColor=0b0f14&color=7f99ad)](https://github.com/pavel-logachev/voice-input/blob/main/LICENSE)

**Что посмотреть:** [архитектура](https://github.com/pavel-logachev/voice-input/blob/main/docs/ARCHITECTURE.md) · [тесты](https://github.com/pavel-logachev/voice-input/tree/main/tests) · [исследование локальных моделей](https://github.com/pavel-logachev/voice-input/blob/main/docs/MODEL_RESEARCH.md) · [скачать установщик](https://github.com/pavel-logachev/voice-input/releases/latest)

<a href="https://github.com/pavel-logachev/pora"><picture><source media="(max-width: 767px)" srcset="assets/card-pora-mobile.png"><img src="assets/card-pora.png" alt="Пора: история приемов лекарств, экран «Сегодня» с ближайшим приемом и темная тема."></picture></a>

**[Пора](https://github.com/pavel-logachev/pora)** — Android-приложение с расписанием лекарств, напоминаниями и историей приема: основные функции работают без аккаунта и интернета. Спроектировал и разработал приложение, хранение данных на телефоне и необязательную синхронизацию, протестировал и выпустил подписанный APK. В справочнике ЕСКЛП — 23 001 препарат; приложение не назначает лечение и не проверяет совместимость лекарств.

[![Последний релиз](https://img.shields.io/github/v/release/pavel-logachev/pora?style=flat-square&label=%D1%80%D0%B5%D0%BB%D0%B8%D0%B7&labelColor=0b0f14&color=c3f451)](https://github.com/pavel-logachev/pora/releases/latest) [![Проверки в CI](https://img.shields.io/github/actions/workflow/status/pavel-logachev/pora/ci.yml?branch=main&style=flat-square&label=CI&labelColor=0b0f14)](https://github.com/pavel-logachev/pora/actions/workflows/ci.yml) [![Лицензия](https://img.shields.io/github/license/pavel-logachev/pora?style=flat-square&label=%D0%BB%D0%B8%D1%86%D0%B5%D0%BD%D0%B7%D0%B8%D1%8F&labelColor=0b0f14&color=7f99ad)](https://github.com/pavel-logachev/pora/blob/main/LICENSE)

**Что посмотреть:** [архитектура и модель доверия](https://github.com/pavel-logachev/pora/blob/main/docs/ARCHITECTURE.md) · [уведомления](https://github.com/pavel-logachev/pora/tree/main/src/notifications) · [синхронизация](https://github.com/pavel-logachev/pora/tree/main/src/sync) · [скачать APK](https://github.com/pavel-logachev/pora/releases/latest)

<a href="https://github.com/pavel-logachev/dsh-mobile"><picture><source media="(max-width: 767px)" srcset="assets/card-dsh-mobile-mobile.png"><img src="assets/card-dsh-mobile.png" alt="DSH Mobile: список чатов, чат с работающим агентом и выбор проекта."></picture></a>

**[DSH Mobile](https://github.com/pavel-logachev/dsh-mobile)** — неофициальный Android-клиент для DeepSeek Harness, агентной среды на компьютере. С телефона можно открыть чат проекта, поставить задачу и следить за ответом агента в реальном времени; подключение — по Wi-Fi или через Tailscale. Агент работает на компьютере: компьютер и DSH должны быть включены, облачного сервера нет.

[![Последний релиз](https://img.shields.io/github/v/release/pavel-logachev/dsh-mobile?style=flat-square&label=%D1%80%D0%B5%D0%BB%D0%B8%D0%B7&labelColor=0b0f14&color=c3f451)](https://github.com/pavel-logachev/dsh-mobile/releases/latest) [![Проверки в CI](https://img.shields.io/github/actions/workflow/status/pavel-logachev/dsh-mobile/ci.yml?branch=main&style=flat-square&label=CI&labelColor=0b0f14)](https://github.com/pavel-logachev/dsh-mobile/actions/workflows/ci.yml) [![Лицензия](https://img.shields.io/github/license/pavel-logachev/dsh-mobile?style=flat-square&label=%D0%BB%D0%B8%D1%86%D0%B5%D0%BD%D0%B7%D0%B8%D1%8F&labelColor=0b0f14&color=7f99ad)](https://github.com/pavel-logachev/dsh-mobile/blob/main/LICENSE)

**Что посмотреть:** [архитектура](https://github.com/pavel-logachev/dsh-mobile/blob/main/docs/ARCHITECTURE.md) · [протокол](https://github.com/pavel-logachev/dsh-mobile/blob/main/docs/PROTOCOL.md) · [безопасность](https://github.com/pavel-logachev/dsh-mobile/blob/main/docs/SECURITY.md) · [скачать APK](https://github.com/pavel-logachev/dsh-mobile/releases/latest)

## Боты, автоматизация и ИИ-агенты

<a href="https://github.com/pavel-logachev/ai-tender-radar"><picture><source media="(max-width: 767px)" srcset="assets/card-ai-tender-radar-mobile.png"><img src="assets/card-ai-tender-radar.png" alt="AI Tender Radar: макет карточки лида в Telegram на синтетических данных — закупка, срок, заказчик, контакт и начало разговора."></picture></a>

**[AI Tender Radar](https://github.com/pavel-logachev/ai-tender-radar)** — агент-исследователь для отдела продаж: читает документы закупок серверов и СХД на Bidzaar и отчетность ФНС, ищет контакт и готовит карточку в Telegram — что покупают, кому звонить и о чем говорить. Разработал инструменты агента, механическую сверку цифр телефона с прочитанным источником и доставку карточек. На одном наборе из 16 закупок агент нашел контакт человека со сверенным телефоном в 8–9 случаях в зависимости от модели, прежняя цепочка кода — в 3. Это один рабочий прогон, набор не опубликован; актуальность номера менеджер выясняет при звонке.

[![Проверки в CI](https://img.shields.io/github/actions/workflow/status/pavel-logachev/ai-tender-radar/quality.yml?branch=main&style=flat-square&label=CI&labelColor=0b0f14)](https://github.com/pavel-logachev/ai-tender-radar/actions/workflows/quality.yml) [![Лицензия](https://img.shields.io/github/license/pavel-logachev/ai-tender-radar?style=flat-square&label=%D0%BB%D0%B8%D1%86%D0%B5%D0%BD%D0%B7%D0%B8%D1%8F&labelColor=0b0f14&color=7f99ad)](https://github.com/pavel-logachev/ai-tender-radar/blob/main/LICENSE)

**Что посмотреть:** [сверка контактов с источником](https://github.com/pavel-logachev/ai-tender-radar/blob/main/agent_radar/lead_agent/grounding.py) · [архитектура](https://github.com/pavel-logachev/ai-tender-radar/blob/main/docs/ARCHITECTURE.md) · [протокол проверки](https://github.com/pavel-logachev/ai-tender-radar/blob/main/docs/VERIFICATION.md) · [что опубликовано](https://github.com/pavel-logachev/ai-tender-radar/blob/main/docs/PUBLICATION_BOUNDARY.md) · [разбор в журнале](https://logachev.net/journal/ii-agent-dlya-generacii-lidov-zakupki/)

<a href="https://github.com/pavel-logachev/stock-configurator"><picture><source media="(max-width: 767px)" srcset="assets/card-stock-configurator-mobile.png"><img src="assets/card-stock-configurator.png" alt="Stock Configurator: макет листа Excel «КП» на синтетических данных — позиции, суммы и блок «Перед отправкой проверить»."></picture></a>

**[Stock Configurator](https://github.com/pavel-logachev/stock-configurator)** — подбор оборудования по складу дистрибьютора: запрос в Telegram превращается в черновик серверной спецификации в Excel. Настроил подбор моделью, диалог в Telegram и API; код подставляет артикулы, цены и остатки и пересчитывает суммы, а инженер проверяет состав, совместимость и условия поставки. Первая рабочая версия; экономия времени не измерялась.

[![Проверки в CI](https://img.shields.io/github/actions/workflow/status/pavel-logachev/stock-configurator/ci.yml?branch=main&style=flat-square&label=CI&labelColor=0b0f14)](https://github.com/pavel-logachev/stock-configurator/actions/workflows/ci.yml) [![Лицензия](https://img.shields.io/github/license/pavel-logachev/stock-configurator?style=flat-square&label=%D0%BB%D0%B8%D1%86%D0%B5%D0%BD%D0%B7%D0%B8%D1%8F&labelColor=0b0f14&color=7f99ad)](https://github.com/pavel-logachev/stock-configurator/blob/main/LICENSE)

**Что посмотреть:** [архитектура](https://github.com/pavel-logachev/stock-configurator/blob/main/docs/ARCHITECTURE.md) · [сверка со складом](https://github.com/pavel-logachev/stock-configurator/tree/main/app/matching) · [офлайн-оценка](https://github.com/pavel-logachev/stock-configurator/tree/main/app/evaluation) · [что опубликовано](https://github.com/pavel-logachev/stock-configurator/blob/main/docs/PUBLIC_RELEASE_BOUNDARY.md) · [разбор в журнале](https://logachev.net/journal/podbor-oborudovaniya-po-skladu-ii/)

## Клиентские проекты

Код этих проектов закрыт, данные клиентов не публикую.

<a href="https://resnichki.moscow/"><picture><source media="(max-width: 767px)" srcset="assets/card-resnichki-mobile.png"><img src="assets/card-resnichki.png" alt="«Реснички от Юли»: главная страница сайта студии и страница курса на телефоне."></picture></a>

**[«Реснички от Юли»](https://resnichki.moscow/)** — сайт студии наращивания ресниц и [страница курса](https://resnichki.moscow/kurs). Заявки сохраняются на сервере и сразу приходят в Telegram — мне и Юле. Сайт используется для рекламы в Яндекс Директе.

<a href="https://logachev.net/#case-fund-portal"><picture><source media="(max-width: 767px)" srcset="assets/card-fund-portal-mobile.png"><img src="assets/card-fund-portal.png" alt="Портал заявок: кабинет оргкомитета и кабинет предприятия на демонстрационных данных."></picture></a>

**[Портал заявок на поддержку предприятий](https://logachev.net/#case-fund-portal)** — два кабинета одного портала: предприятие подает заявку, оргкомитет ее рассматривает. В кабинете оргкомитета — реестр заявок, очередь задач, этапы рассмотрения, журнал действий и генерация документов; локальный сервис читает PDF и DOCX и предлагает значения полей с указанием места в исходнике, а ключевые решения подтверждает человек. Кабинет оргкомитета — пилот на сервере, кабинет предприятия — прототип; на скриншотах демонстрационные данные.

**[AI Proposal Builder](https://logachev.net/journal/kommercheskoe-predlozhenie-ii/)** — уточняет недостающие данные в Telegram и готовит коммерческое предложение в DOCX и PDF по шаблону компании; цены, условия и отправку подтверждает менеджер. Первая рабочая версия.

## Обсудить задачу

Готовое ТЗ не нужно. Опишите задачу своими словами [на почту](mailto:pavel@logachev.net) или [в Telegram](https://t.me/pavel_logachev) — начну с бесплатного разбора на 20–30 минут. До начала работы согласуем первый объем, стоимость и срок.

Я в Москве. Работаю удаленно с бизнесом и частными лицами по всей России и в СНГ.
