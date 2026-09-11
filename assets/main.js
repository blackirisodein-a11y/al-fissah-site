/* ============================================================
   AL-FISSAH — script commun à toutes les pages
   ============================================================ */
const $=(s,r=document)=>r.querySelector(s),$$=(s,r=document)=>[...r.querySelectorAll(s)];
const mq=matchMedia('(prefers-reduced-motion: reduce)');

/* ---------- Préloader (page d'accueil uniquement) ---------- */
const loader=$('#loader');
let introSeen=false;try{introSeen=!!sessionStorage.getItem('af-intro')}catch(e){}
if(loader&&introSeen){
  // Déjà vu dans cette session (clic sur le logo, retour à l'accueil) : on n'affiche pas l'écran d'ouverture.
  loader.remove();document.body.classList.add('ready');
}else if(loader){
  try{sessionStorage.setItem('af-intro','1')}catch(e){}
  const T=window.I18N||{};const twMsg=T.typew||"Bienvenue à Al-Fissah",twEl=$('#typew'),subEl=$('#typew-sub');
  if(subEl)subEl.textContent=T.typew_sub||"École internationale de langue arabe et du Coran";
  let twI=0,twDone=false;
  // Rythme volontairement posé : le titre s'écrit en ~1,8 s (≈ 85 ms par lettre), puis le sous-titre
  // apparaît en fondu et l'ensemble reste affiché ~2 s avant l'ouverture du site (≈ 4,6 s au total).
  const twSpeed=Math.min(110,Math.max(60,Math.round(1800/Math.max(twMsg.length,1))));
  (function type(){
    if(twI<twMsg.length){twEl.textContent+=twMsg[twI++];setTimeout(type,twSpeed)}
    else{loader.classList.add('typed');setTimeout(()=>{twDone=true},2200)}
  })();
  const closeLoader=()=>{if(loader.classList.contains('done')||loader.classList.contains('closing'))return;
    // ne jamais fermer avant la fin du message et du temps de lecture : on repousse
    if(!twDone){setTimeout(closeLoader,120);return}
    loader.classList.add('closing');
    setTimeout(()=>{loader.classList.add('done');document.body.classList.add('ready')},520)};
  addEventListener('load',()=>setTimeout(closeLoader,900));
  setTimeout(closeLoader,4600);
}else{document.body.classList.add('ready')}

/* ---------- Header au scroll ---------- */
const hd=$('#hd');
if(hd)addEventListener('scroll',()=>hd.classList.toggle('scrolled',scrollY>30),{passive:true});

/* ---------- Menu mobile ---------- */
const burger=$('#burger'),mob=$('#mobmenu');
if(burger&&mob){
  burger.addEventListener('click',()=>{const o=!mob.classList.contains('open');
    mob.classList.toggle('open',o);burger.classList.toggle('open',o);
    burger.setAttribute('aria-expanded',o);mob.setAttribute('aria-hidden',!o);
    document.body.style.overflow=o?'hidden':''});
  $$('a',mob).forEach(a=>a.addEventListener('click',()=>{if(mob.classList.contains('open'))burger.click()}));
}

