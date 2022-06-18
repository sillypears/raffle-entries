$(function () {

    console.log("Hi pal. Hope your day is going nicely. Or night. You've picked a wild adventure trying to set this up.")
    console.log("Or maybe send me a message on Discord, pears#0001, and say hello or tell me how messed up this is.")

    console.log(`           ████
             ██                    
             ████                  
               ██                  
               ▒▒▒▒▒▒              
             ▒▒▒▒▒▒▒▒▒▒            
           ▒▒▒▒▒▒▒▒▒▒▒▒            
           ▒▒▒▒▒▒▒▒▒▒▒▒▒▒          
           ▒▒▒▒▒▒▒▒▒▒▒▒▒▒          
           ▒▒▒▒▒▒▒▒▒▒▒▒▒▒          
           ▒▒▒▒▒▒▒▒▒▒▒▒▒▒          
           ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒        
           ▒▒▒▒▒▒▒▒  ▒▒▒▒▒▒▒▒      
         ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒    
         ▒▒▒▒▒▒▒▒▒▒▒▒  ▒▒▒▒▒▒▒▒▒▒  
       ▒▒▒▒▒▒▒▒▒▒▒▒  ▒▒▒▒  ▒▒▒▒▒▒  
       ▒▒▒▒▒▒▒▒  ▒▒▒▒▒▒      ▒▒▒▒▒▒
     ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒  ▒▒  ▒▒  ▒▒▒▒
     ▒▒▒▒▒▒▒▒▒▒▒▒  ▒▒▒▒  ▒▒  ▒▒▒▒▒▒
     ▒▒▒▒▒▒▒▒  ▒▒▒▒▒▒  ▒▒      ▒▒▒▒
     ▒▒▒▒▒▒▒▒▒▒▒▒▒▒  ▒▒▒▒▒▒  ▒▒▒▒▒▒
     ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒  ▒▒▒▒▒▒▒▒▒▒
       ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒  
         ▒▒▒▒▒▒▒▒▒▒████▒▒▒▒▒▒▒▒    
           ▒▒▒▒▒▒▒▒██▒▒▒▒▒▒ `)
    $('td.epoch').each(function () {
        console.log(this.textContent)
        this.innerHTML = moment.unix(this.textContent).format('Y-MM-DD')
    })
    var myModal = document.getElementById('hi-there')
    
    myModal.addEventListener('shown.bs.modal', function () {
    })
    document.cookie = `tz_info=${new Date().getTimezoneOffset()}`
})

function toggleResult(id, result) {
    $.ajax({
        url: "/toggle-result",
        method: "PUT",
        data: {
            'id': id,
            'result': result
        },
        success: function (res) {
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
                tWins -= 1
                $(`#result-${id}`).text("L").removeClass('result-green').addClass('result-red')
                $(`#flip-result-${id}`).attr("onclick", `toggleResult(${id}, 0)`)
                $('#lose-perc-num').text(tLoses)
                $('#win-perc-num').text(tWins)
            }
            const tWinsPerc = (tWins / tTotal * 100.00).toFixed(2)
            $('span#win-perc-navbar')[0].textContent = tWinsPerc
            $('span#lose-perc-navbar')[0].textContent = (100.00 - tWinsPerc).toFixed(2)
        }

    })
}