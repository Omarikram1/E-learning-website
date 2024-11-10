



document.getElementById('loginForm').addEventListener('submit', function(event) {
    event.preventDefault();  // Prevent the form's default submission

    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    // Ensure the CSRF token is retrieved properly
    const csrftoken = getCookie('csrftoken');
    const accessToken = getCookie('Access_Token');
    
    // Perform the POST request using fetch
    fetch('/users/login/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
           
        },
        body: JSON.stringify({ email: email, password: password })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        // const accessToken = getCookie('Access_Token');
        

        return fetch('/users/privatedata/', {
            method: 'GET',
            headers: {
                'X-CSRFToken': csrftoken,
                'Authorization': `Bearer ${accessToken}`,  // Send the Bearer token in the Authorization header
                'Content-Type': 'application/json',
            },
            credentials: 'include',  // Ensure cookies are sent with the request
            
        });
         ////////////////////////////////////////////////////////////

    })
    .catch(error => console.error('Error:', error));
});

function getCookie(name) {
    const cookieArray = document.cookie.split('; ');
    for (let cookie of cookieArray) {
      const [cookieName, cookieValue] = cookie.split('=');
      if (cookieName === name) {
        return cookieValue;
      }
    }
    return null;  // Return null if the cookie is not found
  }


function getAccessTokenFromCookie() {
    const name = 'Access_Token';
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.startsWith(name + '=')) {
            return cookie.substring(name.length + 1);
        }
    }
    return null;  // Return null if no token found
}