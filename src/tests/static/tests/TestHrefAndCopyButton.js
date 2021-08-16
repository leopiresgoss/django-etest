// Create test href and change url input value
testCode = document.getElementById('test-code-input')
urlInput = document.getElementById('test-href')

href = `${location.origin}/test/${testCode.value}`

urlInput.value = href

// To copy this link
// Code based on https://www.w3schools.com/howto/howto_js_copy_clipboard.asp
function copyButton() {
    /* Get the text field */
    var copyText = urlInput
  
    /* Select the text field */
    copyText.select();
    copyText.setSelectionRange(0, 99999) /* For mobile devices */
  
    /* Copy the text inside the text field */
    document.execCommand("copy")
  }

