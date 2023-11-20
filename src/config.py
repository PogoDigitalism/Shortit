class Config:
    def __init__(self) -> None:
        self.version = 1.0
        self.name = 'Profile API'
    
    @staticmethod
    def ConnectionSRV() -> str:
        return 'mongodb+srv://pdigitalism:8g2xrrWkM@profiles.8bnjfpk.mongodb.net/?retryWrites=true&w=majority'
    
    @staticmethod
    def EndpointConstants() -> dict:
        return {
            '_get_profile': {
                # RETURN PROFILE STATISTICS (USERNAME, DISPLAYNAME, USERID, AVATAR_HEADSHOT_THUMBNAIL)
                'Cooldown': 60,
                'MaxTokens': 2
            },
            '_get_root': {
                # RETURN ROOT
                'Cooldown': 3,
                'MaxTokens': 6
            },
            '_get_version': {
                # RETURN VERSION                                                                                                                                      cccccccccccccccccccccccccccccccccccccccccccc               cg
                'Cooldown': 10,
                'MaxTokens': 2
            },
        }
        
    @staticmethod
    def HTML_404():
        return """
            <!DOCTYPE html>
            <html>
            <head>
                <!-- HTML Codes by Quackit.com -->
                <title>
                </title>
                <meta name="viewport" content="width=device-width, initial-scale=1">
                <style>
                    body {background-color:#ff0000;background-repeat:no-repeat;background-position:top left;background-attachment:fixed;}
                    h1{font-family:Arial, sans-serif;color:#000000;background-color:#ffffff;}
                    p {font-family:Georgia, serif;font-size:14px;font-style:normal;font-weight:normal;color:#000000;background-color:#ffffff;}
                </style>
            </head>
            <body>
                <h1>404: PAGE NOT FOUND</h1>
                <p></p>
            </body>
            </html>
            """