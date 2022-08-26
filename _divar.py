import requests
import bs4
from unidecode import unidecode
import re
import pandas as pd
import json
import time

class BasePage:
    def __init__(self, url: str):
        self.url = url
        response = requests.get(url)
        soup = bs4.BeautifulSoup(response.text, "html.parser")
        post_list = soup.find("div", {"class": "browse-post-list"})
        self.card_list = post_list.find_all("div", {"class": "post-card-item kt-col-6 kt-col-xxl-4"})

class Divar(BasePage):
    def __init__(self, url: str, callback: callable=None):
        super().__init__(url)
        self._eligible_homes_rent = dict()
        self.callback = callback

    def eligible_home_rent(self, max_deposit: int=None, max_rent: int=None):
        """
        Return a list of eligible homes
        
        Parameters
        ----------
        max_deposit : int, optional(Toman unit)
            Maximum deposit amount. The default is None.
        max_rent : int, optional(Toman unit)
            Maximum rent amount. The default is None.
        
        Returns
        -------
        list
            List of eligible homes.
        
        Notes
        -----
        If max_deposit and max_rent are not specified, return all eligible homes.
        """
        while True:
            
            for card in self.card_list:
                href = "https://divar.ir" + card.a["href"]
                title = card.find("h2", {"class": "kt-post-card__title"}).text
                deposit, rent = (i.text.split(":")[1].split(" ")[1].strip()
                                for i in card.find_all(
                                    "div",
                                    {"class": "kt-post-card__description"}))
                deposit = ConvertStr.to_float(deposit)
                rent = ConvertStr.to_float(rent)
                if max_deposit and deposit > max_deposit:
                    continue
                if max_rent and rent > max_rent:
                    continue
                home = {
                    "title": title,
                    "href": href,
                    "deposit": deposit,
                    "rent": rent
                }
                _check = self._eligible_homes_rent.get(href)
                if _check and _check == home:
                    continue
                self._eligible_homes_rent[href] = home
                if self.callback:
                    msg = f"عنوان: {title}\n"\
                        f"ودیعه: {deposit:,}\n"\
                        f"اجاره بها: {rent:,}\n"\
                        f"لینک: {href}"
                    self.callback(msg)
                    time.sleep(1)
                    
            if self.callback:
                super().__init__(self.url)
                time.sleep(10)
            else:
                break
        return self._eligible_homes_rent.values()
    
class ConvertStr:
    @classmethod
    def to_float(cls, value: str):
        """
        Convert str to float
        """
        value = unidecode("".join(value.split(",")))
        if cls.persian_alphabet(value):
            value = 0
        try:
            value = float(value)
            return value
        except:
            raise ValueError("Invalid value")
        
    @staticmethod
    def persian_alphabet(value: str):
        """
        Check if value contains persian alphabet
        """
        if re.search(r"[\u0600-\u06FF]", value):
            return True
        else:
            return False
        
class Export:
    @staticmethod
    def to_dataframe(_list: list):
        """
        Export eligible homes to dataframe
        """
        return pd.DataFrame(_list)
    
    @staticmethod
    def to_json(_list: list):
        """
        Export eligible homes to json
        """
        return json.dumps(list(_list), ensure_ascii=False)
    
class ResizeMessage:
    @staticmethod
    def resize(msg: str, max_bytes: int=512):
        """
        Resize message to max_bytes
        """
        msg = msg.encode("utf-8")
        if len(msg) > max_bytes:
            msg = msg[:max_bytes]
            msg = msg.decode("utf-8")
            msg = msg.rstrip("\n")
            msg = msg + "..."
        return msg
    