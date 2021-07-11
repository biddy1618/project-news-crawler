import datetime
import logging

from typing import List

logger = logging.getLogger(__name__)

class Helper():
    
    @staticmethod
    def _message(msg: str, e: Exception = None) -> str:
        """
        Helper function to print messages.

        Args:
            msg (str): Message.
            e (Exception, optional): Exception if raised. Defaults to None.

        Returns:
            str: message formatted.
        """
        if e: return f'{msg}. {type(e).__name__}: "{e}".'
        else: return f'{msg}'    
    
    @staticmethod
    def generate_dates(start_date: str, end_date: str = None) -> List[str]:        
        """
        Generates date(s) for fetching url links for specific dates.

        Args:
            startDate (str): Start date in format "dd.mm.yyyy".
            endDate (str, optional): End date in format "dd.mm.yyyy", should be later than start date. 
            Defaults to None.

        Returns:
            List[str]: List of dates for the given date range (days) or None in case of error.
        """
        format = '%d.%m.%Y'
        try:
            start_date = datetime.datetime.strptime(start_date, format)
            end_date = datetime.datetime.strptime(end_date, format) if end_date is not None else start_date + datetime.timedelta(days=1)
        except ValueError as e:
            logger.error(Helper._message('Invalid date format: {start_date}, {end_date}. Input the date in following format: "dd.mm.yyyy"', e))
            # raise SystemExit(e)
            return None
        
        if start_date >= end_date:
            logger.error(Helper._message('Make sure that the end date is after the start date'))
            # raise SystemExit()
            return None
        
        date_generated = [(start_date + datetime.timedelta(days=x)).strftime(format) for x in range(0, (end_date-start_date).days)]

        return date_generated

