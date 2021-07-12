const eventBox = document.getElementById('event-box')
console.log(eventBox.textCotent)
const date = new Date()
console.log(date)
const countdownBox = document.getElementById('countdown-box')

//get milliseconds
const endDate = Date.parse(eventBox.textContent)
endDate.toLocaleString('en-US', { timeZone: 'America/New_York' })
console.log('asd')

const myCountdown= setInterval(()=>{

    const currentDate = new Date().getTime()

    console.log(currentDate)
    console.log(endDate)
    const difference = endDate - currentDate
//    console.log(difference)
    //days
    const d = Math.floor(endDate/(1000*60*60*24)-(currentDate/(1000*60*60*24)))
    //hrs
    const h = Math.floor((endDate/(1000*60*60)-(currentDate/(1000*60*60))) % 24)
    // mins
    const m = Math.floor((endDate/(1000*60)-(currentDate/(1000*60))) % 60)
    //seconds
    const s = Math.floor((endDate/(1000)-(currentDate/(1000))) % 60)

    if (difference>0){
    countdownBox.innerHTML = d + "Days, " + h+ "hours, "+ m+ "minutes, "+s+ "seconds"
    }
    else{
       clearInterval(myCountdown)
       countdownBox.innerHTML = "Time Over"
    }
}, 1000)

