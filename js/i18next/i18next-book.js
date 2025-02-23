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
            "book_title": "Book your stay",
            "who_button": "Who's coming?",
            "when_button": "When's your trip?",
            "payment_button": "Payment method",
            "who": {
                "name": "Name",
                "phone": "Phone",
                "email": "Email",
                "guests1": "1 Guest",
                "guests2": "2 Guests",
                "guests3": "3 Guests",
                "guests4": "4 Guests",
                "pets": "Pets"
            },
            "when": {
                "arrival": "Arrival",
                "departure": "Departure"
            },
            "pay": {
                "name": "Name",
                "card": "Card Number",
                "expiration": "Expiration (mm/yy)",
                "security": "Security Code",
            },
            "book": "Book",
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
            "book_title": "Réservez votre séjour",
            "who_button": "Qui vient?",
            "when_button": "Quand partez-vous?",
            "payment_button": "Méthode de paiement",
            "who": {
                "name": "Nom",
                "phone": "Téléphone",
                "email": "Email",
                "guests1": "1 Invité",
                "guests2": "2 Invités",
                "guests3": "3 Invités",
                "guests4": "4 Invités",
                "pets": "Animaux de compagnie"
            },
            "when": {
                "arrival": "Arrivée",
                "departure": "Départ"
            },
            "pay": {
                "name": "Nom",
                "card": "Numéro de carte",
                "expiration": "Expiration (mm/aa)",
                "security": "Code de sécurité",
            },
            "book": "Réserver",
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
            "book_title": "Reserve su estancia",
            "who_button": "¿Quién viene?",
            "when_button": "¿Cuándo es tu viaje?",
            "payment_button": "Método de pago",
            "who": {
                "name": "Nombre",
                "phone": "Teléfono",
                "email": "Correo electrónico",
                "guests1": "1 Invitado",
                "guests2": "2 Invitados",
                "guests3": "3 Invitados",
                "guests4": "4 Invitados",
                "pets": "Mascotas"
            },
            "when": {
                "arrival": "Llegada",
                "departure": "Salida"
            },
            "pay": {
                "name": "Nombre",
                "card": "Número de tarjeta",
                "expiration": "Vencimiento (mm/aa)",
                "security": "Código de seguridad",
            },
            "book": "Reservar",
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