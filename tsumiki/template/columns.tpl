<div class="columns{{ column_count }}">
  {% for p in paragraph %}
    <div class="col{{ loop.index }}">
    {{ p }}
    </div>
  {% endfor %}
</div>