/* ---------- Symboles flottants ---------- */
const cv=$('#floatsyms');
if(cv&&!mq.matches){
  const ctx=cv.getContext('2d');let syms=[],W,H;
  // Décor à 5-12 % d'opacité : une résolution plafonnée à 1,5× suffit (moitié moins de pixels à redessiner sur mobile).
  const dpr=()=>Math.min(devicePixelRatio||1,1.5);
  const size=()=>{W=cv.width=innerWidth*dpr();H=cv.height=innerHeight*dpr()};
  const make=()=>{const d=dpr();syms=[];
    const chars=['A','a','1','2','\u03c0','\u2211','\u221a','=','+','x\u00b2','\u0627','\u0628','\u062a','\u0641','\u0645','\u0646','\u064a','\u0661','\u0662','\u0663'];
    const ns=Math.min(20,Math.floor(innerWidth/68));
    for(let i=0;i<ns;i++){const ch=chars[Math.floor(Math.random()*chars.length)];
      syms.push({x:Math.random()*W,y:Math.random()*H,s:(22+Math.random()*26)*d,vx:(Math.random()-.5)*.18*d,vy:(-.08-Math.random()*.16)*d,
        o:.05+Math.random()*.07,or:Math.random()<.4,ph:Math.random()*Math.PI*2,rot:(Math.random()-.5)*.3,ch,ar:/[\u0600-\u06FF]/.test(ch)})}};
  // 30 images/s et déplacement calculé sur le temps écoulé : même vitesse qu'avant sur tous les écrans (60 ou 120 Hz), moitié moins de travail.
  let last=0;
  const tick=t=>{if(t-last<32){requestAnimationFrame(tick);return}
    const k=Math.min(3,(t-(last||t-16))/16);last=t;ctx.clearRect(0,0,W,H);
    for(const p of syms){p.x+=p.vx*k;p.y+=p.vy*k;
      if(p.y<-60)p.y=H+60;if(p.x<-60)p.x=W+60;if(p.x>W+60)p.x=-60;
      const b=.7+.3*Math.sin(t/1100+p.ph);
      ctx.save();ctx.translate(p.x,p.y);ctx.rotate(Math.sin(t/2800+p.ph)*p.rot);
      ctx.font=`${p.s}px ${p.ar?'Amiri,serif':"'Space Grotesk',sans-serif"}`;
      ctx.fillStyle=p.or?`rgba(217,111,15,${(p.o*b).toFixed(2)})`:`rgba(36,65,140,${(p.o*b).toFixed(2)})`;
      ctx.fillText(p.ch,0,0);ctx.restore()}
    requestAnimationFrame(tick)};
  size();make();requestAnimationFrame(tick);addEventListener('resize',()=>{size();make()});
}

/* ---------- Révélation au scroll ---------- */
const io=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting){e.target.classList.add('show');io.unobserve(e.target)}}),{threshold:.18});
$$('.io').forEach(el=>io.observe(el));

/* ---------- Tilt 3D + boutons magnétiques ---------- */
if(matchMedia('(pointer:fine)').matches&&!mq.matches){
  $$('.tilt').forEach(card=>{
    card.addEventListener('mousemove',e=>{const r=card.getBoundingClientRect(),
      x=(e.clientX-r.left)/r.width-.5,y=(e.clientY-r.top)/r.height-.5;
      card.style.transform=`rotateY(${x*7}deg) rotateX(${-y*7}deg) translateY(-4px)`});
    card.addEventListener('mouseleave',()=>card.style.transform='')});
  $$('.btn').forEach(b=>{
    b.addEventListener('mousemove',e=>{const r=b.getBoundingClientRect();
      b.style.translate=`${(e.clientX-r.left-r.width/2)*.2}px ${(e.clientY-r.top-r.height/2)*.32}px`});
    b.addEventListener('mouseleave',()=>b.style.translate='')});
}

/* ---------- Barre de progression + flottants + parallaxe ---------- */
const bar=$('#progress'),top_=$('#totop'),ctaF=$('#ctafloat');
const pb1=$('.blob.b1'),pb2=$('.blob.b2'),pb3=$('.blob.b3'),pa1=$('.aur.a1'),pa2=$('.aur.a2');
addEventListener('scroll',()=>{const h=document.documentElement,y=scrollY;
  if(bar)bar.style.width=(h.scrollTop/(h.scrollHeight-h.clientHeight)*100)+'%';
  if(top_)top_.classList.toggle('on',y>700);
  if(ctaF)ctaF.classList.toggle('on',y>innerHeight*.55);
  if(!mq.matches){
    if(pb1)pb1.style.translate=`0 ${y*.06}px`;if(pb2)pb2.style.translate=`0 ${-y*.04}px`;if(pb3)pb3.style.translate=`0 ${y*.05}px`;
    if(pa1)pa1.style.translate=`0 ${y*.08}px`;if(pa2)pa2.style.translate=`0 ${-y*.05}px`;
    if(cv)cv.style.translate=`0 ${y*.03}px`}},{passive:true});
