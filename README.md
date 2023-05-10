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
`/customers/birthday` Get the customers with birthdays today.
`/customers/last-order-per-customer` Get the last order date per customer.
`/products/top-selling-products/{year}` Get the top 10 selling products for a given year.