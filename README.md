## Maria's Coffee Shop

## Deploy with Docker

```
$ chmod +x start.sh
$ ./start.sh
```

## Expected result

After the application starts, you can reach the endpoints in your web browser or through the terminal:
```
$ curl http://localhost:5000/customers/last-order-per-customer
{
  "customers": [
        {
            "customer_email": "Venus@adipiscing.edu",
            "customer_id": 1,
            "last_order_date": "2019-04-29"
        },
        {
            "customer_email": "Nora@fames.gov",
            "customer_id": 2,
            "last_order_date": "2019-04-26"
        }, ...
    ]
}
```

## Available endpoints

The API exposes 3 endpoints:
1. `/customers/birthday` Get the customers with birthdays today.
2. `/customers/last-order-per-customer` Get the last order date per customer.
3. `/products/top-selling-products/{year}` Get the top 10 selling products for a given year.

## Tests

Unittests can be found in app/tests. To run the unittests do the following:

1. Set the APP_TESTING env variable to true. `$ expose APP_TESTING=True`
2. Start the test database. Use the following script to run a Postgres docker container. `$ docker run --name my_test_postgres -e POSTGRES_USER=mytestuser -e POSTGRES_PASSWORD=mytestpassword -e POSTGRES_DB=mytestdb -p 5432:5432 -d postgres:latest`
The URI config can be found in app/config.py if you want to connect to a different database just modify the `SQLALCHEMY_DATABASE_URI`.
3. Run the tests. `python -m unittest discover`.