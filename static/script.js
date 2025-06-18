async function typeWriterEffect(text, element, delay = 25) {
  element.textContent = "";
  for (let i = 0; i < text.length; i++) {
    element.textContent += text.charAt(i);
    await new Promise(resolve => setTimeout(resolve, delay));
  }
}

async function showEventsSequentially(events) {
  const tbody = document.getElementById('events');
  tbody.innerHTML = '';

  for (const event of events) {
    const row = document.createElement('tr');

    // Дата (без анимации)
    const dateTd = document.createElement('td');
    dateTd.textContent = event.date;
    row.appendChild(dateTd);

    // Французский (с эффектом)
    const frTd = document.createElement('td');
    const frSpan = document.createElement('span');
    frTd.appendChild(frSpan);
    row.appendChild(frTd);
    // Добавляем строку сначала (с пустыми ячейками), затем анимацию текста
    tbody.appendChild(row);

    // Печатание
    await typeWriterEffect(event.label, frSpan, 30);
  }
}

document.addEventListener("DOMContentLoaded", () => {
  const data = document.getElementById("events-data");
  if (data) {
    const events = JSON.parse(data.textContent);
    showEventsSequentially(events);
  }
});