if(top_)top_.addEventListener('click',()=>scrollTo({top:0,behavior:'smooth'}));

/* ---------- Étincelles du CTA ---------- */
const ctaInner=$('.cta .inner');
if(ctaInner&&!mq.matches){
  for(let i=0;i<20;i++){const s=document.createElement('span');s.className='tw';
    const sz=3+Math.random()*4;s.style.cssText=`width:${sz}px;height:${sz}px;left:${Math.random()*100}%;top:${Math.random()*100}%;animation-delay:${(Math.random()*3).toFixed(2)}s;animation-duration:${(2.4+Math.random()*2.4).toFixed(2)}s`;
    ctaInner.appendChild(s)}
}

/* ---------- Leçons qui se succèdent dans la classe virtuelle ---------- */
const crL=$('#crlesson'),crA=$('#crar'),crT=$('#crtrad');
if(crL&&crA&&crT){
  const lessons=[
    {t:"Leçon 1 — L'alphabet",a:"ا \u00b7 ب \u00b7 ت",f:"\u00ab Alif, Ba, Ta \u00bb — vos trois premières lettres"},
    {t:"Leçon 4 — Les salutations",a:"مَرْحَبًا",f:"\u00ab Bienvenue \u00bb — répétez après moi"},
    {t:"Leçon 7 — Se présenter",a:"أَنَا طَالِبٌ",f:"\u00ab Je suis un étudiant \u00bb"},
    {t:"Leçon 12 — La famille",a:"هٰذِهِ عَائِلَتِي",f:"\u00ab Voici ma famille \u00bb"},
    {t:"Cours de Coran — Tajwid",a:"بِسْمِ اللهِ الرَّحْمٰنِ الرَّحِيمِ",f:"Lecture avec les règles de tajwid"}];
  let li=0;
  crA.addEventListener('animationiteration',()=>{li=(li+1)%lessons.length;
    crL.classList.add('sw');crT.classList.add('sw');
    setTimeout(()=>{const L=lessons[li];crL.textContent=L.t;crA.textContent=L.a;crT.textContent=L.f;
      crL.classList.remove('sw');crT.classList.remove('sw')},180)});
}

/* ---------- Accordéons (FAQ, règlement, support) ---------- */
$$('.qa button').forEach(b=>b.addEventListener('click',()=>{
  const qa=b.parentElement,open=qa.classList.contains('open'),group=qa.parentElement;
  $$('.qa.open',group).forEach(o=>{o.classList.remove('open');$('button',o).setAttribute('aria-expanded','false')});
  if(!open){qa.classList.add('open');b.setAttribute('aria-expanded','true')}}));

/* ---------- Scrollspy ---------- */
const spyLinks=$$('header ul.menu a[href^="#"]').filter(a=>a.getAttribute('href').length>1);
if(spyLinks.length){
  const spyMap=new Map(spyLinks.map(a=>[a.getAttribute('href').slice(1),a]));
  const spy=new IntersectionObserver(es=>es.forEach(e=>{const l=spyMap.get(e.target.id);if(!l)return;
    if(e.isIntersecting){spyLinks.forEach(a=>a.classList.remove('active'));l.classList.add('active')}}),{rootMargin:'-40% 0px -55% 0px'});
  spyMap.forEach((l,id)=>{const sec=document.getElementById(id);if(sec)spy.observe(sec)});
}

/* ---------- Vidéo de présentation ---------- */
/* Vidéo YouTube : le lecteur n'est chargé qu'au clic sur l'image (il pesait ≈ 1 Mo dès l'ouverture de la page sur bureau). */
$$('.yt-poster').forEach(p=>{p.addEventListener('click',()=>{if(p.classList.contains('hide'))return;
  const f=document.createElement('iframe');f.src=`https://www.youtube-nocookie.com/embed/${p.dataset.yt}?autoplay=1&rel=0`;
  f.title=p.getAttribute('aria-label')||'';f.allow='accelerometer; autoplay; encrypted-media; picture-in-picture';f.allowFullscreen=true;
  f.style.cssText='position:absolute;inset:0;width:100%;height:100%;border:0';p.parentElement.appendChild(f);p.classList.add('hide')})});
