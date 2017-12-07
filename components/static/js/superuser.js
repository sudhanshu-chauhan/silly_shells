let tokenInstance;
let userDataSet;
let dataTableInstance;
let dataTableColumns = [{
    data: "uuid"
  },
  {
    data: "first_name"
  },
  {
    data: "last_name"
  },
  {
    data: "email"
  },
  {
    data: "security_credential"
  },
  {
    data: "is_superuser"
  },
]
class Token {
  constructor(token) {
    console.log('initiating token class instance...');
    this.token = token;
  }
}

class UserData {
  constructor() {
    console.log('initiating user data class instance...');
  }
  getUserData() {
    $.ajax({
      url: '/users/',
      type: 'GET',
      headers: {
        Authorization: tokenInstance.token,
      },
    }).done((data) => {
      try {
        userDataSet = data;
        dataTableInstance = $('#users-list-table').DataTable({
          data: userDataSet,
          columns: dataTableColumns,
        });

        $('#users-list-table tbody').on('click', 'tr', function() {
          if ($(this).hasClass('selected')) {
            $(this).removeClass('selected');
          } else {
            dataTableInstance.$('tr.selected').removeClass('selected');
            $(this).addClass('selected');
          }
        });
      } catch (error) {
        console.log(error);
        console.log(`UserData::getUserData::ajax(/users/):${error.message}`);
      }
    });
  }
}
class Authentication {
  constructor() {
    console.log('initiating authentication class instance...');
  }
  autheticate_superuser(credentials) {
    if (!('email' in credentials || 'password' in credentials)) {
      return false;
    }
    $.ajax({
      url: /get_superuser_token/,
      method: 'POST',
      data: JSON.stringify(credentials),
    }).done((data) => {
      try {
        data = JSON.parse(data);
        if ('token' in data) {
          tokenInstance = new Token(data['token']);
          $('#myModal').modal('hide');
          let userDataInstance = new UserData();
          userDataInstance.getUserData();
        }
      } catch (error) {
        console.log(`Authentication::authenticate_superuser:${error.message}`)
      }

    });
  }
}

$(document).ready(function() {
  $('#myModal').modal('show');
  $('#login-btn').click(function() {
    let credentials = {
      email: $('#email').val(),
      password: $('#password').val()
    };
    let authenticanInstance = new Authentication();
    authenticanInstance.autheticate_superuser(credentials);

  });
});
