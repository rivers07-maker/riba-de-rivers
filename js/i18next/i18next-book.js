const resources = {
    en: {
        translation: {
            brand_title: "Riba de Rivers",
            brand_subtitle: "Apartments",
            book_now: "Book Now",
            nav: {
                home: "Home",
                overview: "Overview",
                map: "Map",
                gallery: "Gallery",
                book: "Book Now",
                reviews: "Reviews",
                contact: "Contact"
            },
            calendar: {
                where: "Where",
                arrival: "Arrival",
                departure: "Departure",
                who: "Who"
            },
            dropdown: {
                adults: "Adults",
                adults_age: "Age: 13 or more",
                children: "Children",
                children_age: "Ages: 2 - 12",
                pets: "Pets",
                summary: "{{count}} guest",
                summary_plural: "{{count}} guests",
                summaryWithPets: "{{count}} guest, {{pets}} pet",
                summaryWithPets_plural: "{{count}} guests, {{pets}} pets"
            },
            info: {
                name: "Name",
                phone: "Phone",
                email: "Email"
            },
            pay: "Pay",
            footer: {
                copyright: "2024 Riba de Rivers Apartments. All rights reserved."
            }
        }
    },
    fr: {
        translation: {
            brand_title: "Riba de Rivers",
            brand_subtitle: "Appartements",
            book_now: "Réserver",
            nav: {
                home: "Accueil",
                overview: "Aperçu",
                map: "Carte",
                gallery: "Galerie",
                book: "Réserver",
                reviews: "Avis",
                contact: "Contact"
            },
            calendar: {
                where: "Où",
                arrival: "Arrivée",
                departure: "Départ",
                who: "Qui"
            },
            dropdown: {
                adults: "Adultes",
                adults_age: "Âge : 13 ans ou plus",
                children: "Enfants",
                children_age: "Âges : 2 à 12 ans",
                pets: "Animaux",
                summary: "{{count}} invité",
                summary_plural: "{{count}} invités",
                summaryWithPets: "{{count}} invité, {{pets}} animal",
                summaryWithPets_plural: "{{count}} invités, {{pets}} animaux"
            },
            info: {
                name: "Nom",
                phone: "Téléphone",
                email: "Email"
            },
            pay: "Payer",
            footer: {
                copyright: "2024 Riba de Rivers Appartements. Tous droits réservés."
            }
        }
    },
    es: {
        translation: {
            brand_title: "Riba de Rivers",
            brand_subtitle: "Apartamentos",
            book_now: "Reservar",
            nav: {
                home: "Inicio",
                overview: "Visión general",
                map: "Mapa",
                gallery: "Galería",
                book: "Reservar",
                reviews: "Reseñas",
                contact: "Contacto"
            },
            calendar: {
                where: "Dónde",
                arrival: "Llegada",
                departure: "Salida",
                who: "Quién"
            },
            dropdown: {
                adults: "Adultos",
                adults_age: "Edad: 13 años o más",
                children: "Niños",
                children_age: "Edades: 2 a 12 años",
                pets: "Mascotas",
                summary: "{{count}} huésped",
                summary_plural: "{{count}} huéspedes",
                summaryWithPets: "{{count}} huésped, {{pets}} mascota",
                summaryWithPets_plural: "{{count}} huéspedes, {{pets}} mascotas"
            },
            info: {
                name: "Nombre",
                phone: "Teléfono",
                email: "Correo electrónico"
            },
            pay: "Pagar",
            footer: {
                copyright: "2024 Riba de Rivers Apartamentos. Todos los derechos reservados."
            }
        }
    }
};

// Initialize i18next
i18next.init({
    lng: "en",
    debug: true,
    fallbackLng: "en",
    resources,
    interpolation: {
        escapeValue: false
    },
    pluralSeparator: '_',
    saveMissing: true
}, function () {
    updateSummary();
    updateContent();
    document.dispatchEvent(new Event("i18nReady"));
});

// Change language
function changeLanguage(lang) {
    i18next.changeLanguage(lang, function () {
        updateContent();
        updateSummary(); // Important to update plural-sensitive text too

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

        selectedLangElement.innerHTML = `<span class="flag-icon ${flagClass}"></span> ${languageText}`;
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

// ✅ FIXED: Update the translated guest summary with proper plural logic
function updateSummary(customGuests) {
    const g = customGuests || guests; // use passed guests or global
    if (!g) return; // prevent crash

    const totalGuests = (g.adults || 0) + (g.children || 0);
    const pets = g.pets || 0;

    const summaryText = pets > 0
        ? i18next.t("dropdown.summaryWithPets", { count: totalGuests, pets: pets })
        : i18next.t("dropdown.summary", { count: totalGuests });

    const summaryElement = document.getElementById("guest-summary");
    if (summaryElement) {
        summaryElement.textContent = summaryText;
        summaryElement.style.display = "inline";
    }
}
