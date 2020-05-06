$(document).on("daPageLoad", () => {
    $("[data-toggle=\"tooltip\"]").tooltip();
    $("[data-da-action]").each((index, element) => {
        $(element).on("click", event => {
            event.preventDefault();
            const action = element.dataset.daAction;
            element.disabled = true;
            action_call(action, {}, data => {
                message = element.dataset.daMessage;
                if (message) {
                    flash(message, 'info');
                }
                element.disabled = false;
            });
        });
    });
});