(function(){
  const root = document.getElementById('chatbot-widget');
  if (!root) return;

  const sessionId = (function(){
    let id = localStorage.getItem('chatbot_session_id');
    if (!id){
      id = 'sess-' + Math.random().toString(36).slice(2);
      localStorage.setItem('chatbot_session_id', id);
    }
    return id;
  })();

  root.innerHTML = `
    <div id="cb-tooltip" class="cb-tooltip">Une question ?</div>
    <div id="cb-toggle" class="cb-toggle" aria-label="Ouvrir l'assistant">
      <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"></path></svg>
    </div>
    <div id="cb-panel" class="cb-panel">
      <div class="cb-header">Une question ?</div>
      <div id="cb-messages" class="cb-messages"></div>
      <form id="cb-form" class="cb-form">
        <input id="cb-input" class="cb-input" type="text" placeholder="Votre question...">
        <button type="submit" class="cb-send">→</button>
      </form>
    </div>`;

  const tooltip = document.getElementById('cb-tooltip');
  const panel = document.getElementById('cb-panel');
  let hasOpened = false;
  let tooltipTimer = null;

  const showTimer = setTimeout(() => {
    tooltip.classList.add('is-open');
    tooltipTimer = setTimeout(() => { tooltip.classList.remove('is-open'); }, 6000);
  }, 3000);

  function hideTooltip(){
    clearTimeout(showTimer);
    clearTimeout(tooltipTimer);
    tooltip.classList.remove('is-open');
  }

  document.getElementById('cb-toggle').addEventListener('click', () => {
    hideTooltip();
    const opening = !panel.classList.contains('is-open');
    panel.classList.toggle('is-open');
    if (opening && !hasOpened){
      hasOpened = true;
      addMessage("Bonjour, je peux répondre à vos questions sur les projets, mon parcours ou vous aider à préparer une demande.", 'bot');
    }
  });

  function addMessage(text, from){
    const messages = document.getElementById('cb-messages');
    const bubble = document.createElement('div');
    bubble.classList.add('cb-msg', from === 'bot' ? 'cb-msg--bot' : 'cb-msg--user');
    bubble.textContent = (from === 'bot' ? '' : 'Vous : ') + text;
    messages.appendChild(bubble);
    messages.scrollTop = messages.scrollHeight;
  }

  document.getElementById('cb-form').addEventListener('submit', async function(e){
    e.preventDefault();
    const input = document.getElementById('cb-input');
    const message = input.value.trim();
    if (!message) return;
    addMessage(message, 'user');
    input.value = '';

    try {
      const res = await fetch('/chatbot/message', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({message: message, session_id: sessionId})
      });
      if (res.status === 429){
        addMessage("Trop de messages envoyés, réessayez dans un moment.", 'bot');
        return;
      }
      if (res.status >= 500){
        addMessage("Le chatbot est momentanément indisponible.", 'bot');
        return;
      }
      const data = await res.json();
      addMessage(data.reponse, 'bot');
    } catch (err) {
      addMessage("Erreur réseau, réessayez.", 'bot');
    }
  });
})();
