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
            "further_info": "Further Info",
            "address": "Address",
            "address_full": "Calle Corbeta Oeste, Ribadesella, Asturias-Spain",
            "bus": "Bus",
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
            "further_info": "Informations Complémentaires",
            "address": "Adresse",
            "address_full": "Calle Corbeta Oeste, Ribadesella, Asturies-Espagne",
            "bus": "Bus",
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
            "further_info": "Más Información",
            "address": "Dirección",
            "address_full": "Calle Corbeta Oeste, Ribadesella, Asturias-España",
            "bus": "Autobús",
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
        element.textContent = i18next.t(key);
    });
}