function createExampleBlockById(numberId) {
	var source = $(".example-" + numberId);
	$('<pre class="code-example-' + numberId + '">').insertAfter($('.example-' + numberId)).text(source.html());
}
