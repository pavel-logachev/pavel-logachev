<a href="https://logachev.net/"><picture><source media="(max-width: 767px)" srcset="assets/profile-banner-mobile.png"><img src="assets/profile-banner.png" alt="Павел Логачев. Вайб-кодер, 20 лет в ИТ. Реализую любое решение: сайт, веб-сервис, Telegram-бот, приложение или ИИ-агент. Код пишу с ИИ-агентами, за результат отвечаю сам."></picture></a>

[Сайт](https://logachev.net/) · [Журнал](https://logachev.net/journal/) · [Telegram-канал](https://t.me/neirogazeta) · [Обсудить задачу](mailto:pavel@logachev.net)

Я вайб-кодер: описываю задачу ИИ-агентам, они пишут код, а я отвечаю за то, чтобы решение работало. Поэтому не привязан к одному языку или платформе — форму и стек выбираю под задачу. Ниже рабочие примеры: приложения для Windows и Android, ИИ-агент, Telegram-бот с API, сайт и веб-портал — на C#, Kotlin, TypeScript и Python.

За плечами 20 лет в ИТ: 10 лет сетей, серверов и информационной безопасности, затем 10 лет руководства проектами системной интеграции с бюджетами от 200 млн ₽. Отсюда привычка проектировать, проверять и доводить до запуска самому, а не верить модели на слово: у открытых проектов ниже есть тесты, CI и честно описанные ограничения.

## Что могу сделать для вас

- **[Сайт или лендинг](https://logachev.net/sites/)** — рассказать о компании, услуге или курсе и принимать заявки. Пример: [«Реснички от Юли»](https://resnichki.moscow/).
- **[Веб-сервис, личный кабинет, внутренняя система](https://logachev.net/services/)** — заявки, документы, этапы и доступ по ролям. Пример: [портал заявок](https://logachev.net/#case-fund-portal).
- **[Telegram-бот](https://logachev.net/bots/)** — заявки, запись, ответы на частые вопросы, связь с CRM, оплатой или ИИ. Пример: [Stock Configurator](https://github.com/pavel-logachev/stock-configurator).
- **[Приложение для Windows или Android](https://logachev.net/apps/)** — отдельный инструмент на компьютере или телефоне. Примеры: [Voice Input](https://github.com/pavel-logachev/voice-input), [Пора](https://github.com/pavel-logachev/pora), [DSH Mobile](https://github.com/pavel-logachev/dsh-mobile).
- **[Автоматизация и ИИ-агенты](https://logachev.net/ai/)** — поиск данных, обработка документов, подготовка материалов с проверкой человеком. Пример: [AI Tender Radar](https://github.com/pavel-logachev/ai-tender-radar).
- **[Нестандартная задача](https://logachev.net/#unusual)** — расчеты, обработка данных, поиск по архиву, обмен между программами. Опишите ее своими словами — скажу, как бы я ее решал.

## Приложения

<a href="https://github.com/pavel-logachev/voice-input"><picture><source media="(max-width: 767px)" srcset="assets/card-voice-input-mobile.png"><img src="assets/card-voice-input.png" alt="Voice Input, приложение для Windows: оверлей диктовки в трех состояниях — «Слушаю», «Распознаю», «Готово»."></picture></a>

**[Voice Input](https://github.com/pavel-logachev/voice-input) — диктовка в любое поле ввода Windows.** Зажали горячую клавишу, сказали фразу, отпустили — текст появился у курсора. Собрал приложение целиком: интерфейс и настройки, запись звука, распознавание через OpenAI, вставку текста и установщик. Выпущен релиз 1.0; автотесты проверяют диктовку, отмену, хранение ключа и вставку. Для распознавания нужны интернет и API-ключ OpenAI.

[![Последний релиз](https://img.shields.io/github/v/release/pavel-logachev/voice-input?style=flat-square&label=%D1%80%D0%B5%D0%BB%D0%B8%D0%B7&labelColor=0b0f14&color=c3f451)](https://github.com/pavel-logachev/voice-input/releases/latest) [![Проверки в CI](https://img.shields.io/github/actions/workflow/status/pavel-logachev/voice-input/ci.yml?branch=main&style=flat-square&label=CI&labelColor=0b0f14)](https://github.com/pavel-logachev/voice-input/actions/workflows/ci.yml) [![Лицензия](https://img.shields.io/github/license/pavel-logachev/voice-input?style=flat-square&label=%D0%BB%D0%B8%D1%86%D0%B5%D0%BD%D0%B7%D0%B8%D1%8F&labelColor=0b0f14&color=7f99ad)](https://github.com/pavel-logachev/voice-input/blob/main/LICENSE)

**Что посмотреть:** [архитектура](https://github.com/pavel-logachev/voice-input/blob/main/docs/ARCHITECTURE.md) · [тесты](https://github.com/pavel-logachev/voice-input/tree/main/tests) · [исследование локальных моделей](https://github.com/pavel-logachev/voice-input/blob/main/docs/MODEL_RESEARCH.md) · [скачать установщик](https://github.com/pavel-logachev/voice-input/releases/latest)

<a href="https://github.com/pavel-logachev/pora"><picture><source media="(max-width: 767px)" srcset="assets/card-pora-mobile.png"><img src="assets/card-pora.png" alt="Пора, приложение для Android: история приемов лекарств, экран «Сегодня» с ближайшим приемом и темная тема."></picture></a>

**[Пора](https://github.com/pavel-logachev/pora) — напоминания о лекарствах на Android без аккаунта и интернета.** Расписание, уведомления с отметкой прямо из шторки, история приема и встроенный справочник ЕСКЛП на 23 001 препарат. Спроектировал и собрал приложение, хранение данных на телефоне, необязательную синхронизацию и сервер для нее; выпустил подписанный APK. 78 автотестов, проверки в CI. Приложение не назначает лечение и не проверяет совместимость лекарств.

[![Последний релиз](https://img.shields.io/github/v/release/pavel-logachev/pora?style=flat-square&label=%D1%80%D0%B5%D0%BB%D0%B8%D0%B7&labelColor=0b0f14&color=c3f451)](https://github.com/pavel-logachev/pora/releases/latest) [![Проверки в CI](https://img.shields.io/github/actions/workflow/status/pavel-logachev/pora/ci.yml?branch=main&style=flat-square&label=CI&labelColor=0b0f14)](https://github.com/pavel-logachev/pora/actions/workflows/ci.yml) [![Лицензия](https://img.shields.io/github/license/pavel-logachev/pora?style=flat-square&label=%D0%BB%D0%B8%D1%86%D0%B5%D0%BD%D0%B7%D0%B8%D1%8F&labelColor=0b0f14&color=7f99ad)](https://github.com/pavel-logachev/pora/blob/main/LICENSE)

**Что посмотреть:** [архитектура и модель доверия](https://github.com/pavel-logachev/pora/blob/main/docs/ARCHITECTURE.md) · [уведомления](https://github.com/pavel-logachev/pora/tree/main/src/notifications) · [синхронизация](https://github.com/pavel-logachev/pora/tree/main/src/sync) · [скачать APK](https://github.com/pavel-logachev/pora/releases/latest)

<a href="https://github.com/pavel-logachev/dsh-mobile"><picture><source media="(max-width: 767px)" srcset="assets/card-dsh-mobile-mobile.png"><img src="assets/card-dsh-mobile.png" alt="DSH Mobile, мобильный клиент для ИИ-агента: список чатов, чат с работающим агентом и выбор проекта."></picture></a>

**[DSH Mobile](https://github.com/pavel-logachev/dsh-mobile) — ИИ-агент на компьютере, задачи с телефона.** Неофициальный Android-клиент для DeepSeek Harness: открыть чат проекта, поставить задачу, следить за ответом в реальном времени и получить уведомление, когда агент закончил. Сделал приложение, плагин для компьютера и защищенное соединение между ними по Wi-Fi или через Tailscale. 190 JVM-тестов и 9 UI-тестов приложения, 121 тест плагина. Компьютер должен быть включен, облачного сервера нет.

[![Последний релиз](https://img.shields.io/github/v/release/pavel-logachev/dsh-mobile?style=flat-square&label=%D1%80%D0%B5%D0%BB%D0%B8%D0%B7&labelColor=0b0f14&color=c3f451)](https://github.com/pavel-logachev/dsh-mobile/releases/latest) [![Проверки в CI](https://img.shields.io/github/actions/workflow/status/pavel-logachev/dsh-mobile/ci.yml?branch=main&style=flat-square&label=CI&labelColor=0b0f14)](https://github.com/pavel-logachev/dsh-mobile/actions/workflows/ci.yml) [![Лицензия](https://img.shields.io/github/license/pavel-logachev/dsh-mobile?style=flat-square&label=%D0%BB%D0%B8%D1%86%D0%B5%D0%BD%D0%B7%D0%B8%D1%8F&labelColor=0b0f14&color=7f99ad)](https://github.com/pavel-logachev/dsh-mobile/blob/main/LICENSE)

**Что посмотреть:** [архитектура](https://github.com/pavel-logachev/dsh-mobile/blob/main/docs/ARCHITECTURE.md) · [протокол](https://github.com/pavel-logachev/dsh-mobile/blob/main/docs/PROTOCOL.md) · [безопасность](https://github.com/pavel-logachev/dsh-mobile/blob/main/docs/SECURITY.md) · [скачать APK](https://github.com/pavel-logachev/dsh-mobile/releases/latest)

## Боты, автоматизация и ИИ-агенты

<a href="https://github.com/pavel-logachev/ai-tender-radar"><picture><source media="(max-width: 767px)" srcset="assets/card-ai-tender-radar-mobile.png"><img src="assets/card-ai-tender-radar.png" alt="AI Tender Radar, ИИ-агент для продаж: макет карточки лида в Telegram на синтетических данных — закупка, срок, заказчик, контакт и начало разговора."></picture></a>

**[AI Tender Radar](https://github.com/pavel-logachev/ai-tender-radar) — ИИ-агент, который готовит менеджеру звонок.** Читает документы закупок серверов и СХД на Bidzaar и отчетность ФНС, ищет контакт и присылает в Telegram карточку: что покупают, кому звонить и о чем говорить. Агенту не верю на слово: код механически сверяет цифры телефона с прочитанным источником. На одном наборе из 16 закупок агент нашел сверенный контакт человека в 8–9 случаях в зависимости от модели, прежняя цепочка кода — в 3. Это один рабочий прогон, набор не опубликован. В репозитории 726 тестов.

[![Проверки в CI](https://img.shields.io/github/actions/workflow/status/pavel-logachev/ai-tender-radar/quality.yml?branch=main&style=flat-square&label=CI&labelColor=0b0f14)](https://github.com/pavel-logachev/ai-tender-radar/actions/workflows/quality.yml) [![Лицензия](https://img.shields.io/github/license/pavel-logachev/ai-tender-radar?style=flat-square&label=%D0%BB%D0%B8%D1%86%D0%B5%D0%BD%D0%B7%D0%B8%D1%8F&labelColor=0b0f14&color=7f99ad)](https://github.com/pavel-logachev/ai-tender-radar/blob/main/LICENSE)

**Что посмотреть:** [сверка контактов с источником](https://github.com/pavel-logachev/ai-tender-radar/blob/main/agent_radar/lead_agent/grounding.py) · [архитектура](https://github.com/pavel-logachev/ai-tender-radar/blob/main/docs/ARCHITECTURE.md) · [протокол проверки](https://github.com/pavel-logachev/ai-tender-radar/blob/main/docs/VERIFICATION.md) · [что опубликовано](https://github.com/pavel-logachev/ai-tender-radar/blob/main/docs/PUBLICATION_BOUNDARY.md) · [разбор в журнале](https://logachev.net/journal/ii-agent-dlya-generacii-lidov-zakupki/)

<a href="https://github.com/pavel-logachev/stock-configurator"><picture><source media="(max-width: 767px)" srcset="assets/card-stock-configurator-mobile.png"><img src="assets/card-stock-configurator.png" alt="Stock Configurator, Telegram-бот и API: макет листа Excel «КП» на синтетических данных — позиции, суммы и блок «Перед отправкой проверить»."></picture></a>

**[Stock Configurator](https://github.com/pavel-logachev/stock-configurator) — Telegram-бот, который собирает черновик спецификации.** Менеджер пишет запрос в Telegram и получает Excel с серверной спецификацией по складу дистрибьютора. Модель подбирает оборудование, а артикулы, цены и остатки подставляет код — он же пересчитывает суммы; состав и совместимость проверяет инженер. Сделал бота, API на FastAPI, коннекторы к складам и отчеты. Первая рабочая версия; экономия времени не измерялась.

[![Проверки в CI](https://img.shields.io/github/actions/workflow/status/pavel-logachev/stock-configurator/ci.yml?branch=main&style=flat-square&label=CI&labelColor=0b0f14)](https://github.com/pavel-logachev/stock-configurator/actions/workflows/ci.yml) [![Лицензия](https://img.shields.io/github/license/pavel-logachev/stock-configurator?style=flat-square&label=%D0%BB%D0%B8%D1%86%D0%B5%D0%BD%D0%B7%D0%B8%D1%8F&labelColor=0b0f14&color=7f99ad)](https://github.com/pavel-logachev/stock-configurator/blob/main/LICENSE)

**Что посмотреть:** [архитектура](https://github.com/pavel-logachev/stock-configurator/blob/main/docs/ARCHITECTURE.md) · [сверка со складом](https://github.com/pavel-logachev/stock-configurator/tree/main/app/matching) · [офлайн-оценка](https://github.com/pavel-logachev/stock-configurator/tree/main/app/evaluation) · [что опубликовано](https://github.com/pavel-logachev/stock-configurator/blob/main/docs/PUBLIC_RELEASE_BOUNDARY.md) · [разбор в журнале](https://logachev.net/journal/podbor-oborudovaniya-po-skladu-ii/)

## Сайты и веб-сервисы для клиентов

Код этих проектов закрыт, данные клиентов не публикую.

<a href="https://resnichki.moscow/"><picture><source media="(max-width: 767px)" srcset="assets/card-resnichki-mobile.png"><img src="assets/card-resnichki.png" alt="«Реснички от Юли», сайт и лендинг: главная страница сайта студии и страница курса на телефоне."></picture></a>

**[«Реснички от Юли»](https://resnichki.moscow/) — сайт студии и лендинг курса.** Сайт студии наращивания ресниц и [страница курса](https://resnichki.moscow/kurs). Заявки сохраняются на сервере и сразу приходят в Telegram — мне и Юле. Сайт работает и используется для рекламы в Яндекс Директе.

<a href="https://logachev.net/#case-fund-portal"><picture><source media="(max-width: 767px)" srcset="assets/card-fund-portal-mobile.png"><img src="assets/card-fund-portal.png" alt="Портал заявок, веб-сервис с кабинетами: кабинет оргкомитета и кабинет предприятия на демонстрационных данных."></picture></a>

**[Портал заявок на поддержку предприятий](https://logachev.net/#case-fund-portal) — веб-сервис с двумя кабинетами.** Предприятие подает заявку, оргкомитет ее рассматривает: реестр заявок, очередь задач, этапы, журнал действий и генерация документов. Локальный сервис читает PDF и DOCX и предлагает значения полей с указанием места в исходнике; ключевые решения подтверждает человек. Кабинет оргкомитета — пилот на сервере, кабинет предприятия — прототип; на скриншотах демонстрационные данные.

**[AI Proposal Builder](https://logachev.net/journal/kommercheskoe-predlozhenie-ii/) — коммерческое предложение из диалога в Telegram.** Система уточняет недостающие данные и готовит КП в DOCX и PDF по шаблону компании; цены, условия и отправку подтверждает менеджер. Первая рабочая версия.

## Как я работаю

1. **Разбираю задачу — бесплатно.** За 20–30 минут обсуждаем, что вы хотите получить, как работаете сейчас и какие есть ограничения. До начала работы согласуем первый объем, стоимость и срок.
2. **Собираю с ИИ-агентами.** Проектирую решение и ставлю задачи агентам; они пишут код, я принимаю результат. Работаю один — задача не теряется между менеджером, аналитиком и разработчиком.
3. **Проверяю и запускаю.** Тесты, CI и ручная приемка, как в проектах выше. Там, где в продукте работает модель, ее ответ проверяет код или человек. Об ограничениях говорю прямо.
4. **Развиваю после запуска.** Обсуждаем, что добавить в следующей версии; развитие и поддержку согласуем отдельно.

## Обсудить задачу

Готовое ТЗ не нужно. Опишите задачу своими словами [на почту](mailto:pavel@logachev.net) или [в Telegram](https://t.me/pavel_logachev) — начну с бесплатного разбора.

Я в Москве. Работаю удаленно с бизнесом и частными лицами по всей России и в СНГ.
