// Enhance language switching
function applyLang(lang){
  document.documentElement.lang = lang;

  document.querySelectorAll('.language-switcher [data-lang]').forEach(btn=>{
    btn.setAttribute('aria-pressed', String(btn.getAttribute('data-lang')===lang));
  });

  if (typeof translations !== 'undefined') {
    document.querySelectorAll('[data-translate]').forEach(el=>{
      const key = el.getAttribute('data-translate');
      if (translations[lang] && translations[lang].hasOwnProperty(key)) {
        el.innerText = translations[lang][key];
      }
    });
  }

  localStorage.setItem('eco_lang', lang);

  // カレンダーの言語反映
  if (window.calendar) {
    window.calendar.setOption('locale', lang);
  }
}


document.addEventListener('DOMContentLoaded', () => {

  const saved = localStorage.getItem('eco_lang') || 'ja';
    
  // ======================
  // FullCalendar 예약 달력
  // ======================
  const calendarEl = document.getElementById('calendar');
  const msg = document.getElementById('selectDateMessage');

  if (calendarEl) {
    window.calendar = new FullCalendar.Calendar(calendarEl, {
      initialView: 'dayGridMonth',
      selectable: true,
      locale: saved,  // ← 5言語自動対応

      dateClick: function(info) {
        msg.textContent = `選択した日付: ${info.dateStr}（予約可能）`;
        msg.style.color = "#2a7a2a";
      },

      validRange: {
        start: new Date().toISOString().split("T")[0]
      }
    });

    window.calendar.render();
  }

  // Mobile menu toggle
  const menuBtn = document.querySelector('nav button.menu');
  const list = document.getElementById('primary-menu');
  menuBtn?.addEventListener('click', ()=>{
    const open = list.classList.toggle('open');
    menuBtn.setAttribute('aria-expanded', String(open));
  });

  // 言語初期化
  applyLang(saved); 

  // 言語ボタン
  document.querySelectorAll('.language-switcher [data-lang]').forEach(btn=>{
    btn.addEventListener('click', ()=> applyLang(btn.getAttribute('data-lang')));
  });

  // Form validation
  const form = document.getElementById('contactForm');
  form.addEventListener('submit', (e)=>{
    if (!form.checkValidity()) {
      e.preventDefault();
      [...form.elements].forEach(el=> el.reportValidity && el.reportValidity());
    }
  });
});
