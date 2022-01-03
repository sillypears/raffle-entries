$(function () {

    console.log('sup')
    $('td.epoch').each(function() {
        console.log(this.textContent)
        this.innerHTML = moment.unix(this.textContent).format('Y-MM-DD')
    })
})

function toggleResult(id, result) {
    console.log(id, result)
    $.ajax({
        url: "/toggle-result",
        method: "POST",
        data: {
            'id': id,
            'result': result
        },
        success: function(res) {
            $(`td#result-${id}`).text(($(`td#result-${id}`).text() === "W") ? "L" : "W")
        }
    })
}