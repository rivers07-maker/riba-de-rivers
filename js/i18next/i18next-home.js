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
            "hero_title": "Feel like a local",
            "reservation": {
                "arrival": "Arrival",
                "departure": "Departure",
                "guests": "Guests",
                "adults": "Adults",
                "age_1": "Age: 13 or more",
                "children": "Children",
                "age_2": "Ages: 2 - 12",
                "pets": "Pets",
                "search": "Search"
            },
            "description_1": "Discover a cozy retreat just a few minutes’ walk from the beach, in a tranquil area of Ribadesella, Asturias.",
            "description_2": "Whether you’re seeking a romantic getaway or a family trip, Riba de Rivers offers the ideal combination of comfort and exploration.",
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
            "hero_title": "Ressentez-vous comme un local",
            "reservation": {
                "arrival": "Arrivée",
                "departure": "Départ",
                "guests": "Invités",
                "adults": "Adultes",
                "age_1": "Âge: 13 ans ou plus",
                "children": "Enfants",
                "age_2": "Âges: 2 - 12",
                "pets": "Animaux de compagnie",
                "search": "Rechercher"
            },
            "description_1": "Découvrez un refuge confortable à quelques minutes de la plage, dans une zone tranquille de Ribadesella, Asturies.",
            "description_2": "Que vous recherchiez une escapade romantique ou un voyage en famille, Riba de Rivers offre le confort et l'exploration idéals.",
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
            "hero_title": "Siéntete como un local",
            "reservation": {
                "arrival": "Llegada",
                "departure": "Salida",
                "guests": "Huéspedes",
                "adults": "Adultos",
                "age_1": "Edad: 13 o más",
                "children": "Niños",
                "age_2": "Edades: 2 - 12",
                "pets": "Mascotas",
                "search": "Buscar"
            },
            "description_1": "Descubre un refugio acogedor a pocos minutos de la playa, en una zona tranquila de Ribadesella, Asturias.",
            "description_2": "Ya sea que busques una escapada romántica o un viaje familiar, Riba de Rivers ofrece la combinación ideal de comodidad y exploración.",
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
        element.textContent = i18next.t(key);
    });
}