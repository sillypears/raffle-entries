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
        method: "PUT",
        data: {
            'id': id,
            'result': result
        },
        success: function(res) {
            
            if ($(`#result-${id}`).text() === "L") {
                $(`#result-${id}`).text("W").addClass('result-green').removeClass('result-red')
            } else {
                $(`#result-${id}`).text("L").removeClass('result-green').addClass('result-red')
            }
            const results = $('.result')
            let wResults = lResults = tResults = 0
            for (result of results) {
                if (result.textContent == "W") { wResults += 1}
                if (result.textContent =="L") { lResults += 1}
                tResults += 1
            }
            $('span#win-perc-navbar')[0].textContent = (wResults /tResults * 100).toFixed()
            $('span#lose-perc-navbar')[0].textContent = (lResults /tResults * 100).toFixed()

        }
    })
}