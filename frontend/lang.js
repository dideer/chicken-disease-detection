/*
   ==================================================
   LANG.JS - Multi-language Translation Strings
   ==================================================
   
   Supported Languages:
   - en: English
   - rw: Kinyarwanda
   - fr: French
   ==================================================
*/

const translations = {
    en: {
        // -----------------------------------------------
        // App & Navigation
        // -----------------------------------------------
        app_name: 'Chicken Disease Detection',
        dashboard_title: 'Chicken Disease Detection System',
        login_title: 'Welcome Back',
        register_title: 'Create Account',
        result_title: 'Detection Result',
        logout_btn: 'Logout',

        // -----------------------------------------------
        // Login Page
        // -----------------------------------------------
        username: 'Username',
        password: 'Password',
        login_btn: 'Login',
        error_empty_fields: 'Please fill in all fields',
        no_account: "Don't have an account?",
        sign_up: 'Sign up here',
        demo_info: 'Demo: Use any username and password',

        // -----------------------------------------------
        // Register Page
        // -----------------------------------------------
        email: 'Email',
        confirm_password: 'Confirm Password',
        create_account_btn: 'Create Account',
        username_error: 'Username must be 3-20 characters',
        email_error: 'Please enter a valid email',
        password_error: 'Password must be at least 6 characters',
        password_mismatch: 'Passwords do not match',
        strength_weak: 'Weak',
        strength_fair: 'Fair',
        strength_good: 'Good',
        strength_strong: 'Strong',
        have_account: 'Already have an account?',
        login: 'Login here',

        // -----------------------------------------------
        // Dashboard Page
        // -----------------------------------------------
        scans_done: 'Total Scans',
        diseases_found: 'Diseases Found',
        healthy_results: 'Healthy Results',
        upload_label: 'Upload Chicken Image',
        upload_instructions: 'Click to select or drag and drop',
        detect_btn: 'Detect Disease',
        filename: 'Filename',
        file_size: 'File Size',
        farmer_tip_title: "Farmer's Tip",
        farmer_tip: 'Take a clear close-up photo in good lighting for best results',
        upload_btn: 'Upload Image',
        recent_detections: 'Recent Detections',
        no_detections: 'No detections yet. Upload an image to start!',
        loading_history: 'Loading history...',
        refresh_btn: 'Refresh',
        scanned_by: 'Scanned by',
        upload_different: 'Upload Different Image',

        // -----------------------------------------------
        // Result Page — Header
        // -----------------------------------------------
        confidence_scores: 'Confidence Scores',
        warning_title: 'Important',
        scan_another_btn: 'Scan Another Chicken',
        print_btn: 'Print Result',
        symptoms_title: 'Symptoms',
        scanned_by: 'Scanned by',

        // -----------------------------------------------
        // Result Page — Badges
        // -----------------------------------------------
        badge_disease: '⚠️ Disease Detected',
        badge_healthy: '✅ Healthy',

        // -----------------------------------------------
        // Result Page — Urgency
        // -----------------------------------------------
        urgency_high: '🔴 High Urgency — Act within 24 hours',
        urgency_medium: '🟡 Medium Urgency — Act within 48 hours',
        urgency_none: '🟢 No Urgency — Continue routine care',

        // -----------------------------------------------
        // Result Page — Section Titles
        // -----------------------------------------------
        treatment_title: 'Recommended Treatment',
        care_title: 'Care Recommendations',
        medicine_suggestions: 'Medicine Suggestions',
        care_tips: 'Care Tips',

        // -----------------------------------------------
        // Result Page — Warning Messages
        // -----------------------------------------------
        warning_crd: 'Isolate infected birds immediately to prevent spread. Consult a veterinarian for proper antibiotic dosage.',
        warning_fowlpox: 'Separate affected birds and vaccinate the healthy flock. Monitor daily for new lesions.',
        warning_healthy: 'Your flock appears healthy. Maintain good hygiene and regular vaccination schedules.',

        // -----------------------------------------------
        // Disease Names
        // -----------------------------------------------
        disease_crd: 'Chronic Respiratory Disease (CRD)',
        disease_fowlpox: 'Fowl Pox',
        disease_healthy: 'Healthy Chicken',
        fowl_pox: 'Fowl Pox',
        crd: 'CRD',
        healthy: 'Healthy',

        // -----------------------------------------------
        // Disease Descriptions
        // -----------------------------------------------
        desc_crd: 'A bacterial infection causing chronic respiratory problems in poultry.',
        desc_fowlpox: 'A viral infection causing wart-like lesions on the skin and comb.',
        desc_healthy: 'Your chicken appears healthy with no signs of disease detected.',
        fowl_pox_desc: 'A viral infection causing scabs on the skin',
        crd_desc: 'Chronic respiratory disease affecting the lungs',
        healthy_desc: 'Your chicken is healthy with no detected diseases',

        // -----------------------------------------------
        // Symptoms
        // -----------------------------------------------
        symptoms_crd: 'Nasal discharge, coughing, sneezing, swollen face, difficulty breathing, reduced egg production.',
        symptoms_fowlpox: 'Wart-like scabs on comb, face, eyelids and legs. Possible mouth lesions.',
        symptoms_healthy: 'Active behavior, bright eyes, clean feathers, normal eating and drinking habits.',

        // -----------------------------------------------
        // Treatment — CRD
        // -----------------------------------------------
        treatment_crd_1: 'Isolate all infected birds from the healthy flock immediately',
        treatment_crd_2: 'Administer Tylosin antibiotic mixed in drinking water',
        treatment_crd_3: 'Use Enrofloxacin or Tetracycline (consult vet for dosage)',
        treatment_crd_4: 'Improve ventilation in the poultry house to reduce stress',
        treatment_crd_5: 'Disinfect the entire poultry house thoroughly',
        treatment_crd_6: 'Continue treatment for at least 7 to 14 days',

        // -----------------------------------------------
        // Treatment — Fowl Pox
        // -----------------------------------------------
        treatment_fowlpox_1: 'Separate infected birds from the healthy flock immediately',
        treatment_fowlpox_2: 'Apply 1% iodine solution to lesions every day',
        treatment_fowlpox_3: 'Vaccinate all healthy birds using wing-web stab method',
        treatment_fowlpox_4: 'Give Vitamin A supplements to boost immune system',
        treatment_fowlpox_5: 'Keep wounds clean to prevent secondary bacterial infections',
        treatment_fowlpox_6: 'Monitor all birds daily and report new cases',

        // -----------------------------------------------
        // Treatment — Healthy
        // -----------------------------------------------
        treatment_healthy_1: 'Continue with the regular daily feeding schedule',
        treatment_healthy_2: 'Ensure clean and fresh water is always available',
        treatment_healthy_3: 'Keep the poultry house well ventilated and clean',
        treatment_healthy_4: 'Perform regular health checks every week',
        treatment_healthy_5: 'Keep all vaccination schedules up to date',
        treatment_healthy_6: 'Record and monitor weight and egg production regularly',
    },

    // ==================================================
    // KINYARWANDA
    // ==================================================
    rw: {
        // -----------------------------------------------
        // App & Navigation
        // -----------------------------------------------
        app_name: 'Gusuzuma Indwara z\'Inkoko',
        dashboard_title: 'Sisitemu yo Gusuzuma Indwara z\'Inkoko',
        login_title: 'Murakaza Neza',
        register_title: 'Fungura Konti',
        result_title: 'Ibisubizo by\'Isuzuma',
        logout_btn: 'Sohoka',

        // -----------------------------------------------
        // Login Page
        // -----------------------------------------------
        username: 'Izina ry\'umukoresha',
        password: 'Ijambo ry\'ibanga',
        login_btn: 'Injira',
        error_empty_fields: 'Uzuza ibice byose bikenewe',
        no_account: 'Nta konti ufite?',
        sign_up: 'Iyandikishe hano',
        demo_info: 'Demo: Koresha izina iryo ari ryo ryose na ijambo ry\'ibanga',

        // -----------------------------------------------
        // Register Page
        // -----------------------------------------------
        email: 'Imeyili',
        confirm_password: 'Emeza Ijambo ry\'ibanga',
        create_account_btn: 'Fungura Konti',
        username_error: 'Izina rigomba kuba inyuguti 3-20',
        email_error: 'Injiza imeyili nziza',
        password_error: 'Ijambo ry\'ibanga rigomba kuba nibura inyuguti 6',
        password_mismatch: 'Amagambo y\'ibanga ntavugana',
        strength_weak: 'Ntakomeye',
        strength_fair: 'Bishoboka',
        strength_good: 'Nziza',
        strength_strong: 'Ikomeye cyane',
        have_account: 'Usanganywe konti?',
        login: 'Injira hano',

        // -----------------------------------------------
        // Dashboard Page
        // -----------------------------------------------
        scans_done: 'Isuzuma Ryose',
        diseases_found: 'Indwara Zabonetse',
        healthy_results: 'Ibisubizo Nzima',
        upload_label: 'Ohereza Ifoto y\'Inkoko',
        upload_instructions: 'Klikiliza gushora cyangwa uhumeke hano',
        detect_btn: 'Shakisha Indwara',
        filename: 'Izina ry\'ifoto',
        file_size: 'Ubunini bw\'ifoto',
        farmer_tip_title: 'Inama y\'Umuhinzi',
        farmer_tip: 'Fata ifoto nziza hafi y\'inkoko mu mucyo mwiza kugira ibisubizo byiza',
        upload_btn: 'Ohereza Ifoto',
        recent_detections: 'Isuzuma Ryakozwe Vuba',
        no_detections: 'Nta suzuma ryakozwe. Ohereza ifoto gutangira!',
        loading_history: 'Gushaka amakuru...',
        refresh_btn: 'Vugurura',
        scanned_by: 'Yasuzumwe na',
        upload_different: 'Ohereza Ifoto Yindi',

        // -----------------------------------------------
        // Result Page — Header
        // -----------------------------------------------
        confidence_scores: 'Indangakamere z\'Icyizere',
        warning_title: 'Icyitonderwa',
        scan_another_btn: 'Suzuma Inkoko Iyindi',
        print_btn: 'Fotokopinya Ibisubizo',
        symptoms_title: 'Ibimenyetso',
        scanned_by: 'Yasuzumwe na',

        // -----------------------------------------------
        // Result Page — Badges
        // -----------------------------------------------
        badge_disease: '⚠️ Indwara Yabonetse',
        badge_healthy: '✅ Nzima',

        // -----------------------------------------------
        // Result Page — Urgency
        // -----------------------------------------------
        urgency_high: '🔴 Biihuta Cyane — Kora mu masaha 24',
        urgency_medium: '🟡 Biihuta — Kora mu masaha 48',
        urgency_none: '🟢 Nta Ihuta — Komeza ubwitaho busanzwe',

        // -----------------------------------------------
        // Result Page — Section Titles
        // -----------------------------------------------
        treatment_title: 'Ubuvuzi Burashinzwe',
        care_title: 'Inama z\'Ubwitaho',
        medicine_suggestions: 'Imiti Irashinzwe',
        care_tips: 'Inama z\'Ubuzima',

        // -----------------------------------------------
        // Result Page — Warning Messages
        // -----------------------------------------------
        warning_crd: 'Shyira inkoko zarwaye ahantu hatandukanye ako kanya kugira ngo indwara itandukire. Baza inzobere y\'ubuvuzi bw\'inyamaswa.',
        warning_fowlpox: 'Shyira inkoko zarwaye ahantu hatandukanye hanyuma ukingire inzima. Genzura buri munsi.',
        warning_healthy: 'Inkoko zawe zigaragara nzima. Komeza isuku nziza no gukingira ku gihe.',

        // -----------------------------------------------
        // Disease Names
        // -----------------------------------------------
        disease_crd: 'Indwara y\'Ubuhumekero (CRD)',
        disease_fowlpox: 'Agakoko k\'Inkoko',
        disease_healthy: 'Inkoko Nzima',
        fowl_pox: 'Agakoko k\'Inkoko',
        crd: 'CRD',
        healthy: 'Nzima',

        // -----------------------------------------------
        // Disease Descriptions
        // -----------------------------------------------
        desc_crd: 'Indwara ya bagiteri iteranya ibibazo by\'ubuhumekero mu nkoko.',
        desc_fowlpox: 'Indwara ya virusi iteranya imigote ku gashali no mu maso y\'inkoko.',
        desc_healthy: 'Inkoko yawe igaragara nzima nta ndwara yagaragajwe.',
        fowl_pox_desc: 'Indwara ya virasi itera k\'imigote ku gashali',
        crd_desc: 'Indwara y\'ubuhumekero itera mu mahara',
        healthy_desc: 'Inkoko yawe ni nzima nta ndwara yagaragajwe',

        // -----------------------------------------------
        // Symptoms
        // -----------------------------------------------
        symptoms_crd: 'Inzira y\'amazuru iva, inkorora, gusinda, mu maso akavimba, guhumeka bigoye, kugabanuka kw\'amagi.',
        symptoms_fowlpox: 'Imigote ku gashali, mu maso, hafi y\'amaso no ku maguru. Ibibazo bishoboka mu kanwa.',
        symptoms_healthy: 'Imyitwarire myiza, amaso mazima, inyoya nziza, kurya no kunywa bisanzwe.',

        // -----------------------------------------------
        // Treatment — CRD
        // -----------------------------------------------
        treatment_crd_1: 'Shyira inkoko zarwaye ahantu hatandukanye ako kanya',
        treatment_crd_2: 'Tanga umuti wa Tylosin mu mazi yo kunywa',
        treatment_crd_3: 'Koresha Enrofloxacin cyangwa Tetracycline (baza inzobere)',
        treatment_crd_4: 'Ongerera indaho ubuhumekero kugira ngo habeho umwuka mwiza',
        treatment_crd_5: 'Sana neza inzu yose y\'inkoko',
        treatment_crd_6: 'Komeza kuvura nibura iminsi 7 kugeza 14',

        // -----------------------------------------------
        // Treatment — Fowl Pox
        // -----------------------------------------------
        treatment_fowlpox_1: 'Shyira inkoko zarwaye ahantu hatandukanye ako kanya',
        treatment_fowlpox_2: 'Shyira umuti wa iodine 1% ku migote buri munsi',
        treatment_fowlpox_3: 'Kingira inkoko nzima zose ukoresheje uburyo bwo gutera mu baba',
        treatment_fowlpox_4: 'Tanga viyitamini A kugira ngo inzira zo kurwanya indwara zikomeke',
        treatment_fowlpox_5: 'Hisha ibikomere kugira ngo bagiteri zindi zitinjira',
        treatment_fowlpox_6: 'Genzura inkoko zose buri munsi',

        // -----------------------------------------------
        // Treatment — Healthy
        // -----------------------------------------------
        treatment_healthy_1: 'Komeza gutanga ibiribwa bisanzwe buri munsi',
        treatment_healthy_2: 'Menya ko amazi meza asanzwe ari hafi igihe cyose',
        treatment_healthy_3: 'Komeza inzu y\'inkoko ine umwuka kandi isuku',
        treatment_healthy_4: 'Genzura ubuzima buri cyumweru',
        treatment_healthy_5: 'Komeza gukingira ku gihe',
        treatment_healthy_6: 'Andika no gukurikirana ibiro n\'umusaruro w\'amagi',
    },

    // ==================================================
    // FRENCH
    // ==================================================
    fr: {
        // -----------------------------------------------
        // App & Navigation
        // -----------------------------------------------
        app_name: 'Détection des Maladies des Poulets',
        dashboard_title: 'Système de Détection des Maladies des Poulets',
        login_title: 'Bon Retour',
        register_title: 'Créer un Compte',
        result_title: 'Résultat de Détection',
        logout_btn: 'Déconnexion',

        // -----------------------------------------------
        // Login Page
        // -----------------------------------------------
        username: 'Nom d\'utilisateur',
        password: 'Mot de passe',
        login_btn: 'Connexion',
        error_empty_fields: 'Veuillez remplir tous les champs',
        no_account: 'Pas encore de compte?',
        sign_up: 'S\'inscrire ici',
        demo_info: 'Démo: Utilisez n\'importe quel identifiant et mot de passe',

        // -----------------------------------------------
        // Register Page
        // -----------------------------------------------
        email: 'Email',
        confirm_password: 'Confirmer le mot de passe',
        create_account_btn: 'Créer un compte',
        username_error: 'Le nom d\'utilisateur doit contenir 3 à 20 caractères',
        email_error: 'Veuillez entrer un email valide',
        password_error: 'Le mot de passe doit contenir au moins 6 caractères',
        password_mismatch: 'Les mots de passe ne correspondent pas',
        strength_weak: 'Faible',
        strength_fair: 'Moyen',
        strength_good: 'Bon',
        strength_strong: 'Fort',
        have_account: 'Vous avez déjà un compte?',
        login: 'Se connecter ici',

        // -----------------------------------------------
        // Dashboard Page
        // -----------------------------------------------
        scans_done: 'Total des Scans',
        diseases_found: 'Maladies Détectées',
        healthy_results: 'Résultats Sains',
        upload_label: 'Télécharger une Photo de Poulet',
        upload_instructions: 'Cliquez pour sélectionner ou glissez-déposez',
        detect_btn: 'Détecter la Maladie',
        filename: 'Nom du fichier',
        file_size: 'Taille du fichier',
        farmer_tip_title: 'Conseil de l\'Éleveur',
        farmer_tip: 'Prenez une photo nette en bonne lumière pour de meilleurs résultats',
        upload_btn: 'Télécharger l\'Image',
        recent_detections: 'Détections Récentes',
        no_detections: 'Aucune détection. Téléchargez une image pour commencer!',
        loading_history: 'Chargement de l\'historique...',
        refresh_btn: 'Actualiser',
        scanned_by: 'Scanné par',
        upload_different: 'Télécharger une Autre Image',

        // -----------------------------------------------
        // Result Page — Header
        // -----------------------------------------------
        confidence_scores: 'Scores de Confiance',
        warning_title: 'Important',
        scan_another_btn: 'Scanner un Autre Poulet',
        print_btn: 'Imprimer le Résultat',
        symptoms_title: 'Symptômes',
        scanned_by: 'Scanné par',

        // -----------------------------------------------
        // Result Page — Badges
        // -----------------------------------------------
        badge_disease: '⚠️ Maladie Détectée',
        badge_healthy: '✅ En Bonne Santé',

        // -----------------------------------------------
        // Result Page — Urgency
        // -----------------------------------------------
        urgency_high: '🔴 Urgence Élevée — Agir dans les 24 heures',
        urgency_medium: '🟡 Urgence Moyenne — Agir dans les 48 heures',
        urgency_none: '🟢 Aucune Urgence — Continuez les soins habituels',

        // -----------------------------------------------
        // Result Page — Section Titles
        // -----------------------------------------------
        treatment_title: 'Traitement Recommandé',
        care_title: 'Recommandations de Soins',
        medicine_suggestions: 'Suggestions de Médicaments',
        care_tips: 'Conseils de Soin',

        // -----------------------------------------------
        // Result Page — Warning Messages
        // -----------------------------------------------
        warning_crd: 'Isolez immédiatement les oiseaux infectés pour éviter la propagation. Consultez un vétérinaire pour le dosage approprié des antibiotiques.',
        warning_fowlpox: 'Séparez les oiseaux affectés et vaccinez le troupeau sain. Surveillez quotidiennement les nouvelles lésions.',
        warning_healthy: 'Votre troupeau semble en bonne santé. Maintenez une bonne hygiène et les calendriers de vaccination réguliers.',

        // -----------------------------------------------
        // Disease Names
        // -----------------------------------------------
        disease_crd: 'Maladie Respiratoire Chronique (MRC)',
        disease_fowlpox: 'Variole Aviaire',
        disease_healthy: 'Poulet en Bonne Santé',
        fowl_pox: 'Variole Aviaire',
        crd: 'MRC',
        healthy: 'Sain',

        // -----------------------------------------------
        // Disease Descriptions
        // -----------------------------------------------
        desc_crd: 'Une infection bactérienne causant des problèmes respiratoires chroniques chez les volailles.',
        desc_fowlpox: 'Une infection virale causant des lésions verruqueuses sur la peau et la crête.',
        desc_healthy: 'Votre poulet semble en bonne santé, aucun signe de maladie détecté.',
        fowl_pox_desc: 'Une infection virale causant des croûtes sur la peau',
        crd_desc: 'Maladie respiratoire chronique affectant les poumons',
        healthy_desc: 'Votre poulet est en bonne santé sans maladie détectée',

        // -----------------------------------------------
        // Symptoms
        // -----------------------------------------------
        symptoms_crd: 'Écoulement nasal, toux, éternuements, gonflement du visage, difficultés respiratoires, baisse de production d\'œufs.',
        symptoms_fowlpox: 'Croûtes verruqueuses sur la crête, le visage, les paupières et les pattes. Lésions possibles dans la bouche.',
        symptoms_healthy: 'Comportement actif, yeux brillants, plumes propres, habitudes alimentaires et de boisson normales.',

        // -----------------------------------------------
        // Treatment — CRD
        // -----------------------------------------------
        treatment_crd_1: 'Isolez immédiatement tous les oiseaux infectés du troupeau sain',
        treatment_crd_2: 'Administrez l\'antibiotique Tylosin mélangé dans l\'eau de boisson',
        treatment_crd_3: 'Utilisez Enrofloxacine ou Tétracycline (consultez un vétérinaire pour le dosage)',
        treatment_crd_4: 'Améliorez la ventilation dans le poulailler pour réduire le stress',
        treatment_crd_5: 'Désinfectez complètement tout le poulailler',
        treatment_crd_6: 'Continuez le traitement pendant au moins 7 à 14 jours',

        // -----------------------------------------------
        // Treatment — Fowl Pox
        // -----------------------------------------------
        treatment_fowlpox_1: 'Séparez immédiatement les oiseaux infectés du troupeau sain',
        treatment_fowlpox_2: 'Appliquez une solution d\'iode 1% sur les lésions chaque jour',
        treatment_fowlpox_3: 'Vaccinez tous les oiseaux sains par la méthode de piqûre alaire',
        treatment_fowlpox_4: 'Donnez des suppléments de Vitamine A pour renforcer l\'immunité',
        treatment_fowlpox_5: 'Gardez les plaies propres pour éviter les infections bactériennes secondaires',
        treatment_fowlpox_6: 'Surveillez tous les oiseaux quotidiennement et signalez les nouveaux cas',

        // -----------------------------------------------
        // Treatment — Healthy
        // -----------------------------------------------
        treatment_healthy_1: 'Continuez avec le programme d\'alimentation quotidien habituel',
        treatment_healthy_2: 'Assurez-vous que de l\'eau propre et fraîche est toujours disponible',
        treatment_healthy_3: 'Gardez le poulailler bien ventilé et propre',
        treatment_healthy_4: 'Effectuez des contrôles de santé réguliers chaque semaine',
        treatment_healthy_5: 'Maintenez tous les calendriers de vaccination à jour',
        treatment_healthy_6: 'Enregistrez et surveillez régulièrement le poids et la production d\'œufs',
    }
};