const vid=$('#presvid'),poster=$('#poster');
if(vid&&poster){
  const playVid=()=>{vid.style.display='block';poster.classList.add('hide');vid.play().catch(()=>{})};
  poster.addEventListener('click',playVid);
  poster.addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' ')playVid()});
}

/* ============================================================
   FORMULAIRE D'ESSAI GRATUIT
   ------------------------------------------------------------
   Deux modes, sans serveur à gérer :
   1) FORM_ENDPOINT renseigné (Formspree, Getform, Basin, Web3Forms…)
      → envoi en AJAX, message de confirmation à l'écran.
   2) FORM_ENDPOINT vide → ouverture d'un e-mail pré-rempli vers
      CONTACT_EMAIL (fonctionne partout, sans configuration).
   ============================================================ */
const FORM_ENDPOINT="";                       // ex. "https://api.web3forms.com/submit" ou "https://formspree.io/f/xxxxxxxx"
const FORM_KEY="";                            // clé Web3Forms (laisser vide pour Formspree/Getform)
const CONTACT_EMAIL="c.alfissah@gmail.com";  // adresse qui reçoit les demandes
const WHATSAPP_NUMBER="";                     // ex. "33612345678" (sans + ni espaces) — optionnel

const form=$('#trial-form');
if(form){
  const status=$('#form-status'),submitBtn=$('button[type=submit]',form);
  const radios=$$('input[name=profil]',form),enfantBox=$('#enfant-fields');
  const syncProfil=()=>{const kid=(radios.find(r=>r.checked)||{}).value==='enfant';enfantBox.hidden=!kid;
    $$('input,select',enfantBox).forEach(i=>i.required=kid)};
  radios.forEach(r=>r.addEventListener('change',syncProfil));syncProfil();

  const say=(msg,type)=>{status.textContent=msg;status.className='form-status '+type;status.hidden=false};
  const fields=()=>Object.fromEntries(new FormData(form).entries());
  const S=(window.I18N||{}).summary||["Demande de cours d'essai — Al-Fissah","Nom","E-mail","Téléphone / WhatsApp","Pays","Profil","Prénom de l'enfant","ans","Programme souhaité","Niveau actuel","Disponibilités","Message"];
  const I=window.I18N||{};
  const summary=d=>[S[0],``,`${S[1]} : ${d.nom}`,`${S[2]} : ${d.email}`,`${S[3]} : ${d.tel||'—'}`,`${S[4]} : ${d.pays||'—'}`,
    `${S[5]} : ${d.profil==='enfant'?(I.child||'enfant'):(I.adult||'adulte')}`,d.profil==='enfant'?`${S[6]} : ${d.enfant_prenom} (${d.enfant_age} ${S[7]})`:null,
    `${S[8]} : ${d.programme}`,`${S[9]} : ${d.niveau}`,`${S[10]} : ${d.dispo||'—'}`,``,`${S[11]} : ${d.message||'—'}`].filter(x=>x!==null).join('\n');

  form.addEventListener('submit',async e=>{
    e.preventDefault();
    if(!form.checkValidity()){form.reportValidity();return}
    if($('#f-website',form).value)return; // anti-spam (honeypot)
    const d=fields();
    if(FORM_ENDPOINT){
      submitBtn.disabled=true;say(I.sending||'Envoi en cours…','pending');
      try{
        const r=await fetch(FORM_ENDPOINT,{method:'POST',headers:{'Accept':'application/json','Content-Type':'application/json'},body:JSON.stringify(FORM_KEY?{access_key:FORM_KEY,subject:"Demande de cours d'essai — Al-Fissah",...d}:d)});
        if(!r.ok)throw new Error(r.status);
        form.reset();syncProfil();
        say(I.trial_ok||'Demande envoyée.','ok');
      }catch(err){
        say((I.err||'Erreur. Écrivez à {email}.').replace('{email}',CONTACT_EMAIL),'err');
      }finally{submitBtn.disabled=false}
    }else{
      location.href=`mailto:${CONTACT_EMAIL}?subject=${encodeURIComponent((I.subject_trial||"Demande de cours d'essai — {name}").replace('{name}',d.nom))}&body=${encodeURIComponent(summary(d))}`;
      say(I.mail_ok||'Votre messagerie s\'ouvre avec la demande pré-remplie.','ok');
    }
  });
  const wa=$('#wa-link');
  if(wa){if(WHATSAPP_NUMBER){wa.href='https://wa.me/'+WHATSAPP_NUMBER+'?text='+encodeURIComponent(I.wa||"Bonjour, je souhaite réserver un cours d'essai de 30 min.")}else wa.parentElement.remove()}
}

