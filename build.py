# -*- coding: utf-8 -*-
"""Génère le site Al-Fissah dans toutes les langues.

Usage :
  python3 build.py                              toutes les langues
  python3 build.py fr en                        langues choisies
  python3 build.py --site https://exemple.fr    change l'adresse du site
  python3 build.py --preview                    version d'essai : demande à Google
                                                de ne PAS indexer (à utiliser tant que
                                                le site n'est pas sur son adresse finale)

L'adresse est mémorisée dans site.conf : elle sert aux balises canoniques,
au sitemap et au partage sur les réseaux sociaux.
Contenu : lang/fr.py, lang/en.py, lang/ar.py, lang/es.py, lang/de.py
"""
import os, sys, json, re, importlib.util

ROOT = os.path.dirname(os.path.abspath(__file__))
LOGO_ABS = 'https://al-fissah.com/assets/images/Logo.png'   # utilisé pour le partage social et Schema.org
LOGO_FILE = 'assets/logo-mark.png'                          # calligraphie seule, dans l'en-tête et le pied de page
LOGO_FULL = 'assets/logo.png'                               # logo complet, sur l'écran de chargement
LOGIN = 'https://al-fissah.com/fr/login'
REGISTER = 'https://al-fissah.com/fr/register'
SITE = 'https://al-fissah.com'
PREVIEW = False
APP = ''        # adresse de la plateforme des comptes (site.conf, clé app=) ; vide = pas encore reliée
YEAR = '2026'
MAIL = 'c.alfissah@gmail.com'
ASSET_VER = '14'
INLINE = '--inline' in sys.argv   # pages autonomes : style, script et logos intégrés   # à incrémenter à chaque modification de style.css ou main.js

# --- adresse du site : site.conf, puis --site / --preview en ligne de commande ---
_conf = os.path.join(ROOT, 'site.conf')
if os.path.exists(_conf):
    for _l in open(_conf, encoding='utf-8'):
        _l = _l.strip()
        if _l.startswith('site='):
            SITE = _l[5:].strip().rstrip('/')
        elif _l.startswith('preview='):
            PREVIEW = _l[8:].strip().lower() in ('1', 'true', 'oui', 'yes')
        elif _l.startswith('app='):
            APP = _l[4:].strip().rstrip('/')
if '--site' in sys.argv:
    SITE = sys.argv[sys.argv.index('--site') + 1].rstrip('/')
if '--preview' in sys.argv:
    PREVIEW = True
if '--public' in sys.argv:
    PREVIEW = False
LANGS = [c for c in ['fr', 'en', 'ar', 'ru', 'es', 'de'] if os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'lang', c + '.py'))]
LANG_NAMES = {'fr': 'Français', 'en': 'English', 'ar': 'العربية', 'ru': 'Русский', 'es': 'Español', 'de': 'Deutsch'}
# --- Polices : hébergées sur le site (assets/fonts/*.woff2, licence OFL, fichiers Google Fonts) ---
# Avant : une feuille de style chargée depuis fonts.googleapis.com bloquait l'affichage de chaque
# page (~0,5 à 0,8 s sur mobile). Désormais les règles @font-face sont dans la page et les fichiers
# sont servis depuis le même domaine ; seuls les sous-ensembles utiles sont fournis (latin pour
# fr/en/es/de, arabe pour ar, cyrillique + latin pour ru) et le navigateur ne télécharge que les
# graisses réellement affichées (unicode-range). Poppins n'est plus chargée : elle ne servait
# qu'au texte de secours affiché si l'image du logo manque.
# Inventaire : assets/fonts/polices.json (famille, graisse, sous-ensemble, fichier, unicode-range).
FONT_FAMILIES = {                      # familles chargées selon la langue de la page
  'default': ['Space Grotesk', 'Karla', 'Amiri'],
  'ar': ['Tajawal', 'Amiri'],
  'ru': ['Manrope', 'Amiri'],
}
FONT_PRELOAD = {                       # (famille, graisse, sous-ensemble) préchargés : titre + texte courant
  'default': [('Space Grotesk', 700, 'latin'), ('Karla', 400, 'latin')],
  'ar': [('Tajawal', 700, 'arabic'), ('Tajawal', 400, 'arabic')],
  'ru': [('Manrope', 700, 'cyrillic'), ('Manrope', 400, 'cyrillic')],
}
FONT_FACES = json.load(open(os.path.join(ROOT, 'assets/fonts/polices.json'), encoding='utf-8'))

def fonts_css(lang, rel):
    """Règles @font-face de la page (font-display:swap : le texte s'affiche tout de suite en police de secours)."""
    fams = FONT_FAMILIES.get(lang, FONT_FAMILIES['default'])
    return ''.join(f"@font-face{{font-family:'{f['famille']}';font-style:normal;font-weight:{f['graisse']};font-display:swap;"
                   f"src:url({rel}assets/fonts/{f['fichier']}) format('woff2');unicode-range:{f['unicode_range']}}}"
                   for f in FONT_FACES if f['famille'] in fams)

def fonts_preload(lang, rel):
    """Préchargement des deux polices du premier écran (titre, texte courant)."""
    want = FONT_PRELOAD.get(lang, FONT_PRELOAD['default'])
    files = [f['fichier'] for f in FONT_FACES if (f['famille'], f['graisse'], f['sous_ensemble']) in want]
    return '\n'.join(f'<link rel="preload" href="{rel}assets/fonts/{n}" as="font" type="font/woff2" crossorigin>' for n in files)

def min_css(s):
    """Allège le CSS intégré : commentaires et retours à la ligne superflus (aucune règle modifiée)."""
    s = re.sub(r'/\*.*?\*/', '', s, flags=re.S)
    out = []
    for line in s.split('\n'):
        line = line.strip()
        if not line: continue
        if out and out[-1][-1] not in '{;},':
            out.append(' ' + line)
        else:
            out.append(line)
    return ''.join(out)

def min_js(s):
    """Allège le script intégré : commentaires de bloc et lignes de commentaire, indentation. Les lignes sont conservées."""
    s = re.sub(r'^[ \t]*/\*.*?\*/[ \t]*\n?', '', s, flags=re.S | re.M)
    out = []
    for line in s.split('\n'):
        t = line.strip()
        if not t or t.startswith('//'): continue
        out.append(t)
    return '\n'.join(out)
PAGES = ['index', 'programmes', 'tarifs', 'faq', 'temoignages', 'reglement', 'a-propos', 'contact', 'essai', 'inscription', 'mentions-legales', '404']


