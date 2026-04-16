row.innerHTML = `
      <div>${p.id}</div>
      <div>${p.title}</div>
      <div class="difficulty ${p.difficulty}">${p.difficulty}</div>
      <div class="status ${p.solved ? 'solved' : ''}">
        ${p.solved ? '✔ Solved' : ''}
      </div>
    `;