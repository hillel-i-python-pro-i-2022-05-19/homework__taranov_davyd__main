# Fuzz generator

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
make app-result words_count=100 word_length=5
```

where instead of `100` and `5` you substitute your value