# --- Deux parcours distincts : essai gratuit et inscription aux études ---
# Chaque langue définit : les libellés des boutons, puis les textes des 2 pages.
# Code couleur : « Commencer maintenant » (inscription) = orange ; « Demander un essai gratuit » = bleu marine.
PARCOURS = {
 'fr': dict(
   box_kick="Deux façons de commencer", box_h2="Inscrivez-vous aux études, ou essayez d'abord", box_p="Vous êtes décidé ? Choisissez votre programme, votre formule et votre créneau. Vous hésitez encore ? Commencez par un cours d'essai gratuit de 30 minutes.",
   btn_essai="Demander un essai gratuit", btn_essai_court="Essai gratuit", btn_insc="Commencer maintenant",
   app_b="Continuer sur la plateforme", app_p="La suite se passe sur notre plateforme sécurisée : vous y créez votre compte, choisissez votre professeur et votre créneau, et retrouvez ensuite votre espace élève.", app_btn="Continuer", app_acc="Vous avez déjà un compte ?", app_login="Se connecter",
   essai=dict(crumb="Cours d'essai", title="Demander un cours d'essai gratuit — AL-FISSAH",
     desc="Demandez votre cours d'essai gratuit de 30 minutes : sans engagement et sans moyen de paiement.",
     h1="Demander un cours d'essai gratuit",
     lead="30 minutes avec un professeur, gratuitement et sans engagement. Aucun paiement n'est demandé à cette étape.",
     badge="Gratuit · 30 minutes · sans engagement",
     steps=[("Vos informations","Nom, contact et pays de résidence."),
            ("Niveau et besoins","Adulte ou enfant, programme souhaité et niveau actuel."),
            ("Choix du professeur","Les professeurs disponibles pour votre programme."),
            ("Disponibilités","Le planning réel du professeur, à votre fuseau horaire."),
            ("Choix du créneau","Vous réservez l'horaire de votre essai."),
            ("Confirmation","Vous recevez le lien de connexion à la classe virtuelle.")],
     autre_b="Vous souhaitez vous inscrire directement ?", autre_a="Inscription aux études"),
   etudes=dict(crumb="Inscription", title="S'inscrire aux études — AL-FISSAH",
     desc="Inscription aux cours d'arabe et de Coran : programme, formule, professeur, créneaux et paiement.",
     h1="S'inscrire aux études",
     lead="L'inscription définitive à nos cours. Vous choisissez votre programme, votre formule et votre créneau hebdomadaire.",
     badge="Sessions de 4 semaines · à partir de 28 €",
     steps=[("Informations de l'élève","Identité, contact, pays et fuseau horaire."),
            ("Programme et niveau","Langue arabe ou Coran, individuel ou collectif, niveau évalué."),
            ("Choix de la formule","De 1 h à 7 h par semaine, ou formule en binôme."),
            ("Choix du professeur","Selon votre programme et vos horaires."),
            ("Jours et créneaux","Le planning réel du professeur ; vous fixez vos cours hebdomadaires."),
            ("Paiement et confirmation","Règlement de la session, puis accès à l'espace étudiant.")],
     autre_b="Vous préférez essayer d'abord ?", autre_a="Demander un cours d'essai gratuit"),
   steps_h2="Les 6 étapes de ce parcours",
   steps_p="Aujourd'hui, l'administration réalise avec vous les étapes 3 à 5 (professeur, planning, créneau) par e-mail ou WhatsApp, dès réception de votre formulaire.",
   back="Retour à l'accueil"),

 'en': dict(
   box_kick="Two ways to start", box_h2="Enrol in the courses, or try first", box_p="Made up your mind? Choose your programme, your plan and your time slot. Still unsure? Start with a free 30-minute trial lesson.",
   btn_essai="Request a free trial", btn_essai_court="Free trial", btn_insc="Get started now",
   app_b="Continue on the platform", app_p="The next step takes place on our secure platform: create your account, choose your teacher and your time slot, then find your student area there.", app_btn="Continue", app_acc="Already have an account?", app_login="Log in",
   essai=dict(crumb="Trial lesson", title="Request a free trial lesson — AL-FISSAH",
     desc="Request your free 30-minute trial lesson: no commitment, no payment details required.",
     h1="Request a free trial lesson",
     lead="30 minutes with a teacher, free and with no commitment. No payment is asked for at this stage.",
     badge="Free · 30 minutes · no commitment",
     steps=[("Your details","Name, contact and country of residence."),
            ("Level and needs","Adult or child, chosen programme and current level."),
            ("Choose a teacher","Teachers available for your programme."),
            ("Availability","The teacher's real timetable, in your time zone."),
            ("Choose a slot","You book the time of your trial lesson."),
            ("Confirmation","You receive the link to the virtual classroom.")],
     autre_b="Would you rather enrol straight away?", autre_a="Enrol in the courses"),
   etudes=dict(crumb="Enrolment", title="Enrol in the courses — AL-FISSAH",
     desc="Enrolment in Arabic and Quran lessons: programme, plan, teacher, time slots and payment.",
     h1="Enrol in the courses",
     lead="Full enrolment in our lessons. You choose your programme, your plan and your weekly time slot.",
     badge="4-week sessions · from €28",
     steps=[("Student details","Identity, contact, country and time zone."),
            ("Programme and level","Arabic or Quran, individual or group, assessed level."),
            ("Choose a plan","From 1 to 7 hours per week, or the two-student plan."),
            ("Choose a teacher","Based on your programme and your schedule."),
            ("Days and slots","The teacher's real timetable; you set your weekly lessons."),
            ("Payment and confirmation","Payment of the session, then access to the student area.")],
     autre_b="Would you rather try first?", autre_a="Request a free trial lesson"),
   steps_h2="The 6 steps of this journey",
   steps_p="For now, the administration carries out steps 3 to 5 with you (teacher, timetable, slot) by e-mail or WhatsApp, as soon as your form is received.",
   back="Back to home"),

 'es': dict(
   box_kick="Dos formas de empezar", box_h2="Inscríbase en los cursos, o pruebe primero", box_p="¿Ya está decidido? Elija su programa, su tarifa y su horario. ¿Todavía duda? Empiece con una clase de prueba gratuita de 30 minutos.",
   btn_essai="Solicitar clase de prueba", btn_essai_court="Clase de prueba", btn_insc="Empezar ahora",
   app_b="Continuar en la plataforma", app_p="El siguiente paso se realiza en nuestra plataforma segura: cree su cuenta, elija su profesor y su horario, y acceda después a su espacio de alumno.", app_btn="Continuar", app_acc="¿Ya tiene una cuenta?", app_login="Iniciar sesión",
   essai=dict(crumb="Clase de prueba", title="Solicitar una clase de prueba gratuita — AL-FISSAH",
     desc="Solicite su clase de prueba gratuita de 30 minutos: sin compromiso y sin datos de pago.",
     h1="Solicitar una clase de prueba gratuita",
     lead="30 minutos con un profesor, gratis y sin compromiso. En esta etapa no se solicita ningún pago.",
     badge="Gratis · 30 minutos · sin compromiso",
     steps=[("Sus datos","Nombre, contacto y país de residencia."),
            ("Nivel y necesidades","Adulto o niño, programa deseado y nivel actual."),
            ("Elección del profesor","Los profesores disponibles para su programa."),
            ("Disponibilidad","El horario real del profesor, en su zona horaria."),
            ("Elección del horario","Usted reserva la hora de su clase de prueba."),
            ("Confirmación","Recibe el enlace para conectarse al aula virtual.")],
     autre_b="¿Prefiere inscribirse directamente?", autre_a="Inscripción en los cursos"),
   etudes=dict(crumb="Inscripción", title="Inscribirse en los cursos — AL-FISSAH",
     desc="Inscripción en las clases de árabe y Corán: programa, tarifa, profesor, horarios y pago.",
     h1="Inscribirse en los cursos",
     lead="La inscripción definitiva en nuestras clases. Elige su programa, su tarifa y su horario semanal.",
     badge="Ciclos de 4 semanas · desde 28 €",
     steps=[("Datos del alumno","Identidad, contacto, país y zona horaria."),
            ("Programa y nivel","Árabe o Corán, individual o en grupo, nivel evaluado."),
            ("Elección de la tarifa","De 1 a 7 horas por semana, o tarifa para dos."),
            ("Elección del profesor","Según su programa y sus horarios."),
            ("Días y horarios","El horario real del profesor; usted fija sus clases semanales."),
            ("Pago y confirmación","Pago del ciclo y acceso al espacio del estudiante.")],
     autre_b="¿Prefiere probar primero?", autre_a="Solicitar una clase de prueba gratuita"),
   steps_h2="Las 6 etapas de este proceso",
   steps_p="Por ahora, la administración realiza contigo las etapas 3 a 5 (profesor, horario, franja) por correo o WhatsApp, en cuanto recibe tu formulario.",
   back="Volver al inicio"),

 'de': dict(
   box_kick="Zwei Wege zum Start", box_h2="Zum Unterricht anmelden oder erst ausprobieren", box_p="Schon entschieden? Wählen Sie Programm, Tarif und Termin. Noch unsicher? Beginnen Sie mit einer kostenlosen 30-minütigen Probestunde.",
   btn_essai="Kostenlose Probestunde anfragen", btn_essai_court="Probestunde", btn_insc="Jetzt anmelden",
   app_b="Auf der Plattform fortfahren", app_p="Der nächste Schritt findet auf unserer sicheren Plattform statt: Konto anlegen, Lehrkraft und Termin wählen, danach steht Ihnen Ihr Schülerbereich zur Verfügung.", app_btn="Weiter", app_acc="Sie haben bereits ein Konto?", app_login="Anmelden",
   essai=dict(crumb="Probestunde", title="Kostenlose Probestunde anfragen — AL-FISSAH",
     desc="Fragen Sie Ihre kostenlose 30-minütige Probestunde an: unverbindlich und ohne Zahlungsdaten.",
     h1="Kostenlose Probestunde anfragen",
     lead="30 Minuten mit einer Lehrkraft, kostenlos und unverbindlich. In diesem Schritt wird keine Zahlung verlangt.",
     badge="Kostenlos · 30 Minuten · unverbindlich",
     steps=[("Ihre Angaben","Name, Kontakt und Wohnsitzland."),
            ("Niveau und Bedarf","Erwachsener oder Kind, gewünschtes Programm und aktuelles Niveau."),
            ("Wahl der Lehrkraft","Die für Ihr Programm verfügbaren Lehrkräfte."),
            ("Verfügbarkeit","Der tatsächliche Stundenplan der Lehrkraft, in Ihrer Zeitzone."),
            ("Terminwahl","Sie buchen die Uhrzeit Ihrer Probestunde."),
            ("Bestätigung","Sie erhalten den Link zum virtuellen Klassenzimmer.")],
     autre_b="Möchten Sie sich lieber direkt anmelden?", autre_a="Anmeldung zum Unterricht"),
   etudes=dict(crumb="Anmeldung", title="Zum Unterricht anmelden — AL-FISSAH",
     desc="Anmeldung zum Arabisch- und Koranunterricht: Programm, Tarif, Lehrkraft, Termine und Zahlung.",
     h1="Zum Unterricht anmelden",
     lead="Die verbindliche Anmeldung zu unserem Unterricht. Sie wählen Programm, Tarif und wöchentlichen Termin.",
     badge="4-Wochen-Blöcke · ab 28 €",
     steps=[("Angaben zum Schüler","Identität, Kontakt, Land und Zeitzone."),
            ("Programm und Niveau","Arabisch oder Koran, einzeln oder in der Gruppe, geprüftes Niveau."),
            ("Tarifwahl","Von 1 bis 7 Stunden pro Woche oder Tarif zu zweit."),
            ("Wahl der Lehrkraft","Passend zu Programm und Zeiten."),
            ("Tage und Termine","Der tatsächliche Stundenplan; Sie legen Ihre wöchentlichen Stunden fest."),
            ("Zahlung und Bestätigung","Bezahlung des Blocks, dann Zugang zum Schülerbereich.")],
     autre_b="Möchten Sie es lieber erst ausprobieren?", autre_a="Kostenlose Probestunde anfragen"),
   steps_h2="Die 6 Schritte dieser Strecke",
   steps_p="Derzeit führt die Verwaltung die Schritte 3 bis 5 (Lehrkraft, Stundenplan, Termin) mit Ihnen per E-Mail oder WhatsApp durch, sobald Ihr Formular eingegangen ist.",
   back="Zurück zur Startseite"),

 'ru': dict(
   box_kick="Два способа начать", box_h2="Записаться на обучение или сначала попробовать", box_p="Уже решили? Выберите программу, тариф и время. Ещё сомневаетесь? Начните с бесплатного пробного урока на 30 минут.",
   btn_essai="Записаться на пробный урок", btn_essai_court="Пробный урок", btn_insc="Начать обучение",
   app_b="Продолжить на платформе", app_p="Следующий шаг проходит на нашей защищённой платформе: создайте аккаунт, выберите преподавателя и время занятий, затем пользуйтесь личным кабинетом ученика.", app_btn="Продолжить", app_acc="Уже есть аккаунт?", app_login="Войти",
   essai=dict(crumb="Пробный урок", title="Бесплатный пробный урок — AL-FISSAH",
     desc="Запишитесь на бесплатный пробный урок 30 минут: без обязательств и без платёжных данных.",
     h1="Записаться на бесплатный пробный урок",
     lead="30 минут с преподавателем, бесплатно и без обязательств. На этом этапе оплата не требуется.",
     badge="Бесплатно · 30 минут · без обязательств",
     steps=[("Ваши данные","Имя, контакты и страна проживания."),
            ("Уровень и цели","Взрослый или ребёнок, программа и текущий уровень."),
            ("Выбор преподавателя","Преподаватели, доступные для вашей программы."),
            ("Расписание","Реальное расписание преподавателя, в вашем часовом поясе."),
            ("Выбор времени","Вы бронируете время пробного урока."),
            ("Подтверждение","Вы получаете ссылку на виртуальный класс.")],
     autre_b="Хотите записаться сразу?", autre_a="Запись на обучение"),
   etudes=dict(crumb="Запись на обучение", title="Записаться на обучение — AL-FISSAH",
     desc="Запись на уроки арабского и Корана: программа, тариф, преподаватель, расписание и оплата.",
     h1="Записаться на обучение",
     lead="Полная запись на наши занятия. Вы выбираете программу, тариф и еженедельное время.",
     badge="Циклы по 4 недели · от 28 €",
     steps=[("Данные ученика","Имя, контакты, страна и часовой пояс."),
            ("Программа и уровень","Арабский или Коран, индивидуально или в группе, оценка уровня."),
            ("Выбор тарифа","От 1 до 7 часов в неделю или тариф «вдвоём»."),
            ("Выбор преподавателя","С учётом программы и вашего времени."),
            ("Дни и время","Реальное расписание преподавателя; вы назначаете свои уроки."),
            ("Оплата и подтверждение","Оплата цикла и доступ в личный кабинет.")],
     autre_b="Хотите сначала попробовать?", autre_a="Записаться на бесплатный пробный урок"),
   steps_h2="6 шагов этого пути",
   steps_p="Пока шаги 3–5 (преподаватель, расписание, время) администрация проходит вместе с вами по эл. почте или в WhatsApp, как только получит вашу форму.",
   back="На главную"),

 'ar': dict(
   box_kick="طريقتان للبدء", box_h2="سجِّل في الدراسة، أو جرِّب أولًا", box_p="حسمت أمرك؟ اختر برنامجك وصيغتك وموعدك. ما زلت متردّدًا؟ ابدأ بحصة تجريبية مجانية مدتها 30 دقيقة.",
   btn_essai="اطلب حصة تجريبية مجانية", btn_essai_court="حصة تجريبية", btn_insc="ابدأ الدراسة الآن",
   app_b="المتابعة على المنصة", app_p="تتم الخطوة التالية على منصتنا الآمنة: أنشئ حسابك، واختر أستاذك وموعدك، ثم ستجد فضاءك الطلابي هناك.", app_btn="متابعة", app_acc="لديك حساب بالفعل؟", app_login="تسجيل الدخول",
   essai=dict(crumb="حصة تجريبية", title="طلب حصة تجريبية مجانية — الفصاح",
     desc="اطلب حصتك التجريبية المجانية (30 دقيقة): دون التزام ودون بيانات دفع.",
     h1="اطلب حصة تجريبية مجانية",
     lead="30 دقيقة مع أستاذ، مجانًا ودون أي التزام. ولا يُطلب أي دفع في هذه المرحلة.",
     badge="مجانًا · 30 دقيقة · دون التزام",
     steps=[("بياناتك","الاسم ووسيلة التواصل وبلد الإقامة."),
            ("المستوى والاحتياج","كبير أو طفل، البرنامج المطلوب والمستوى الحالي."),
            ("اختيار الأستاذ","الأساتذة المتاحون لبرنامجك."),
            ("المواعيد المتاحة","الجدول الفعلي للأستاذ، بتوقيتك المحلي."),
            ("اختيار الموعد","تحجز موعد حصتك التجريبية."),
            ("التأكيد","تستلم رابط الدخول إلى الفصل الافتراضي.")],
     autre_b="تفضّل التسجيل مباشرةً؟", autre_a="التسجيل في الدراسة"),
   etudes=dict(crumb="التسجيل", title="التسجيل في الدراسة — الفصاح",
     desc="التسجيل في دروس العربية والقرآن: البرنامج، الصيغة، الأستاذ، المواعيد والدفع.",
     h1="التسجيل في الدراسة",
     lead="التسجيل النهائي في دروسنا. تختار برنامجك وصيغتك وموعدك الأسبوعي.",
     badge="دورات من 4 أسابيع · ابتداءً من 28 €",
     steps=[("بيانات الطالب","الهوية ووسيلة التواصل والبلد والمنطقة الزمنية."),
            ("البرنامج والمستوى","لغة عربية أو قرآن، فردي أو جماعي، مع تقييم المستوى."),
            ("اختيار الصيغة","من ساعة إلى 7 ساعات أسبوعيًا، أو صيغة الثنائي."),
            ("اختيار الأستاذ","حسب برنامجك وأوقاتك."),
            ("الأيام والمواعيد","الجدول الفعلي للأستاذ؛ وتحدّد دروسك الأسبوعية."),
            ("الدفع والتأكيد","دفع الدورة ثم الدخول إلى فضاء الطالب.")],
     autre_b="تفضّل التجربة أولًا؟", autre_a="اطلب حصة تجريبية مجانية"),
   steps_h2="المراحل الست لهذا المسار",
   steps_p="حاليًا تُنجز الإدارة معك المراحل 3 إلى 5 (الأستاذ والجدول والموعد) عبر البريد الإلكتروني أو واتساب، فور استلام استمارتك.",
   back="العودة إلى الرئيسية"),
}

