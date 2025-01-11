const loandata = document.getElementById("loanForm");
const resultdiv = document.getElementById("result");
console.log(loandata);

loandata.addEventListener('submit',async function(event){
    event.preventDefault();
    const formdata = new FormData(loandata);
    data = {};
    formdata.forEach((value,key) => {
        data[key]=value;
    });

    try{
        const response = await fetch('http://localhost:8000/api/eligibility_checker',{
            method : 'POST',
            headers : {
                "Content-Type": "application/json", 
            },
            body : JSON.stringify(data),  
        })

        if(response.ok){
            const result = await response.json();
            console.log(result.data);
            resultdiv.textContent = result.message;
            resultdiv.className = "result-success";
            
          } else {
            const error = await response.json();
            resultdiv.className = "result-error";
            resultdiv.textContent = `Error: ${error.message}`;
          }
    } catch (error) {
      resultdiv.textContent = `Network error: ${error.message}`;
      resultDiv.className = "result error"; 
      console.log(error);
      console.log(error.message);
    }
    resultdiv.classList.remove("hidden");
})

