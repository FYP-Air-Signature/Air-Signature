import requests
from App.verification.Preprocess import deleteDirectory
from dotenv import dotenv_values

# Load environment variables from .env file
env_vars = dotenv_values()
class PdfAPI:
    def __init__(self):
        self.base_url = env_vars["BASE_URL"]
        self.downloadedPdf = None
        self.signedPdf = None

    def getPDF(self, pdfId, userName, token):
        url = f"{self.base_url}/pdf/" + pdfId
        response = requests.get(url, headers={"Cookie" : token})

        if response.status_code == 200:
            pdfContent = response.content

            # create folder for pdfs for temp verification
            savePath = "verification//application_data//pdfsForVerification" + f"//{userName}_{pdfId}.pdf"

            # Save PDF to local file
            with open(savePath, 'wb') as file:
                file.write(pdfContent)
            self.downloadedPdf = savePath
            return True

        else:
            print("There is no pdf with id : " + pdfId)
            return False


    def getDownloadedPdf(self):
        return self.downloadedPdf

    def deleteDownloadedPdf(self):
        deleteDirectory(self.downloadedPdf)
