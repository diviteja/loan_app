const loginForm = document.getElementById("login-form");
console.log(document.getElementById("login-form"));

loginForm.addEventListener('submit', async function(event) {
    event.preventDefault();
    let isValid = true; // Fix case
    const usernameField = document.getElementById("username");
    const passwordField = document.getElementById("password");
    console.log("Entered Event Listener");
    if (isValid) {
        const loginData = {
            username: usernameField.value,
            password: passwordField.value,
        };

        try {
            const response = await fetch('http://18.133.30.151:8000/api/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(loginData),
            });

            const result = await response.json();

            if (response.ok) {
                alert("Login Successful");
                console.log("For login request, Server response: ", result);
                window.location.href = "/checker.html"; // Fix syntax
            } else {
                alert(result.message || "Login failed, please try again");
                console.error("Error: ", result);
            }
        } catch (error) {
            console.error("Network error:", error);
            alert("An error occurred. Please try again later.");
        }
    }
});