FORMULES = [(1, 28), (2, 48), (3, 72), (4, 96), (5, 120), (6, 144), (7, 168)]   # heures par semaine → prix de la session de 4 semaines
PICS = json.load(open(os.path.join(ROOT, 'pics.json')))
if INLINE:
    import base64, io
    from PIL import Image
    def _b64(path, height, fmt='WEBP'):
        """Image redimensionnée (hauteur en px, taille d'affichage ×2 pour les écrans Retina) en data URI.
        WebP sans perte : moitié moins lourd que le PNG pour une image identique — les logos faisaient 60 % du poids des pages."""
        im = Image.open(os.path.join(ROOT, path))
        r = height / im.height
        im = im.resize((max(1, int(im.width * r)), height), Image.LANCZOS)
        buf = io.BytesIO()
        if fmt == 'WEBP':
            im.save(buf, 'WEBP', lossless=True, method=6)   # sans perte : identique au PNG, deux fois plus léger
        else:
            im.save(buf, 'PNG', optimize=True)
        return f'data:image/{fmt.lower()};base64,' + base64.b64encode(buf.getvalue()).decode(), im.width, im.height
    CSS_INLINE = min_css(open(os.path.join(ROOT, 'assets/style.css'), encoding='utf-8').read())
    JS_INLINE = min_js(open(os.path.join(ROOT, 'assets/main.js'), encoding='utf-8').read())
    MARK_B64, MARK_W, MARK_H = _b64('assets/logo-mark.png', 124)
    FULL_B64, FULL_W, FULL_H = _b64('assets/logo.png', 420)
    FAVICON_B64, _, _ = _b64('assets/favicon.png', 48, 'PNG')   # PNG : format d'icône compris par tous les navigateurs
else:
    MARK_W, MARK_H, FULL_W, FULL_H = 124, 124, 313, 420
# Lettres arabes flottantes de l'écran d'ouverture : (lettre, position gauche %, délai s, durée s, orange ?)
LD_SYMS = ''.join(f'<span class="ld-sym{" o" if o else ""}" style="left:{x}%;animation-delay:{d}s;animation-duration:{t}s" aria-hidden="true">{ch}</span>'
                  for ch, x, d, t, o in [('ا', 6, -1, 9, 0), ('ب', 16, -4.5, 10, 1), ('ت', 27, -7, 8.5, 0), ('ج', 38, -2.2, 11, 0), ('د', 50, -5.8, 9.5, 1), ('ر', 61, -8.2, 10, 0),
                                         ('س', 72, -3.6, 8.8, 1), ('ع', 83, -6.4, 10.5, 0), ('ف', 92, -0.5, 9.2, 0), ('م', 45, -9, 9.8, 1), ('ن', 22, -3, 10.4, 0), ('ي', 78, -7.5, 9, 0)])
CLASSROOM_RAW = open(os.path.join(ROOT, 'part_classroom.html'), encoding='utf-8').read()
sys.path.insert(0, os.path.join(ROOT, 'lang'))
from testimonials import TESTI  # témoignages réels, en français

def load_lang(code):
    spec = importlib.util.spec_from_file_location(code, os.path.join(ROOT, 'lang', code + '.py'))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m.L

def strip(s): return re.sub('<[^>]+>', ' ', s).strip()

