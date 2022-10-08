def lambda_handler(event, context):
    response = {
        "statusCode": 200,
        "statusDescription": "200 OK",
        "isBase64Encoded": False,
        "headers": {
        "Content-Type": "text/html; charset=utf-8"
        }
    }

    response['body'] = """
    <html>
        <head>
            <title>Lambda URL</title>
            <style>
                html, body {
                background-color:rgb(22, 30, 43);
                margin: 10; padding: 10;
                font-family: arial; font-weight: 10; font-size: 1em;
                text-align: center;
                }
                html, h1 {
                color: white;
                font-family: verdana;
                font-size: 150%;
                }
                html, p {
                color: white;
                ont-size: 50%;
                }
            </style>
        </head>
        <body>
            <h1>Hello Stranger!</h1>
            <p>Hello from Lambda - Python</p>
            <img src="https://acegif.com/wp-content/gifs/banana-82.gif" width="450" />
        </body>
    </html>
    """

    return response