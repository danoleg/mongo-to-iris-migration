# About application
Using this application, you can transfer data from the MongoDB collections to the IRIS globals. When data is migrated, a global of the same name is created. The data structure of the collection is reproduced in the IRIS global.

This application uses nativeAPI to work with IRIS.
## How to use it
It is very simple. To start the application, clone project and run the command:
```
$ docker-compose up -d
```

By url http://127.0.0.1:8011/restaurants will open a demo page with a collection of restaurants. 

On this page, you can migrate data or clear IRIS.
To start migration click on button and wait few seconds. After finishing the page reload with updated information.

The demo presents only one collection, but in order to open management of another collection, just change its name in the url path.
