
$(document).ready(function () {
    // Register a custom button named 'my_custom'
    $.extend($.summernote.plugins, {
        'my_custom': function (context) {
            var ui = $.summernote.ui;
            
            // Create a button
            var button = ui.button({
                contents: '<i class="fa fa-hr"></i>', // Replace with your preferred icon
                tooltip: 'Insert Horizontal Rule',
                click: function () {
                    // Add the action when the button is clicked
                    context.invoke('editor.insertHorizontalRule');
                }
            });
            
            return button.render();
        }
    });
});
