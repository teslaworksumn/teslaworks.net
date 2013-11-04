{% macro js() %}

$('form .has-error :input:visible:enabled:first').focus();

{% endmacro %}