/* ============================================================
   FORMULAIRE DE CONTACT (même mécanisme : endpoint ou e-mail)
   ============================================================ */
const cform=$('#contact-form');
if(cform){
  const st=$('#contact-status'),btn=$('button[type=submit]',cform);
  const say=(m,t)=>{st.textContent=m;st.className='form-status '+t;st.hidden=false};
  cform.addEventListener('submit',async e=>{
    e.preventDefault();
    if(!cform.checkValidity()){cform.reportValidity();return}
    if($('#c-website',cform).value)return;
    const d=Object.fromEntries(new FormData(cform).entries());
    const body=`Nom : ${d.nom}\nPrénom : ${d.prenom}\nE-mail : ${d.email}\nSujet : ${d.sujet}\n\n${d.message}`;
    if(FORM_ENDPOINT){
      const I=window.I18N||{};btn.disabled=true;say(I.sending||'Envoi en cours…','pending');
      try{const r=await fetch(FORM_ENDPOINT,{method:'POST',headers:{'Accept':'application/json','Content-Type':'application/json'},body:JSON.stringify(FORM_KEY?{access_key:FORM_KEY,subject:'Contact — Al-Fissah',...d,_type:'contact'}:{...d,_type:'contact'})});
        if(!r.ok)throw new Error(r.status);cform.reset();
        say(I.contact_ok||'Message envoyé.','ok');
      }catch(err){say((I.err||'Erreur. Écrivez à {email}.').replace('{email}',CONTACT_EMAIL),'err')}
      finally{btn.disabled=false}
    }else{
      location.href=`mailto:${CONTACT_EMAIL}?subject=${encodeURIComponent('['+d.sujet+'] '+d.prenom+' '+d.nom)}&body=${encodeURIComponent(body)}`;
      say((window.I18N||{}).mail_ok||'Votre messagerie s\'ouvre avec le message pré-rempli.','ok');
    }
  });
}

/* ---------- Sélecteur de langue ---------- */
const lsw=$('.langsw');
if(lsw){const b=$('.langbtn',lsw);
  b.addEventListener('click',e=>{e.stopPropagation();const o=lsw.classList.toggle('open');b.setAttribute('aria-expanded',o)});
  document.addEventListener('click',()=>{lsw.classList.remove('open');b.setAttribute('aria-expanded','false')});
  lsw.addEventListener('keydown',e=>{if(e.key==='Escape'){lsw.classList.remove('open');b.focus()}});
}

/* ============================================================
   FORMULAIRE D'INSCRIPTION AUX ÉTUDES (page inscription.html)
   Parcours distinct du cours d'essai ; même mécanisme d'envoi.
   ============================================================ */
