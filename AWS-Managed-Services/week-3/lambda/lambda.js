exports.handler = async (event) => {
    console.log('Lambda is called from LB and the payload is'); 
    console.log(JSON.stringify(event));
    
    const html = `
        <html>
            <head>
                <title>Lambda URL</title>
                <style>
                    html, body {
                    background-color:rgb(255, 255, 255);
                    margin: 10; padding: 10;
                    font-family: arial; font-weight: 10; font-size: 1em;
                    text-align: center;
                    }
                    html, h1 {
                    color: black;
                    font-family: verdana;
                    font-size: 150%;
                    }
                    html, p {
                    color: black;
                    ont-size: 50%;
                    }
                </style>
            </head>
            <body>

                <h1>Hello Stranger!</h1>
                <p style="color:White;">Hello from Lambda - Java Script</p>
                <img src="https://acegif.com/wp-content/gifs/banana-82.gif" width="450" />
            </body>
        </html>
    `;

    const response = {
        statusCode: 200, 
        statusDescription: "200 OK", 
        isBase64Encoded: false, 
        headers: {
            "Content-Type": "text/html" 
            },
            body: html

        };
        return response; 
    };
    