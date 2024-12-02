
# Riba de Rivers

Welcome to **Riba de Rivers**, a web project that celebrates the natural beauty, cultural richness and community activities of **Riba de Rivers Apartments**  and **Ribadesella region** in Asturias-Spain. This website offers visitors a multilingual experience, allowing them to explore its features in English, French or Spanish. By leveraging modern web technologies such as i18next for translations, this project ensures accessibility for a wider audience. Whether you’re exploring the interactive map, browsing the gallery or reaching out through the contact form, **Riba de Rivers** provides a seamless and engaging experience for all users.

The project is hosted on **GitHub Pages** for static content and **Vercel** for the backend services. Below, we’ll guide you through the project’s features, setup process, multilingual capabilities and the technologies used.

---

## About the Project

**Riba de Rivers** is a comprehensive digital experience designed to highlight the beauty of Riba de Rivers Apartments and the community life of Ribadesella. It features a clean and responsive design that ensures a consistent user experience across devices. The project integrates dynamic functionalities such as a contact form, powered by Flask and SQLite, and an interactive map for exploring the region.

Additionally, to cater to international audiences, the website includes a translation feature using **i18next**. This allows visitors to switch seamlessly between English, French and Spanish. This multilingual capability ensures that the site remains accessible and welcoming to users from diverse linguistic backgrounds.

---

## Features

The website is packed with features designed to enhance the user experience:

1. **Responsive Design**: The site adapts to any screen size, offering a mobile-friendly experience.
2. **Multilingual Support**: Using i18next, the site supports English, French and Spanish with a dynamic language-switching dropdown.
3. **Interactive Map**: Explore the region with an easy-to-navigate interactive map.
4. **Gallery**: View stunning visuals of the natural beauty and cultural highlights of Ribadesella.
5. **Contact Form**: A fully functional contact form powered by a Flask backend on Vercel.
6. **Modern and Minimalist Design**: The layout emphasizes simplicity, making content the main focus.
7. **Dynamic and Static Integration**: The static frontend is hosted on GitHub Pages, while dynamic content is handled by Vercel.

---

## Multilingual Capabilities with i18next

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

Here’s the language-switching logic:
```javascript
function changeLanguage(lang) {
    i18next.changeLanguage(lang, function () {
        updateContent(); // Update the page content
        // Update the dropdown button with the selected language and flag
    });
}
```

---

## Technologies Used

This project combines modern technologies to deliver an accessible, multilingual, and dynamic experience:

### Frontend
- **HTML5 & CSS3**: For semantic structure and styling.
- **Bootstrap**: For responsive layouts and UI components.
- **i18next**: For internationalization and multilingual support.

### Backend
- **Flask**: Handles contact form submissions and other backend logic.
- **SQLite**: A lightweight database for storing form data.
- **Vercel**: Hosts the serverless backend for high availability.

By integrating these technologies, Riba de Rivers ensures a robust and user-friendly experience for visitors.

---

## Live Preview

You can explore the project live on the following platforms:
1. **Static Website**: Hosted on GitHub Pages [here](https://rivers07-maker.github.io/riba-de-rivers/).
2. **Backend Services**: Hosted on Vercel, powering the dynamic features such as the contact form.

---

## Local Development

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

## Contributing

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

## License

This project is licensed under the MIT License. Feel free to use, modify, and distribute it with proper attribution. See the [LICENSE](LICENSE) file for details.

---

## Contact

For inquiries or feedback, reach out to:
- **Name**: Andres Rios
- **GitHub**: [rivers07-maker](https://github.com/rivers07-maker)
- **Website**: [Riba de Rivers](https://rivers07-maker.github.io/riba-de-rivers/)

Enjoy exploring the world of Riba de Rivers!
