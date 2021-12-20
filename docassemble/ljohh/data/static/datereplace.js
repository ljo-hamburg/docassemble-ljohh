$(document).on("daPageLoad", function () {
  $('input[type="date"]').each(function () {
    var dateElement = this;
    $(dateElement).hide();
    $(dateElement).attr("type", "hidden");
    var parentElement = $('<div class="form-row">');
    var dayParent = $('<div class="col">');
    var monthParent = $('<div class="col">');
    var yearParent = $('<div class="col">');
    var dayElement = $('<select class="form-control">');
    var monthElement = $('<select class="form-control">');
    var yearElement = $('<select class="form-control">');
    var today = new Date();
    var dateEntered;
    if ($(dateElement).val()) {
      var utcDate = new Date($(dateElement).val());
      dateEntered = new Date(
        utcDate.getUTCFullYear(),
        utcDate.getUTCMonth(),
        utcDate.getUTCDate()
      );
    } else {
      dateEntered = null;
    }
    var opt = $("<option disabled>");
    opt.val("");
    opt.text("Tag");
    dayElement.append(opt);
    if (!dateEntered) {
      opt.attr("selected", "selected")
    }
    for (var day = 1; day <= 31; day++) {
      var opt = $("<option>");
      if (day < 10) {
        opt.val("0" + day);
      } else {
        opt.val(day);
      }
      opt.text(day);
      if (dateEntered && day == dateEntered.getDate()) {
        opt.attr("selected", "selected");
      }
      dayElement.append(opt);
    }
    
    opt = $("<option disabled>");
    opt.val("");
    opt.text("Monat");
    if (!dateEntered) {
      opt.attr("selected", "selected")
    }
    monthElement.append(opt);
    for (var month = 0; month < 12; month++) {
      opt = $("<option>");
      if (month < 9) {
        opt.val("0" + (month + 1));
      } else {
        opt.val(month + 1);
      }
      var dt = new Date(1970, month, 15);
      opt.text(dt.toLocaleString("default", { month: "long" }));
      if (dateEntered && month == dateEntered.getMonth()) {
        opt.attr("selected", "selected");
      }
      monthElement.append(opt);
    }
    
    opt = $("<option disabled>");
    opt.val("");
    opt.text("Jahr");
    if (!dateEntered) {
      opt.attr("selected", "selected")
    }
    yearElement.append(opt);
    for (
      var year = today.getFullYear() - 10;
      year > today.getFullYear() - 35;
      year--
    ) {
      opt = $("<option>");
      opt.val(year);
      opt.text(year);
      if (dateEntered && year == dateEntered.getFullYear()) {
        opt.attr("selected", "selected");
      }
      yearElement.append(opt);
    }
    function updateDate() {
      $(dateElement).val(
        $(yearElement).val() +
          "-" +
          $(monthElement).val() +
          "-" +
          $(dayElement).val()
      );
    }

    parentElement.css("display", "flex");
    $(dateElement).before(parentElement);
    $(dayParent).append(dayElement);
    $(parentElement).append(dayParent);
    $(monthParent).append(monthElement);
    $(parentElement).append(monthParent);
    $(yearParent).append(yearElement);
    $(parentElement).append(yearParent);
    dayElement.on("change", updateDate);
    monthElement.on("change", updateDate);
    yearElement.on("change", updateDate);
    updateDate();
  });
});
