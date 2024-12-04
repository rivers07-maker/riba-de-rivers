# RIBA DE RIVERS

## Video Demo:  <URL HERE>

## Description:

Welcome to **Riba de Rivers**, a comprehensive web platform dedicated to showcasing a unique vacation apartment experience in the picturesque Ribadesella region of Asturias, Spain. This website serves as a digital gateway to an exceptional holiday destination, offering potential guests an immersive preview of a charming vacation rental that seamlessly blends modern comfort with the breathtaking natural and cultural landscape of Northern Spain.

While the primary focus is on presenting our vacation apartment as an ideal accommodation choice, the website also celebrates the extraordinary environment surrounding the property. Visitors will discover the rich tapestry of Ribadesella's natural beauty, cultural heritage and vibrant community activities, providing context and inspiration for their potential stay.

The website offers a multilingual experience, allowing visitors to explore its features in English, French or Spanish. By leveraging modern web technologies such as i18next for translations, this project ensures accessibility for a diverse, international audience. Whether you're exploring the interactive map, browsing the gallery or reaching out through the contact form, **Riba de Rivers** provides an engaging digital experience.

The project is hosted on **GitHub Pages** for static content, with the backend currently configured for local development.

---

## Features:

The website is packed with features designed to enhance the user experience:

1. **Responsive Design**: The site adapts to any screen size, offering a mobile-friendly experience.
2. **Multilingual Support**: Using i18next, the site supports English, French and Spanish with a dynamic language-switching dropdown.
3. **Interactive Map**: Explore the region with an easy-to-navigate interactive map.
4. **Gallery**: View stunning visuals of the vacation apartment and the natural beauty of Ribadesella.
5. **Contact Form**: A fully functional contact form powered by a local Flask backend.
6. **Modern and Minimalist Design**: The layout emphasizes simplicity, making content the main focus.
7. **Static Frontend**: Hosted on GitHub Pages for reliable and fast content delivery.

---

## Multilingual Capabilities with i18next:

### Overview

Riba de Rivers incorporates i18next, a popular internationalization framework, to make the website accessible in three languages: English, French and Spanish. Visitors can easily switch between these languages using a dropdown menu that displays the selected language and corresponding flag.

### How It Works

- **Translation Resources**: A JSON-like structure defines translations for key elements of the website in all three languages.
- **Dynamic Updates**: The text on the page updates automatically based on the selected language, using the `i18next.changeLanguage` method.
- **Fallback Language**: If a translation is missing for a specific language, the site defaults to English.

### Example Translation Resources

The translations are defined as follows:
```javascript
const resources = {
    en: { translation: { /* English translations */ } },
    fr: { translation: { /* French translations */ } },
    es: { translation: { /* Spanish translations */ } }
};
```

Each key corresponds to a piece of text on the website, ensuring seamless translation updates.

### Language Switching Functionality

A dropdown menu allows users to select their preferred language. When a language is chosen, the following happens:
1. **Language Change**: The `i18next.changeLanguage` function switches to the selected language.
2. **Flag Update**: The dropdown button updates to show the corresponding flag and language code (e.g., "EN", "FR", "ES").
3. **Content Refresh**: All elements on the page with a `data-i18n` attribute are updated dynamically using the `updateContent` function.

Here's the language-switching logic:
```javascript
function changeLanguage(lang) {
    i18next.changeLanguage(lang, function () {
        updateContent(); // Update the page content
        // Update the dropdown button with the selected language and flag
    });
}
```

---

## Technologies Used:

This project combines modern technologies to deliver an accessible, multilingual, and dynamic experience:

### Frontend
- **HTML5 & CSS3**: For semantic structure and styling.
- **Bootstrap**: For responsive layouts and UI components.
- **i18next**: For internationalization and multilingual support.

### Backend
- **Flask**: Handles contact form submissions and other backend logic.
- **SQLite**: A lightweight database for storing form data.
- **Local Development**: Backend services are currently configured for local setup due to file-system SQLite limitations.

By integrating these technologies, Riba de Rivers ensures a robust and user-friendly experience for visitors.

---

## Live Preview:

You can explore the project live on the following platform:
1. **Static Website**: Hosted on GitHub Pages [here](https://rivers07-maker.github.io/riba-de-rivers/).

Note: Backend services are currently configured for local development only.

---

## Local Development:

To set up the project locally, follow these steps:

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/rivers07-maker/riba-de-rivers.git
    cd riba-de-rivers
    ```

2. **Static Website**: Open the `index.html` file in your browser.

3. **Backend**:
    - Install dependencies:
        ```bash
        pip install -r backend/requirements.txt
        ```
    - Run the Flask server:
        ```bash
        python backend/app.py
        ```
    - Access the site at `http://localhost:5000`.

4. **Enable Translations**:
    - Include the i18next resources in your frontend code.
    - Make sure all translatable elements have the `data-i18n` attribute.

---

## Contributing:

Contributions are welcome! To contribute:
1. Fork the repository.
2. Create a branch for your changes:
    ```bash
    git checkout -b feature-name
    ```
3. Commit your updates:
    ```bash
    git commit -m "Description of changes"
    ```
4. Push your branch and open a pull request.

Your contributions can enhance Riba de Rivers for everyone!

---

## License:

This project is licensed under the MIT License. Feel free to use, modify, and distribute it with proper attribution. See the [LICENSE](LICENSE) file for details.

---

## Contact:

For inquiries or feedback, reach out to:
- **Name**: Andres Rios
- **GitHub**: [rivers07-maker](https://github.com/rivers07-maker)
- **Website**: [Riba de Rivers](https://rivers07-maker.github.io/riba-de-rivers/)

Enjoy exploring the world of Riba de Rivers!
