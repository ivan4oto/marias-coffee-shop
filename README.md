## Maria's Coffee Shop

## Deploy with docker compose

```
$ chmod +x start.sh
$ ./start.sh
```

## Expected result

After the application starts, navigate to `http://localhost:8000` in your web browser or run:
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
