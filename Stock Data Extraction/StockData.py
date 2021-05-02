"""
# Enter the sheet number between 0 to 9
# Function returns a dataframe with the price from 2016 to present day
# small_data_flag is set to true is the last 100 trading days quotes are required
"""
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
import gspread

class SingleStockData:
    def __init__(self,sheet_number = 0,require_small_data = True):
        self.sheet_number = sheet_number
        self.require_small_data = require_small_data
        self.df = pd.DataFrame()

    def __str__(self):
        return (self.df.to_string())

    def generate_dataframe(self):
        self.get_sheet()
    
    def get_sheet(self):
        scope = ["https://spreadsheets.google.com/feeds","https://www.googleapis.com/auth/spreadsheets","https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
        cred_ob = {
        "type": "service_account",
        "project_id": "stockdataextract-1604151948917",
        "private_key_id": "1d79195cbae01f00aa6c4aa7f6011611e1216192",
        "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDV8pPtKFmWsyjV\n5hVO306sk1ZJOZJy++k8o2FjyLNhsmj63dFYvfPzvNPwBUdgYQDXf9N1mTyV35nm\nfQFN/JUy1OkOKqpQc6lvcl0wTh9kZvqycxgtn4jrvUVnQ8KmuXU3KVpYB4CIRarK\nmkOdM77aT5qNRWs8rbOtjBlL6o22Kr9JdGAdysZzTnhETzkwo4PgCknuENHZoqM9\n2QjeMRzeSrWHZhwk7fH6a+4ztXs130cDuqLpdMWAqLsg/Nj13k3I8aNF2+jQrQYw\nbgy005QYvPKw6T+W/rukhxoqGBlY6QnCFr+0brsmuLVibDZZDcDEnAz+He2+7vPy\nHv38y/Q9AgMBAAECggEAPNdQA9g+qeFnEnTsyFIuoFsB5a7um65RpIHdty+i+3xt\n6DFeUDssfbrMFmyZ4KmVQLNEIiQim4hLzsTrsw7KKvtrDzFI37oUi/Hc2FjPCpFS\nZ57dWFQO7uMTMouNdjY1RCuJWpE/lwEg0Z7O7YyCkLikfdoo5ceL2iWGKBWamRvH\n0MEEKINMp4NhQu/ihmUIIlPjrJzmKMPC0QPKsFzEQ+YxmIkizdNtzJxWnr4JbFck\nNmMVPKv4JBKEbMQLqcdLo/Qhzy9K9AjQ5EVkJF9y1Kf0dguULg8k++GGisLV/bl3\nCdiwgfhds/M85S61nJ/3YyOowUxRyZn4KGAbPlkWrQKBgQDqIKxanfuk2IHwmIy7\nFwgd5nxQ7d1p7+PLOfFNnVnnSXfyO2coQDdNSIRDMF54zjoVCiP/UeGMMDV91zNP\n0vlCwWbDPDV4SkAI3lZJ0/soKoSOGmn7BOJU3ShKUqjNcAV5k4dT1cR367X3Q0yI\nhh1DFWzthZA6ki4afRcqUpFNywKBgQDp70jFdEc5TVOnvYvGeMbkswTw7kfxzQK4\nPyeKL43rIty2+rINoqrAxWGBE1jgDzRU6ZFsqivEGnjPN4MCMfM2h0ASTrpJTdKH\nJc2+0M6nBZojNDb1NVw4CNDib7HE3L1r2HdLvuUq5kX/LwyhPLMXIQdDHeFhD7fw\nIXhbuosFFwKBgEkSJXiqse1C/Vr/4XxKtefPFaGUe3QiwK+ex+b3YyXCUkMxswJm\n+FuQdGcb44BErPAAGDgJcCF2slsyHPue1ti0z8PDONTwJ4gdDEVCebKRgolvSQBl\nB9aAp6B6p+BmQ+8r0iKiJw1ebY5cXLiHUv6q4zJGazs8gFMYE3DMEDl9AoGBALjJ\nQvp19yzUYBhIKXkFPla48lY+YqYmAtf3Swxks/3g8+e175/Ftou/Xl3PIo0adYP9\nW9oyMZAeOP+2Ic5CFpQkEgBkH9J3nq0St4ra9eIJEtBsFl1rYQUCMb4r7IhMtXPS\n8ajriapxayk/yQI0KGNEu6/Qko9RE0KjracHm3jRAoGAcRufNuJjUMbH+4fXQPIF\n4j1QWdQffxcK7fVLZEnLvqjkQaj58EQg3xaCiLhsWquv8YkYGp29KSDhQ2RBPyW4\nqRZIbtFgrLW5Z2oTKUf1/vbgvg8sSM9SOmxNqu8JfVEykk2AMgQiLfwnZMEtjyMI\nQpHXii91CmqW/KlQCi+IUrk=\n-----END PRIVATE KEY-----\n",
        "client_email": "moregunsstanley@stockdataextract-1604151948917.iam.gserviceaccount.com",
        "client_id": "107562319169822496944",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/moregunsstanley%40stockdataextract-1604151948917.iam.gserviceaccount.com"
        }

        
        creds = ServiceAccountCredentials.from_json_keyfile_dict(cred_ob, scope)

        client = gspread.authorize(creds)
        sheet = client.open("Stock Sheet")
        worksheet = sheet.get_worksheet(self.sheet_number)

        if(self.require_small_data):
            limit = -100
        else:
            limit = 1

        date_list = worksheet.col_values(2)
        self.df['DATE'] = date_list[limit:]

        open_list = worksheet.col_values(3)
        self.df['OPEN'] = open_list[limit:]

        high_list = worksheet.col_values(4)
        self.df['HIGH'] = high_list[limit:]

        low_list = worksheet.col_values(5)
        self.df['LOW'] = low_list[limit:]

        close_list = worksheet.col_values(6)
        self.df['CLOSE'] = close_list[limit:]

        volume_list = worksheet.col_values(7)
        self.df['VOLUME'] = volume_list[limit:]

        self.df['OPEN'] = self.df['OPEN'].astype(float)
        self.df['HIGH'] = self.df['HIGH'].astype(float)
        self.df['LOW'] = self.df['LOW'].astype(float)
        self.df['CLOSE'] = self.df['CLOSE'].astype(float)
        self.df['VOLUME'] = self.df['VOLUME'].astype(float)

def main():
    stock_data = StockData(0,True)
    stock_data.create_dataframe()
    print(stock_data)

if __name__ == '__main__':
    main()