class Builder:
    def __init__(self, code, L):
        self.c, self.L = code, L
        self.out = ROOT if code == 'fr' else os.path.join(ROOT, code)
        self.rel = '' if code == 'fr' else '../'
        os.makedirs(self.out, exist_ok=True)

    def rel_page(self, page):
        return page + '.html'

    @property
    def I(self):
        return PARCOURS.get(self.c, PARCOURS['fr'])

    def url(self, page):
        p = '' if page == 'index' else page + '.html'
        return f"{SITE}/{p}" if self.c == 'fr' else f"{SITE}/{self.c}/{p}"

    def app_url(self, path):
        """Adresse d'une page de la plateforme des comptes (site.conf, clé app=) dans la langue de la page.
        La plateforme existe en fr/en/ar/ru ; les pages es/de renvoient vers l'anglais."""
        return f"{APP}/{self.c if self.c in ('fr', 'en', 'ar', 'ru') else 'en'}/{path}"

    def login_url(self):
        return self.app_url('login') if APP else LOGIN

    def register_url(self):
        return self.app_url('register') if APP else REGISTER

    # Parcours : dès que la plateforme est reliée (app=), « Demander un essai gratuit » et
    # « Commencer maintenant » y mènent DIRECTEMENT — aucune page intermédiaire sur le site.
    def essai_url(self):
        return self.app_url('essai') if APP else 'essai.html'

    def insc_url(self, query=''):
        return (self.app_url('inscription') if APP else 'inscription.html') + (('?' + query) if query else '')

    def head(self, title, desc, page, extra=''):
        L = self.L; m = L['meta']
        noindex = '\n<meta name="robots" content="noindex, nofollow">' if PREVIEW else ''
        pp = '' if page == 'index' else page + '.html'
        hreflang = '\n'.join(f'<link rel="alternate" hreflang="{c}" href="{SITE}/{"" if c=="fr" else c+"/"}{pp}">' for c in LANGS)
        org = json.dumps({"@context":"https://schema.org","@type":"EducationalOrganization","name":"Al-Fissah","url":SITE,"logo":LOGO_ABS,
                          "description":m['org_desc'],"email":"c.alfissah@gmail.com",
                          "sameAs":["http://www.facebook.com/Ecole.al.fissah1","https://www.instagram.com/ecolealfissah/","https://twitter.com/AlFissah","https://blog.al-fissah.com"]}, ensure_ascii=False)
        return f'''<!DOCTYPE html>
<html lang="{m['html_lang']}" dir="{m.get('dir','ltr')}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="#0D204E">{noindex}
<link rel="icon" type="image/png" href="{FAVICON_B64 if INLINE else self.rel + 'assets/favicon.png'}">
<link rel="canonical" href="{self.url(page)}">
{hreflang}
<link rel="alternate" hreflang="x-default" href="{SITE}/{pp}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="{LOGO_ABS}">
<meta property="og:type" content="website">
<meta property="og:url" content="{self.url(page)}">
<meta property="og:locale" content="{m['og_locale']}">
{fonts_preload(self.c, self.rel)}
<style>{fonts_css(self.c, self.rel)}</style>
{("<style>" + CSS_INLINE + "</style>") if INLINE else f'<link rel="stylesheet" href="{self.rel}assets/style.css?v={ASSET_VER}">'}
<script type="application/ld+json">{org}</script>
<script>window.I18N={json.dumps(L['js'], ensure_ascii=False)};</script>
{'<script>try{if(sessionStorage.getItem("af-intro"))document.documentElement.classList.add("intro-seen")}catch(e){}</script>' if page == 'index' else ''}
{extra}
</head>
<body class="lang-{self.c}">
'''

    def langswitch(self, page):
        p = 'index.html' if page == 'index' else page + '.html'
        items = ''.join(f'<a href="{self.rel}{"" if c=="fr" else c+"/"}{p}" hreflang="{c}" lang="{c}"{" class=\"on\"" if c==self.c else ""}>{LANG_NAMES[c]}</a>' for c in LANGS)
        return f'<div class="langsw"><button type="button" class="langbtn" aria-haspopup="true" aria-expanded="false" aria-label="{self.L["nav"]["language"]}">{self.c.upper()} ▾</button><div class="langmenu">{items}</div></div>'

    def chrome(self, page, home=False):
        L = self.L; n = L['nav']
        loader = f'''<div id="loader">
  <div class="ld-dots" aria-hidden="true"></div>
  {LD_SYMS}
  <div class="ld-box">
    <span class="ld-ring" aria-hidden="true"></span>
    <img class="ld-logo" src="{FULL_B64 if INLINE else self.rel + LOGO_FULL}" width="{FULL_W}" height="{FULL_H}" alt="" fetchpriority="high" onerror="this.style.display='none'">
    <div class="word"><span id="typew"></span><span class="caret"></span></div>
    <div class="word-sub" id="typew-sub"></div>
    <div class="ld-line" aria-hidden="true"></div>
  </div>
</div>
''' if home else ''
        nav = [('index.html', n['accueil'], 'index'), ('programmes.html', n['programmes'], 'programmes'), ('tarifs.html', n['tarifs'], 'tarifs'),
               ('faq.html', n['faq'], 'faq'), ('temoignages.html', n['temoignages'], 'temoignages'), ('a-propos.html', n['apropos'], 'a-propos'), ('contact.html', n['contact'], 'contact')]
        # menu de bureau sans « Accueil » (le logo y mène) pour laisser la place au bouton « Demander un essai gratuit » ; le menu mobile le garde
        menu = '\n      '.join(f'<li><a href="{h}"{" class=\"active\"" if k == page else ""}>{l}</a></li>' for h, l, k in nav if k != 'index')
        mob = '\n    '.join(f'<a href="{h}">{l}</a>' for h, l, k in nav) + f'\n    <a href="reglement.html">{n["reglement"]}</a>'
        return loader + f'''<div id="progress" aria-hidden="true"></div>
<button class="totop" id="totop" aria-label="{n['totop']}">↑</button>
<a class="btn btn-orange cta-float" id="ctafloat" href="{self.insc_url()}">{self.I['btn_insc']}</a>

<div class="dots" aria-hidden="true"></div>
<div class="aur a1" aria-hidden="true"></div>
<div class="aur a2" aria-hidden="true"></div>
<div class="blob b1" aria-hidden="true"></div>
<div class="blob b2" aria-hidden="true"></div>
<div class="blob b3" aria-hidden="true"></div>
<canvas id="floatsyms" aria-hidden="true"></canvas>

<header id="hd">
  <div class="wrap nav">
    <a class="logo" href="index.html"><img class="logomark" src="{MARK_B64 if INLINE else self.rel + LOGO_FILE}" width="{MARK_W}" height="{MARK_H}" alt="Al-Fissah" onerror="this.style.display='none';this.nextElementSibling.style.display='grid'"><span class="mark" style="display:none">A</span> <span class="logo-txt"><b>al fissah</b><small>{self.L["meta"].get("tagline","")}</small></span></a>
    <ul class="menu">
      {menu}
    </ul>
    <div class="nav-right">
      {self.langswitch(page)}
      <a class="hd-login" href="{self.login_url()}">{n['login']}</a>
      <a class="btn btn-orange login" id="hd-essai" href="{self.essai_url()}"><span class="lbl-long">{self.I['btn_essai']}</span><span class="lbl-short">{self.I['btn_essai_court']}</span> <span class="login-sub">{L['nav']['essai_sub']}</span></a>
      <button class="burger" id="burger" aria-label="{n['menu']}" aria-expanded="false"><span></span><span></span><span></span></button>
    </div>
  </div>
</header>

<div class="mobmenu" id="mobmenu" aria-hidden="true">
  <nav>
    {mob}
    <a href="https://livres.al-fissah.com">{n['livres']}</a>
    <a href="https://blog.al-fissah.com">{n['blog']}</a>
    <a class="btn btn-orange" href="{self.insc_url()}">{self.I['btn_insc']}</a>
    <a class="btn btn-navy" href="{self.essai_url()}">{self.I['btn_essai']}</a>
    <a class="btn btn-navy" href="{self.login_url()}">{n['login_full']}</a>
  </nav>
</div>

'''

    def footer(self):
        L = self.L; f = L['footer']; n = L['nav']
        return f'''
<footer class="site">
  <div class="wrap">
    <div class="cols">
      <div>
        <a class="logo" href="index.html" style="color:#fff"><img class="logomark" src="{MARK_B64 if INLINE else self.rel + LOGO_FILE}" width="{MARK_W}" height="{MARK_H}" alt="Al-Fissah" loading="lazy" onerror="this.style.display='none';this.nextElementSibling.style.display='grid'"><span class="mark" style="display:none;background:#fff;color:var(--navy)">A</span> <span class="logo-txt"><b>al fissah</b><small>{self.L["meta"].get("tagline","")}</small></span></a>
        <p style="margin-top:.9rem;max-width:26rem">{f['desc']}</p>
        <div class="socials">
          <a href="http://www.facebook.com/Ecole.al.fissah1" aria-label="Facebook" target="_blank" rel="noopener"><svg viewBox="0 0 24 24"><path d="M14 8h3V4h-3a4 4 0 0 0-4 4v2H7v4h3v6h4v-6h3l1-4h-4V8z"/></svg></a>
          <a href="https://www.instagram.com/ecolealfissah/" aria-label="Instagram" target="_blank" rel="noopener"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r="1" fill="currentColor"/></svg></a>
          <a href="https://twitter.com/AlFissah" aria-label="X / Twitter" target="_blank" rel="noopener"><svg viewBox="0 0 24 24"><path d="M4 4l6.5 8.5L4 20h2.2l5.3-6.1L16 20h4l-6.8-9L19.5 4h-2.2l-4.9 5.6L8 4z"/></svg></a>
          <a href="https://www.youtube.com/watch?v=MNiWkEPoGNw" aria-label="YouTube" target="_blank" rel="noopener"><svg viewBox="0 0 24 24"><path d="M22 8.2a3 3 0 0 0-2.1-2.1C18 5.6 12 5.6 12 5.6s-6 0-7.9.5A3 3 0 0 0 2 8.2 31 31 0 0 0 1.6 12 31 31 0 0 0 2 15.8a3 3 0 0 0 2.1 2.1c1.9.5 7.9.5 7.9.5s6 0 7.9-.5a3 3 0 0 0 2.1-2.1 31 31 0 0 0 .4-3.8 31 31 0 0 0-.4-3.8zM10 15V9l5.2 3z"/></svg></a>
        </div>
      </div>
      <div>
        <h4>{f['col1']}</h4>
        <ul>
          <li><a href="a-propos.html">{n['apropos']}</a></li>
          <li><a href="programmes.html">{f['prog_ind']}</a></li>
          <li><a href="programmes.html#collectifs">{f['prog_col']}</a></li>
          <li><a href="tarifs.html">{n['tarifs']}</a></li>
          <li><a href="temoignages.html">{n['temoignages']}</a></li>
          <li><a href="{self.essai_url()}">{f['essai']}</a></li>
        </ul>
      </div>
      <div>
        <h4>{f['col2']}</h4>
        <ul>
          <li><a href="faq.html">{f['faq']}</a></li>
          <li><a href="reglement.html">{n['reglement']}</a></li>
          <li><a href="https://livres.al-fissah.com">{n['livres']}</a></li>
          <li><a href="https://blog.al-fissah.com">{n['blog']}</a></li>
          <li><a href="contact.html">{f['contact']}</a></li>
          <li><a href="mentions-legales.html">{n['mentions']}</a></li>
        </ul>
      </div>
    </div>
    <div class="base">
      <span>© 2020–{YEAR} Al-Fissah — {f['copy']}</span>
      <span><a href="{self.login_url()}">{n['login']}</a> · <a href="{self.register_url()}">{f['register']}</a></span>
    </div>
  </div>
</footer>

{("<script>" + JS_INLINE + "</script>") if INLINE else f'<script src="{self.rel}assets/main.js?v={ASSET_VER}"></script>'}
</body>
</html>
'''

    def page_hero(self, crumb, h1, lead, updated=None):
        u = f'<span class="updated">{self.L["common"]["updated"]} {updated}</span>' if updated else ''
        return f'''<div class="page-hero">
  <div class="wrap">
    <p class="crumbs"><a href="index.html">{self.L['nav']['accueil']}</a> › {crumb}</p>
    <h1>{h1}</h1>
    <p class="lead">{lead}</p>
    {u}
  </div>
</div>
'''

    def write(self, name, html):
        with open(os.path.join(self.out, name), 'w', encoding='utf-8') as f: f.write(html)

    def qa(self, q, a, cls=''):
        return f'<div class="qa"><button aria-expanded="false">{q}<span class="chev">▾</span></button><div class="ans"><div class="{cls}">{a}</div></div></div>'

    # ------------------------------------------------------------ pages
    def build_index(self):
        L = self.L; H = L['home']; F = L['form']; P = L['progs']; c = L['common']
        cr = CLASSROOM_RAW
        for a, b in H['classroom'].items(): cr = cr.replace(a, b)
        ios = ['io io-l', 'io d1', 'io io-r d2', 'io io-l d1', 'io d2', 'io io-r d3']
        cards = ''.join(f'''      <article class="prog tilt io {ios[i]}">
        {PICS[i]}
        <div class="num">{i+1:02d}</div>
        <h3>{p['titre']}</h3>
        <div class="facts">{''.join(f'<span>{x}</span>' for x in p['facts'])}</div>
        <p>{p['court']}</p>
        <a class="more" href="programmes.html#{p['id']}">{c['discover']} →</a>
      </article>
''' for i, p in enumerate(P['items']))
        steps = ''.join(f'<div class="jstep"><span class="n">{i+1}</span><b>{t}</b><span>{d}</span></div>' for i, (t, d) in enumerate(H['journey']))
        pillars = ''.join(f'<div class="pillar io {x}"><div class="ar">{ar}</div><h3>{t}</h3>{body}</div>' for (ar, t, body), x in zip(H['pillars'], ['io-l', 'd1', 'io-r d2']))
        checks_ad = ''.join(f'<li>{x}</li>' for x in H['adultes_checks'])
        checks_app = ''.join(f'<li>{x}</li>' for x in H['app_checks'])
        phone = ''.join(f'<div class="item"><b>{a}</b><span>{b}</span></div>' for a, b in H['phone'])
        plans = ''
        for (t, price, per, feats), x, bt in zip(H['plans'], ['io io-l', 'featured io d1', 'io io-r d2'], ['btn-navy', 'btn-orange', 'btn-navy']):
            plans += f'<div class="plan {x}"><h3>{t}</h3><div class="price">{price}<small>/{c["session"]}</small></div><div class="per">{per}</div><ul>{"".join(f"<li>{f}</li>" for f in feats)}</ul><a class="btn {bt}" href="tarifs.html">{c["details"]}</a></div>'
        posts = ''.join(f'<a class="post" href="{u}" target="_blank" rel="noopener"><span class="post-tag">{tag}</span><b>{t}</b><span class="post-meta">Blog Al-Fissah · {d}</span></a>' for u, tag, t, d in H['posts'])
        vids = [('Nqwj4BfOaSg', 12, 12), ('_TVQsB01a5o', 12, 9), ('67vD_tLzQt4', 12, 8), ('q-NHRbJhJwU', 11, 7), ('pTpY0QsvLIw', 10, 4), ('7i9LYB64RZA', 9, 4)]
        videos = ''.join(f'<a class="vid" href="https://www.youtube.com/watch?v={v}" target="_blank" rel="noopener"><img src="https://i.ytimg.com/vi/{v}/hqdefault.jpg" alt="" loading="lazy"><span>{H["book"]} {b} · {H["unit"]} {u}</span></a>' for v, b, u in vids)
        quotes = ''.join(f'<blockquote class="quote io {x}"><span class="stars">★★★★★</span><p>{q}</p><footer>{w}</footer></blockquote>' for (q, w), x in zip(H['quotes'], ['io-l', 'io-z d1', 'io-r d2']))
        faq = ''.join(self.qa(q, a) for q, a in H['faq'])
        html = f'''<div class="hero">
  <div class="wrap hero-grid">
    <div class="reveal-seq">
      <span class="badge"><span class="dot"></span> {H['badge']}</span>
      <h1>{H['h1_pre']} <span class="hl">{H['h1_hl']}<svg viewBox="0 0 300 14" preserveAspectRatio="none"><path d="M4 10 C 60 3, 120 12, 180 7 S 270 4, 296 9"/></svg></span>{H['h1_post']}</h1>
      <p class="lead">{H['lead']}</p>
      <div class="hero-cta">
        <a class="btn btn-orange btn-hero" href="{self.insc_url()}">{self.I['btn_insc']} <span class="arr">→</span></a>
        <a class="btn btn-ghost btn-hero" href="programmes.html"><span class="ico">▸</span> {H['cta2']}</a>
      </div>
      <p class="hero-note">{' &nbsp;·&nbsp; '.join(f'<b>✓</b> {x}' for x in H['note'])}</p>
    </div>
    {cr}
  </div>
</div>

<div class="journey"><div class="wrap"><div class="jgrid io" id="jgrid"><div class="jline" aria-hidden="true"><i></i></div>{steps}</div></div></div>

<section id="methode"><div class="wrap">
  <div class="head center io"><span class="kick">{H['methode_kick']}</span><h2>{H['methode_h2']}</h2><p>{H['methode_p']}</p></div>
  <div class="pillars">{pillars}</div>
</div></section>

<section id="programmes"><div class="wrap">
  <div class="head io"><span class="kick">{H['prog_kick']}</span><h2>{H['prog_h2']}</h2><p>{H['prog_p']}</p></div>
  <div class="progs">
{cards}  </div>
</div></section>

<section id="video"><div class="wrap"><div class="videowrap io io-z">
  <div class="head center"><span class="kick">{H['video_kick']}</span><h2>{H['video_h2']}</h2><p>{H['video_p']}</p></div>
  <div class="video-frame"><iframe src="https://www.youtube-nocookie.com/embed/MNiWkEPoGNw" title="{H['video_h2']}" loading="lazy" allow="accelerometer; encrypted-media; picture-in-picture" allowfullscreen style="position:absolute;inset:0;width:100%;height:100%;border:0"></iframe></div>
  <p class="video-more"><a href="https://www.youtube.com/watch?v=MNiWkEPoGNw" target="_blank" rel="noopener">{H['video_more']} →</a></p>
</div></div></section>

<section id="adultes"><div class="wrap split">
  <div class="io io-l">
    <div class="head" style="margin-bottom:0"><span class="kick">{H['adultes_kick']}</span><h2>{H['adultes_h2']}</h2><p>{H['adultes_p']}</p></div>
    <ul class="checks">{checks_ad}</ul>
  </div>
  <div class="panel io io-r d1"><p class="big">{' · '.join(f'<span>{w}</span>' for w in H['big'])}</p><p class="trad">{H['big_sub']}</p></div>
</div></section>

<section id="app"><div class="wrap split">
  <div class="io io-l"><div class="phone" aria-label="App"><div class="screen"><div class="bar">AL-FISSAH</div>{phone}</div></div></div>
  <div class="io io-r d1">
    <div class="head" style="margin-bottom:0"><span class="kick">{H['app_kick']}</span><h2>{H['app_h2']}</h2><p>{H['app_p']}</p></div>
    <ul class="checks">{checks_app}</ul>
    <div class="store-btns">
      <a class="store" href="https://apps.apple.com/fr/app/al-fissah/id6476883231"><small>{H['store_ios']}</small><b>App Store</b></a>
      <a class="store" href="https://play.google.com/store/apps/details?id=com.alfissah.dev"><small>{H['store_android']}</small><b>Google Play</b></a>
    </div>
  </div>
</div></section>

<section id="tarifs"><div class="wrap">
  <div class="head center io"><span class="kick">{L['nav']['tarifs']}</span><h2>{H['tarifs_h2']}</h2><p>{H['tarifs_p']}</p></div>
  <div class="plans">{plans}</div>
  <p class="tarif-note">{H['tarifs_note']} <a href="tarifs.html">{H['tarifs_all']} →</a></p>
</div></section>

<section id="blog"><div class="wrap">
  <div class="head center io"><span class="kick">{H['blog_kick']}</span><h2>{H['blog_h2']}</h2><p>{H['blog_p']}</p></div>
  <div class="posts io d1">{posts}</div>
  <div class="videos io d2">{videos}</div>
  <p class="tarif-note">{H['blog_note']} <a href="https://blog.al-fissah.com" target="_blank" rel="noopener">{H['blog_all']}</a> · <a href="https://www.youtube.com/watch?v=MNiWkEPoGNw" target="_blank" rel="noopener">{H['yt']}</a></p>
</div></section>

<section id="avis"><div class="wrap">
  <div class="head center io"><span class="kick">{L['nav']['temoignages']}</span><h2>{H['avis_h2']}</h2></div>
  <div class="quotes">{quotes}</div>
  <p class="tarif-note"><a href="temoignages.html">{H['avis_all']} →</a></p>
</div></section>

<section id="faq"><div class="wrap">
  <div class="head center io"><span class="kick">FAQ</span><h2>{H['faq_h2']}</h2></div>
  <div class="faq io d1">{faq}</div>
  <p class="tarif-note"><a href="faq.html">{H['faq_all']} →</a></p>
</div></section>

<section id="inscription" class="ctasec"><div class="wrap">
  <div class="ctabox io io-z">
    <span class="kick">{self.I['box_kick']}</span>
    <h2>{self.I['box_h2']}</h2>
    <p>{self.I['box_p']}</p>
    <ul class="checks">{''.join(f'<li>{x}</li>' for x in F['checks'])}</ul>
    <div class="cta-duo">
      <a class="btn btn-orange big" href="{self.insc_url()}">{self.I['btn_insc']} <span class="arr">→</span></a>
      <a class="btn btn-ghost big" href="{self.essai_url()}">{self.I['btn_essai']}</a>
    </div>
  </div>
</div></section>
'''
        self.write('index.html', self.head(L['meta']['title_home'], L['meta']['desc_home'], 'index') + self.chrome('index', home=True) + html + self.footer())

    def build_programmes(self):
        L = self.L; P = L['progs']; c = L['common']
        toc = ''.join(f'<li><a href="#{p["id"]}">{p["titre"]}</a></li>' for p in P['items'])
        secs = ''
        for i, p in enumerate(P['items']):
            secs += f'''<article class="pdetail io {'io-l' if i % 2 == 0 else 'io-r'}" id="{p['id']}">
  <div class="pd-head"><div class="pd-ar">{p['ar']}</div><div><span class="kick">{p['tag']}</span><h2>{p['titre']}</h2><div class="facts">{''.join(f'<span>{x}</span>' for x in p['facts'])}</div></div></div>
  <div class="prose">{p['long']}</div>
  <div class="pd-actions"><a class="btn btn-orange" href="{self.insc_url(f"programme={p['id']}")}">{p['cta']} <span class="arr">→</span></a><a class="btn btn-ghost" href="tarifs.html">{c['see_prices']}</a></div>
</article>
'''
        html = self.page_hero(L['nav']['programmes'], P['h1'], P['lead']) + f'''<div class="page"><div class="wrap">
  <aside class="toc"><b>{L['nav']['programmes']}</b><ol>{toc}</ol><p class="toc-note">{P['toc_note']}</p></aside>
  <div class="pd-list">{secs}</div>
</div></div>
'''
        self.write('programmes.html', self.head(P['title'], P['desc'], 'programmes') + self.chrome('programmes') + html + self.footer())

    def build_tarifs(self):
        L = self.L; T = L['tarifs']; c = L['common']
        def grid(duo):
            prog = 'arabe-adultes' if duo else 'coran'
            s = ''.join(f'<div class="tcard{" featured" if h == 2 else ""}"{f' data-badge="{T.get("badge","")}"' if h == 2 else ""}><span class="tf">{T["formule"]} {h}</span><div class="price">{e}&nbsp;€</div><div class="per">{T["per"].format(h=h)}</div><a class="btn {"btn-orange" if h == 2 else "btn-navy"}" href="{self.insc_url(f"formule={h}&amp;programme={prog}")}">{T["choose"]}</a></div>' for h, e in FORMULES)
            if duo: s += f'<div class="tcard duo"><span class="tf">{T["duo"]}</span><div class="price">36&nbsp;€</div><div class="per">{T["duo_per"]}</div><a class="btn btn-navy" href="contact.html">{T["ask"]}</a></div>'
            return s
        values = ''.join(f'<div class="value"><div class="ar">{a}</div><b>{b}</b><p>{p}</p></div>' for a, b, p in T['values'])
        html = self.page_hero(L['nav']['tarifs'], T['h1'], T['lead']) + f'''<div class="page"><div class="wrap single tarifs-page">
  <div class="head io"><span class="kick">{T['arabe_kick']}</span><h2>{T['arabe_h2']}</h2><p>{T['arabe_p']}</p></div>
  <div class="tgrid io d1">{grid(True)}</div>
  <div class="head io" style="margin-top:4rem"><span class="kick">{T['coran_kick']}</span><h2>{T['coran_h2']}</h2><p>{T['coran_p']}</p></div>
  <div class="tgrid io d1">{grid(False)}</div>
  <article class="prose" style="margin-top:4rem">
    <h2>{T['good_h2']}</h2><div class="values">{values}</div>
    <h2>{T['pay_h2']}</h2>{T['pay_body']}
    <div class="note"><b>{T['note_b']}</b> {T['note_p']} <a href="{self.essai_url()}">{c['request']}</a></div>
  </article>
</div></div>
'''
        self.write('tarifs.html', self.head(T['title'], T['desc'], 'tarifs') + self.chrome('tarifs') + html + self.footer())

    def build_faq(self):
        L = self.L; Q = L['faq']
        ld = json.dumps({"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":strip(a)}} for q, a in Q['items']]}, ensure_ascii=False)
        html = self.page_hero('FAQ', Q['h1'], Q['lead']) + f'''<div class="page"><div class="wrap single">
  <div class="faq wide io">{''.join(self.qa(q, a, 'prose-lite') for q, a in Q['items'])}</div>
  <div class="prose" style="margin-top:3rem"><div class="note"><b>{Q['note_b']}</b> <a href="contact.html">{Q['note_a']}</a>{Q['note_p']}</div></div>
</div></div>
'''
        self.write('faq.html', self.head(Q['title'], Q['desc'], 'faq', f'<script type="application/ld+json">{ld}</script>') + self.chrome('faq') + html + self.footer())

    def build_temoignages(self):
        L = self.L; T = L['temoignages']; M = L['common']['months']
        def fdate(d):
            y, m, dd = d.split('-'); return T['date_fmt'].format(d=int(dd), m=M[int(m) - 1], y=y)
        tags = T['tags']
        cards = ''.join(f'''<blockquote class="tcard-t io {'io-l' if i % 2 == 0 else 'io-r'}" lang="fr" dir="ltr">
  <div class="tt-top"><span class="stars">★★★★★</span><span class="tt-tag">{tags.get(tag, tag)}</span></div>{body}
  <footer><b>{n}</b><time datetime="{d}">{fdate(d)}</time></footer>
</blockquote>''' for i, (n, d, tag, body) in enumerate(TESTI))
        ld = json.dumps({"@context":"https://schema.org","@type":"EducationalOrganization","name":"Al-Fissah","url":SITE,
              "aggregateRating":{"@type":"AggregateRating","ratingValue":"5","bestRating":"5","reviewCount":str(len(TESTI))},
              "review":[{"@type":"Review","author":{"@type":"Person","name":n},"datePublished":d,"inLanguage":"fr","reviewRating":{"@type":"Rating","ratingValue":"5"},"reviewBody":strip(b)[:500]} for n, d, _, b in TESTI]}, ensure_ascii=False)
        kids = sum(1 for x in TESTI if x[2] == 'Enfants')
        note_lang = f'<p class="lang-note">{T["lang_note"]}</p>' if self.c != 'fr' else ''
        html = self.page_hero(L['nav']['temoignages'], T['h1'], T['lead'].format(n=len(TESTI))) + f'''<div class="page"><div class="wrap single tpage">
  <div class="stats io">
    <div class="stat"><div class="n">{len(TESTI)}</div><span>{T['s1']}</span></div>
    <div class="stat"><div class="n">★ 5/5</div><span>{T['s2']}</span></div>
    <div class="stat"><div class="n">{kids}</div><span>{T['s3']}</span></div>
    <div class="stat"><div class="n">2021</div><span>{T['s4']}</span></div>
  </div>
  {note_lang}
  <div class="tcols">{cards}</div>
  <div class="prose"><div class="note"><b>{T['note_b']}</b> {T['note_p']} <a href="{self.login_url()}">{T['note_a']}</a>.</div></div>
</div></div>
'''
        self.write('temoignages.html', self.head(T['title'], T['desc'], 'temoignages', f'<script type="application/ld+json">{ld}</script>') + self.chrome('temoignages') + html + self.footer())

    def build_reglement(self):
        L = self.L; R = L['reglement']
        toc = ''.join(f'<li><a href="#art-{i+1}">{t}</a></li>' for i, (t, _) in enumerate(R['articles']))
        arts = ''.join(f'<h2 id="art-{i+1}"><span class="art">{R["article"]} {i+1}</span>{t}</h2>{b}' for i, (t, b) in enumerate(R['articles']))
        html = self.page_hero(L['nav']['reglement'], R['h1'], R['lead'], R['updated']) + f'''<div class="page"><div class="wrap">
  <aside class="toc"><b>{L['common']['toc']}</b><ol>{toc}</ol></aside>
  <article class="prose">{arts}</article>
</div></div>
'''
        self.write('reglement.html', self.head(R['title'], R['desc'], 'reglement') + self.chrome('reglement') + html + self.footer())

    def build_apropos(self):
        L = self.L; A = L['apropos']
        stats = ''.join(f'<div class="stat"><div class="n">{n}</div><span>{s}</span></div>' for n, s in A['stats'])
        values = ''.join(f'<div class="value"><div class="ar">{a}</div><b>{b}</b><p>{p}</p></div>' for a, b, p in A['values'])
        links = ''.join(f'<li><b>{t}</b><a href="{u}" target="_blank" rel="noopener">{A["read"]} →</a></li>' for u, t in A['links'])
        html = self.page_hero(L['nav']['apropos'], A['h1'], A['lead']) + f'''<div class="page"><div class="wrap single"><article class="prose">
  <div class="stats">{stats}</div>
  <h2>{A['prog_h2']}</h2>{A['prog_body']}
  <h2>{A['is_h2']}</h2><div class="values">{values}</div>
  <h2>{A['coran_h2']}</h2>{A['coran_body']}
  <h2>{A['more_h2']}</h2><ul class="timeline">{links}</ul>
  <div class="note"><b>{A['note_b']}</b> {A['note_p']} <a href="{self.essai_url()}">{L['common']['request']}</a></div>
</article></div></div>
'''
        self.write('a-propos.html', self.head(A['title'], A['desc'], 'a-propos') + self.chrome('a-propos') + html + self.footer())

    def build_contact(self):
        L = self.L; C = L['contact']
        subj = ''.join(f'<option>{s}</option>' for s in C['subjects'])
        html = self.page_hero(L['nav']['contact'], C['h1'], C['lead']) + f'''<div class="page"><div class="wrap form-grid contact-grid">
  <div class="form-aside io io-l"><div class="support-grid one">
    <div class="sup"><div class="ico">✉</div><b>{C['mail_t']}</b><p>{C['mail_p']}</p><a class="btn btn-navy" href="mailto:c.alfissah@gmail.com">c.alfissah@gmail.com</a></div>
    <div class="sup"><div class="ico">🕘</div><b>{C['hours_t']}</b><p>{C['hours_p']}</p></div>
    <div class="sup"><div class="ico">▶</div><b>{C['new_t']}</b><p>{C['new_p']}</p><a class="btn btn-navy" href="{self.essai_url()}">{self.I['btn_essai']}</a></div>
  </div></div>
  <form id="contact-form" class="card-form io io-r d1" novalidate>
    <fieldset>
      <legend><i>✉</i> {C['form_t']}</legend>
      <div class="row2">
        <div class="field"><label for="c-nom">{C['nom']}</label><input id="c-nom" name="nom" type="text" required autocomplete="family-name"></div>
        <div class="field"><label for="c-prenom">{C['prenom']}</label><input id="c-prenom" name="prenom" type="text" required autocomplete="given-name"></div>
      </div>
      <div class="field"><label for="c-email">{L['form'].get("email","E-mail")}</label><input id="c-email" name="email" type="email" required autocomplete="email"></div>
      <div class="field"><label for="c-sujet">{C['sujet']}</label><select id="c-sujet" name="sujet" required><option value="">{L['form']['choose']}</option>{subj}</select></div>
      <div class="field"><label for="c-msg">{C['message']}</label><textarea id="c-msg" name="message" required></textarea></div>
      <div class="hp" aria-hidden="true"><label>Website <input id="c-website" name="website" type="text" tabindex="-1" autocomplete="off"></label></div>
    </fieldset>
    <div class="form-actions"><button type="submit" class="btn btn-orange">{C['send']} <span class="arr">→</span></button></div>
    <p id="contact-status" class="form-status" hidden role="status" aria-live="polite"></p>
  </form>
</div></div>
'''
        self.write('contact.html', self.head(C['title'], C['desc'], 'contact') + self.chrome('contact') + html + self.footer())

    def build_mentions(self):
        L = self.L; M = L['mentions']
        toc = ''.join(f'<li><a href="#{i}">{t}</a></li>' for i, t in M['toc'])
        html = self.page_hero(L['nav']['mentions'], M['h1'], M['lead'], M['updated']) + f'''<div class="page"><div class="wrap">
  <aside class="toc"><b>{L['common']['toc']}</b><ol>{toc}</ol></aside>
  <article class="prose">{M['body']}</article>
</div></div>
'''
        self.write('mentions-legales.html', self.head(M['title'], M['desc'], 'mentions-legales') + self.chrome('mentions-legales') + html + self.footer())

    def build_404(self):
        L = self.L; N = L['nf']
        html = f'''<div class="page-hero notfound"><div class="wrap">
  <div class="nf-ar">٤٠٤</div><h1>{N['h1']}</h1><p class="lead">{N['p']}</p>
  <div class="hero-cta" style="margin-top:1.6rem"><a class="btn btn-orange" href="index.html">{N['home']} <span class="arr">→</span></a><a class="btn btn-ghost" href="programmes.html">{L['nav']['programmes']}</a><a class="btn btn-ghost" href="contact.html">{L['nav']['contact']}</a></div>
</div></div><div style="height:4rem"></div>
'''
        self.write('404.html', self.head(N['title'], N['p'], '404', '<meta name="robots" content="noindex">') + self.chrome('404') + html + self.footer())


    # Formulaire de demande de cours d'essai (essai.html). Ids et noms de champs attendus par assets/main.js
    # (#trial-form, #enfant-fields, #wa-link, #form-status) : ne pas les renommer.
    def trial_form(self):
        F = self.L['form']
        ages = ''.join(f'<option>{a}</option>' for a in range(5, 18))
        progopts = ''.join(f'<option>{o}</option>' for o in F['programmes'])
        nivopts = ''.join(f'<option>{o}</option>' for o in F['niveaux'])
        return f'''<form id="trial-form" class="card-form io io-r d1" novalidate>
    <fieldset>
      <legend><i>1</i> {F['who']}</legend>
      <div class="seg" role="radiogroup"><label><input type="radio" name="profil" value="adulte" checked><span>{F['adult']}</span></label><label><input type="radio" name="profil" value="enfant"><span>{F['child']}</span></label></div>
      <div id="enfant-fields" hidden><div class="row2">
        <div class="field"><label for="f-enfant">{F['child_name']}</label><input id="f-enfant" name="enfant_prenom" type="text" autocomplete="off"></div>
        <div class="field"><label for="f-age">{F['age']}</label><select id="f-age" name="enfant_age"><option value="">—</option>{ages}</select></div>
      </div></div>
      <div class="row2">
        <div class="field"><label for="f-programme">{F['programme']}</label><select id="f-programme" name="programme" required><option value="">{F['choose']}</option>{progopts}</select></div>
        <div class="field"><label for="f-niveau">{F['niveau']}</label><select id="f-niveau" name="niveau" required><option value="">{F['choose']}</option>{nivopts}</select></div>
      </div>
    </fieldset>
    <fieldset>
      <legend><i>2</i> {F['coords']}</legend>
      <div class="row2">
        <div class="field"><label for="f-nom">{F['name']}</label><input id="f-nom" name="nom" type="text" required autocomplete="name"></div>
        <div class="field"><label for="f-email">{F.get("email","E-mail")}</label><input id="f-email" name="email" type="email" required autocomplete="email"></div>
      </div>
      <div class="row2">
        <div class="field"><label for="f-tel">{F['tel']} <small>({F['optional']})</small></label><input id="f-tel" name="tel" type="tel" autocomplete="tel" placeholder="+33 6 …"></div>
        <div class="field"><label for="f-pays">{F['country']}</label><input id="f-pays" name="pays" type="text" autocomplete="country-name" required></div>
      </div>
    </fieldset>
    <fieldset>
      <legend><i>3</i> {F['dispo_t']}</legend>
      <div class="field"><label for="f-dispo">{F['dispo']} <small>({F['dispo_hint']})</small></label><input id="f-dispo" name="dispo" type="text" placeholder="{F['dispo_ph']}"></div>
      <div class="field"><label for="f-msg">{F['message']} <small>({F['optional']})</small></label><textarea id="f-msg" name="message" placeholder="{F['msg_ph']}"></textarea></div>
      <label class="consent"><input type="checkbox" name="consent" required><span>{F['consent']} <a href="mentions-legales.html#confidentialite">{F['privacy']}</a>.</span></label>
      <div class="hp" aria-hidden="true"><label>Website <input id="f-website" name="website" type="text" tabindex="-1" autocomplete="off"></label></div>
    </fieldset>
    <div class="form-actions">
      <button type="submit" class="btn btn-orange">{F['submit']} <span class="arr">→</span></button>
      <span class="alt">{F['or']} <a id="wa-link" href="#" target="_blank" rel="noopener">{F['whatsapp']}</a></span>
    </div>
    <p id="form-status" class="form-status" hidden role="status" aria-live="polite"></p>
  </form>'''

    # Formulaire d'inscription aux études (inscription.html) — champs propres à l'inscription : programme, formule,
    # jours, début souhaité, acceptation du règlement. Traité par le bloc « signup-form » de assets/main.js.
    def signup_form(self):
        L = self.L; S = L['signup']; F = L['form']
        ages = ''.join(f'<option>{a}</option>' for a in range(5, 18))
        progopts = ''.join(f'<option value="{k}">{o}</option>' for k, o in S['programmes'])
        nivopts = ''.join(f'<option>{o}</option>' for o in F['niveaux'])
        hours = ''.join(f'<option value="{h}">{S["hours_opt"].format(h=h, e=e)}</option>' for h, e in FORMULES)
        hours += f'<option value="duo">{S["duo_opt"]}</option><option value="collectif">{S["group_opt"]}</option>'
        starts = ''.join(f'<option>{o}</option>' for o in S['start_opts'])
        return f'''<form id="signup-form" class="card-form io io-r d1" novalidate>
    <fieldset>
      <legend><i>1</i> {S['who']}</legend>
      <div class="seg" role="radiogroup"><label><input type="radio" name="profil" value="adulte" checked><span>{F['adult']}</span></label><label><input type="radio" name="profil" value="enfant"><span>{F['child']}</span></label></div>
      <div id="s-enfant-fields" hidden><div class="row2">
        <div class="field"><label for="s-enfant">{F['child_name']}</label><input id="s-enfant" name="enfant_prenom" type="text" autocomplete="off"></div>
        <div class="field"><label for="s-age">{F['age']}</label><select id="s-age" name="enfant_age"><option value="">—</option>{ages}</select></div>
      </div></div>
      <div class="row2">
        <div class="field"><label for="s-programme">{S['programme']}</label><select id="s-programme" name="programme" required><option value="">{F['choose']}</option>{progopts}</select></div>
        <div class="field"><label for="s-niveau">{F['niveau']}</label><select id="s-niveau" name="niveau" required><option value="">{F['choose']}</option>{nivopts}</select></div>
      </div>
    </fieldset>
    <fieldset>
      <legend><i>2</i> {S['rythme_t']}</legend>
      <div class="field"><label for="s-heures">{S['hours']} <small>({S['hours_hint']})</small></label><select id="s-heures" name="formule" required><option value="">{F['choose']}</option>{hours}</select></div>
      <div class="row2">
        <div class="field"><label for="s-jours">{S['days']} <small>({F['dispo_hint']})</small></label><input id="s-jours" name="jours" type="text" required placeholder="{F['dispo_ph']}"></div>
        <div class="field"><label for="s-debut">{S['start']}</label><select id="s-debut" name="debut" required><option value="">{F['choose']}</option>{starts}</select></div>
      </div>
    </fieldset>
    <fieldset>
      <legend><i>3</i> {F['coords']}</legend>
      <div class="row2">
        <div class="field"><label for="s-nom">{S['name']}</label><input id="s-nom" name="nom" type="text" required autocomplete="name"></div>
        <div class="field"><label for="s-email">{F.get("email","E-mail")}</label><input id="s-email" name="email" type="email" required autocomplete="email"></div>
      </div>
      <div class="row2">
        <div class="field"><label for="s-tel">{F['tel']}</label><input id="s-tel" name="tel" type="tel" required autocomplete="tel" placeholder="+33 6 …"></div>
        <div class="field"><label for="s-pays">{F['country']}</label><input id="s-pays" name="pays" type="text" autocomplete="country-name" required></div>
      </div>
    </fieldset>
    <fieldset>
      <legend><i>4</i> {S['valid_t']}</legend>
      <div class="field"><label for="s-msg">{F['message']} <small>({F['optional']})</small></label><textarea id="s-msg" name="message" placeholder="{S['msg_ph']}"></textarea></div>
      <label class="consent"><input type="checkbox" name="reglement" required><span>{S['rules_pre']} <a href="reglement.html" target="_blank" rel="noopener">{S['rules_link']}</a>{S['rules_post']}</span></label>
      <label class="consent"><input type="checkbox" name="consent" required><span>{S['consent']} <a href="mentions-legales.html#confidentialite">{F['privacy']}</a>.</span></label>
      <div class="hp" aria-hidden="true"><label>Website <input id="s-website" name="website" type="text" tabindex="-1" autocomplete="off"></label></div>
    </fieldset>
    <div class="form-actions">
      <button type="submit" class="btn btn-orange">{S['submit']} <span class="arr">→</span></button>
      <span class="alt">{F['or']} <a id="signup-wa" href="#" target="_blank" rel="noopener">{F['whatsapp']}</a></span>
    </div>
    <p id="signup-status" class="form-status" hidden role="status" aria-live="polite"></p>
  </form>'''

    def _parcours(self, kind, fichier, autre_href):
        """Page d'un parcours : son formulaire propre (avec encart d'accompagnement), puis les 6 étapes, et le renvoi vers l'autre parcours.
        Plateforme reliée (app=) : la page n'existe plus que pour les anciens liens — elle renvoie aussitôt vers la plateforme."""
        I = self.I; P = I[kind]
        if APP:
            dest = self.app_url('essai' if kind == 'essai' else 'inscription')
            self.write(fichier, f'''<!DOCTYPE html>
<html lang="{self.L['meta']['html_lang']}" dir="{self.L['meta'].get('dir','ltr')}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<meta http-equiv="refresh" content="0; url={dest}">
<link rel="canonical" href="{dest}">
<title>{P['title']}</title>
<script>location.replace({json.dumps(dest)});</script>
<style>body{{margin:0;min-height:100vh;display:flex;align-items:center;justify-content:center;font-family:Karla,system-ui,sans-serif;background:#F6F8FD;color:#0D204E}}a{{color:#D96F0F;font-weight:700}}</style>
</head>
<body><p>{I['app_p']} <a href="{dest}">{I['app_btn']} →</a></p></body>
</html>
''')
            return
        A = self.L['signup'] if kind == 'etudes' else self.L['form']     # textes de l'encart à côté du formulaire
        form = self.signup_form() if kind == 'etudes' else self.trial_form()
        if APP:   # plateforme reliée : la demande se fait sur la plateforme, le formulaire local disparaît
            form = f'''<div class="card-form app-card io io-r d1" id="app-card">
      <h3>{I['app_b']}</h3>
      <p>{I['app_p']}</p>
      <a class="btn btn-orange big" href="{self.app_url('essai' if kind == 'essai' else 'inscription')}">{I['app_btn']} <span class="arr">→</span></a>
      <p class="tarif-note" style="text-align:start"><b>{I['app_acc']}</b> <a href="{self.login_url()}">{I['app_login']}</a></p>
    </div>'''
        steps = ''.join(
            f'<li class="istep"><span class="n">{i+1}</span><div><b>{ti}</b><span>{de}</span></div></li>'
            for i, (ti, de) in enumerate(P['steps']))
        html = self.page_hero(P['crumb'], P['h1'], P['lead']) + f'''<div class="page parcours"><div class="wrap single">
  <p class="ibadge io">{P['badge']}</p>
  <section class="form-grid" id="formulaire">
    <div class="form-aside io io-l">
      <div class="head"><span class="kick">{A['kick']}</span><h2>{A['h2']}</h2><p>{A['p']}</p></div>
      <ul class="checks">{''.join(f'<li>{x}</li>' for x in A['checks'])}</ul>
      <div class="assur"><span class="ar">بِسْمِ اللهِ</span><b>{A['next_t']}</b><p>{A['next_p']}</p></div>
      <div class="iautre"><b>{P['autre_b']}</b> <a href="{autre_href}">{P['autre_a']} →</a></div>
    </div>
    {form}
  </section>
  <div class="psteps io d1">
    <h2>{I['steps_h2']}</h2>
    <ol class="isteps">{steps}</ol>
    {'' if APP else f'<p class="tarif-note" style="text-align:start">{I["steps_p"]}</p>'}
  </div>
  <p class="tarif-note"><a href="index.html">← {I['back']}</a></p>
</div></div>
'''
        self.write(fichier, self.head(P['title'], P['desc'], fichier[:-5]) + self.chrome(fichier[:-5]) + html + self.footer())

    def build_essai(self):
        self._parcours('essai', 'essai.html', self.insc_url())

    def build_inscription(self):
        self._parcours('etudes', 'inscription.html', self.essai_url())

    def build(self):
        for f in [self.build_index, self.build_programmes, self.build_tarifs, self.build_faq, self.build_temoignages,
                  self.build_reglement, self.build_apropos, self.build_contact, self.build_mentions, self.build_essai, self.build_inscription, self.build_404]:
            f()
        print('✓', self.c, '→', os.path.relpath(self.out, ROOT) or '.')

