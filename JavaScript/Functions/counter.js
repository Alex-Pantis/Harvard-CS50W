        //let counter = 0;

        // Check if we already have a counter saved in the browser
        // localStorage = special place in browser that remembers things even after closing
        if(!localStorage.getItem('counter')){
            localStorage.setItem('counter', 0);
        }
        // Main function — runs when you click the button
        function count() {
            // Get the current number from storage (it's a string like "5")
            let counter = localStorage.getItem('counter');
            counter++;
            // document = page object, querySelector("h1") = function with parameter, innerHTML = property, counter = variable
            // Update the <h1> text on the page to show new number
            // document.querySelector("h1") = find the <h1> tag
            // .innerHTML = change the text inside it
            document.querySelector("h1").innerHTML = counter;
            /*if (counter % 10 === 0 && counter !== 0) {
                     alert(`Count is now ${counter}`);
                     }*/
            // Save the new number back to storage so it remembers
            localStorage.setItem('counter', counter);   
        }
        
        // When page loads completely → run this
        document.addEventListener('DOMContentLoaded', function() {
            // Show the saved number when page opens
            document.querySelector('h1').innerHTML = localStorage.getItem('counter');
            // When button is clicked → run the count function
            document.querySelector('button').onclick = count;

            //setInterval(count, 1000);
        });