// ================================================
// LANGUAGE UTILITY FUNCTIONS
// ================================================

// Get current language from localStorage
function getCurrentLanguage() {
    return localStorage.getItem('appLang') || 'en';
}

// Set language in localStorage
function setLanguage(lang) {
    if (translations[lang]) {
        localStorage.setItem('appLang', lang);
        return true;
    }
    return false;
}

// Get translation string by key
function getTranslation(key, lang = null) {
    const language = lang || getCurrentLanguage();
    return (translations[language] && translations[language][key]) ||
           (translations['en'] && translations['en'][key]) ||
           key;
}

// Apply translations to all elements with data-lang-key
function loadLanguage() {
    const lang = getCurrentLanguage();
    document.querySelectorAll('[data-lang-key]').forEach(el => {
        const key = el.getAttribute('data-lang-key');
        const text = getTranslation(key, lang);
        if (text && text !== key) {
            el.textContent = text;
        }
    });
}

// Apply translations to a specific element and its children
function updateLanguageForElement(element) {
    const lang = getCurrentLanguage();
    element.querySelectorAll('[data-lang-key]').forEach(el => {
        const key = el.getAttribute('data-lang-key');
        const text = getTranslation(key, lang);
        if (text && text !== key) {
            el.textContent = text;
        }
    });
}

// Switch language and reload translations
function switchLanguage(lang) {
    if (setLanguage(lang)) {
        loadLanguage();
        // Reload result page content if on result page
        if (typeof loadResult === 'function') {
            loadResult();
        }
        // Reload statistics if on dashboard
        if (typeof loadStatistics === 'function') {
            loadStatistics();
        }
    }
}