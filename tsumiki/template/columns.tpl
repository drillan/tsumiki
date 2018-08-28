<div class="columns{{ column_count }}">
  {% for section in sections %}
    <div id="col{{ loop.index }}">
    {{ section }}
    </div>
  {% endfor %}
</div> 