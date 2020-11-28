import requests
import json as j
import pprint as p

class Frontend:
  """Class for homeport frontend API tests."""

  def __init__(self):
    """Constructor initialize url and endpoints dictionary."""
    self.url = "http://test.homeport.cz/api/"
    self.endpoints =  {
      "login": "auth",
      "bike": "bike-detail",
      "info": "tutorioal",
      "pin": "change-pin",
      "bug": "bug-report",
      "card": "get-customer-cards"
    }
    self.head = ""

  def getBikeInfo(self,bikeNum):
    """
    Prints bike info.
      Parameter:
        bikeNum (int)
    """
    params = {"BikeIdentifier": str(bikeNum)}
    p.pprint(requests.get(self.url + self.endpoints["bike"],params=params).json())

  def login(self,cardNum,pin):
    """
    gets authentification bearer.
      Parameters:
        cardNum (int), pin (int)
    """
    parameters = {
      "lang": "en"
    }
    credentials = {
      "CardNumber": str(cardNum),
      "Pin": str(pin)
    }
    response = requests.post(self.url + self.endpoints["login"],params=parameters,data=credentials)
    token = response.json()["data"]["token"]
    if(not token):
      print("Login unsucesfull")
    else:
      print("Login sucesfull")
      self.cardNum = cardNum
      self.head = {
        "Authorization": "Bearer " + token,
      }

  def changePin(self,oldPin,newPin):
    """
    Changes PIN.
      Parameters:
        oldPin (int), newPin (int)
    """
    if(not self.head):
      print("Login first!")
      return

    data = {
      "CardNumber": str(self.cardNum),
      "NewPin": str(newPin),
      "OldPin": str(oldPin)
    }
    response = requests.post(self.url + self.endpoints["pin"],data=data,headers=self.head)
    if(response.json()["success"]):
      print("Pin changed")

  def report(self,message):
    """
    Sends bug report.
      Parameters:
        message (string)
    """
    if(not self.head):
      print("Login first!")
      return
    data = {
      "Message": message,
      "Platform": "Adam's testing python class",
      "Version": "0.1a",
      "App": "Ubuntu",
      "Location": "20"
    }
    response = requests.post(self.url + self.endpoints["bug"],data=data,headers=self.head)
    p.pprint(response.json())
  
  def showCards(self):
    """Displays customer's cards."""
    if(not self.head):
      print("Login first!")
      return
    response = requests.get(self.url + self.endpoints["card"],headers=self.head)
    p.pprint(response.json())
