[![Build Status](https://travis-ci.org/DevOps2018-Promotions/promotions.svg?branch=master)](https://travis-ci.org/DevOps2018-Promotions/promotions)
[![codecov](https://codecov.io/gh/DevOps2018-Promotions/promotions/branch/master/graph/badge.svg)](https://codecov.io/gh/DevOps2018-Promotions/promotions)

# promotions
Welcome to NYU DevOps Spring 2018 Promotion team!
The promotions resource is a representation of a special promotion or sale that is running against a product or perhaps the entire store. Some examples are "buy 1 get 1 free", "20% off" etc.

## Launch the server

Clone the repo
```
git clone https://github.com/DevOps2018-Promotions/promotions.git
cd promotions
```

If running in Windows, open Vagrantfile and comment out
```
# config.vm.network "private_network", ip: "192.168.33.10"
```

Otherwise you will get error,
`VBoxManage.exe: error: Could not find Host Interface Networking driver! Please reinstall`

```
vagrant up
vagrant ssh
```
If running in Windows, you might get a prompt from Windows Defender to allow Ruby to run. Click Allow access.

Once you are in the virtual machine, `cd /vagrant` to where the code lives.
To double check, run `nosetests` to see if all test cases pass.
Then run `python server.py`.

Now, the server should be available at `http://localhost:5000`


## Interact with the Server.

#### Content-Type
The `content-type` of the http request we accept is `application/json`.


#### HTTP Request Types
Our server allows the following operations
- **CREATE**: Create a promotion entry. The database will internally assign an id for it.
  `POST http://localhost:5000/promotions`
- **READ**: Read a promotion entry by it's id.
  `GET http://localhost:5000/promotions/<int:promotion_id>`
- **LIST ALL**: List all the promotions registered in the database.
  `GET http://localhost:5000/promotions`
- **QUERY**: Query some promotion enties by single condition.
  `GET http://localhost:5000/promotions?<query-string>`
- **UPDATE**: Update the fields of a promotion using its id.
  `PUT http://localhost:5000/promotions/<int:promotion_id>`
- **DELETE**: Delete a promotion by its id.
  `DELETE http://localhost:5000/promotions/<int:promotion_id>`
- **REDEEM** (ACTION, not RESTful): Increment the counter for a promotion.
  `POST http://localhost:5000/promotions/<int:promotion_id>/redeem`

#### HTTP Request Args
- `<int:promotion_id>`: Set automatically on creation. No one is supposed to modity this field.
- `<str:name>`: After creation, it can be modified by `PUT`.
- `<int:product_id>`: After creation, it can be modified by `PUT`.
- `<float:discount_ratio>`: After creation, it can be modified by `PUT`.
- `<int:counter>`: Incremented on `PUT http://localhost:5000/promotions/<int:promotion_id>/redeem`. The field is associated with the `promotion_id`, and will persist after **UPDATE**s.

  More comming soon.
