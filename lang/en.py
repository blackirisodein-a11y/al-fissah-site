# -*- coding: utf-8 -*-
# ENGLISH content
L = {
'meta': dict(tagline="International School of Arabic Language and Quran", html_lang='en', og_locale='en_GB', dir='ltr',
  title_home="AL-FISSAH — International School of Arabic Language and Quran",
  desc_home="Online Arabic and Quran lessons for non-Arabic-speaking children and adults: trained native Arabic teachers, 100% Arabic immersion, free 30-minute trial lesson.",
  org_desc="International School of Arabic Language and Quran, online, for non-Arabic-speaking children and adults."),
'js': dict(typew="Welcome to Al-Fissah", typew_sub="International School of Arabic Language and Quran", sending="Sending…",
  trial_ok="Request sent. The administration will contact you to schedule your trial lesson, in shaa Allah.",
  contact_ok="Message sent. Our advisor will reply as soon as possible, in shaa Allah.",
  err="Sending failed. Please try again, or write to us directly at {email}.",
  mail_ok="Your e-mail app is opening with the message pre-filled. Just press send.",
  subject_trial="Trial lesson request — {name}", wa="Hello, I would like to book a free 30-minute trial lesson.",
  summary=["Trial lesson request — Al-Fissah","Name","E-mail","Phone / WhatsApp","Country","Profile","Child's first name","years old","Requested programme","Current level","Availability","Message"],
  adult="adult", child="child"),
'nav': dict(accueil="Home", programmes="Programmes", tarifs="Prices", faq="FAQ", temoignages="Testimonials", reglement="School rules",
  apropos="About us", contact="Contact", mentions="Legal notice", livres="Books &amp; materials", blog="Blog",
  login="Log in", login_full="Log in — Student area", essai="Trial lesson", essai_sub="30 min free",
  essai_mob="Trial lesson — 30 min", cta_float="Request a trial lesson", menu="Open menu", totop="Back to top", language="Language"),
'footer': dict(desc="Al-Fissah, International School of Arabic Language and Quran, is an online school specialised in teaching non-Arabic speakers. Its aim is to educate children and adults, with native Arabic-speaking teachers trained in teaching non-Arabic speakers.",
  col1="The school", col2="Resources", prog_ind="Individual programmes", prog_col="Group programmes", essai="30-min trial lesson",
  faq="FAQ — Frequently asked questions", contact="Contact us", copy="Online courses", register="Sign up"),
'common': dict(discover="Discover the programme", see_prices="See prices", details="See details", session="session", request="Request one",
  updated="Last updated:", toc="Contents",
  months=['January','February','March','April','May','June','July','August','September','October','November','December']),

'home': dict(
  badge="30-minute trial lesson — on request",
  h1_pre="Arabic and the Quran,", h1_hl="taught live", h1_post=", at home.",
  lead="Al-Fissah is an international school of arabic language and quran specialised in teaching non-Arabic-speaking children and adults, with native Arabic-speaking teachers trained in teaching.",
  cta1="Request a trial lesson", cta2="See the programmes",
  note=["Children aged 5 to 18", "Adults, all levels", "100% Arabic immersion"],
  classroom={"EN DIRECT":"LIVE","Cours d'arabe · Niveau 3":"Arabic lesson · Book 3","Leçon 1 — L'alphabet":"Lesson 1 — The alphabet",
    "« Alif, Ba, Ta » — vos trois premières lettres":"“Alif, Ba, Ta” — your first three letters","Oustadh arabophone":"Native Arabic teacher",
    "✓ Essai gratuit — 30 min":"✓ Trial lesson — 30 min","Suivi individuel de chaque élève":"100% Arabic immersion"},
  journey=[("Trial lesson","30 minutes to meet a teacher and assess your level"),("Enrolment","Choose the programme, days and teacher; the administration confirms"),
    ("Live lessons","4-week sessions in the virtual classroom, 100% in Arabic"),("Exam &amp; next level","An exam at the end of each book validates moving up a level")],
  methode_kick="Our approach", methode_h2="A real Arabic school at home", methode_p="A tailored programme, total immersion and rigorous follow-up: the three pillars of the Al-Fissah school.",
  pillars=[("مَنْهَج","An innovative programme","<p><b>For children aged 5 to 18:</b> “Arabic in our children's hands”, 12 textbooks with pictures, colours, dialogues, audio…</p><p><b>For adults:</b> “Arabic in your hands”, a series divided into 10 levels, with pictures, dialogues, a simple style and exercises that aid comprehension.</p>"),
    ("غَمْر","Total immersion","<p>Immersed in the Arabic language, with no French or English, you work on <b>listening</b> and <b>speaking</b> — the two skills a non-Arabic speaker needs to progress in the best way and become an Arabic speaker in turn.</p>"),
    ("مُتَابَعَة","Rigorous follow-up","<p>Whether you are a student or a student's parent, you can follow progress, needs, difficulties and remarks in the student area, check the live timetable, contact us through a dedicated address and join lessons via an integrated platform.</p>")],
  prog_kick="Our programmes", prog_h2="Programmes designed by specialist academics",
  prog_p="Our programmes “Arabic in our children's hands” and “Arabic in your hands” were designed by academics specialised in teaching non-Arabic speakers; both come with audio for every lesson.",
  video_kick="Discover", video_h2="A classroom dialogue, in 90 seconds", video_p="Excerpt from a lesson of the programme “Arabic in our children's hands” — book 12, unit 11.", video_more="See all videos on YouTube",
  vid=dict(kick="Videos", h2="Our videos, sorted by theme", p="Lesson excerpts, reading method, invocations and testimonials: pick a theme, then a video. It plays right here.",
    cats=dict(dialogues="Dialogues for children", lecture="Learning to read", invocations="Invocations and good manners", temoignages="Testimonials", ecole="The school and the app"),
    part="Part", lesson="Lesson", playlist="See this playlist on YouTube", channel="All the channel's videos", count="{n} videos", now="Now playing"),
  adultes_kick="Adults", adultes_h2="Been learning for a while but still not speaking Arabic?",
  adultes_p="The Al-Fissah institute also teaches adults, focusing first on your speaking and comprehension so that you are able to hold a conversation. You speak and you understand.",
  adultes_checks=["Lessons exclusively in Arabic, from the very first level","Complete beginners welcome: no prerequisites","One-to-one, or in pairs for the Arabic language","Exam at the end of each book, diploma from 80%"],
  big=["Listen","Speak","Understand"], big_sub="The skills practised in immersion, with no French or English.",
  app_kick="New mobile app", app_h2="The school in your pocket", app_p="We are launching our mobile app to improve online learning.",
  app_checks=["Easy access to your lessons and follow-up","Teachers' remarks, homework and grades","Live timetable and lesson reminders"],
  phone=[("Next lesson","Wednesday 6:00 pm — Book 3"),("Teacher's remark","Very good recitation, revise unit 4"),("Timetable","2 lessons this week"),("Grades &amp; homework","Book 2 exam: 17/20")],
  store_ios="Download on the", store_android="Get it on",
  tarifs_h2="4-week sessions, at your own pace", tarifs_p="Choose the number of hours per week, starting from one one-hour lesson. Same price for Arabic and Quran.",
  plans=[("Plan 1","€28","1 h per week · 4 weeks",["Live one-to-one lesson","Arabic or Quran","Student area and follow-up","Teacher's remarks"]),
    ("Plan 2","€48","2 h per week · 4 weeks",["Live one-to-one lesson","Arabic or Quran","Student area and follow-up","Teacher's remarks"]),
    ("Plan 3","€72","3 h per week · 4 weeks",["Live one-to-one lesson","Arabic or Quran","Student area and follow-up","Teacher's remarks"]),
    ("Pair plan","€36","1 h per week · 4 weeks · for 2 people",["Arabic language only","i.e. €4.50 per student per hour","Student area and follow-up","On request to the administration"])],
  tarifs_note="Up to 7 h per week (€168). 10% discount from the second enrolment in the same family.", tarifs_all="All plans",
  blog_kick="Blog &amp; videos", blog_h2="School news", blog_p="Our articles to understand the method, and lesson excerpts to hear the classroom.",
  posts=[("http://blog.al-fissah.com/?p=2654","Method","Immersion teaching (100% Arabic): what is it? Why? (in French)","16 January 2022"),
    ("http://blog.al-fissah.com/?p=2609","The school","Who are we? (in French)","26 August 2021"),
    ("http://blog.al-fissah.com/?p=2533","Follow-up","Rigorous follow-up at Al-Fissah: what, why, how? (in French)","1 July 2021")],
  book="Book", unit="Unit", blog_note="Arabic dialogues for children — العربية بين يدي أولادنا.", blog_all="All articles", yt="YouTube channel",
  avis_h2="What our students say", avis_all="Read all 24 testimonials",
  quotes=[("“My children are progressing wonderfully: they learned to read in under 2 weeks and are reading faster and faster.”","Imrane El Boutaïbi — parent"),
    ("“Even though the lessons are entirely in Arabic, she makes everything very clear. I recommend the institute 100%, for beginners as well as for those who want to improve.”","Maeva Thezenas — Arabic language"),
    ("“I have been taking Quran lessons at Al-Fissah for several years and I am very satisfied, especially with the follow-up; the institute is always responsive and accommodating.”","Linda Bitam — Quran")],
  faq_h2="Frequently asked questions", faq_all="See all questions",
  faq=[("What are the prerequisites?","No particular level is required to join the institute: all levels are accepted, from complete beginner to advanced."),
    ("What language are lessons taught in?","Lessons are taught in Arabic. It is a 100% Arabic immersion method, which gives fast and effective results in shaa Allah. Our teachers are Egyptian and have been trained to teach non-Arabic speakers."),
    ("Is there a trial lesson?","Yes, a free 30-minute trial lesson: click « Request a free trial » and follow the steps. The trial is completely free and with no commitment."),
    ("How long is a session?","A session lasts 4 weeks and can be renewed. Not to be confused with the level: the level is the book being studied, which usually takes more than 4 weeks depending on the student."),
    ("What equipment do I need?","A stable internet connection, a computer, a headset and a microphone. Our virtual classrooms work on Windows, Mac and tablets; using a smartphone is strongly discouraged."),
    ("Where do lessons take place?","In a virtual classroom built into your student area: at lesson time, students and teacher log in and interact orally, in writing and through screen sharing.")],
),

'form': dict(kick="Trial lesson", h2="Request your 30-minute trial lesson",
  p="Meet a teacher, assess your level (or your child's) and discover the virtual classroom. The administration will contact you to set the time.",
  checks=["No level required: all levels accepted","Children aged 5 to 18 and adults","Trained native Arabic teachers"],
  next_t="What happens next", next_p="Our advisor replies as soon as possible, in shaa Allah. If the trial suits you, you choose a plan and a 4-week session starts right away, on the days you have chosen.",
  who="Who is learning?", adult="An adult", child="A child", child_name="Child's first name", age="Age", programme="Requested programme", niveau="Current level", choose="Choose…",
  programmes=["Arabic language — child (one-to-one)","Arabic language — adult (one-to-one)","Arabic language — group lesson","Quran — child or adult","Memorisation of texts (Mutūn)","Easy method to master reading","I don't know yet"],
  niveaux=["Complete beginner (cannot read Arabic)","I decode slowly","I read and understand a little","Intermediate","Advanced"],
  email="Email", coords="Your details", name="Full name", tel="Phone / WhatsApp", optional="optional", country="Country",
  dispo_t="Your availability", dispo="Days and times that suit you", dispo_hint="please state your time zone", dispo_ph="E.g. Wednesday 5–7 pm, Saturday morning (London time)",
  message="Message", msg_ph="Goals, context, questions…",
  consent="I agree that my information is used to organise my trial lesson, in accordance with the", privacy="privacy policy",
  submit="Request my trial lesson", **{'or': "or"}, whatsapp="write to us on WhatsApp"),

'progs': dict(title="Online Arabic and Quran course programmes — AL-FISSAH", desc="Arabic for children and adults, Quran, memorisation of the Mutūn, reading method: all the programmes of the Al-Fissah institute.",
  h1="Our programmes", lead="One-to-one or group lessons, for non-Arabic-speaking children and adults. Every programme comes with materials and audio, and takes place live with a native Arabic teacher.",
  toc_note="Books and materials are not provided on enrolment: order them at <a href=\"https://livres.al-fissah.com\">livres.al-fissah.com</a>. The administration guides you according to your level.",
  items=[
   dict(id='arabe-enfants', tag='Arabic language', ar='العَرَبِيَّةُ بَيْنَ أَوْلَادِنَا', titre="Arabic in our children's hands", facts=['12 textbooks','Audio included','Children 5–18'],
     court="The reference programme for non-Arabic-speaking children aged 5 to 18: 12 textbooks with pictures, colours, dialogues and audio.",
     long="""<p>“Arabic in our children's hands” is a programme designed for non-Arabic speakers, aimed at children aged 5 to 18. Developed by an elite of academics specialised in teaching, it consists of 12 textbooks with audio, pictures, colours, dialogues and exercises.</p>
<p>Your child does not speak Arabic? Arabic is not their mother tongue? With Allah's help, the Al-Fissah institute assists you and offers to make your child an Arabic speaker. You and us, together, to give your child a second language.</p>
<p>Lessons take place in immersion, exclusively in Arabic, one-to-one or in a group. Parents follow progress, remarks and homework in the student area.</p>""", cta="Enrol my child"),
   dict(id='arabe-adultes', tag='Arabic language', ar='العَرَبِيَّةُ بَيْنَ يَدَيْكَ', titre="Arabic in your hands", facts=['8 textbooks','10 levels','Adults'],
     court="The complete course for non-Arabic-speaking adults: 8 textbooks divided into 10 levels within the school, with pictures, dialogues, exercises and audio for every lesson.",
     long="""<p>“Arabic in your hands” is a series for non-Arabic speakers, aimed mainly at adults. Written by the same authors as “Arabic in our children's hands”, it consists of 8 textbooks divided into 10 levels within our school, with pictures, dialogues, a simple style and exercises that aid comprehension.</p>
<p>Been learning for a while but still not speaking Arabic? The Al-Fissah institute focuses first on your speaking and comprehension, so that you are able to hold a conversation: you speak and you understand.</p>
<p>Progress at your own pace, one-to-one or in pairs, in an authentic learning environment, 100% in Arabic.</p>""", cta="Start level 1"),
   dict(id='coran', tag='Quran', ar='القُرْآنُ الكَرِيم', titre="Quran programme for children and adults", facts=['One-to-one lessons','From 30 min','All levels'],
     court="One-to-one Quran lessons, suited to beginners and advanced students alike, with the main goal of memorising the Book of Allah.",
     long="""<p>Discover our one-to-one Quran lessons. Whether for yourself or your child, progress at your own pace with programmes carefully designed and selected at the Al-Fissah school. Suited to beginners and advanced students alike, these lessons have the main goal of enabling the student to memorise the Book of Allah. Concrete results are at stake.</p>
<p>Al-Fissah has qualified teachers experienced in teaching the Book of Allah. Our aim is to build a real Quran school at home, with rigorous and careful follow-up, so as to establish a You–Us–Teacher relationship.</p>
<p>The Quran is studied one-to-one only. 30-minute sessions are possible for the Quran.</p>""", cta="Book a lesson"),
   dict(id='mutun', tag='Islamic sciences', ar='طَالِبُ العِلْم', titre="Memorisation of texts — Mutūn", facts=['5 levels','Classical texts','With a teacher'],
     court="A progressive 5-level course to memorise the main Islamic texts: creed, hadith, fiqh, Arabic language and foundations, with a teacher's guidance.",
     long="""<p>A progressive programme for learning and memorising the main Islamic texts. It is organised in 5 levels, allowing the student to progress gradually in the study of creed, hadith, fiqh, the Arabic language and other Islamic sciences. Each level includes a selection of texts suited to the student's progress, to be memorised with a teacher's guidance.</p>
<div class="levels">
<div><b>Level 1</b><ul><li>The Nullifiers of Islam (Nawāqid al-Islām)</li><li>The Four Principles</li><li>The Three Fundamental Principles and their proofs</li><li>The Forty Hadith of an-Nawawī</li></ul></div>
<div><b>Level 2</b><ul><li>Al-Bayqūniyyah — hadith terminology</li><li>Tuhfat al-Atfāl — rules of Tajwīd</li><li>Conditions, pillars and obligations of prayer</li><li>Kitāb at-Tawhīd — The Book of Monotheism</li></ul></div>
<div><b>Level 3</b><ul><li>The poem of Abū Ishāq al-Ilbīrī</li><li>Al-Ājurrūmiyyah — introduction to grammar</li><li>Al-‘Aqīdah al-Wāsitiyyah — creed</li></ul></div>
<div><b>Level 4</b><ul><li>Al-Waraqāt — foundations of jurisprudence</li><li>Ar-Rahbiyyah — rules of inheritance</li><li>Al-‘Aqīdah at-Tahāwiyyah — creed</li></ul></div>
<div><b>Level 5</b><ul><li>Bulūgh al-Marām — hadith of legal rulings</li><li>Zād al-Mustaqni‘ — jurisprudence</li><li>Alfiyyat Ibn Mālik — Arabic grammar</li></ul></div>
</div>""", cta="Start a text"),
   dict(id='lecture', tag='Arabic language', ar='القِرَاءَة', titre="The easy method to master reading", facts=['Fluency','Speed','Accuracy'],
     court="For those who can already read: a progressive method to gain fluency, speed and accuracy while reducing reading errors.",
     long="""<p>The easy method to master reading is a programme designed for people who have already acquired the basics of reading Arabic but now wish to perfect it. Some students can read, but their reading remains slow, hesitant or still contains errors. This method allows them to progress step by step, thanks to structured and progressive learning.</p>
<p>The programme notably helps to:</p>
<ul><li>improve reading fluency;</li><li>gradually increase reading speed;</li><li>correct frequent errors;</li><li>develop more accurate and natural reading;</li><li>strengthen the student's confidence;</li><li>read Arabic texts with greater ease.</li></ul>
<p>This programme is particularly suited to those who wish to perfect their Arabic reading and prepare to approach reading the Quran, books and various Arabic texts with more ease.</p>""", cta="Assess my reading"),
   dict(id='collectifs', tag='Group lessons', ar='الدُّرُوسُ الجَمَاعِيَّة', titre="Group Arabic lessons — levels 1 to 12", facts=['3 h / week','3 to 10 students','Children'],
     court="Your child progresses alongside other children: more stimulating, with the desire to get more involved. Groups of 3 to 10 students, 3 hours per week.",
     long="""<p>Discover our group Arabic lessons. Your child progresses alongside other children: it is more stimulating, with the desire to get more involved. Classes generally consist of 3 to 10 students at most and follow the programme “Arabic in our children's hands”, from level 1 to level 12, at 3 hours per week.</p>
<p>Times, days and the start and end of the session are to be confirmed with the administration. Can't see a group at your level? Contact us: we will put you on a waiting list and form a group with other students at your level.</p>
<p>The Quran is not studied in groups; it is taught one-to-one only.</p>""", cta="Join a group"),
  ]),

'tarifs': dict(title="Prices of online Arabic and Quran lessons — AL-FISSAH", desc="Prices for one-to-one Arabic and Quran lessons: 4-week sessions from €28 (1 h/week) to €168 (7 h/week), pair plan €36.",
  h1="Prices for one-to-one lessons", lead="Lessons run over 4 weeks. The student chooses the number of hours to study, with a minimum of one one-hour lesson per week.",
  badge="Most popular", badge_reco="Recommended", formule="Plan", per="{h} h per week<br>for 4 weeks", choose="Choose", duo="Pair plan", duo_per="1 h per week for 4 weeks<br><b>for 2 people</b>", ask="Ask",
  arabe_kick="Arabic language", arabe_h2="Arabic language lessons", arabe_p="Programmes “Arabic in our children's hands” and “Arabic in your hands”, reading method.",
  coran_kick="Quran", coran_h2="Quran lessons", coran_p="One-to-one lessons only. 30-minute sessions are possible for the Quran: contact the administration.",
  good_h2="Good to know",
  values=[("٪١٠","Family discount","From the second enrolment in the same family, a 10% discount on sessions is granted."),
    ("٢","Lessons in pairs","Possible for the Arabic language: €4.50 per student per hour, i.e. €36 for a 4-week session of 1 h per week for two people."),
    ("٤","Session ≠ level","A session lasts 4 weeks and can be renewed. The level is the book being studied: it usually takes more than 4 weeks.")],
  pay_h2="Payment and renewal",
  pay_body="""<p>Payment is made by bank card through a secure link (Stripe) or by bank transfer. Sessions are renewed automatically every 4 weeks with a scheduled payment. To cancel the subscription, inform the administration at least 7 days before the end of the current session.</p>
<p>All enrolments are final: no postponement or refund is granted after payment of the session. Enrol only if you are available and motivated to learn. Books and materials are not provided on enrolment and must be ordered at <a href="https://livres.al-fissah.com">livres.al-fissah.com</a>.</p>
<p>Lessons in pairs or in a group: you enrol with your own partner or your own group (3 to 10 students). The school does not form groups. The group price is given by the administration at enrolment.</p>""",
  note_b="Not decided yet?", note_p="Start with a 30-minute trial lesson."),

'faq': dict(title="FAQ — Online Arabic and Quran lessons — AL-FISSAH", desc="Enrolment, immersion method, books used, sessions, trial lesson, payment, equipment: all the answers from the Al-Fissah institute.",
  h1="Frequently asked questions", lead="Everything you need to know before starting: enrolment, method, books, sessions, payment and equipment.",
  note_b="Can't find the answer to your question?", note_a="Contact us", note_p=", our team will reply as soon as possible, in shaa Allah.",
  items=[
 ('How do I enrol?', """<p>Enrolment is done entirely online. Simply click « Get started now » and follow the steps.</p>
<p>You can choose between:</p>
<ul><li>a one-to-one lesson;</li><li>a lesson in pairs;</li><li>a group lesson.</li></ul>
<p>For lessons in pairs and in a group, the students must be brought together at the time of enrolment. One person must be designated as responsible for the pair or the group, for the handling of payments. You come with your own partner or group: the school does not form groups.</p>"""),
 ('What are the prerequisites?', '<p>No particular level is required to join the institute. All levels are accepted, from complete beginner to advanced.</p>'),
 ('What teaching method do you use?', "<p>Our lessons follow a progressive method, adapted to each student's level. The programme and the materials are set according to the subject studied and to the student's level.</p>"),
 ('Which books are used?', """<p>The books used depend on the programme and on the student's level.</p>
<p>If the books required are not provided at enrolment, you will find in the « Remarks » section the information needed to order them from the website indicated.</p>"""),
 ('What language are lessons taught in?', '<p>Lessons are taught in Arabic. It is a 100% Arabic immersion method, which gives fast and effective results in shaa Allah. Our teachers are Egyptian and have been trained to teach non-Arabic speakers; moreover, the programmes used were specially designed for non-Arabic speakers.</p>'),
 ('How long is a session?', "<p>A session lasts 4 weeks, with the option to renew as you wish. <b>Please note</b>, do not confuse the session and the level. A session lasts 4 weeks; the level (1, 2, 3, 4…) is the book being studied, which generally takes more than 4 weeks depending on the student's level.</p>"),
 ('How big is a group?', '<p>A class generally consists of 3 to 10 students at most.</p>'),
 ('Can the Quran be studied in a group?', '<p>No, it is not possible to study the Quran in a group.</p>'),
 ('Is it possible to study for 30 minutes?', '<p>Yes, it is possible to study for 30 minutes, for the Quran only.</p>'),
 ('Is it possible to study in pairs?', """<p>Yes, this is possible for the Arabic language.</p>
<p>To do so, you must enrol directly as a pair when you register.</p>"""),
 ('What is the price for a pair?', '<p>The price is €4.50 per student. Example: for 1 hour per week for 4 weeks, €4.50 × 2 (pair) = €9 × 4 (weeks) = <b>€36</b>.</p>'),
 ('Is there a trial lesson or trial period?', """<p>Yes. You can have a free 30-minute trial lesson.</p>
<p>To do so, click « Request a free trial » and follow the steps to send your request.</p>
<p>The trial is completely free and with no commitment.</p>"""),
 ('If I change my mind, can I cancel my enrolment?', '<p>All enrolments are final; no postponement or refund will be granted. Enrol only if you are available and motivated to learn.</p>'),
 ('How do I make the payment?', '<p>Payment is made by bank card or by bank transfer.</p>'),
 ('What equipment is needed to follow the lessons?', """<p>To follow the lessons in good conditions, we recommend:</p>
<ul><li>a stable internet connection;</li><li>a computer;</li><li>a headset;</li><li>a microphone.</li></ul>
<p>Our virtual classrooms work on Windows and Mac computers, as well as on tablets.</p>
<p>Using a smartphone is strongly discouraged, so that the lessons run as well as possible.</p>"""),
 ('Where do lessons take place?', """<p>Lessons take place remotely, in a virtual classroom built directly into the student area.</p>
<p>Once logged in to your account, you can enter your classroom from your personal area.</p>"""),
 ('Once payment is made, when do lessons start?', '<p>Lessons start after enrolment and once your request has been approved by the office.</p>'),
  ]),

'temoignages': dict(title="Student and parent testimonials — AL-FISSAH", desc="What our students say: parents and students of the Al-Fissah institute, online Arabic and Quran lessons.",
  h1="What our students say", lead="{n} testimonials from parents and students, published between 2021 and 2025 in the student area.",
  s1="testimonials", s2="average rating", s3="families of child students", s4="first reviews", date_fmt="{d} {m} {y}",
  tags={'Enfants':'Children','Langue arabe':'Arabic language','Coran':'Quran','Lecture &amp; Coran':'Reading &amp; Quran'},
  lang_note="Testimonials are shown in their original language (French), as written by the students and parents.",
  note_b="Are you a student or a student's parent?", note_p="You can leave your testimonial from your", note_a="student area"),

'reglement': dict(title="School rules — AL-FISSAH", desc="The Al-Fissah school rules: behaviour, equipment, time slots, attendance and absences, payment, exams, disputes.",
  h1="School rules", lead="The Al-Fissah school specialises in teaching the Arabic language, the Quran and its various subjects. It has no political affiliation and supports no activity contrary to the teachings of the Quran and the Sunnah.",
  updated="February 2025", article="Article",
  articles=[
 ("Student behaviour", """<p>Every student must behave in accordance with Islamic values and the principles of the student of knowledge. They must respect their teachers as well as members of the administration. In case of a problem, the student must inform the administration so that a solution can be found as soon as possible.</p>
<p>The administration reserves the right, after observing inappropriate behaviour by a student towards a teacher or a member of the administration, to exclude that student without notice.</p>
<p>Exchanging personal contact details between students and salaried teachers is forbidden.</p>"""),
 ("Equipment", """<p>Using smartphones for studying is not recommended. A tablet at minimum is recommended, and a PC is preferable. We do not guarantee that all tools will work correctly for smartphone users.</p>
<p>Before each lesson, every student must make sure their equipment works properly by checking:</p>
<ul><li>the connection of the microphone and headset;</li><li>that programmes unrelated to the lesson are closed (in particular apps using audio or video such as Messenger).</li></ul>"""),
 ("Time slots", """<p>Students may ask to change their time slot by contacting the administration. We will do our utmost to satisfy this request. However, the school cannot be held responsible for lost days if teachers are not available in the slot the student wants.</p>
<p>If necessary, the school may ask the student to change slot if a teacher has to stop or if one of the prayers coincides with the chosen slot.</p>"""),
 ("General organisation of studies", """<p>Students must complete all homework given by teachers. Behaviour respectful of Islam towards teachers and the administration is required.</p>
<p>It is also compulsory for students or their parents to regularly consult the teachers' remarks. These comments are essential to know the homework, the revisions, and whether the session is over. Active cooperation is expected from everyone to ensure careful follow-up and the smooth running of lessons.</p>"""),
 ("Attendance and absences", """<h3>Lateness</h3>
<p>The student must be punctual. If more than 30 minutes late for a one-hour lesson or 15 minutes for a 30-minute lesson, the lesson will be cancelled and counted as completed.</p>
<p>If the teacher is more than 10 minutes late, the student must promptly inform the administration. The student must wait 15 minutes before logging out if the teacher is late; beyond that, the lesson will be considered an absence by the student.</p>
<h3>Absences</h3>
<p>Any absence, justified or not, without at least 24 hours' notice given during office hours (8:00 am to 6:00 pm), will be deducted from the student's study days. A student may be absent with justification for a number of days equal to their weekly lesson days. Beyond that number, any absence will be counted as unjustified, <b>and this also includes slot changes in case of absence, even if it is a different time on the same day or in the same week.</b></p>
<div class="note"><b>Example:</b> a student with two lesson days per week may be absent up to two days per month with justification. Any additional absence will be deducted.</div>
<h3>Temporary break</h3>
<p>For an extended break of three days or more, the student must inform the administration at least one week in advance. The student will lose priority on their slot and teacher when resuming. The count of remaining days will be valid for three months, after which missed lessons can no longer be recovered. If the student does not give one week's notice, they will lose the remaining study days.</p>"""),
 ("Payment terms", """<p>Payment is made by bank card through a secure link. Sessions are renewed automatically every 4 weeks with a scheduled payment. To cancel the subscription, please inform the administration at least 7 days before the end of the current session. If you do not, the automatic payment will be maintained.</p>
<p><b>Discount:</b> from the second enrolment in the same family, a 10% discount on sessions is granted.</p>"""),
 ("Organisation of exams", """<p>An exam is compulsory at the end of each session or book. The student will not be counted among those who have completed the level without having taken this exam.</p>
<p>The student may not be absent on exam day except with notice to the administration and a valid justification, assessed by the administration. If the student does not attend without justification, they will not be able to obtain official documents (diploma, certificates…).</p>
<table><tr><th>Result</th><th>Consequence</th></tr><tr><td>Over 60%</td><td>Moves up to the next level</td></tr><tr><td>Over 80% and the teacher's permission</td><td>Diploma awarded</td></tr></table>
<p>The exam must be printed before the lesson starts. Without prior printing, the lesson will be cancelled and counted as completed.</p>"""),
 ("Payment rules", """<p>No refund will be made after payment of the session.</p><p>If a student is expelled from the school, no refund will be made.</p>"""),
 ("Disputes", """<ul><li>Any complaint must be detailed (circumstances, date, time, nature of the problem).</li><li>In case of dispute, the student must provide audio evidence.</li><li>Recording lessons is allowed for evidence purposes in case of dispute.</li><li>Without evidence, the complaint will not be accepted.</li><li>The Management will handle the complaint within 7 days.</li></ul>"""),
  ]),

'apropos': dict(title="About the Al-Fissah institute — Arabic and Quran online", desc="International school of Arabic language and Quran: online lessons for non-Arabic-speaking children and adults, with trained native Arabic teachers.",
  h1="Online Arabic and Quran lessons", lead="Al-Fissah is an international school of arabic language and quran specialised in teaching non-Arabic-speaking children and adults, with native Arabic-speaking teachers trained in teaching.",
  stats=[("12","children's textbooks"),("10","adult levels"),("100%","in Arabic"),("2020","online lessons since")],
  prog_h2="Our programme",
  prog_body="""<p>Our programmes “Arabic in our children's hands (العَرَبِيَّةُ بَيْنَ أَوْلَادِنَا)” and “Arabic in your hands (العَرَبِيَّةُ بَيْنَ يَدَيْكَ)” were designed by academics specialised in teaching non-Arabic speakers. The first consists of 12 textbooks, the second of 8 textbooks divided into 10 levels within our school; both come with audio for every lesson.</p>
<p>Our aim is to create a real Arabic school at home, with rigorous and careful follow-up, so as to establish an Us–You–Teacher relationship and gather around you or your child to give everyone the best possible education.</p>""",
  is_h2="Al-Fissah is…",
  values=[("مَنْهَج","A tailored programme","Enjoy a programme tailored to each person: dialogues, exercises, activities, audio, exams…"),
    ("مُتَابَعَة","Rigorous follow-up","In the student area, follow homework, remarks, grades… A You–Us–Teacher relationship for greater success."),
    ("مُعَلِّم","Trained teachers","Give the whole family the chance to learn with a real teacher: native Arabic-speaking, trained, qualified."),
    ("١٠٠٪","100% Arabic","Immerse the whole family in the Arabic language for effective progress."),
    ("قُرْآن","Quran lessons","Bring Arabic and Quran learning together in one school."),
    ("بَيْت","A real school at home","No need to go out or travel: the Arabic school is at home.")],
  coran_h2="Online Quran lessons",
  coran_body="""<p>Al-Fissah has also taken the teaching of the Quran to heart. Certainly, the student, having begun learning the Arabic language, needs to add the learning of the Quran to it.</p>
<p>Al-Fissah has qualified teachers experienced in teaching the Book of Allah. Our aim is also to build a real Quran school at home, with rigorous and careful follow-up, so as to establish a You–Us–Teacher relationship and give the whole family the best possible education.</p>""",
  more_h2="Read more", read="Read the article on the blog (French)",
  links=[("http://blog.al-fissah.com/?p=2654","Immersion teaching (100% Arabic): what is it? Why?"),("http://blog.al-fissah.com/?p=2609","Who are we?"),("http://blog.al-fissah.com/?p=2533","Rigorous follow-up at Al-Fissah: what, why, how?")],
  note_b="Would you like to meet us?", note_p="The best way to discover the school is a 30-minute trial lesson."),

'contact': dict(title="Contact — Al-Fissah institute, online Arabic and Quran lessons", desc="Contact the Al-Fissah institute: our advisor replies as soon as possible, in shaa Allah.",
  h1="We are here to help", lead="Fill in this form and our advisor will reply as soon as possible, in shaa Allah.",
  mail_t="By e-mail", mail_p="For any administrative or teaching question.",
  hours_t="Office hours", hours_p="Monday to Friday, 9 am to 6 pm (Paris time). Absences must be reported during office hours (8 am – 6 pm), at least 24 h in advance.",
  new_t="New here?", new_p="Request a 30-minute trial lesson rather than a simple message: you will meet a teacher directly.",
  form_t="Contact us", nom="Last name", prenom="First name", sujet="Subject", message="Message", send="Send",
  subjects=["Enrolment / trial lesson","Group lessons (with my own group)","Lessons in pairs","Change of slot or teacher","Student area / login","Payment / invoice","Books and materials","Other"]),

'mentions': dict(title="Legal notice &amp; privacy — AL-FISSAH", desc="Legal notice, terms of sale and privacy policy of the al-fissah.com website.",
  h1="Legal notice and privacy", lead="Information about the site publisher, hosting, intellectual property and the protection of your data.", updated="September 2026",
  toc=[("editeur","Site publisher"),("hebergement","Hosting"),("propriete","Intellectual property"),("cgv","Terms of sale"),("droit","Governing law"),("confidentialite","Privacy"),("transferts","Data transfers"),("cookies","Cookies"),("contact","Contact")],
  body="""<div class="note"><b>To be completed before going live.</b> The bracketed items must be filled in: registered address, New Mexico business ID, registered agent, publication manager and hosting provider.</div>
<h2 id="editeur">Site publisher</h2>
<dl><dt>Name</dt><dd>Al-Fissah LLC — operator of the Al-Fissah International School of Arabic Language and Quran</dd>
<dt>Legal form</dt><dd>Limited Liability Company (LLC) under United States law</dd>
<dt>State of registration</dt><dd>New Mexico, United States of America</dd>
<dt>Registered office</dt><dd>[Full address, New Mexico, USA]</dd>
<dt>Business ID</dt><dd>[NM Business ID issued by the New Mexico Secretary of State]</dd>
<dt>Registered agent</dt><dd>[Name and address of the registered agent]</dd>
<dt>Publication manager</dt><dd>[First and last name of the manager]</dd>
<dt>Email</dt><dd><a href="mailto:c.alfissah@gmail.com">c.alfissah@gmail.com</a></dd></dl>
<h2 id="hebergement">Hosting</h2><p>The al-fissah.com website is hosted by [host name], [address], [phone or website].</p>
<h2 id="propriete">Intellectual property</h2><p>The entire site — texts, textbooks, audio files, illustrations, logo and the name “Al-Fissah” — is protected by intellectual property law and remains the exclusive property of Al-Fissah LLC or its partners. Any reproduction, display, adaptation or distribution, in whole or in part, without prior written permission is prohibited. Teaching materials provided to students are for strictly personal use within the lessons.</p>
<h2 id="cgv">Terms of sale</h2><p>Lessons are sold in 4-week sessions, payable in advance by card (Stripe) or bank transfer. Sessions renew automatically every 4 weeks; cancellation must be notified to the administration at least 7 days before the end of the current session. Prices are shown in euros on the <a href="tarifs.html">Prices</a> page. The 30-minute trial lesson is free with no obligation to buy.</p>
<p>Every enrolment is final: no postponement or refund is granted once a session has been paid for, in accordance with the <a href="reglement.html">school rules</a>, which form an integral part of these terms.</p>
<p>Students residing in the European Union benefit from the 14-day right of withdrawal provided by the consumer law of their country of residence. As lessons are a service starting on an agreed date, a student who asks for lessons to begin before that period ends acknowledges that the right of withdrawal lapses for services already delivered.</p>
<h2 id="droit">Governing law</h2><p>These notices and the contractual relationship with Al-Fissah LLC are governed by the law of the State of New Mexico (USA), without prejudice to the mandatory consumer-protection provisions applicable in the student's country of habitual residence. Any dispute will first be handled amicably with the administration; failing agreement, it falls to the competent courts of New Mexico, except where the consumer's national law reserves jurisdiction to its own courts.</p>
<h2 id="confidentialite">Privacy policy</h2>
<p>Al-Fissah LLC is the controller of the data collected on this site. As a large share of our students reside in the European Union, we apply the General Data Protection Regulation (GDPR) to all our processing.</p>
<h3>Data collected</h3><p>When you request a trial lesson, contact us or enrol, we collect: first and last name, email, phone (optional), country and, for a minor student, the child's first name and age. During the lessons we keep teaching follow-up data (attendance, teacher comments, marks, exams).</p>
<h3>Purposes</h3><ul><li>organising the trial lesson and regular lessons;</li><li>providing teaching follow-up and communicating with the student or parents;</li><li>managing invoicing and payments;</li><li>with your consent, informing you of school news.</li></ul>
<h3>Legal basis and retention</h3><p>Processing is based on performance of the contract and, for news emails, on your consent. Data is kept for the duration of the enrolment and then 3 years after the last contact; billing data is kept in line with applicable accounting obligations.</p>
<h3>Recipients</h3><p>Data is accessible to the school administration and to the assigned teacher, solely for the purposes described above. It may be processed by our technical providers (hosting, virtual classroom, Stripe payments, email delivery) strictly within their remit. It is never sold or transferred.</p>
<h3>Your rights</h3><p>You have the right to access, rectify, erase, restrict, object to and port your data. To exercise these rights, write to <a href="mailto:c.alfissah@gmail.com">c.alfissah@gmail.com</a>. You may also lodge a complaint with the supervisory authority of your country of residence.</p>
<h3>Minors</h3><p>Data concerning a minor student is provided and managed by their parent or legal guardian, who remains the school's sole point of contact.</p>
<h2 id="transferts">Transfers outside the European Union</h2><p>As Al-Fissah LLC is established in the United States, student data is processed and stored, in whole or in part, outside the European Union. These transfers are covered by the appropriate safeguards required by the GDPR, in particular the European Commission's standard contractual clauses signed with our providers. You may request a copy of these safeguards by writing to <a href="mailto:c.alfissah@gmail.com">c.alfissah@gmail.com</a>.</p>
<h2 id="cookies">Cookies</h2><p>The al-fissah.com website uses Google Tag Manager for audience measurement, together with strictly necessary technical cookies (student area session). Fonts are loaded from Google Fonts and videos from YouTube (“nocookie” mode); these services may record your IP address when loading.</p>
<h2 id="contact">Contact</h2><p>For any question about these notices or your data: <a href="mailto:c.alfissah@gmail.com">c.alfissah@gmail.com</a>, or via the <a href="contact.html">Contact</a> page.</p>"""),

'nf': dict(title="Page not found — AL-FISSAH", h1="This page does not exist", p="The link may be old, or the address contains a typo. Here is where to go:", home="Back to home"),
}

