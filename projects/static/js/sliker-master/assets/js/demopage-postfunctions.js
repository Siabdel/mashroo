$(document).ready(function(){
	$("pre").each(function(){
		$(this).append('<span>code <i class="fa fa-chevron-down"></i><i class="fa fa-chevron-up"></i></span>');
	});
	$("blockquote").each(function(){
		$(this).append('<span>infos <i class="fa fa-chevron-down"></i><i class="fa fa-chevron-up"></i></span>');
	});
});

$("pre, blockquote").on("click","span",function(){
	target = $(this).parents("pre, blockquote");

	if(target.is(".selected")){
		target.removeClass("selected");
	}else{
		target.addClass("selected");
	}
});
