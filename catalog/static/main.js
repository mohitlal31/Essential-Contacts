function start() {
  gapi.load('auth2', function() {
    console.log("start called");
    auth2 = gapi.auth2.init({
      client_id: '1008740663928-crpp30q0usbethaqufgg4rcnrcbresqk.apps.googleusercontent.com',
    });
  });
}

$(document).ready(function() {
  $('#signinButton').click(function() {
    auth2.grantOfflineAccess().then(signInCallback);
  });
});

function signInCallback(authResult) {
  console.log("authResult['code'] = " + authResult['code']);
  console.log("state = " + login_state);
  if (authResult['code']) {
    // Hide the sign-in and cancel button now that the user is authorized
    $('#signinButton').attr('style', 'display: none !important');
    $('#loginCancel').attr('style', 'display: none !important');

    // Send the code to the server
    $.ajax({
      type: 'POST',
      url: 'http://localhost:5000/signin',
      // Always include an `X-Requested-With` header in every AJAX request,
      // to protect against CSRF attacks.
      headers: {'X-Requested-With': 'XMLHttpRequest'},
      contentType: 'application/json',
      data: JSON.stringify({authCode: authResult['code'], state: login_state}),
      success: function(result, textStatus, jqXHR ) {
        // Handle or verify the server response.
        if (result) {
          $('#result').html('Login Successful!</br>' + 'Redirecting...')
          setTimeout(function() {
            window.location.href = "http://localhost:5000";
          }, 2000);
        }
      },
      error: function(jqXHR, textStatus, errorThrown) {
        $('#result').html('Login Failed</br>' + textStatus + '</br>Redirecting...')
        setTimeout(function() {
          window.location.href = "http://localhost:5000";
        }, 2000);
      }
    });
  }
  else {
    console.log("Sign In failed");
  }
}
