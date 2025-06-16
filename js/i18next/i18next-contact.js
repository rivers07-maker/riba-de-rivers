// Load translations
const resources = {
    en: {
        translation: {
            "brand_title": "Riba de Rivers",
            "brand_subtitle": "Apartments",
            "book_now": "Book Now",
            "nav": {
                "home": "Home",
                "overview": "Overview",
                "map": "Map",
                "gallery": "Gallery",
                "book": "Book Now",
                "reviews": "Reviews",
                "contact": "Contact"
            },
            "contact_title": "About host",
            "contact": "Contact",
            "placeholder": {
                "name": "Name",
                "email": "Email",
                "comment": "Any additional comments?"
            },
            "successfully": "Your message has been sent successfully!",
            "send": "Send",
            "footer": {
                "copyright": "2025 Riba de Rivers Apartments. All rights reserved."
            }
        }
    },
    fr: {
        translation: {
            "brand_title": "Riba de Rivers",
            "brand_subtitle": "Appartements",
            "book_now": "Réserver",
            "nav": {
                "home": "Accueil",
                "overview": "Aperçu",
                "map": "Carte",
                "gallery": "Galerie",
                "book": "Réserver",
                "reviews": "Avis",
                "contact": "Contact"
            },
            "contact_title": "À propos de l'hôte",
            "contact": "Contact",
            "placeholder": {
                "name": "Nom",
                "email": "Email",
                "comment": "Des commentaires supplémentaires?"
            },
            "successfully": "Votre message a été envoyé avec succès!",
            "send": "Envoyer",
            "footer": {
                "copyright": "2025 Riba de Rivers Appartements. Tous droits réservés."
            }
        }
    },
    es: {
        translation: {
            "brand_title": "Riba de Rivers",
            "brand_subtitle": "Apartamentos",
            "book_now": "Reservar",
            "nav": {
                "home": "Inicio",
                "overview": "Visión general",
                "map": "Mapa",
                "gallery": "Galería",
                "book": "Reservar",
                "reviews": "Reseñas",
                "contact": "Contacto"
            },
            "contact_title": "Sobre el anfitrión",
            "contact": "Contacto",
            "placeholder": {
                "name": "Nombre",
                "email": "Correo electrónico",
                "comment": "¿Algún comentario adicional?"
            },
            "successfully": "¡Su mensaje ha sido enviado con éxito!",
            "send": "Enviar",
            "footer": {
                "copyright": "2025 Riba de Rivers Apartamentos. Todos los derechos reservados."
            }
        }
    }
};

// Get saved language from localStorage or default to 'en'
const savedLang = localStorage.getItem('selectedLanguage') || 'es';

// Initialize i18next
i18next.init({
    lng: savedLang,
    debug: true,
    fallbackLng: "es",
    resources,
    interpolation: {
        escapeValue: false
    },
    pluralSeparator: '_',
    saveMissing: true
}, function () {
    // Set language UI and translations based on saved language
    changeLanguage(savedLang);

    // Once i18n is ready, notify the rest of the page
    document.dispatchEvent(new Event("i18nReady"));
});

// Change language and update UI
function changeLanguage(lang) {
    i18next.changeLanguage(lang, function () {
        // Save selected language to localStorage
        localStorage.setItem('selectedLanguage', lang);

        // Update translated content
        updateContent();

        // Update flag icon and language label in dropdown button
        const selectedLangElement = document.getElementById('languageDropdown');

        let flagClass;
        let languageText;

        switch (lang) {
            case 'en':
                flagClass = 'flag-icon-gb';
                languageText = 'EN';
                break;
            case 'es':
                flagClass = 'flag-icon-es';
                languageText = 'ES';
                break;
            case 'fr':
                flagClass = 'flag-icon-fr';
                languageText = 'FR';
                break;
        }

        if (selectedLangElement) {
            selectedLangElement.innerHTML = `<span class="flag-icon ${flagClass}"></span> ${languageText}`;
        }
    });
}

// Update the content on the page
function updateContent() {
    document.querySelectorAll('[data-i18n]').forEach(function (element) {
        const key = element.getAttribute('data-i18n');

        // Check if the element is an input or textarea
        if (element.tagName.toLowerCase() === 'input' || element.tagName.toLowerCase() === 'textarea') {
            element.placeholder = i18next.t(key); // Update placeholder
        } else {
            element.textContent = i18next.t(key); // Update text content for other elements
        }
    });
}