# PN-Updater

A simple GUI application designed to update other programs by fetching update information from a local configuration file.

## Features

-   **GUI Interface:** A clear and user-friendly graphical interface built with PyQt5.
-   **Update Checks:** Automatically checks for updates based on a local configuration file.
-   **Font Fallback:** Ensures a consistent UI appearance across different systems by using a font fallback chain (Segoe UI, Inter, Arial, Noto Sans).
-   **User Notifications:** Provides native system notifications about the update status (e.g., "Update not required").

## Technology Stack

-   **Language:** Python
-   **GUI Framework:** PyQt5
-   **Dependencies:**
    -   `PyQt5`: For the graphical user interface.
    -   `PyYAML`: For parsing the configuration file.

## Configuration

The application is configured via a YAML file located in the same directory. This file contains the necessary information for the updater to check for and apply updates.

## Building from Source

To build the executable from the source code, you will need Python, the dependencies listed in `requirements.txt`, and `pyinstaller`.

1.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    pip install pyinstaller
    ```

2.  **Build the application:**
    The project includes a `updater.spec` file that contains the correct build configuration. Use the following command to build the executable:
    ```bash
    pyinstaller updater.spec
    ```
    The final executable will be located in the `dist/` directory.

---
---

# PN-Updater (Русский)

Простое графическое приложение, предназначенное для обновления других программ путем получения информации об обновлениях из локального файла конфигурации.

## Особенности

-   **Графический интерфейс:** Понятный и удобный графический интерфейс, созданный с помощью PyQt5.
-   **Проверка обновлений:** Автоматически проверяет наличие обновлений на основе локального файла конфигурации.
-   **Резервные шрифты (Font Fallback):** Обеспечивает единообразный внешний вид интерфейса на разных системах благодаря использованию цепочки резервных шрифтов (Segoe UI, Inter, Arial, Noto Sans).
-   **Уведомления для пользователя:** Выводит системные уведомления о статусе обновления (например, "Обновление не требуется").

## Технологии

-   **Язык:** Python
-   **GUI Фреймворк:** PyQt5
-   **Зависимости:**
    -   `PyQt5`: Для графического интерфейса.
    -   `PyYAML`: Для обработки файла конфигурации.

## Конфигурация

Приложение настраивается через YAML-файл, расположенный в той же директории. Этот файл содержит необходимую информацию для проверки и применения обновлений.

## Сборка из исходного кода

Для сборки исполняемого файла из исходного кода вам понадобится Python, зависимости из `requirements.txt` и `pyinstaller`.

1.  **Установите зависимости:**
    ```bash
    pip install -r requirements.txt
    pip install pyinstaller
    ```

2.  **Соберите приложение:**
    Проект включает файл `updater.spec`, который содержит правильную конфигурацию сборки. Используйте следующую команду для сборки:
    ```bash
    pyinstaller updater.spec
    ```
    Готовый исполняемый файл будет находиться в директории `dist/`.