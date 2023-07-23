# Documentation of iac:
'iac' directory contains .tf files required to manage and provision AWS resources

## Pre-requisites:
1. Load AWS credentials in .aws/credentials file under "scrafter" profile

## Init:
To intialize modules and providers, execute the following command:
```yaml
terraform init
```

## Plan:
To generate execution plan, execute the following command:
```yaml
terraform plan
```

## Apply:
To apply (provision) resources, execute the following command:
```yaml
terraform apply
```

## Version 1.0 - Auto deployment of static site:
'iac' provisions resources, as well as perform the following configurations:

1. s3 bucket to contain static site assets
2.  enables the bucket as a static site
3. copies all files part of site/ directory as s3 objects into the bucket

### Manual steps:
Currently the following steps are manually performed:

Under permissions tab:

1. Uncheck all settings in "Block public access" if not already unchecked
2. Add the following bucket-policy if not already added:
    ```json
    {
        "Version": "2008-10-17",
        "Id": "Policy",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {
                    "AWS": "*"
                },
                "Action": "s3:GetObject",
                "Resource": "arn:aws:s3:::fast-resources-search/*"
            }
        ]
    }
    ```
3. Enable ACLs by editing "Object Ownership"
4. Grant "Read" permission to Everyone (public access) by editing "ACL"