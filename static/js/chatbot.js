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
    <div id="cb-toggle" style="position:fixed;bottom:1.5rem;right:1.5rem;width:52px;height:52px;border-radius:50%;background:#0066ff;color:#fff;display:flex;align-items:center;justify-content:center;cursor:pointer;z-index:200;box-shadow:0 4px 16px rgba(0,0,0,0.2);font-size:1.3rem">💬</div>
    <div id="cb-panel" style="display:none;position:fixed;bottom:5.5rem;right:1.5rem;width:300px;max-height:420px;background:#fff;border:1px solid rgba(0,0,0,0.1);box-shadow:0 8px 32px rgba(0,0,0,0.15);z-index:200;display:none;flex-direction:column;font-family:'Inter',sans-serif">
      <div style="padding:0.75rem 1rem;background:#0d0d0d;color:#fff;font-size:0.8rem">Assistant</div>
      <div id="cb-messages" style="flex:1;overflow-y:auto;padding:0.75rem;font-size:0.78rem;max-height:280px"></div>
      <form id="cb-form" style="display:flex;border-top:1px solid rgba(0,0,0,0.08)">
        <input id="cb-input" type="text" placeholder="Votre question..." style="flex:1;border:none;padding:0.6rem;font-size:0.78rem;outline:none">
        <button type="submit" style="border:none;background:#0066ff;color:#fff;padding:0 0.9rem;cursor:pointer">→</button>
      </form>
    </div>`;

  const panel = document.getElementById('cb-panel');
  document.getElementById('cb-toggle').addEventListener('click', () => {
    panel.style.display = panel.style.display === 'none' ? 'flex' : 'none';
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