# ---- Page inscription.html : formulaire d'inscription aux études (parcours distinct du cours d'essai).
# Les libellés communs aux deux formulaires (adulte/enfant, niveau, e-mail, pays…) sont repris de L['form'].
L['signup'] = dict(kick="Enrolment", h2="Enrol in a 4-week session",
  p="Choose the programme, the plan and your days. The administration contacts you to confirm the teacher and the timetable before any payment.",
  checks=["Live one-to-one lessons with a native Arabic teacher","4-week sessions, renewable","Student area: follow-up, timetable, teacher's remarks"],
  next_t="What happens next", next_p="The administration replies as soon as possible, in shaa Allah: teacher, timetable, then payment of the session. Your lessons start as soon as it is confirmed.",
  who="The student", programme="Programme",
  programmes=[('arabe-enfants',"Arabic language — child (one-to-one)"),('arabe-adultes',"Arabic language — adult (one-to-one)"),('collectifs',"Arabic language — group lesson (children)"),('coran',"Quran — child or adult"),('mutun',"Memorisation of texts (Mutūn)"),('lecture',"Easy method to master reading")],
  rythme_t="Plan and pace", hours="Plan", hours_hint="same price for Arabic and Quran", hours_opt="Plan {h} — {h} h per week — €{e} per 4-week session",
  duo_opt="Two-student plan — 1 h per week for 2 people — €36 (Arabic language only)", group_opt="Group lesson — 3 h per week (price given by the administration)",
  days="Preferred days and times", start="Preferred start", start_opts=["As soon as possible","Within 2 to 4 weeks","Next month","To be agreed with the administration"],
  name="Full name (of the parent if the student is a minor)",
  valid_t="Confirmation", msg_ph="Goals, preferred teacher, details…",
  rules_pre="I have read and accept the", rules_link="school rules", rules_post=" (commitment for the whole 4-week session).",
  consent="I agree that my information is used to process my enrolment, in accordance with the",
  submit="Send my enrolment request")
L['js'].update(signup_ok="Enrolment request sent. The administration will contact you to confirm the teacher and the timetable, in shaa Allah.",
  subject_signup="Enrolment — {name}", wa_signup="Hello, I would like to enrol in the courses (enrolment, not a trial lesson).",
  summary_signup=["Enrolment — Al-Fissah","Name","E-mail","Phone / WhatsApp","Country","Profile","years old","Programme","Current level","Plan","Preferred days and times","Preferred start","Message"])
