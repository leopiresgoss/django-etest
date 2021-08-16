
const deleteTest = (e) => {
    answer = confirm("Do you want to delete your test?")

    if (answer == false) {
        e.preventDefault()
    }

    return
}

function load() {
    const deleteButtons = document.getElementsByClassName('delete-button')
    
    for (button of deleteButtons) {
        button.addEventListener("click", deleteTest)
    }    
}

document.addEventListener("DOMContentLoaded", load, false)