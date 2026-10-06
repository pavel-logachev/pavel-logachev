<!-- github-profile-readme -->

<p align="center">
  <img src="assets/profile-banner.png" alt="Павел Логачев — внедрение ИИ-агентов. Агент готовит, человек решает." width="100%">
</p>

<p align="center">
  <a href="https://logachev.net/">Сайт</a>
  &nbsp;·&nbsp;
  <a href="https://logachev.net/journal/ii-agent-dlya-generacii-lidov-zakupki/">AI Tender Radar</a>
  &nbsp;·&nbsp;
  <a href="https://logachev.net/journal/podbor-oborudovaniya-po-skladu-ii/">Stock Configurator</a>
  &nbsp;·&nbsp;
  <a href="https://t.me/logachev_ai">Telegram-канал</a>
  &nbsp;·&nbsp;
  <a href="mailto:ai@logachev.net?subject=%D0%A5%D0%BE%D1%87%D1%83%20%D0%BE%D0%B1%D1%81%D1%83%D0%B4%D0%B8%D1%82%D1%8C%20%D0%B7%D0%B0%D0%B4%D0%B0%D1%87%D1%83">Написать</a>
</p>

**Я Павел Логачев, внедряю ИИ-агентов в рабочие процессы бизнеса.** За 20 лет в IT я прошёл путь от инженера (10 лет) до руководителя крупных проектов системной интеграции (ещё 10 лет). За последние полгода я больше 1000 часов работал с ИИ-агентами: делаю с ними собственные продукты и инструменты для продаж, закупок и подготовки документов.

## Проекты

<table>
  <tr>
    <td width="50%" valign="top">
      <h3><a href="https://github.com/pavel-logachev/ai-tender-radar">AI Tender Radar</a></h3>
      <p>Ищет закупки серверов и СХД на Bidzaar. Исследовательский агент читает закупку и документы, проверяет финансовую отчётность заказчика в ФНС. Контакт с телефоном ищет сначала в закупке, затем на сайте заказчика и в открытых источниках. Готовит короткую карточку для менеджера: кому позвонить и о чём поговорить.</p>
      <p>Телефон и имя должны буквально встречаться в прочитанных источниках, это проверяет код. В Telegram поступают только карточки с проверенным телефоном; менеджер выбирает «В работу» или «Мимо».</p>
      <p>Проверить: код открыт · Telegram · выгрузка в Excel</p>
      <p><a href="https://logachev.net/journal/ii-agent-dlya-generacii-lidov-zakupki/">Кейс →</a></p>
    </td>
    <td width="50%" valign="top">
      <h3><a href="https://github.com/pavel-logachev/stock-configurator">Stock Configurator</a></h3>
      <p>MVP для менеджеров и инженеров пресейла: из свободного запроса и остатков дистрибьютора собирает черновик спецификации (BOM), сводку и Excel-отчёт. В результате указаны допущения и открытые вопросы. Инженер проверяет состав и совместимость оборудования.</p>
      <p>Стек: Telegram · FastAPI · PostgreSQL · Excel · детерминированная сверка</p>
      <p><a href="https://logachev.net/journal/podbor-oborudovaniya-po-skladu-ii/">Кейс →</a></p>
    </td>
  </tr>
  <tr>
    <td width="50%" valign="top">
      <h3><a href="https://github.com/pavel-logachev/voice-input">Voice Input</a></h3>
      <p>Диктовка для Windows в трее. Удерживайте горячую клавишу и говорите; после отпускания текст появится в активном поле ввода. Речь распознаёт OpenAI по вашему API-ключу, ключ хранится зашифрованным.</p>
      <p>Стек: .NET 10 · WPF · WASAPI · OpenAI · 146 тестов</p>
      <p><a href="https://github.com/pavel-logachev/voice-input/releases/latest">Релиз 1.0.0 →</a></p>
    </td>
    <td width="50%" valign="top">
      <h3><a href="https://github.com/pavel-logachev/pora">Пора</a></h3>
      <p>Android-приложение для тех, кто принимает лекарства по расписанию. Точные напоминания и история приёмов работают без аккаунта и сервера. Встроен офлайн-справочник ЕСКЛП (23 001 препарат), есть светлая и тёмная тема.</p>
      <p>Проверить: подписанный APK 1.1.0 · Android 7+ · 78 тестов</p>
      <p><a href="https://github.com/pavel-logachev/pora/releases/latest">Релиз →</a></p>
    </td>
  </tr>
  <tr>
    <td colspan="2" valign="top">
      <h3><a href="https://github.com/pavel-logachev/dsh-mobile">DSH Mobile</a></h3>
      <p>Неофициальное Android-приложение для DeepSeek Harness. Открывает чаты всех проектов, отправляет задачи с телефона и показывает ответы агента в реальном времени. Пока агент работает, ему можно дописать сообщение, а уведомление сообщит, что ответ готов. QR-привязка, подключение по Wi‑Fi или Tailscale, без облачного сервера приложения. Модели, инструменты и подписки остаются на компьютере.</p>
      <p>Проверить: подписанный APK 0.5.0 · Android 8+ · 190 + 121 тест · QR-привязка</p>
      <p><a href="https://github.com/pavel-logachev/dsh-mobile/releases/latest">Релиз 0.5.0 →</a> · <a href="https://github.com/pavel-logachev/dsh-mobile/blob/main/docs/SETUP.md">Установка →</a></p>
    </td>
  </tr>
</table>

## Как я работаю

Начинаю с рабочего процесса и одного сценария, который можно довести до использования. Проверяю работу в реальном окружении и поведение при отказах. Код связывает агента с рабочими системами, проверяет результат и ограничивает доступ к данным. Вместе с продуктом готовлю тесты, инструкции по установке или развёртыванию, диагностику и описание ограничений, чтобы запуск можно было повторить.

Постепенно перевожу свои продукты на агентов. В AI Tender Radar один исследовательский агент оказался проще и полезнее длинной цепочки кода: на тех же 16 закупках он находил человека с телефоном в 8 или 9 случаях, прежний код в 3. Следующие на очереди Stock Configurator и AI Proposal Builder.

В публичных репозиториях можно изучить код и запустить продукты. Данные клиентов и закрытые рабочие системы я не публикую.

<p align="center">
  Москва · <a href="https://logachev.net/">logachev.net</a> · <a href="https://t.me/pavel_logachev">@pavel_logachev</a> · <a href="https://t.me/logachev_ai">канал</a>
</p>
