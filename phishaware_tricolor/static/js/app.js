const form = document.querySelector('#scan-form');
const result = document.querySelector('#scan-result');
const btn = document.querySelector('#scan-btn');
function textEl(tag, text) { const node = document.createElement(tag); node.textContent = text; return node; }
form.addEventListener('submit', async (event) => {
  event.preventDefault();
  result.hidden = false;
  result.replaceChildren(textEl('p', 'Analyzing URL patterns...'));
  btn.disabled = true;
  try {
    const response = await fetch('/api/scan', {method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({url:document.querySelector('#url').value})});
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || 'Scan failed.');
    const title = textEl('h4', `RISK: ${data.level}  •  ${data.score}/100`);
    title.style.color = data.level === 'HIGH' ? '#ff5757' : data.level === 'MEDIUM' ? '#f5b942' : '#36e5a3';
    const address = textEl('p', data.url);
    const list = document.createElement('ul');
    for (const indicator of data.indicators) list.append(textEl('li', indicator));
    result.replaceChildren(title,address,list,textEl('p',data.disclaimer));
  } catch (err) { result.replaceChildren(textEl('p', err.message)); }
  finally { btn.disabled = false; }
});
