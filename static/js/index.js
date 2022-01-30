$(function () {

    console.log('sup')
    $('td.epoch').each(function() {
        console.log(this.textContent)
        this.innerHTML = moment.unix(this.textContent).format('Y-MM-DD')
    })
})

function toggleResult(id, result) {
    $.ajax({
        url: "/toggle-result",
        method: "PUT",
        data: {
            'id': id,
            'result': result
        },
        success: function(res) {
            let tWins = parseInt($('#win-perc-num').text())
            let tLoses = parseInt($('#lose-perc-num').text())
            let tTotal = tWins + tLoses
            console.log(tWins, tLoses, tTotal)
            if ($(`#result-${id}`).text() === "L") {
                tWins += 1
                $(`#result-${id}`).text("W").addClass('result-green').removeClass('result-red')
                $('#win-perc-num').text(tWins)
                $('#lose-perc-num').text(tLoses-1)
                console.log($(`#flip-result-${id}`))    
                $(`#flip-result-${id}`).attr("onclick", "toggleResult(29, 1)")
                console.log('w')
            } else {
                tLoses += 1
                $(`#result-${id}`).text("L").removeClass('result-green').addClass('result-red')
                $('#lose-perc-num').text(tLoses)
                $('#win-perc-num').text(tWins-1)
                $(`#flip-result-${id}`).attr("onclick", "toggleResult(29, 0)")
                console.log('l')
            }
            $('span#win-perc-navbar')[0].textContent = (tWins /tTotal * 100).toFixed()
            $('span#lose-perc-navbar')[0].textContent = (tLoses/tTotal * 100).toFixed()
        },
        error: function(res, stat, err) {
            console.log(`error: ${err}`)
        },
        complete: function() {
            console.log("it's over")
        }

    })
}