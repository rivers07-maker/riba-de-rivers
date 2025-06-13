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
                "contact": "Contact",
                "description": "Description",
                "pictures": "Pictures",
                "amenities": "Amenities",
                "rules": "House Rules",
                "policy": "Policy and Notes"
            },
            "desc": {
                "description_title": "Description",
                "guests": "4 Guests",
                "bedroom": "1 Bedroom",
                "beds": "2 Beds",
                "bathroom": "1 Bathroom",
                "welcome": 'Welcome to "Riba de Rivers"',
                "welcome_text_1": "Our cozy apartment 10 minutes walk from the beach is perfect for a getaway as a couple, with friends or family. Sleeps 4, it has a room, full bathroom, equipped kitchen, living room with sofa bed, private terrace and parking for cars and bicycles.",
                "welcome_text_2": "Enjoy all that the east coast of Asturias has to offer. Beautiful beaches, incredible landscapes, sports activities, and the best gastronomy.",
            },
            "pics": {
                "pictures_title": "Pictures",
                "bedroom": "Bedroom",
                "living": "Living Room",
                "kitchen": "Kitchen",
                "bathroom": "Bathroom",
                "terrace": "Terrace",
                "parking": "Parking",
                "explore": "Explore all pictures",
            },
            "amenities": {
                "amenities_title": "Amenities",
                "check_in": "Self check-in",
                "text_1": "Check yourself in with the lockbox. Recent guests gave the check-in process a 5-star rating",
                "parking": "Parking",
                "text_2": "Free parking on premises",
                "kitchen": "Kitchen and dining",
                "text_3": "Kitchen, Fridge, Microwave, Cooking basics, Dishes and cutlery, Dishwasher, Other gas cooker, Double oven, Coffee maker, Wine glasses and Toaster",
                "internet": "Internet and office",
                "text_4": "Wifi, TV and Dedicated workspace",
                "pets": "Pets allowed",
                "text_5": "Bring your pets along for the stay",
                "laundry": "Laundry",
                "text_6": "Washing machine, Bed linen, Hangers, Clothes drying rack, Wardrobe and Essentials",
                "outside": "Outside",
                "text_7": "Private Balcony (1)",
                "heating": "Heating and cooling",
                "text_8": "Central heating",
                "sanitary": "Sanitary",
                "text_9": "Hair dryer, Essentials, Bidet, Shower and Hot water",
                "sleeping": "Sleeping",
                "text_10": "1 Double bed and 1 Sofa bed",
                "units": "Units",
                "text_11": "1 Bedroom, 1 Dining room, 1 Kitchen, 1 Living room and 1 Bathroom",
                "further": "Further info",
            },
            "rules": {
                "rules_title": "House Rules",
                "smoking": "Smoking not allowed",
                "party": "Party not allowed",
            },
            "policy": {
                "policy_title": "Policy and Notes",
                "payment": "Payment Schedule",
                "cancellation": "Cancellation Policy",
                "damage": "Damage deposit",
                "airbnb": "Based on Airbnb Policy",
            },
            "book": {
                "asturias": "Asturias, Spain",
                "from": "from",
                "night": "per night"
            },
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
                "contact": "Contact",
                "description": "Description",
                "pictures": "Photos",
                "amenities": "Aménités",
                "rules": "Règles de la maison",
                "policy": "Politique et notes"
            },
            "desc": {
                "description_title": "Description",
                "guests": "4 Invités",
                "bedroom": "1 Chambre",
                "beds": "2 Lits",
                "bathroom": "1 Salle de bain",
                "welcome": 'Bienvenue à "Riba de Rivers"',
                "welcome_text_1": "Notre appartement confortable à 10 minutes à pied de la plage est parfait pour une escapade en couple, entre amis ou en famille. Pour 4 personnes, il dispose d'une chambre, d'une salle de bain complète, d'une cuisine équipée, d'un salon avec canapé-lit, d'une terrasse privée et d'un parking pour voitures et vélos.",
                "welcome_text_2": "Profitez de tout ce que la côte est des Asturies a à offrir. De belles plages, des paysages incroyables, des activités sportives et la meilleure gastronomie.",
            },
            "pics": {
                "pictures_title": "Photos",
                "bedroom": "Chambre",
                "living": "Salon",
                "kitchen": "Cuisine",
                "bathroom": "Salle de bain",
                "terrace": "Terrasse",
                "parking": "Parking",
                "explore": "Explorez toutes les photos",
            },
            "amenities": {
                "amenities_title": "Aménités",
                "check_in": "Arrivée autonome",
                "text_1": "Accédez vous-même avec la boîte à clés. Les invités récents ont donné un score de 5 étoiles au processus d'enregistrement",
                "parking": "Parking",
                "text_2": "Parking gratuit sur place",
                "kitchen": "Cuisine et salle à manger",
                "text_3": "Cuisine, Réfrigérateur, Micro-ondes, Ustensiles de base, Vaisselle, Lave-vaisselle, Cuisinière à gaz, Four double, Cafetière, Verres à vin et Grille-pain",
                "internet": "Internet et bureau",
                "text_4": "Wifi, TV et Espace de travail dédié",
                "pets": "Animaux acceptés",
                "text_5": "Amenez vos animaux de compagnie",
                "laundry": "Buanderie",
                "text_6": "Machine à laver, Linge de lit, Cintres, Séchoir, Garde-robe et Essentiels",
                "outside": "Extérieur",
                "text_7": "Balcon privé (1)",
                "heating": "Chauffage et climatisation",
                "text_8": "Chauffage central",
                "sanitary": "Sanitaire",
                "text_9": "Sèche-cheveux, Essentiels, Bidet, Douche et Eau chaude",
                "sleeping": "Couchage",
                "text_10": "1 Lit double et 1 Canapé-lit",
                "units": "Unités",
                "text_11": "1 Chambre, 1 Salle à manger, 1 Cuisine, 1 Salon et 1 Salle de bain",
                "further": "Informations supplémentaires",
            },
            "rules": {
                "rules_title": "Règles de la maison",
                "smoking": "Interdiction de fumer",
                "party": "Fêtes non autorisées",
            },
            "policy": {
                "policy_title": "Politique et notes",
                "payment": "Calendrier de paiement",
                "cancellation": "Politique d'annulation",
                "damage": "Dépôt de garantie",
                "airbnb": "Basé sur la politique Airbnb",
            },
            "book": {
                "asturias": "Asturies, Espagne",
                "from": "à partir",
                "night": "par nuit"
            },
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
                "contact": "Contacto",
                "description": "Descripción",
                "pictures": "Fotos",
                "amenities": "Comodidades",
                "rules": "Reglas de la casa",
                "policy": "Política y Notas"
            },
            "desc": {
                "description_title": "Descripción",
                "guests": "4 Huéspedes",
                "bedroom": "1 Habitación",
                "beds": "2 Camas",
                "bathroom": "1 Baño",
                "welcome": 'Bienvenido a "Riba de Rivers"',
                "welcome_text_1": "Nuestro acogedor apartamento a 10 minutos a pie de la playa es perfecto para una escapada en pareja, con amigos o en familia. Tiene capacidad para 4 personas, cuenta con una habitación, baño completo, cocina equipada, sala de estar con sofá cama, terraza privada y aparcamiento para coches y bicicletas.",
                "welcome_text_2": "Disfruta de todo lo que la costa este de Asturias tiene para ofrecer. Hermosas playas, paisajes increíbles, actividades deportivas y la mejor gastronomía.",
            },
            "pics": {
                "pictures_title": "Fotos",
                "bedroom": "Habitación",
                "living": "Sala de estar",
                "kitchen": "Cocina",
                "bathroom": "Baño",
                "terrace": "Terraza",
                "parking": "Aparcamiento",
                "explore": "Explora todas las fotos",
            },
            "amenities": {
                "amenities_title": "Comodidades",
                "check_in": "Auto check-in",
                "text_1": "Accede con la caja de llaves. Los huéspedes recientes calificaron con 5 estrellas el proceso de registro",
                "parking": "Aparcamiento",
                "text_2": "Aparcamiento gratuito en las instalaciones",
                "kitchen": "Cocina y comedor",
                "text_3": "Cocina, Frigorífico, Microondas, Utensilios básicos, Platos y cubiertos, Lavavajillas, Cocina de gas, Doble horno, Cafetera, Copas de vino y Tostadora",
                "internet": "Internet y oficina",
                "text_4": "Wifi, TV y Espacio de trabajo dedicado",
                "pets": "Se admiten mascotas",
                "text_5": "Lleva a tus mascotas contigo",
                "laundry": "Lavandería",
                "text_6": "Lavadora, Ropa de cama, Perchas, Tendedero, Armario y Esenciales",
                "outside": "Exterior",
                "text_7": "Balcón privado (1)",
                "heating": "Calefacción y refrigeración",
                "text_8": "Calefacción central",
                "sanitary": "Sanitario",
                "text_9": "Secador de pelo, Esenciales, Bidé, Ducha y Agua caliente",
                "sleeping": "Dormir",
                "text_10": "1 Cama doble y 1 Sofá cama",
                "units": "Unidades",
                "text_11": "1 Habitación, 1 Comedor, 1 Cocina, 1 Sala de estar y 1 Baño",
                "further": "Más información",
            },
            "rules": {
                "rules_title": "Reglas de la casa",
                "smoking": "Prohibido fumar",
                "party": "Fiestas no permitidas",
            },
            "policy": {
                "policy_title": "Política y Notas",
                "payment": "Calendario de pagos",
                "cancellation": "Política de cancelación",
                "damage": "Depósito por daños",
                "airbnb": "Basado en la política de Airbnb",
            },
            "book": {
                "asturias": "Asturias, España",
                "from": "desde",
                "night": "por noche"
            },
            "footer": {
                "copyright": "2024 Riba de Rivers Apartamentos. Todos los derechos reservados."
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