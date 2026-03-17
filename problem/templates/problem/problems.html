{% extends 'home/master.html' %}
{% block content %}
{% load static %}

<link rel="stylesheet" href="{% static 'css/problem/problems.css' %}" />

<section class="problems-section">

  <div class="problems-header">

    <h1>Problems</h1>
  

    {% if request.user.is_authenticated and perms.problem.add_problem %}
      <a href="{% url 'create-problem' %}">+ Create Problem</a>
    {% endif %}
    
    <div class="controls">
      <input type="text" id="searchInput" placeholder="Search problems..." />

      <select id="difficultyFilter">
        <option value="">All Difficulty</option>
        <option value="easy">Easy</option>
        <option value="medium">Medium</option>
        <option value="hard">Hard</option>
        <option value="challenging">Challenging</option>
      </select>

      <select id="tagFilter">
        <option value="">All Categories</option>
        <option value="dp">Dynamic Programming</option>
        <option value="graph">Graph</option>
        <option value="math">Math</option>
        <option value="string">String</option>
      </select>
    </div>
  </div>

  <div class="problems-wrapper">

    <!-- Table Header -->
    <div class="problem-row header">
      <div>ID</div>
      <div>Title</div>
      <div onclick="sortByDifficulty()" class="sortable">
        Difficulty ↑↓
      </div>
      <!-- <div>Tag</div> -->
      <div>Solved</div>
    </div>

    {% for problem in problems %}
      
      <div onclick="window.location.href = `/problems/problem_detail/{{ problem.id }}/`" class="problem-row" 
          data-id="{{ problem.id }}"
          data-difficulty="{{ problem.difficulty }}"
          data-tag="">

        <div class="id">{{ problem.id }}</div>
        <div class="title">{{ problem.title }}</div>
        <div class="difficulty easy">{{ problem.difficulty }}</div>
        <!-- <div class="tag"></div> -->
        <div class="status"></div>
      </div>
    
    {% endfor %}

   </div>
</section>

<script>
const rows = document.querySelectorAll(".problem-row:not(.header)");

rows.forEach(row => {
  const id = row.dataset.id;
  const statusCell = row.querySelector(".status");

  if (localStorage.getItem("solved_" + id)) {
    row.classList.add("solved");
    statusCell.innerHTML = "✔";
  } else {
    statusCell.innerHTML = "•";
  }

  row.addEventListener("click", () => {
    localStorage.setItem("solved_" + id, true);
    row.classList.add("solved");
    statusCell.innerHTML = "✔";
  });
});

function sortByDifficulty() {
  const wrapper = document.querySelector(".problems-wrapper");
  const rowsArray = Array.from(rows);

  rowsArray.sort((a, b) =>
    a.dataset.difficulty - b.dataset.difficulty
  );

  rowsArray.forEach(row => wrapper.appendChild(row));
}
</script>

{% endblock %}