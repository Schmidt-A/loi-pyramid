# TrashVanillaJS

The contents of the static folder are all front end test bed projects. This is trash code that Alex is writing to inform future decisions about how to run the UI. 

The primary purpose of this trash code is to retrieve information from the LoI apis without using ANY javascript frameworks on runtime. Javascript frameworks are being used for running testing only. 

## Local Environment

* Install dependencies inside static folder
```
yarn install
```

## Linting
* Run ESlinting via 
```
./node_modules/.bin/eslint ./
```

Rules managed at:
```/Users/alexmcguigan/dev/loi/loi-pyramid/loi_pyramid/static/.eslintrc.js```

## Run Tests
* Run unit tests in jest via jsdom
```
yarn unit
```

* Run js integration tests in jest jsdom
```
yarn integration
```

* Run all js tests in jest jsdom
```
yarn test
```

Coverage files can be generated with ```--coverage``` are in ```.coverage/```

Configurations are managed at:
```
jest.config.js
jest.unit.config
jest.integration.config
```

## Use application
### Without backend apis
* in the /static folder, stand up a server
```
python3 -m http.server
```
Now navigate in the browser to the test stub page
```http://localhost:8000/views/test_stub.html```

### With backend apis
* in the main /loi-pyramid folder, stand up the Pyramid server
```
pserve development.ini
```

Now navigate in the browser to the index stub page
```http://127.0.0.1/static/views/index_stub.html```

All files in the static folder are available via ```http://127.0.0.1/static/``` when served by Pyramid