def sitemap(codes):
    with open(os.path.join(ROOT, 'sitemap.xml'), 'w', encoding='utf-8') as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n')
        for p in PAGES:
            if p == '404' or (APP and p in ('essai', 'inscription')): continue
            for c in codes:
                loc = f"{SITE}/{'' if c == 'fr' else c + '/'}{'' if p == 'index' else p + '.html'}"
                alts = ''.join(f'<xhtml:link rel="alternate" hreflang="{a}" href="{SITE}/{"" if a == "fr" else a + "/"}{"" if p == "index" else p + ".html"}"/>' for a in codes)
                pr = '1.0' if p == 'index' else ('0.8' if p in ('programmes', 'tarifs') else '0.6')
                f.write(f'  <url><loc>{loc}</loc>{alts}<changefreq>monthly</changefreq><priority>{pr}</priority></url>\n')
        f.write('</urlset>\n')
    with open(os.path.join(ROOT, 'robots.txt'), 'w', encoding='utf-8') as f:
        if PREVIEW:
            f.write('User-agent: *\nDisallow: /\n')
        else:
            f.write(f'User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n')

if __name__ == '__main__':
    _args = sys.argv[1:]
    if '--site' in _args:
        _i = _args.index('--site'); del _args[_i:_i + 2]
    _args = [a for a in _args if not a.startswith('--')]
    codes = _args or LANGS
    for c in codes:
        Builder(c, load_lang(c)).build()
    sitemap(LANGS)
    print('✓ sitemap.xml, robots.txt')
    print(f'✓ adresse du site : {SITE}' + ('   [APERÇU — non indexable par Google]' if PREVIEW else ''))
