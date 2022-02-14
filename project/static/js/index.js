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
            if ($(`#result-${id}`).text() === "L") {
                tWins += 1
                tLoses -= 1
                $(`#result-${id}`).text("W").addClass('result-green').removeClass('result-red')
                $(`#flip-result-${id}`).attr("onclick", `toggleResult(${id}, 1)`)
                $('#win-perc-num').text(tWins)
                $('#lose-perc-num').text(tLoses)
            } else {
                tLoses += 1
                tWins-= 1
                $(`#result-${id}`).text("L").removeClass('result-green').addClass('result-red')
                $(`#flip-result-${id}`).attr("onclick", `toggleResult(${id}, 0)`)
                $('#lose-perc-num').text(tLoses)
                $('#win-perc-num').text(tWins)
            }
            const tWinsPerc = (tWins /tTotal * 100).toFixed()
            $('span#win-perc-navbar')[0].textContent = tWinsPerc
            $('span#lose-perc-navbar')[0].textContent = (100 - tWinsPerc).toFixed()
        }

    })
}