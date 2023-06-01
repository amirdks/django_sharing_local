let inputList = document.querySelectorAll(".date-picker-input");
inputList.forEach(input => {
    input.addEventListener("focus", (event) => {
        var dp = new HaDateTimePicker(`${input.getAttribute("data-ha-datetimepicker")}`, {
            isSolar: true,
            resultFormat: '{year}-{month}-{day}',
        });
        dp.show();
    })
})