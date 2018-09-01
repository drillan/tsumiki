<section class="columns{{ column_count }}">
  {% for section in sections %}
    <section id="col{{ loop.index }}">
    {{ section }}
    </section>
  {% endfor %}
</section> 