# SUCCESS
{
    "Messages": [
        {
            "MessageId": "daf5f08c-3c21-4f4a-8339-3331acdd3776",
            "ReceiptHandle": "AQEB3TfTv0R2LuLS8MlVJir7WtKlpYLhr1cPhBihK+/+c602oNk8LZDnmPc2gurorjoxF9JQTjQ7Xs99ufmitK4L1cM1cobv9MtV9PqdhwTofMw3Ch1RR7T4LY3UUjqtYz1RXX10OTHYYDvBpoyAihetMtCqbjc0wimeVVfSh5mC6eRrg0HZ891ZAl4mgXy61h9LgRXL6YZ6AxUbq8cS6bEK0I3RIU7PbdHCkGwfOWJ+MmOnh0U5Oht/6WXnmnMYO10CKpIkicTBn2YbPpTMaIWtBQmbD5z36eNB03UhuJnGgFPoBV9/+azwOGOWTeKcCsf5CHlebSqjUcoOC2qmIFZ00PJQTHMwz+D1SAHb/ZgETy0cZMxUsEfj0HEbi/4a0R1KbP5XrKFjNbyOMeulC8YwRw==",
            "MD5OfBody": "238af92ed64f60968b4d1da598ec0e32",
            "Body": '{"Cuisine": "restaurants", "Email": "y@y.com", "NumberOfPeople": "4", "Time": "21:00", "Date": "2024-02-18", "Location": "Manhattan"}',
        }
    ],
    "ResponseMetadata": {
        "RequestId": "ef05bdc6-eb23-55a0-ad68-e38a87501660",
        "HTTPStatusCode": 200,
        "HTTPHeaders": {
            "x-amzn-requestid": "ef05bdc6-eb23-55a0-ad68-e38a87501660",
            "x-amzn-trace-id": "Root=1-65d26a31-3eef99047c06ef4578a8fd2e;Parent=43f5f321609f14ca;Sampled=0;Lineage=a0a30d84:0",
            "date": "Sun, 18 Feb 2024 20:36:03 GMT",
            "content-type": "text/xml",
            "content-length": "1104",
            "connection": "keep-alive",
        },
        "RetryAttempts": 0,
    },
}

# FAIL
{
    "ResponseMetadata": {
        "RequestId": "6a22ee89-7f4a-5f26-b88b-b0c5139e9fd2",
        "HTTPStatusCode": 200,
        "HTTPHeaders": {
            "x-amzn-requestid": "6a22ee89-7f4a-5f26-b88b-b0c5139e9fd2",
            "x-amzn-trace-id": "Root=1-65d26a94-5c3fe51a56917f4e29af5895;Parent=3156a3942965dd05;Sampled=0;Lineage=a0a30d84:0",
            "date": "Sun, 18 Feb 2024 20:37:40 GMT",
            "content-type": "text/xml",
            "content-length": "240",
            "connection": "keep-alive",
        },
        "RetryAttempts": 0,
    }
}

