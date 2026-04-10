{% extends 'home/master.html' %}
{% block content %}
{% load static %}

<link rel="stylesheet" href="{% static 'css/problem/create_problem.css' %}" />


<div class="create-problem-container">

<form
    {% if problem_type == "public" %}
        action="{% url 'edit-problem' current_problem.id %}"
    {% elif problem_type == "contest" %}
        action="{% url 'edit-contest-problem' contest.id %}"
    {% endif %}

    method="POST">

    {% csrf_token %}

    <h2>Edit Problem</h2>

    <div class="rules">
        <h3>
            Standard:
        </h3>
        <br>

        <p>
            * For testcases, every space & newline counts
        </p>
        

    </div>

    <br><br>

    <input type="text" name="title" placeholder="Problem Title" value="{{ current_problem.title }}" required>

    <textarea name="statement" placeholder="Problem Statement" required>{{ current_problem.statement }}</textarea>

    <textarea name="problem_input" placeholder="Input Description" required>{{ current_problem.problem_input }}</textarea>

    <textarea name="problem_output" placeholder="Output Description" required>{{ current_problem.problem_output }}</textarea>

    <textarea name="note" placeholder="Note (optional)">{{ current_problem.note|default_if_none:'' }}</textarea>

    <label for="difficulty">Difficulty:</label>
    <select name="difficulty">
        <option value="easy" {% if current_problem.difficulty == "easy" %}selected{% endif %}>Easy</option>
        <option value="medium" {% if current_problem.difficulty == "medium" %}selected{% endif %}>Medium</option>
        <option value="hard" {% if current_problem.difficulty == "hard" %}selected{% endif %}>Hard</option>
        <option value="challenging" {% if current_problem.difficulty == "challenging" %}selected{% endif %}>Challenging</option>
    </select>

    <label for="time_limit">Time Limit</label>
    <input type="number" name="time_limit" value="{{ current_problem.time_limit }}">

    <label for="memory_limit">Memory Limit</label>
    <input type="number" name="memory_limit" value="{{ current_problem.memory_limit }}">


    <div class="divider"></div>

    <h3 class="section-title">Test Cases</h3>

    <div id="testcases-container">

    </div>


    <button type="button" class="btn btn-add" onclick="addTestcase()">
        Add Test Case
    </button>


    <br>

    <button type="submit" class="btn btn-submit">
        Update Problem
    </button>

</form>

</div>

<script>
    let current_testcases_list = [];

    {% for testcase in current_testcases %}
        current_testcases_list.push(
            {
                input_data: "{{ testcase.input_data|escapejs }}",
                expected_output: "{{ testcase.expected_output|escapejs }}",
                is_hidden: {{ testcase.is_hidden|yesno:"true,false" }},
            }
        );
    {% endfor %}

    let testCaseIndex = 0;

    function addTestcase(tc = null) {
        let input_data = "";
        let expected_output = "";
        let is_hidden = "checked";

        if (tc) {
            input_data = tc.input_data;
            expected_output = tc.expected_output;
            is_hidden = tc.is_hidden ? "checked" : "";
        }

        const container = document.getElementById("testcases-container")

        const div = document.createElement("div")
        div.classList.add("testcase")

        div.innerHTML = `
            <textarea name="testcase_input[]" placeholder="Input" required>${input_data}</textarea>

            <textarea name="testcase_output[]" placeholder="Expected Output" required>${expected_output}</textarea>

            <label>
                <input type="checkbox" name="testcase_hidden[]" value="${testCaseIndex}" ${is_hidden}>
                Hidden Test Case
            </label>

            <button type="button" class="btn btn-remove"
            onclick="this.parentElement.remove()">
            Remove
            </button>
        `

        container.appendChild(div)

        testCaseIndex++;
    }

    current_testcases_list.forEach(tc => {
        addTestcase(tc);
    });

</script>


{% endblock %}