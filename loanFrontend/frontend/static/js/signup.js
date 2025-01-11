const signupform = document.getElementById("signup-form");

signupform.addEventListener('submit', async function(event){
    event.preventDefault();
    const usernameField = document.getElementById("username");
    const passwordField = document.getElementById("password");

    const signupData = {
        username : usernameField.value,
        password : passwordField.value,
    }

    try{
        const response = await fetch('http://localhost:8000/api/signup',{
            method: "POST",
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(signupData),
        })
        const result = await response.json()
        if (response.ok) {
            alert('Signup successful! Please log in.');
            window.location.href = '/login.html'; // Redirect to login page
        } else {
            alert(result.message || 'Signup failed.');
        }
    } catch(error){
        alert("Sign-up Failed due to erroe", error);
        console.log("Error messgae", error);
    }

})