# SOMETHING
{
    "Messages": [
        {
            "MessageId": "d9eaffb9-80e9-40ef-aaf1-2c1474f99685",
            "ReceiptHandle": "AQEBnkkpKJYkQoZFNLC0NRL4mVGxBFh0cmy3XHwQuDHdJeyppvIDCi+tS1fxhpnqH8v2hxKy7JM7AKGUtW/kS6JYh9ZyINyqNI4OVhfQgIhDwU/01PYVTDREc+nYU2dtmiM2iWu4R5c1N9zSnWdkGEpa97dPEH0eDrtRnRLbQMDjS9srwjkactxG/YRqwYNr/6UbwHVvrLx8iFb1EXuqN+XDVwME1eZCvKo5h5npqXV8A/U6GSNISQIiW//jKQJ6m56K4PHR1dZ6IMhfhN34cUR1bccrOQs9x5Kq4l6szCHOoswCCf4z0HL54tGqh3JwwsYz21foYTtYBZS3ddvIHsFsrRLI6SiG0tsKk4KGznOs5PMnHB+nQRlJQYN6kI0GxqRP/X38yAWhqZQmQGdvpYe/bA==",
            "MD5OfBody": "e7b7c89ac4ced175d94b8bafd09c6013",
            "Body": '{"Cuisine": "Italian food", "Email": "kaka@ksk.com", "NumberOfPeople": "2", "Time": "18:30", "Date": "2024-02-19", "Location": "Manhattan"}',
        }
    ],
    "ResponseMetadata": {
        "RequestId": "53aa80ff-3ea1-5068-ad34-deb34f2449a5",
        "HTTPStatusCode": 200,
        "HTTPHeaders": {
            "x-amzn-requestid": "53aa80ff-3ea1-5068-ad34-deb34f2449a5",
            "x-amzn-trace-id": "Root=1-65d26f43-7583a2af61596e534381c63d;Parent=7404c33e49d05458;Sampled=0;Lineage=a0a30d84:0",
            "date": "Sun, 18 Feb 2024 20:57:41 GMT",
            "content-type": "text/xml",
            "content-length": "1110",
            "connection": "keep-alive",
        },
        "RetryAttempts": 0,
    },
}

{
    "Item": {
        "rating": {"N": "3.8"},
        "categories": {
            "L": [{"S": "Fast Food"}, {"S": "Chicken Shop"}, {"S": "American"}]
        },
        "zip_code": {"S": "10016"},
        "insertedAtTimestamp": {"S": "2024-02-18 03:20:15"},
        "address": {"L": [{"S": "484 3rd Ave"}, {"S": "New York, NY 10016"}]},
        "id": {"S": "oBcqZs0CAZjsLuMB-mNJ6A"},
        "name": {"S": "Sticky's"},
        "review_count": {"N": "488"},
        "coordinates": {
            "M": {"longitude": {"N": "-73.9788811"}, "latitude": {"N": "40.7450456"}}
        },
    },
    "ResponseMetadata": {
        "RequestId": "OH7ACBO2B7FUGMMRD1RCJNSOKRVV4KQNSO5AEMVJF66Q9ASUAAJG",
        "HTTPStatusCode": 200,
        "HTTPHeaders": {
            "server": "Server",
            "date": "Mon, 19 Feb 2024 02:09:09 GMT",
            "content-type": "application/x-amz-json-1.0",
            "content-length": "419",
            "connection": "keep-alive",
            "x-amzn-requestid": "OH7ACBO2B7FUGMMRD1RCJNSOKRVV4KQNSO5AEMVJF66Q9ASUAAJG",
            "x-amz-crc32": "1539330868",
        },
        "RetryAttempts": 0,
    },
}

[
    {
        "query": {
            "Cuisine": "Pizza",
            "Email": "jj@jj.com",
            "NumberOfPeople": "2",
            "Time": "09:00",
            "Date": "2024-02-20",
            "Location": "Manhattan",
        },
        "message_id": "7418d210-2f84-4b65-8ad4-732f9fc80339",
        "recommendation": [
            "oneivxyaRyF70Dq_If5qkQ",
            "xnqEMpQzCltu06p7NSNMMw",
            "oOr6Ta5gZyDl6PyZ1cq7pg",
        ],
        "results": [
            {"name": "Appas Pizza", "address": ["210 1st Ave", "New York, NY 10009"]},
            {
                "name": "Little Charli",
                "address": ["271 Bleecker St", "New York, NY 10014"],
            },
            {
                "name": "East Village Pizza",
                "address": ["145 1st Ave", "New York, NY 10003"],
            },
        ],
        "email_content": "Hi, here are my suggestions on Pizza restaurants for 2 on 09:00 2024-02-20:\n1. Appas Pizza, located at 210 1st Ave, New York, NY 10009\n1. Little Charli, located at 271 Bleecker St, New York, NY 10014\n1. East Village Pizza, located at 145 1st Ave, New York, NY 10003",
    }
]
