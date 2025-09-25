// Get password and password confirm
const password = document.querySelector("#password")
const password_confirm = document.querySelector("#password_confirm")
const signupForm = document.querySelector("#signup-form")
// Submit event
signupForm.addEventListener("submit",(e)=>{
    e.preventDefault()
    // Remove existing alert if any
    const existingAlert = document.querySelector(".alert");
    if (existingAlert) existingAlert.remove();
    //Check confirm pass and pass confirm
    if (password.value != password_confirm.value){
        const alertElement = document.createElement("div")
        alertElement.className = "alert"
        alertElement.textContent = "Password and password confirm mismatch."
        signupForm.prepend(alertElement)
        return
    }
    signupForm.submit()
})