const sform=$('#signup-form');
if(sform){
  const st=$('#signup-status'),btn=$('button[type=submit]',sform);
  const radios=$$('input[name=profil]',sform),kidBox=$('#s-enfant-fields');
  const syncProfil=()=>{const kid=(radios.find(r=>r.checked)||{}).value==='enfant';kidBox.hidden=!kid;
    $$('input,select',kidBox).forEach(i=>i.required=kid)};
  radios.forEach(r=>r.addEventListener('change',syncProfil));syncProfil();
  // Préremplissage depuis l'adresse : inscription.html?formule=2&programme=coran (liens des pages Tarifs et Programmes)
  try{const q=new URLSearchParams(location.search),hs=$('#s-heures',sform),ps=$('#s-programme',sform);
    const pf=q.get('formule'),pp=q.get('programme');
    if(pf&&hs.querySelector(`option[value="${pf}"]`))hs.value=pf;
    if(pp&&ps.querySelector(`option[value="${pp}"]`))ps.value=pp;
    if(pp==='arabe-enfants'||pp==='collectifs'){radios.forEach(r=>r.checked=(r.value==='enfant'));syncProfil()}
  }catch(e){}
  const I=window.I18N||{},S=I.summary_signup||["Inscription aux études — Al-Fissah","Nom","E-mail","Téléphone / WhatsApp","Pays","Profil","ans","Programme","Niveau actuel","Formule","Jours et heures souhaités","Début souhaité","Message"];
  const say=(m,t)=>{st.textContent=m;st.className='form-status '+t;st.hidden=false};
  const txt=n=>{const el=sform.elements[n];if(!el)return'';if(el.tagName==='SELECT'){const o=el.options[el.selectedIndex];return o&&o.value?o.text.trim():''}return(el.value||'').trim()};
  const summary=d=>[S[0],``,`${S[1]} : ${d.nom}`,`${S[2]} : ${d.email}`,`${S[3]} : ${d.tel||'—'}`,`${S[4]} : ${d.pays||'—'}`,
    `${S[5]} : ${d.profil==='enfant'?(I.child||'enfant')+(d.enfant_prenom?` — ${d.enfant_prenom} (${d.enfant_age} ${S[6]})`:''):(I.adult||'adulte')}`,
    `${S[7]} : ${txt('programme')}`,`${S[8]} : ${d.niveau}`,`${S[9]} : ${txt('formule')}`,`${S[10]} : ${d.jours||'—'}`,`${S[11]} : ${d.debut||'—'}`,``,`${S[12]} : ${d.message||'—'}`].join('\n');
  sform.addEventListener('submit',async e=>{
    e.preventDefault();
    if(!sform.checkValidity()){sform.reportValidity();return}
    if($('#s-website',sform).value)return; // anti-spam (honeypot)
    const d=Object.fromEntries(new FormData(sform).entries());
    d.programme_libelle=txt('programme');d.formule_libelle=txt('formule');
    if(FORM_ENDPOINT){
      btn.disabled=true;say(I.sending||'Envoi en cours…','pending');
      try{
        const r=await fetch(FORM_ENDPOINT,{method:'POST',headers:{'Accept':'application/json','Content-Type':'application/json'},body:JSON.stringify(FORM_KEY?{access_key:FORM_KEY,subject:"Inscription aux études — Al-Fissah",...d,_type:'inscription'}:{...d,_type:'inscription'})});
        if(!r.ok)throw new Error(r.status);
        sform.reset();syncProfil();
        say(I.signup_ok||'Demande envoyée.','ok');
      }catch(err){
        say((I.err||'Erreur. Écrivez à {email}.').replace('{email}',CONTACT_EMAIL),'err');
      }finally{btn.disabled=false}
    }else{
      location.href=`mailto:${CONTACT_EMAIL}?subject=${encodeURIComponent((I.subject_signup||"Inscription aux études — {name}").replace('{name}',d.nom))}&body=${encodeURIComponent(summary(d))}`;
      say(I.mail_ok||'Votre messagerie s\'ouvre avec la demande pré-remplie.','ok');
    }
  });
  const wa=$('#signup-wa');
  if(wa){if(WHATSAPP_NUMBER){wa.href='https://wa.me/'+WHATSAPP_NUMBER+'?text='+encodeURIComponent(I.wa_signup||"Bonjour, je souhaite m'inscrire aux cours.")}else wa.parentElement.remove()}
}
