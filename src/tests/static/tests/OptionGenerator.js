// change option to green or red
const options = document.getElementsByClassName('option')
const length = options.length
for (option of options) {
    answer = option.getElementsByClassName('correct-answer')[0].value
    
    if (answer == "T") {
        // change it to green
        option.getElementsByClassName('option-input')[0].className = "option-input border border-success w-75"
        option.getElementsByClassName('check-icon')[0].className = "material-icons text-success check-icon"
    }
}

// To delete selected option 
const deleteoption = (e) => {
    // Check if it is possible
    const options = document.getElementsByClassName('option')
    const length = options.length
    
    if (length < 3) {
        console.log("2 is the minimum")
        return
    }
    // Remove Input
    e.parentNode.remove()

    const options_updated = document.getElementsByClassName('option')
    const length_updated = options_updated.length

    for (let i = 0; i < length_updated; i++) {
        // ASCII a => letter 97
        // Update a) b)...
        options_updated[i].childNodes[3].innerHTML = `${String.fromCharCode(97 + i)})`
    }
}


// Get total options and check if it is > 2
const newOption = () => {
    const options = document.getElementsByClassName('option')
    const length = options.length
    
    // Check options length
    if (length > 7 || length < 2) {
        return
    }
    
    last_letter = options[length - 1].getElementsByClassName('letter')[0].innerHTML.charCodeAt(0)
    next_letter = `${String.fromCharCode(last_letter + 1)})`
    
    let div = document.createElement("div")
    div.className = "option"

    div.innerHTML = `
        <input type="hidden" name="correct-answer" class="correct-answer" value="F">
        <p class="letter">${next_letter}</p>
        <input type="text" class="option-input border border-danger w-75" name="question-option" required>
        <span class="material-icons cancel" onclick="deleteoption(this)">clear</span>
        <span class="material-icons text-danger check-icon" onclick="correct(this)">done_outline</span>
    `
    document.getElementsByClassName('question-option-div')[0].append(div)
}


// Update correct answer
const correct = (e) => {
    const options = document.getElementsByClassName('option')
    const length = options.length
    let element = e.parentNode

    for (let i = 0; i < length; i++) {
        // Change all hidden inputs to F
        options[i].childNodes[1].value = "F"
        options[i].getElementsByClassName('option-input')[0].className = "option-input border border-danger w-75"
        options[i].getElementsByClassName('check-icon')[0].className = "material-icons text-danger check-icon"
    }

    // Change red to green
    element.getElementsByClassName('option-input')[0].className = "option-input border border-success w-75"
    element.getElementsByClassName('check-icon')[0].className = "material-icons text-success check-icon"
    
    // Change correct-answer to true
    element.childNodes[1].value = "T"
}

// Check if there is a correct answer
const isValidForm = (e) => {
    const options = document.getElementsByClassName('option')
    const length = options.length
    const checkCorrectAnswer = false
    
    if (length < 2) {
        alert("Please, select one correct answer")
        e.preventDefault()
        return  
    } 
    
    for (const option of options) {
        inputValue = option.getElementsByClassName('correct-answer')[0].value
        
        // check if there is one correct answer
        if (inputValue == "T") {   
            // to avoid problems with html manipulation
            if (checkCorrectAnswer == true) {
                alert("Please, select only one correct answer")
                e.preventDefault()
                return 
            }
            
            checkCorrectAnswer = true
        }
    }

    if (!checkCorrectAnswer) {
        alert("Please, select only one correct answer")
        e.preventDefault()
        return 
    } 
}

function load() {
    const newOptionButton = document.getElementsByClassName('new-option')
    const form = document.getElementById('form-create')
    
    newOptionButton[0].addEventListener("click", newOption)
    form.addEventListener("submit", isValidForm)
}

document.addEventListener("DOMContentLoaded", load, false)
