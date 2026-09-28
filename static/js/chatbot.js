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
    <div id="cb-tooltip" style="display:none;position:fixed;bottom:1.7rem;right:5.5rem;background:#fff;color:#141413;font-size:0.82rem;padding:0.6rem 0.9rem;border-radius:10px;box-shadow:0 6px 20px rgba(0,0,0,0.15);z-index:200;white-space:nowrap;font-family:'Inter',sans-serif">Une question ?</div>
    <div id="cb-toggle" aria-label="Ouvrir l'assistant" style="position:fixed;bottom:1.5rem;right:1.5rem;width:52px;height:52px;border-radius:50%;background:#0066ff;color:#fff;display:flex;align-items:center;justify-content:center;cursor:pointer;z-index:200;box-shadow:0 4px 16px rgba(0,0,0,0.2)">
      <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"></path></svg>
    </div>
    <div id="cb-panel" style="display:none;position:fixed;bottom:5.5rem;right:1.5rem;width:300px;max-height:420px;background:#fff;border:1px solid rgba(0,0,0,0.1);box-shadow:0 8px 32px rgba(0,0,0,0.15);z-index:200;flex-direction:column;font-family:'Inter',sans-serif">
      <div style="padding:0.75rem 1rem;background:#0d0d0d;color:#fff;font-size:0.8rem;font-weight:600">Une question ?</div>
      <div id="cb-messages" style="flex:1;overflow-y:auto;padding:0.75rem;font-size:0.78rem;max-height:280px"></div>
      <form id="cb-form" style="display:flex;border-top:1px solid rgba(0,0,0,0.08)">
        <input id="cb-input" type="text" placeholder="Votre question..." style="flex:1;border:none;padding:0.6rem;font-size:0.78rem;outline:none">
        <button type="submit" style="border:none;background:#0066ff;color:#fff;padding:0 0.9rem;cursor:pointer">→</button>
      </form>
    </div>`;

  const tooltip = document.getElementById('cb-tooltip');
  const panel = document.getElementById('cb-panel');
  let hasOpened = false;
  let tooltipTimer = null;

  const showTimer = setTimeout(() => {
    tooltip.style.display = 'block';
    tooltipTimer = setTimeout(() => { tooltip.style.display = 'none'; }, 6000);
  }, 3000);

  function hideTooltip(){
    clearTimeout(showTimer);
    clearTimeout(tooltipTimer);
    tooltip.style.display = 'none';
  }

  document.getElementById('cb-toggle').addEventListener('click', () => {
    hideTooltip();
    const opening = panel.style.display === 'none' || !panel.style.display;
    panel.style.display = opening ? 'flex' : 'none';
    if (opening && !hasOpened){
      hasOpened = true;
      addMessage("Bonjour, je peux répondre à vos questions sur les projets, mon parcours ou vous aider à préparer une demande.", 'bot');
    }
  });

  function addMessage(text, from){
    const messages = document.getElementById('cb-messages');
    const bubble = document.createElement('div');
    bubble.style.margin = '0.4rem 0';
    bubble.style.color = from === 'bot' ? '#333' : '#0066ff';
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
