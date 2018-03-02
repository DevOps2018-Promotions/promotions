[![Build Status](https://travis-ci.org/DevOps2018-Promotions/promotions.svg?branch=master)](https://travis-ci.org/DevOps2018-Promotions/promotions)
[![codecov](https://codecov.io/gh/DevOps2018-Promotions/promotions/branch/master/graph/badge.svg)](https://codecov.io/gh/DevOps2018-Promotions/promotions)

# promotions
The promotions resource is a representation of a special promotion or sale that is running against a product or perhaps the entire store. Some examples are "buy 1 get 1 free", "20% off" etc.

To Run, clone the repo


```
git clone https://github.com/DevOps2018-Promotions/promotions.git
```

```
cd promotions
```

If running in Windows, open Vagrantfile and comment out


 *#config.vm.network "private_network", ip: "192.168.33.10"*


Otherwise you will get error, "VBoxManage.exe: error: Could not find Host Interface Networking driver! Please reinstall"

```
vagrant up
```

If running in Windows, you might get a prompt from Windows Defender to allow Ruby to run. Click Allow access.


```
vagrant ssh
```

```
cd /vagrant
```
