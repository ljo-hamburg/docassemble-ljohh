$(document).on("daPageLoad", () => {
    $("[data-toggle=\"tooltip\"]").tooltip();
    $("[data-da-action]").each((index, element) => {
        $(element).on("click", event => {
            event.preventDefault();
            const action = element.dataset.daAction;
            const args = element.dataset.args ? JSON.parse(element.dataset.args) : {};
            element.disabled = true;
            action_call(action, args, data => {
                const message = element.dataset.daMessage;
                if (message) {
                    flash(message, 'info');
                }
                element.disabled = false;
            });
        });
    });
});