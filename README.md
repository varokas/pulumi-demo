# Pulumi Demo

## Prerequisite
1. Install pulumi
```
$ brew install pulumi
```

2. Create a bucket for pulumi state (e.g. varokas-pulumi-demo)

3. Login
```
pulumi login 's3://varokas-pulumi-demo?region=us-west-2&awssdk=v2'
```

4. Apply change
```
pulumi up
``` 