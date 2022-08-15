# Crawler

___

## Docker

### Run

To run the app in docker use:

```shell
make d-run
```

### Stop

To stop app in docker use:

```shell
make d-stop
```

### Clean

To clean up an app in docker use:

```shell
make d-purge
```

___

## App

### Run

To run the app:

```shell
make app-result number_of_urls=100 crawling_depth=10
```

where instead of `100` and `10` you substitute your value.