// Round 3 shared JS. Prototype only.
window.headerScroll = () => addEventListener('scroll', () => document.getElementById('hd').classList.toggle('sc', scrollY > 40), { passive: true });

// Agent console: types a request through triage -> task -> runbook -> draft -> human approval. Starts when visible.
window.agentConsole = function (el) {
  const L = [['k','▸ ny henvendelse  '],['h','"Serveren er langsom, og ingen kan printe"\n'],
    ['k','▸ triage          '],['','kunde genkendt · prioritet '],['w','HØJ'],['','\n'],
    ['k','▸ opgave          '],['','oprettet og koblet til kunden\n'],
    ['k','▸ runbook         '],['','1 spooler · 2 diskplads · 3 seneste opdatering\n'],
    ['k','▸ udkast          '],['','svar til kunden er klar\n'],
    ['k','▸ menneske        '],['o','venter på godkendelse ✓\n\n'],['h','Intet sendes, ændres eller købes uden et ja.']];
  let started = false;
  new IntersectionObserver(es => {
    if (!es[0].isIntersecting || started) return; started = true; let i = 0, j = 0, html = '';
    const step = () => {
      if (i >= L.length) { el.innerHTML = html + '<span class="caret"></span>'; setTimeout(() => { html = ''; i = 0; j = 0; step(); }, 7000); return; }
      const [c, s] = L[i]; j++; el.innerHTML = html + `<span class="${c}">${s.slice(0, j)}</span><span class="caret"></span>`;
      if (j >= s.length) { html += `<span class="${c}">${s}</span>`; i++; j = 0; }
      setTimeout(step, RM ? 0 : (s[j - 1] === '\n' ? 320 : 16));
    }; step();
  }, { threshold: .35 }).observe(el);
};

// Missed-backup toasts
window.toasts = function (host, ids) {
  new IntersectionObserver((es, o) => { if (!es[0].isIntersecting) return; o.disconnect();
    ids.forEach((id, k) => setTimeout(() => document.getElementById(id).classList.add('on'), 600 + k * 2000)); }, { threshold: .4 }).observe(host);
};
