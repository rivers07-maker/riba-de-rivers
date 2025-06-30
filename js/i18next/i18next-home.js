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
                "search": "Search"
            },
            "dropdown": {
                "adults": "Adults",
                "adults_age": "Age: 13 or more",
                "children": "Children",
                "children_age": "Ages: 2 - 12",
                "pets": "Pets",
                "summary_one": "{{count}} guest",
                "summary_other": "{{count}} guests",
                "summaryWithPets_one": "{{count}} guest, {{pets}} pet",
                "summaryWithPets_other": "{{count}} guest, {{pets}} pets",
                "summaryWithPets_pets_one": "{{count}} guests, {{pets}} pet",
                "summaryWithPets_pets_other": "{{count}} guests, {{pets}} pets"
            },
            "description_1": "Discover a cozy retreat just a few minutes’ walk from the beach, in a tranquil area of Ribadesella, Asturias. This thoughtfully designed space is the perfect spot to enjoy the natural beauty of the Asturian coast.",
            "description_2": "Whether you’re seeking a romantic getaway, a family trip, an adventure with friends or a space to work remotely, Riba de Rivers offers the ideal blend of comfort and exploration.",
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
            "hero_title": "Ressentez-vous comme un local",
            "reservation": {
                "arrival": "Arrivée",
                "departure": "Départ",
                "guests": "Invités",
                "search": "Rechercher"
            },
            "dropdown": {
                "adults": "Adultes",
                "adults_age": "Âge : 13 ans ou plus",
                "children": "Enfants",
                "children_age": "Âges : 2 à 12 ans",
                "pets": "Animaux",
                "summary_one": "{{count}} invité",
                "summary_other": "{{count}} invités",
                "summaryWithPets_one": "{{count}} invité, {{pets}} animal",
                "summaryWithPets_other": "{{count}} invité, {{pets}} animaux",
                "summaryWithPets_pets_one": "{{count}} invités, {{pets}} animal",
                "summaryWithPets_pets_other": "{{count}} invités, {{pets}} animaux"
            },
            "description_1": "Découvrez un refuge confortable à quelques minutes de la plage, dans une zone tranquille de Ribadesella, Asturies. Cet espace soigneusement conçu est l'endroit idéal pour profiter de la beauté naturelle de la côte asturienne.",
            "description_2": "Que vous recherchiez une escapade romantique, un voyage en famille, une aventure entre amis ou un espace pour travailler à distance, Riba de Rivers offre la combinaison idéale de confort et d'exploration.",
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
            "hero_title": "Siéntete como un local",
            "reservation": {
                "arrival": "Llegada",
                "departure": "Salida",
                "guests": "Huéspedes",
                "search": "Buscar"
            },
            "dropdown": {
                "adults": "Adultos",
                "adults_age": "Edad: 13 años o más",
                "children": "Niños",
                "children_age": "Edades: 2 a 12 años",
                "pets": "Mascotas",
                "summary_one": "{{count}} huésped",
                "summary_other": "{{count}} huéspedes",
                "summaryWithPets_one": "{{count}} huésped, {{pets}} mascota",
                "summaryWithPets_other": "{{count}} huésped, {{pets}} mascotas",
                "summaryWithPets_pets_one": "{{count}} huéspedes, {{pets}} mascota",
                "summaryWithPets_pets_other": "{{count}} huéspedes, {{pets}} mascotas"
            },
            "description_1": "Descubre un refugio acogedor a pocos minutos de la playa, en una zona tranquila de Ribadesella, Asturias. Este espacio cuidadosamente diseñado es el lugar perfecto para disfrutar de la belleza natural de la costa asturiana.",
            "description_2": "Ya sea que busques una escapada romántica, un viaje familiar, una aventura con amigos o un espacio para trabajar de forma remota, Riba de Rivers ofrece la combinación ideal de comodidad y exploración.",
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

        // Update translated content and summary
        updateContent();
        updateSummary(); // Important for dropdown summary like "2 guests, 1 pet"

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

// Update content
function updateContent() {
    document.querySelectorAll('[data-i18n]').forEach(function (element) {
        const key = element.getAttribute('data-i18n');
        if (element.tagName.toLowerCase() === 'input' || element.tagName.toLowerCase() === 'textarea') {
            element.placeholder = i18next.t(key);
        } else {
            element.textContent = i18next.t(key);
        }
    });
}

// Update summary
function updateSummary(customGuests) {
    const g = customGuests || window.guests || { adults: 1, children: 0, pets: 0 };
    if (!g) return;
    const totalGuests = (g.adults || 0) + (g.children || 0);
    const pets = g.pets || 0;
    let summaryText;
    if (pets > 0) {
        if (totalGuests === 1 && pets === 1) {
            summaryText = i18next.t("dropdown.summaryWithPets_one", { count: totalGuests, pets });
        } else if (totalGuests === 1 && pets > 1) {
            summaryText = i18next.t("dropdown.summaryWithPets_pets_other", { count: totalGuests, pets });
        } else if (totalGuests > 1 && pets === 1) {
            summaryText = i18next.t("dropdown.summaryWithPets_pets_one", { count: totalGuests, pets });
        } else if (totalGuests > 1 && pets > 1) {
            summaryText = i18next.t("dropdown.summaryWithPets_pets_other", { count: totalGuests, pets });
        }
    } else {
        summaryText = i18next.t("dropdown.summary", { count: totalGuests });
    }
    // Fix: singular/plural for guests and pets
    summaryText = summaryText.replace('guests', totalGuests === 1 ? 'guest' : 'guests');
    summaryText = summaryText.replace('huéspedes', totalGuests === 1 ? 'huésped' : 'huéspedes');
    summaryText = summaryText.replace('pets', pets === 1 ? 'pet' : 'pets');
    summaryText = summaryText.replace('mascotas', pets === 1 ? 'mascota' : 'mascotas');
    // French singular/plural fix
    summaryText = summaryText.replace('invités', totalGuests === 1 ? 'invité' : 'invités');
    summaryText = summaryText.replace('animaux', pets === 1 ? 'animal' : 'animaux');
    const summaryElement = document.getElementById("guest-summary");
    if (summaryElement) {
        summaryElement.textContent = summaryText;
        summaryElement.style.display = "inline";
    }
}