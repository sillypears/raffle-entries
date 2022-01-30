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
            $(`td#result-${id}`).text(($(`td#result-${id}`).text() === "W") ? "L" : "W")
            const results = $('td.result')
            let wResults = lResults = tResults = 0
            for (result of results) {
                if (result.textContent == "W") { wResults += 1}
                if (result.textContent =="L") { lResults += 1}
                tResults += 1
            }
            console.log($('span#win-perc-navbar'))
            $('span#win-perc-navbar')[0].textContent = (wResults /tResults * 100).toFixed()
            $('span#lose-perc-navbar')[0].textContent = (lResults /tResults * 100).toFixed()

        }
    })
}