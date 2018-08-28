<style>
  .tsumiki .columns{{ column_count }} {
    -webkit-columns: {{ column_count }};
    -moz-columns: {{ column_count }};
    -ms-columns: {{ column_count }};
    columns: {{ column_count }};
    display: inline-flex;
    align-items: top;
    width: 100%;
  }

{% for col in range(column_count) %}
  .tsumiki #col{{ col }} {
      width: calc(100% / {{ column_count }});
  }
{% endfor %}
</style>
