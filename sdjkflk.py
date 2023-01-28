from firebase import firebase

firebase = firebase.FirebaseApplication('https://musketeerterminal2-default-rtdb.firebaseio.com/')

data = {
    'email': 'rymantheman@yahoo.com',
    'password': 'superidol123!'}

firebase.post('https://musketeerterminal2-default-rtdb.firebaseio.com/Users', data)
