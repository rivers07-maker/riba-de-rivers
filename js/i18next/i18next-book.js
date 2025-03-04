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
            "calendar": {
                "where": "Where",
                "arrival": "Arrival",
                "departure": "Departure",
                "who": "Who"
            },
            "info": {
                "name": "Name",
                "phone": "Phone",
                "email": "Email"
            },
            "pay": "Pay",
            "footer": {
                "copyright": "2024 Riba de Rivers Apartments. All rights reserved."
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
            "calendar": {
                "where": "Où",
                "arrival": "Arrivée",
                "departure": "Départ",
                "who": "Qui"
            },
            "info": {
                "name": "Nom",
                "phone": "Téléphone",
                "email": "Email"
            },
            "pay": "Payer",
            "footer": {
                "copyright": "2024 Riba de Rivers Appartements. Tous droits réservés."
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
            "calendar": {
                "where": "Dónde",
                "arrival": "Llegada",
                "departure": "Salida",
                "who": "Quién"
            },
            "info": {
                "name": "Nombre",
                "phone": "Teléfono",
                "email": "Correo electrónico"
            },
            "pay": "Pagar",
            "footer": {
                "copyright": "2024 Riba de Rivers Apartamentos. Todos los derechos reservados."
            }
        }
    }
};


// Initialize i18next
i18next.use(i18nextBrowserLanguageDetector).init({
    resources, // your translation resources
    fallbackLng: 'en',
    debug: true
}, function (err, t) {
    updateContent();
});

// Change language and update the button with the selected language and flag
function changeLanguage(lang) {
    i18next.changeLanguage(lang, function () {
        updateContent(); // Update the content on the page

        // Update the button with the correct flag and language
        const selectedLangElement = document.getElementById('languageDropdownDesktop');

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
            default:
                flagClass = 'flag-icon-gb';
                languageText = 'EN';
        }

        // Update the button's inner HTML
        selectedLangElement.innerHTML = `<span class="flag-icon ${flagClass}"></span> ${languageText}`;
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